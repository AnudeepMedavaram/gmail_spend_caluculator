import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable

from src.api.service import (
    build_dashboard,
    get_health,
    get_insights,
    get_report,
    get_summary,
    get_transactions,
)


HOST = "127.0.0.1"
PORT = 8000


ROUTES: dict[str, Callable[[], Any]] = {
    "/health": get_health,
    "/transactions": get_transactions,
    "/summary": get_summary,
    "/insights": get_insights,
    "/report": get_report,
    "/dashboard": build_dashboard,
}


class ApiHandler(BaseHTTPRequestHandler):
    """Handle read-only Phase 7 API requests."""

    def do_GET(self) -> None:
        route = ROUTES.get(self.path)

        if route is None:
            self._send_json(
                {"error": "Not found"},
                status=404,
            )
            return

        try:
            payload = route()

        except (OSError, ValueError, TypeError, json.JSONDecodeError) as error:
            self._send_json(
                {"error": str(error)},
                status=500,
            )
            return

        self._send_json(payload)

    def _send_json(
        self,
        payload: Any,
        status: int = 200,
    ) -> None:
        body = json.dumps(
            payload,
            ensure_ascii=False,
        ).encode("utf-8")

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

    def log_message(self, format: str, *args: Any) -> None:
        return


class ReusableHttpServer(ThreadingHTTPServer):
    allow_reuse_address = True


def main() -> None:
    server = ReusableHttpServer(
        (HOST, PORT),
        ApiHandler,
    )

    print(
        f"Phase 7 API running at http://{HOST}:{PORT}"
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:
        print("\nStopping Phase 7 API.")

    finally:
        server.server_close()


if __name__ == "__main__":
    main()