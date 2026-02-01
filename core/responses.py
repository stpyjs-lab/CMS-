# Sends HTTP responses back to the client (JSON or HTML)

import json
from core.middleware import add_cors_headers

def send_json(handler, status, data):
    handler.send_response(status)
    add_cors_headers(handler)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps(data).encode("utf-8"))

def send_404(handler):
    handler.send_response(404)
    add_cors_headers(handler)
    handler.send_header("Content-Type", "text/html")
    handler.end_headers()
    handler.wfile.write(b"<h1>404 Not Found</h1>")