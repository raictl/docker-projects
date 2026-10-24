import logging
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger("logging-demo")


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK\n")
            logger.info("Health check succeeded")
        elif self.path == "/error":
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Simulated application error\n")
            logger.error("Simulated application error requested")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Logging demo application is running\n")
            logger.info("Request processed: path=%s", self.path)

    def log_message(self, format_string, *args):
        logger.info("HTTP access: %s", format_string % args)


server = HTTPServer(("0.0.0.0", 8000), Handler)
logger.info("Application starting on port 8000")
server.serve_forever()
