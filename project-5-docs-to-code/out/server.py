"""GENERATED from spec/openapi.json — do not edit by hand."""

import json
import re
from http.server import BaseHTTPRequestHandler, HTTPServer

VERSION = "1.0.0"
REQUIRED = ['title']

TASKS = []


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass

    def do_GET(self):
        if self.path == "/health":
            return self._send(200, {"ok": True, "version": VERSION})
        if self.path == "/tasks":
            return self._send(200, TASKS)
        m = re.fullmatch(r"/tasks/(\d+)", self.path)
        if m:
            for task in TASKS:
                if task['id'] == int(m.group(1)):
                    return self._send(200, task)
            return self._send(404, {"error": "not found"})
        return self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/tasks":
            return self._send(404, {"error": "not found"})
        try:
            length = int(self.headers.get('Content-Length', 0))
            payload = json.loads(self.rfile.read(length) or b'{}')
        except (ValueError, OSError):
            return self._send(400, {"error": "malformed json"})
        missing = [f for f in REQUIRED if f not in payload]
        if missing:
            return self._send(400, {"error": f"missing: {missing}"})
        task = {
            'id': max([t['id'] for t in TASKS], default=0) + 1,
            'title': payload['title'],
            'done': False,
            'tags': list(payload.get('tags', [])),
        }
        TASKS.append(task)
        return self._send(201, task)


def make_server(port):
    return HTTPServer(('127.0.0.1', port), Handler)


def run(port=8000):
    make_server(port).serve_forever()


if __name__ == "__main__":
    run()
