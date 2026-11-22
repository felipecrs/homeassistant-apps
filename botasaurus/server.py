from fastapi import FastAPI, HTTPException, Request, Response

from botasaurus.browser import browser, Driver

app = FastAPI()


@browser(enable_xvfb_virtual_display=True)
def fetch_page(driver: Driver, data):
    driver.get(data["url"])
    return driver.page_source


@app.get("/")
def health():
    return {"ok": True}


@app.get("/{target:path}")
def fetch(target: str, request: Request):
    url = target
    if request.query_params:
        url += "?" + str(request.query_params)
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        return Response(content=fetch_page({"url": url}), media_type="text/html")
    except Exception as exc:
        raise HTTPException(status_code=502, detail=str(exc))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80)
