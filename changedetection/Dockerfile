# Upstream's dev build (0.70.4 + newer commits), pinned by digest so builds are
# reproducible. To update: pick the new digest and bump `version` in config.yaml.
FROM ghcr.io/dgtlmoon/changedetection.io:dev@sha256:49ee6e0500e24a8aa98578b682b1938b96487d1189ecb76f0f5f83df91518e7d

# The system libraries a Chromium-based browser needs, for plugins that bring
# their own browser. They are the dependencies of Debian's chromium package
# (without recommends), so there is no list to maintain, and the browser itself
# is not installed: only chromium-common and virtual packages are filtered out.
# Chromium's dependencies include no font, so fonts-liberation is added.
RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-liberation \
        $(apt-cache depends --no-recommends --no-suggests --no-conflicts --no-breaks --no-replaces --no-enhances chromium \
            | awk '/^ *\|?Depends:/ {print $2}' | grep -vE '^(chromium|<)') \
    && rm -rf /var/lib/apt/lists/*

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
