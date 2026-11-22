## 4.0.97.1

- Versions now follow the pinned Botasaurus release (4.0.97). The base image, Botasaurus, FastAPI and uvicorn are all pinned.
- Uses Google Chrome from Google's repository (amd64 and arm64) and Botasaurus's own virtual display.
- Serves on port 80 with FastAPI. `GET /<target-url>` returns the rendered page, with no URL-encoding needed.
- Fixed fetching pages: the rendered HTML is read with `page_html`, and errors are returned as HTTP 502.

## 1.0.0

- First release.
