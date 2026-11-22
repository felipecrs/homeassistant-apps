# changedetection.io

Website change detection, restock and price monitoring, with notifications.

- Runs the official `ghcr.io/dgtlmoon/changedetection.io` image, shown in Home
  Assistant through ingress (no separate login needed).
- All data (watches, snapshots, settings) is in the app's own config folder,
  which is included in backups.
- Reachable from other apps at `http://72547810-changedetection:5000`. The
  host port is off by default; enable it in the app's network settings if you
  need direct access.

## Options

- **Environment variables**: extra variables passed to changedetection.io, for
  example `BASE_URL`, `TZ`, `PLAYWRIGHT_DRIVER_URL`, `EXTRA_PACKAGES` (plugins,
  also from `git+https://` addresses), or `ALLOW_IANA_RESTRICTED_ADDRESSES` (to
  watch URLs on your local network). See the upstream documentation for the full
  list. If the packages in `EXTRA_PACKAGES` fail to install, the app does not
  start: fix the value and start it again.

The app trusts the `X-Forwarded-*` headers (`USE_X_SETTINGS`), so behind a reverse
proxy it uses your public address and https. Anyone who can reach its port can
set those headers, so keep the host port off unless you need it.

The image includes the system libraries a Chromium-based browser needs, for
plugins that bring their own browser. The browser itself is not included.

Anything a plugin downloads is lost when the app is rebuilt, unless it is stored
under `/data` (private to the app) or `/config` (the app's config folder). Point
the plugin at one of them with an environment variable.
