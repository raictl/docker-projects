
import os
from http.server import BaseHTTPRequestHandler, HTTPServer


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            if os.environ.get("HEALTH_FAIL") == "1":
                self.send_response(500)
                self.end_headers()
                self.wfile.write(b"UNHEALTHY\n")
            else:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK\n")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Application is running\n")


server = HTTPServer(("0.0.0.0", 8000), Handler)

print("Application listening on port 8000", flush=True)
server.serve_forever()

