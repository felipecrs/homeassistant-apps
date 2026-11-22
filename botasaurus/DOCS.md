# Botasaurus

An experimental stealth-browser HTTP proxy. It fetches a URL with an undetected
Chromium and returns the rendered HTML, for feeding into changedetection.io.

- Endpoint: `GET /<target-url>` → rendered HTML (no URL-encoding needed), e.g.
  `http://72547810-botasaurus/https://amazon.com.br/dp/B0DH8J5YGH`.
- `GET /` → health check.

To use with changedetection, point a watch's URL at
`http://72547810-botasaurus/<target-url>` and set the fetch backend to
`html_requests` — the Botasaurus app does the browser work.
