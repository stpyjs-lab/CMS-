# Feature: app entry — initializes DB and starts HTTP server. Connects: router, database.
# app.py
import os
from http.server import ThreadingHTTPServer
from router import PatientRouter
from database.connection import init_database

def main():
    init_database()

    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer(("0.0.0.0", port), PatientRouter)

    print(f"🚀 Server running at http://localhost:{port}")
    server.serve_forever()

if __name__ == "__main__":
    main()
