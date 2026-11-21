# Inherit the community Botasaurus image — the same base the official starter
# template uses — and layer only our HTTP server on top.
FROM chetan1111/botasaurus:latest

# Xvfb for headed (stealth) mode; refresh botasaurus and add Flask.
RUN apt-get update && apt-get install -y --no-install-recommends \
        xvfb xdotool openbox \
    && rm -rf /var/lib/apt/lists/* \
    && python -m pip install --no-cache-dir botasaurus flask

# undetected-chromedriver downloads Chrome under $HOME; keep it in /data so the
# ~150MB download survives add-on restarts.
ENV HOME=/data

COPY server.py /server.py
COPY run.sh /run.sh
# Executable bit is set in git (`git add --chmod=+x`), so no RUN chmod step.

EXPOSE 3000
CMD ["/run.sh"]
