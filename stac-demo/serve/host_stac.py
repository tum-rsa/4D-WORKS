"""
Serve a STAC catalog statically. Then explore the hosted catalog via STAC Browser: https://browser.moregeo.it/

python host_stac.py --root ./catalog --host 0.0.0.0 --port 8000
"""

import argparse
from functools import partial
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        return super(CORSRequestHandler, self).end_headers()


def main():
    parser = argparse.ArgumentParser(description="Serve a static STAC catalog with CORS.")
    parser.add_argument("--root", type=Path, default=Path("./demo"), help="Catalog root directory")
    parser.add_argument("--host", default="localhost", help="Server host")
    parser.add_argument("--port", type=int, default=5555, help="Server port")
    args = parser.parse_args()

    handler = partial(CORSRequestHandler, directory=str(args.root.resolve()))

    with HTTPServer((args.host, args.port), handler) as httpd:
        print(f"Serving STAC catalog from: {args.root.resolve()}")
        print(f"URL: http://{args.host}:{args.port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
