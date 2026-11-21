from flask import Flask, jsonify, request

from botasaurus.browser import browser, Driver

app = Flask(__name__)


@browser
def fetch_page(driver: Driver, data):
    driver.get(data["url"])
    return driver.page_source


@app.get("/")
def health():
    return jsonify({"ok": True})


@app.get("/<path:target>")
def fetch(target):
    # The target URL is the raw path, e.g. /https://amazon.com.br/dp/XYZ
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
    app.run(host="0.0.0.0", port=3000)
