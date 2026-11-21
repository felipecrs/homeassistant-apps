# homeassistant-apps

Experimental Home Assistant apps (add-ons) that aren't ready to live in a
polished repo yet.

## Rules every app here follows

1. **Never build your own image.** Inherit an upstream image (`FROM ...`) and
   layer only the small patch this app needs on top. Rebuilding a heavy base
   image is the thing to avoid. Modern BuildKit syntax (`RUN --mount`,
   `COPY --chmod`) is fine — but set script exec bits with
   `git add --chmod=+x` instead of `RUN chmod`.
2. **Modern app conventions.** Use the current app manifest fields, set
   `homeassistant_api` wherever the app talks to Home Assistant, and use the
   native add-on data path — write to `/data` (mapped to
   `/addon_configs/<slug>`), never to the shared `/config` and never
   `map: config`.
3. **Less is more.** Fewest files and moving parts: no CI, no icons, no
   boilerplate unless it earns its place. One small entrypoint script at most.

## Add this repository

In Home Assistant: **Settings → Add-ons → Add-on store → ⋮ → Repositories**,
add `https://github.com/felipecrs/homeassistant-apps`.

## Apps

### CloakBrowser

A stealth Chromium (CDP server) that passes bot detection, for use as a browser
backend by tools like changedetection.io.

- Inherits the `cloakhq/cloakbrowser` image and runs its `cloakserve` CDP
  multiplexer on port **9222** (reachable from other add-ons at
  `http://cloakbrowser:9222`).
- **Config:** set your `license_key` (free at cloakbrowser.dev/free). `headless`
  defaults to `true`; set it to `false` for tougher anti-bot targets (Akamai
  and friends).
- **Connect** (Playwright):
  `chromium.connect_over_cdp("http://cloakbrowser:9222?fingerprint=my-site")`.
  Pass a `?fingerprint=` seed per site to keep a stable identity across checks.
- **Known limits:** the CDP port has no auth (CDP has none built in), so keep
  it on the internal add-on network — don't publish it to the internet.

### Botasaurus

An experimental stealth-browser HTTP proxy. It fetches a URL with an
undetected Chromium (headed, anti-detection) and returns the rendered HTML,
for feeding into changedetection.io.

- Endpoint: `GET /<target-url>` → returns the rendered HTML (no URL-encoding
  needed), e.g. `http://<hostname>:3000/https://amazon.com.br/dp/B0DH8J5YGH`.
- `GET /` → health check.
- Runs on port **3000**; reachable from other add-ons at
  `http://<hostname>:3000`.

To use with changedetection, point a watch's URL at
`http://<hostname>:3000/<target-url>` and set the fetch backend to
`html_requests` — the Botasaurus add-on does the browser work.

