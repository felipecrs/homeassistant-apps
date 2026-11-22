# CloakBrowser

A stealth Chromium (CDP server) that passes bot detection, for use as a browser
backend by tools like changedetection.io.

- Inherits the `cloakhq/cloakbrowser` image and runs its `cloakserve` CDP
  multiplexer on port **9222**.
- **Config:** set your `license_key` (free at cloakbrowser.dev/free). `headless`
  defaults to `true`; set it to `false` for tougher anti-bot targets.
- **Connect** (Playwright):
  `chromium.connect_over_cdp("http://72547810-cloakbrowser:9222?fingerprint=my-site")`.
- **Known limits:** the CDP port has no auth (CDP has none built in), so keep
  it on the internal app network.
