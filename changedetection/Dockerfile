# Upstream's dev build (0.70.4 + newer commits), pinned by digest so builds are
# reproducible. To update: pick the new digest and bump `version` in config.yaml.
FROM ghcr.io/dgtlmoon/changedetection.io:dev@sha256:49ee6e0500e24a8aa98578b682b1938b96487d1189ecb76f0f5f83df91518e7d

# Caddy fronts the app on port 5000, for ingress and direct access alike.
# changedetection takes its URL prefix and session cookie path from
# X-Forwarded-Prefix and never resets them, so every request must carry its own:
# the ingress path when it comes from the Supervisor, an empty one otherwise
# (which also keeps clients from spoofing X-Ingress-Path).
# No automatic HTTPS, no admin API.
COPY --from=caddy:2@sha256:4851e54a46b206517c574821bb5cc67f170d2156041e9fbc4c9193b45e84a75b /usr/bin/caddy /usr/local/bin/caddy

COPY <<'EOF' /etc/caddy/Caddyfile
{
	auto_https off
	admin off
	persist_config off
	servers {
		trusted_proxies static private_ranges
	}
}

:5000 {
	@ingress remote_ip 172.30.32.2
	handle @ingress {
		reverse_proxy 127.0.0.1:5001 {
			header_up X-Forwarded-Prefix {header.X-Ingress-Path}
		}
	}
	handle {
		reverse_proxy 127.0.0.1:5001 {
			header_up X-Forwarded-Prefix ""
		}
	}
}
EOF

# Export the "env_vars" option as environment variables, start Caddy, then hand
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
caddy run --config /etc/caddy/Caddyfile &
exec /docker-entrypoint.sh python ./changedetection.py -h 127.0.0.1 -p 5001 -d /config
EOF

ENTRYPOINT ["/run.sh"]
