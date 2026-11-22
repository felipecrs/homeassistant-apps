# Upstream's dev build (0.70.4 + newer commits), pinned by digest so builds are
# reproducible. To update: pick the new digest and bump `version` in config.yaml.
FROM ghcr.io/dgtlmoon/changedetection.io:dev@sha256:49ee6e0500e24a8aa98578b682b1938b96487d1189ecb76f0f5f83df91518e7d

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
