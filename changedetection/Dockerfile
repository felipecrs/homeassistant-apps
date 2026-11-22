# Upstream's dev build (0.70.4 + newer commits), pinned by digest so builds are
# reproducible. To update: pick the new digest and bump `version` in config.yaml.
FROM ghcr.io/dgtlmoon/changedetection.io:dev@sha256:49ee6e0500e24a8aa98578b682b1938b96487d1189ecb76f0f5f83df91518e7d

# The system libraries a Chromium-based browser needs, for plugins that bring
# their own browser. They are the dependencies of Debian's chromium package
# (without recommends), so there is no list to maintain, and the browser itself
# is not installed: only chromium-common and virtual packages are filtered out.
# Chromium's dependencies include no font, so fonts-liberation is added.
# git lets EXTRA_PACKAGES install plugins from git+https:// addresses.
RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-liberation git \
        $(apt-cache depends --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances chromium \
            | awk '/^ *\|?Depends:/ {print $2}' | grep -vE '^(chromium|<)') \
    && rm -rf /var/lib/apt/lists/*

# Screenshots assume every page has a viewport, but stealth browsers (CloakBrowser,
# Camoufox) open pages without one, so the fetch dies with "'NoneType' object is
# not subscriptable" right after the page loaded. Pin a viewport equal to the
# window size when there is none. The assert fails the build if a new upstream
# digest changes that line, so the patch is never silently skipped; drop it once
# upstream handles it (see the pull request "Make browser viewport configurable").
RUN python - <<'PY'
import pathlib
path = pathlib.Path("/app/changedetectionio/content_fetchers/playwright.py")
source = path.read_text()
old = "    original_viewport = page.viewport_size\n"
new = old + (
    "    if original_viewport is None:\n"
    "        window = await page.evaluate('({width: window.innerWidth, height: window.innerHeight})')\n"
    "        original_viewport = {'width': window['width'] or 1280, 'height': window['height'] or 1024}\n"
    "        await page.set_viewport_size(original_viewport)\n"
)
assert source.count(old) == 1, "upstream changed capture_full_page_async: review the viewport patch"
path.write_text(source.replace(old, new))
PY

# Export the "env_vars" option as environment variables, then hand over to
# upstream's entrypoint. The datastore is the app's /config folder.
COPY --chmod=755 <<'EOF' /run.sh
#!/usr/bin/env bash
set -euo pipefail
eval "$(python3 - <<'PY'
import json, shlex
for e in json.load(open("/data/options.json")).get("env_vars", []):
    print(f"export {e['name']}={shlex.quote(e.get('value') or '')}")
PY
)"
exec /docker-entrypoint.sh python ./changedetection.py -d /config
EOF

ENTRYPOINT ["/run.sh"]
