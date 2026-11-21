# Build on a slim Python base; Botasaurus pulls its own undetected Chromium.
FROM python:3.12-slim

# Chromium runtime libs + Xvfb for headed (stealth) mode.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 \
    libxkbcommon0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
    libpango-1.0-0 libcairo2 libasound2 libatspi2.0-0 libx11-6 libxcb1 \
    libxext6 libxshmfence1 libxss1 fonts-liberation \
    xvfb xdotool openbox curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir botasaurus flask

# Bake botasaurus's patched Chrome into the image: a headless launch triggers
# the ~150MB download at build time, so it doesn't happen on first run.
COPY warm.py /warm.py
RUN python /warm.py && rm /warm.py

COPY server.py /server.py
COPY run.sh /run.sh
# Executable bit is set in git (`git add --chmod=+x`), so no RUN chmod step.

EXPOSE 3000
CMD ["/run.sh"]
