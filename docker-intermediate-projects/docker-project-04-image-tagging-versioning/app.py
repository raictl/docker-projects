from http.server import BaseHTTPRequestHandler, HTTPServer

APP_VERSION = "1.1.0"

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        message = f"Application version: {APP_VERSION}\n"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(message.encode())

server = HTTPServer(("0.0.0.0", 8000), Handler)
print(f"Application listening on port 8000, version {APP_VERSION}")
server.serve_forever()
