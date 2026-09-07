"""Contract tests: generated client <-> generated server <-> spec mocks (10 tests)."""
import json
import os
import sys
import threading
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "out")
sys.path.insert(0, OUT)

import mocks
from client import ApiError, TasksClient
from server import TASKS, make_server

with open(os.path.join(ROOT, "spec", "openapi.json"), encoding="utf-8") as fh:
    SPEC = json.load(fh)


class ContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = make_server(0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.client = TasksClient(f"http://127.0.0.1:{cls.port}")

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.thread.join()

    def setUp(self):
        TASKS.clear()

    def test_health_matches_spec_version(self):
        code, body = self.client.getHealth()
        self.assertEqual(code, 200)
        self.assertEqual(body, mocks.HEALTH_EXAMPLE)
        self.assertEqual(body["version"], SPEC["info"]["version"])

    def test_create_round_trip(self):
        code, task = self.client.createTask(**mocks.CREATE_VALID)
        self.assertEqual(code, 201)
        for key in SPEC["schemas"]["Task"]["required"]:
            self.assertIn(key, task)
        _, fetched = self.client.getTask(task["id"])
        self.assertEqual(fetched, task)

    def test_create_missing_title_rejected(self):
        with self.assertRaises(ApiError) as ctx:
            self.client._call("POST", "/tasks", mocks.CREATE_INVALID_MISSING_TITLE)
        self.assertEqual(ctx.exception.code, 400)

    def test_malformed_json_rejected(self):
        import urllib.error
        import urllib.request

        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}/tasks",
            data=b"{oops",
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        self.assertEqual(ctx.exception.code, 400)

    def test_list_contains_created(self):
        _, task = self.client.createTask("A", [])
        _, other = self.client.createTask("B", ["x"])
        _, items = self.client.listTasks()
        self.assertEqual([t["id"] for t in items], [task["id"], other["id"]])

    def test_get_unknown_id_404(self):
        with self.assertRaises(ApiError) as ctx:
            self.client.getTask(9999)
        self.assertEqual(ctx.exception.code, 404)

    def test_tags_default_empty(self):
        _, task = self.client._call("POST", "/tasks", {"title": "No tags"})
        self.assertEqual(task["tags"], [])

    def test_mock_task_satisfies_schema(self):
        schema = SPEC["schemas"]["Task"]
        for field in schema["required"]:
            self.assertIn(field, mocks.TASK_EXAMPLE)
        self.assertIsInstance(mocks.TASK_EXAMPLE["id"], int)

    def test_client_covers_spec_operations(self):
        ops = {
            op.get("operationId")
            for methods in SPEC["paths"].values()
            for op in methods.values()
        }
        for op_id in ops:
            self.assertTrue(hasattr(self.client, op_id), op_id)

    def test_ids_increment(self):
        _, first = self.client.createTask("One", [])
        _, second = self.client.createTask("Two", [])
        self.assertEqual(second["id"], first["id"] + 1)


if __name__ == "__main__":
    unittest.main()
