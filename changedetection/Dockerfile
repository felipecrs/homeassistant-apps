ARG BUILD_VERSION
FROM ghcr.io/dgtlmoon/changedetection.io:${BUILD_VERSION}

# Ingress: nginx accepts only the Supervisor and turns Home Assistant's
# X-Ingress-Path header into the X-Forwarded-Prefix that changedetection reads
# (it is enabled by USE_X_SETTINGS in config.yaml).
RUN apt-get update \
    && apt-get install -y --no-install-recommends nginx \
    && rm -rf /var/lib/apt/lists/*

COPY <<'EOF' /etc/nginx/nginx.conf
pid /run/nginx.pid;
error_log stderr warn;
events {}
http {
    access_log off;
    map $http_upgrade $connection_upgrade {
        default upgrade;
        "" close;
    }
    server {
        listen 8099;
        allow 172.30.32.2;
        deny all;
        client_max_body_size 0;
        location / {
            proxy_pass http://127.0.0.1:5000;
            proxy_http_version 1.1;
            proxy_read_timeout 1d;
            proxy_set_header Host $http_host;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection $connection_upgrade;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Host $host;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_set_header X-Forwarded-Prefix $http_x_ingress_path;
        }
    }
}
EOF

# Export the "env_vars" option as environment variables, start nginx, then hand
# over to upstream's entrypoint. The datastore is the app's /config folder.
COPY --chmod=755 <<'EOF' /run.sh
#!/usr/bin/env bash
set -euo pipefail
eval "$(python3 - <<'PY'
import json, shlex
for e in json.load(open("/data/options.json")).get("env_vars", []):
    print(f"export {e['name']}={shlex.quote(e.get('value') or '')}")
PY
)"
nginx
exec /docker-entrypoint.sh python ./changedetection.py -d /config
EOF

ENTRYPOINT ["/run.sh"]
