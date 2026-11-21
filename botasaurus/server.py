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


@app.get("/fetch")
def fetch():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "?url=<encoded url> is required"}), 400
    try:
        return fetch_page({"url": url})
    except Exception as exc:
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
