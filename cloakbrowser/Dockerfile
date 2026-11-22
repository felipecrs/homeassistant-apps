# Upstream CloakBrowser, pinned by tag and digest. To update: pick the new tag
# and digest, then bump `version` in config.yaml.
FROM cloakhq/cloakbrowser:0.7.3@sha256:77bdb67e5c139ed8e08982f45128d83490bbb83128fe0d1e7bc6054d0f43cf5c

# Persist the ~200MB Chromium binary + browser profiles in the app's own
# data dir (app_configs), so they survive restarts instead of re-downloading.
ENV CLOAKBROWSER_CACHE_DIR=/data/cache

# Executable bit is set in git (`git add --chmod=+x`), so no RUN chmod step.
COPY run.sh /run.sh

# The base image's /entrypoint.sh stays (starts Xvfb for headed mode) and
# execs our script, which launches cloakserve.
CMD ["/run.sh"]
