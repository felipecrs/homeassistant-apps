# Inherit upstream; never build our own image. Only layer the entrypoint on top.
# shortcut: `latest` auto-tracks upstream stealth builds; pin a tag if reproducibility matters.
FROM cloakhq/cloakbrowser:latest

# Persist the ~200MB Chromium binary + browser profiles in the add-on's own
# data dir (addon_configs), so they survive restarts instead of re-downloading.
ENV CLOAKBROWSER_CACHE_DIR=/data/cache

COPY run.sh /run.sh
RUN chmod +x /run.sh

# The base image's /entrypoint.sh stays (starts Xvfb for headed mode) and
# execs our script, which launches cloakserve.
CMD ["/run.sh"]
