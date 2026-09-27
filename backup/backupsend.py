from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/Serenity.tar":
            self.send_error(404)
            return
        with open("/media/Media1/BackupDaily/Serenity.tar", "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "application/x-tar")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

HTTPServer(("0.0.0.0", 8765), Handler).serve_forever()
