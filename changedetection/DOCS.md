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
  example `BASE_URL`, `TZ`, `PLAYWRIGHT_DRIVER_URL`, `EXTRA_PACKAGES` (plugins),
  or `ALLOW_IANA_RESTRICTED_ADDRESSES` (to watch URLs on your local network).
  See the upstream documentation for the full list.
