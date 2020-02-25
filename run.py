from app import app
from webbrowser import open

HOST = "127.0.0.1"
PORT = 5000

open(f"http://{HOST}:{PORT}")
app.run(host=HOST, port=PORT, debug=True)
