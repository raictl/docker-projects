from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            message = b"Hello from Backend Application!"

        elif self.path == "/health":
            message = b"Backend is healthy!"

        else:
            message = b"Backend: Page not found"

        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(message)))
        self.end_headers()

        self.wfile.write(message)


server = HTTPServer(("0.0.0.0", 5000))

print("Backend application running on port 5000")

server.serve_forever()
