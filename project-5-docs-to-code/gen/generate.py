"""Spec-driven codegen: openapi.json -> server.py + client.py + mocks.py.

Usage: python3 gen/generate.py  (writes to out/)
Every emitted file carries a GENERATED header; edit the spec, not the output.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SPEC = os.path.join(HERE, "..", "spec", "openapi.json")
OUT = os.path.join(HERE, "..", "out")

HEADER = '"""GENERATED from spec/openapi.json — do not edit by hand."""\n\n'


def load_spec():
    with open(SPEC, encoding="utf-8") as fh:
        return json.load(fh)


def operations(spec):
    ops = []
    for path, methods in spec["paths"].items():
        for method, op in methods.items():
            ops.append((method.upper(), path, op))
    return ops


def gen_server(spec):
    version = spec["info"]["version"]
    required = spec["paths"]["/tasks"]["post"]["requestBody"]["required"]
    return (
        HEADER
        + "import json\nimport re\nfrom http.server import BaseHTTPRequestHandler, HTTPServer\n\n"
        + f'VERSION = "{version}"\n'
        + f"REQUIRED = {required!r}\n\n"
        + "TASKS = []\n\n\n"
        + "class Handler(BaseHTTPRequestHandler):\n"
        + '    def _send(self, code, obj):\n'
        + '        body = json.dumps(obj).encode()\n'
        + '        self.send_response(code)\n'
        + '        self.send_header("Content-Type", "application/json")\n'
        + '        self.send_header("Content-Length", str(len(body)))\n'
        + "        self.end_headers()\n"
        + "        self.wfile.write(body)\n\n"
        + "    def log_message(self, *args):\n"
        + "        pass\n\n"
        + "    def do_GET(self):\n"
        + '        if self.path == "/health":\n'
        + '            return self._send(200, {"ok": True, "version": VERSION})\n'
        + '        if self.path == "/tasks":\n'
        + "            return self._send(200, TASKS)\n"
        + '        m = re.fullmatch(r"/tasks/(\\d+)", self.path)\n'
        + "        if m:\n"
        + "            for task in TASKS:\n"
        + "                if task['id'] == int(m.group(1)):\n"
        + "                    return self._send(200, task)\n"
        + '            return self._send(404, {"error": "not found"})\n'
        + '        return self._send(404, {"error": "not found"})\n\n'
        + "    def do_POST(self):\n"
        + '        if self.path != "/tasks":\n'
        + '            return self._send(404, {"error": "not found"})\n'
        + "        try:\n"
        + "            length = int(self.headers.get('Content-Length', 0))\n"
        + "            payload = json.loads(self.rfile.read(length) or b'{}')\n"
        + "        except (ValueError, OSError):\n"
        + '            return self._send(400, {"error": "malformed json"})\n'
        + "        missing = [f for f in REQUIRED if f not in payload]\n"
        + "        if missing:\n"
        + '            return self._send(400, {"error": f"missing: {missing}"})\n'
        + "        task = {\n"
        + "            'id': max([t['id'] for t in TASKS], default=0) + 1,\n"
        + "            'title': payload['title'],\n"
        + "            'done': False,\n"
        + "            'tags': list(payload.get('tags', [])),\n"
        + "        }\n"
        + "        TASKS.append(task)\n"
        + "        return self._send(201, task)\n\n\n"
        + "def make_server(port):\n"
        + "    return HTTPServer(('127.0.0.1', port), Handler)\n\n\n"
        + "def run(port=8000):\n"
        + "    make_server(port).serve_forever()\n\n\n"
        + 'if __name__ == "__main__":\n'
        + "    run()\n"
    )


def gen_client(spec):
    methods = [op.get("operationId") for _, _, op in operations(spec)]
    assert {"getHealth", "listTasks", "createTask", "getTask"} <= set(methods)
    return (
        HEADER
        + "import json\nimport urllib.request\nimport urllib.error\n\n\n"
        + "class ApiError(Exception):\n"
        + "    def __init__(self, code, body):\n"
        + "        super().__init__(f'HTTP {code}: {body}')\n"
        + "        self.code = code\n"
        + "        self.body = body\n\n\n"
        + "class TasksClient:\n"
        + '    def __init__(self, base="http://127.0.0.1:8000"):\n'
        + "        self.base = base.rstrip('/')\n\n"
        + "    def _call(self, method, path, payload=None):\n"
        + "        data = json.dumps(payload).encode() if payload is not None else None\n"
        + "        req = urllib.request.Request(\n"
        + "            self.base + path, data=data, method=method,\n"
        + "            headers={'Content-Type': 'application/json'})\n"
        + "        try:\n"
        + "            with urllib.request.urlopen(req) as resp:\n"
        + "                return resp.status, json.loads(resp.read() or b'null')\n"
        + "        except urllib.error.HTTPError as exc:\n"
        + "            raise ApiError(exc.code, exc.read().decode())\n\n"
        + "    def getHealth(self):\n"
        + '        return self._call(' + "'GET', '/health')\n\n"
        + "    def listTasks(self):\n"
        + '        return self._call(' + "'GET', '/tasks')\n\n"
        + "    def createTask(self, title, tags=()):\n"
        + '        return self._call(' + "'POST', '/tasks', {'title': title, 'tags': list(tags)})\n\n"
        + "    def getTask(self, task_id):\n"
        + '        return self._call(' + "'GET', f'/tasks/{task_id}')\n"
    )


def gen_mocks(spec):
    task_props = spec["schemas"]["Task"]["properties"]
    example = {k: v["example"] for k, v in task_props.items()}
    return (
        HEADER
        + f"TASK_EXAMPLE = {example!r}\n"
        + f"TASK_LIST_EXAMPLE = [{example!r}]\n"
        + f"HEALTH_EXAMPLE = {{'ok': True, 'version': {spec['info']['version']!r}}}\n"
        + "CREATE_VALID = {'title': 'Write report', 'tags': ['work']}\n"
        + "CREATE_INVALID_MISSING_TITLE = {'tags': ['work']}\n"
    )


def main():
    spec = load_spec()
    os.makedirs(OUT, exist_ok=True)
    outputs = {
        "server.py": gen_server(spec),
        "client.py": gen_client(spec),
        "mocks.py": gen_mocks(spec),
    }
    for name, content in outputs.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
            fh.write(content)
        print("wrote out/" + name)


if __name__ == "__main__":
    main()
