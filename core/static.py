# Feature: static file server — serves frontend assets and SPA shell. Connects: frontend files and router.
# core/static.py
import os
import mimetypes
from core.responses import send_404

mimetypes.add_type("application/javascript", ".js")

def serve_static(handler, filepath):
    full_path = os.path.join(".", filepath)

    if not os.path.exists(full_path):
        # keep this log, it's useful
        print("STATIC ERROR: File not found:", full_path)
        return send_404(handler)

    try:
        with open(full_path, "rb") as f:
            content = f.read()

        content_type, _ = mimetypes.guess_type(full_path)

        if full_path.endswith(".html"):
            content_type = "text/html; charset=utf-8"
        elif full_path.endswith((".yaml", ".yml")):
            content_type = "text/yaml; charset=utf-8"
        elif full_path.endswith(".js"):
            content_type = "application/javascript; charset=utf-8"
        elif full_path.endswith(".css"):
            content_type = "text/css; charset=utf-8"

        handler.send_response(200)
        handler.send_header("Content-Type", content_type or "application/octet-stream")

        # KEY: allows HTTP/1.1 keep-alive to work nicely
        handler.send_header("Content-Length", str(len(content)))

        # optional but helps repeat loads
        handler.send_header("Cache-Control", "public, max-age=300")

        handler.end_headers()

        try:
            handler.wfile.write(content)
        except BrokenPipeError:
            # browser closed connection early (refresh/navigation) - not a real bug
            return

    except BrokenPipeError:
        return
    except Exception as e:
        print("STATIC ERROR:", e)
        return send_404(handler)