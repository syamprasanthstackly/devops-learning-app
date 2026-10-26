import os
from http.server import BaseHTTPRequestHandler, HTTPServer

APP_NAME = "DevOps Learning App"
APP_ENV = os.getenv("APP_ENV", "development")
PORT = int(os.getenv("PORT", "8000"))


class AppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status":"healthy"}')
            return

        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        message = f"""
        <html>
            <head>
                <title>{APP_NAME}</title>
            </head>
            <body>
                <h1>{APP_NAME}</h1>
                <p>Environment: {APP_ENV}</p>
                <p>Status: Application is running!</p>
                <p>Built with Python, GitHub, and DevOps practices.</p>
                <p>Health endpoint: /health</p>
            </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(message.encode("utf-8"))

    def log_message(self, format_string, *args):
        print(f"{self.address_string()} - {format_string % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), AppHandler)

    print(f"{APP_NAME} starting on port {PORT}")
    print(f"Environment: {APP_ENV}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping application")
    finally:
        server.server_close()
