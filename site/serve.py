"""Local server with clean URLs, matching how the site is hosted in production.

    python3 site/serve.py            # http://localhost:8000
    python3 site/serve.py 8080

/collections/gift-boxes serves collections/gift-boxes.html, /x.html redirects to /x,
the sitemap's 301s are applied, and unknown paths get 404.html.
"""
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent

# Same rules as _redirects / vercel.json (workbook "Redirects & Canonicals" sheet).
REDIRECTS = {
    "/collections/small-attentions": "/collections/small-gifts",
    "/pages/ingredient-transparency": "/pages/ingredients",
}


class CleanURLHandler(SimpleHTTPRequestHandler):
    def redirect(self, location):
        self.send_response(301)
        self.send_header("Location", location)
        self.end_headers()

    def do_GET(self):
        url = urlsplit(self.path)
        path = url.path.rstrip("/") or "/"
        query = f"?{url.query}" if url.query else ""

        if path in REDIRECTS:
            return self.redirect(REDIRECTS[path] + query)
        if path.endswith(".html"):
            clean = path[: -len(".html")]
            return self.redirect(("/" if clean == "/index" else clean) + query)
        if path == "/":
            self.path = "/index.html" + query
        elif not Path(path).suffix and (ROOT / (path.lstrip("/") + ".html")).is_file():
            self.path = path + ".html" + query
        elif not (ROOT / path.lstrip("/")).is_file() or path.startswith("/_build"):
            return self.not_found()
        return super().do_GET()

    def not_found(self):
        body = (ROOT / "404.html").read_bytes()
        self.send_response(404)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def list_directory(self, path):  # never show folder listings
        self.not_found()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    server = ThreadingHTTPServer(("127.0.0.1", port), partial(CleanURLHandler, directory=str(ROOT)))
    print(f"Praline running at http://localhost:{port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
