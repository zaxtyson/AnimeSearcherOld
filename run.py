from app import app, routes
from webbrowser import open_new
from threading import Timer

HOST = "127.0.0.1"
PORT = 5000


def open_browser():
    open_new(f"http://{HOST}:{PORT}")


if __name__ == "__main__":
    Timer(1, open_browser).start()
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)
