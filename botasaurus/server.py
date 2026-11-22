from flask import Flask, jsonify, request
from waitress import serve

from botasaurus.browser import browser, Driver

app = Flask(__name__)


@browser(enable_xvfb_virtual_display=True)
def fetch_page(driver: Driver, data):
    driver.get(data["url"])
    return driver.page_source


@app.get("/")
def health():
    return jsonify({"ok": True})


@app.get("/<path:target>")
def fetch(target):
    url = target
    if request.query_string:
        url += "?" + request.query_string.decode()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        return fetch_page({"url": url})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    # Production WSGI server (Flask's built-in dev server prints a warning and
    # isn't meant for this). threads=1 so each browser launch is serialized.
    serve(app, host="0.0.0.0", port=80, threads=1)
