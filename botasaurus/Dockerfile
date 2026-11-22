# Python 3.12 + uv on Debian (fast, cached builds).
FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim

# Google Chrome (the browser botasaurus drives) + Xvfb for botasaurus's own
# virtual display. The Google repo serves both amd64 and arm64.
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gnupg xvfb \
    && curl -fsSL https://dl.google.com/linux/linux_signing_key.pub \
        | gpg --batch --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" \
        > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

RUN uv pip install --system --no-cache botasaurus flask waitress

COPY server.py /server.py

EXPOSE 80
CMD ["python", "/server.py"]
