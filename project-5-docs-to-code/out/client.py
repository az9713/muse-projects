"""GENERATED from spec/openapi.json — do not edit by hand."""

import json
import urllib.error
import urllib.request


class ApiError(Exception):
    def __init__(self, code, body):
        super().__init__(f'HTTP {code}: {body}')
        self.code = code
        self.body = body


class TasksClient:
    def __init__(self, base="http://127.0.0.1:8000"):
        self.base = base.rstrip('/')

    def _call(self, method, path, payload=None):
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            self.base + path, data=data, method=method,
            headers={'Content-Type': 'application/json'})
        try:
            with urllib.request.urlopen(req) as resp:
                return resp.status, json.loads(resp.read() or b'null')
        except urllib.error.HTTPError as exc:
            raise ApiError(exc.code, exc.read().decode())

    def getHealth(self):
        return self._call('GET', '/health')

    def listTasks(self):
        return self._call('GET', '/tasks')

    def createTask(self, title, tags=()):
        return self._call('POST', '/tasks', {'title': title, 'tags': list(tags)})

    def getTask(self, task_id):
        return self._call('GET', f'/tasks/{task_id}')
