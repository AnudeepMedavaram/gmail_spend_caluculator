import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import urlopen


HOST = "127.0.0.1"
PORT = 8501
API_URL = "http://127.0.0.1:8000/dashboard"
INDEX_FILE = Path(__file__).with_name("index.html")


class DashboardHandler(BaseHTTPRequestHandler):
    """Serve the dashboard and proxy the Phase 7 dashboard payload."""

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]

        if path == "/":
            self._send_file()
            return

        if path == "/api/dashboard":
            self._send_dashboard_data()
            return

        self._send_json(
            {"error": "Not found"},
            status=404,
        )

    def _send_file(self) -> None:
        try:
            body = INDEX_FILE.read_bytes()

        except OSError as error:
            self._send_json(
                {"error": str(error)},
                status=500,
            )
            return

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "text/html; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(body)),
        )
        self.end_headers()
        self.wfile.write(body)

    def _send_dashboard_data(self) -> None:
        try:
            with urlopen(API_URL, timeout=5) as response:
                body = response.read()

        except (HTTPError, URLError, OSError) as error:
            self._send_json(
                {
                    "error": (
                        "Phase 7 API is unavailable. "
                        f"{error}"
                    )
                },
                status=503,
            )
            return

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(body)),
        )
        self.end_headers()
        self.wfile.write(body)

    def _send_json(
        self,
        payload: dict,
        status: int = 200,
    ) -> None:
        body = json.dumps(payload).encode("utf-8")

        self.send_response(status)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(body)),
        )
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format: str, *args: object) -> None:
        return


class ReusableHttpServer(ThreadingHTTPServer):
    allow_reuse_address = True


def main() -> None:
    server = ReusableHttpServer(
        (HOST, PORT),
        DashboardHandler,
    )

    print(
        f"Phase 8 dashboard running at http://{HOST}:{PORT}"
    )
    print(
        f"Reading data from {API_URL}"
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nStopping Phase 8 dashboard.")

    finally:
        server.server_close()


if __name__ == "__main__":
    main()