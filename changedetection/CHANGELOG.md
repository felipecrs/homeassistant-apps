## 0.70.4-dev.20261120.9

- Fixed fetches failing with `'NoneType' object is not subscriptable` for browsers that open pages without a viewport, such as the CloakBrowser and Camoufox plugins. The page loaded, then the screenshot step crashed. A viewport equal to the window size is now set when there is none. The build fails if a new upstream version changes that code, so the patch is reviewed instead of silently skipped.

## 0.70.4-dev.20261120.8

- Added `git` to the image, so `EXTRA_PACKAGES` can install plugins from `git+https://` addresses.

## 0.70.4-dev.20261120.7

- The image now includes the system libraries a Chromium-based browser needs (and `fonts-liberation`), for plugins that bring their own browser. They are installed from the dependencies of Debian's `chromium` package, without the browser itself, about 30 MB.

## 0.70.4-dev.20261120.6

- The app trusts the `X-Forwarded-*` headers of a reverse proxy again (`USE_X_SETTINGS=1`), as the old app did. Behind a proxy it now knows its public address and https, so absolute links, and the sign-in (OAuth) addresses of its MCP server, are right.
- This alone does not make the Home Assistant panel work: that also needs a URL prefix, which Home Assistant does not send in the header changedetection reads.

## 0.70.4-dev.20261120.5

- Removed the CloakBrowser cache setting added in the previous version: the app stays independent of plugins. If you use that plugin, add `CLOAKBROWSER_CACHE_DIR` with a folder under `/data` (for example `/data/cloakbrowser`) to the environment variables to keep its download across rebuilds.

## 0.70.4-dev.20261120.4

- The CloakBrowser plugin's browser download (about 200 MB) now goes to the app's data folder through `CLOAKBROWSER_CACHE_DIR=/data/cloakbrowser`, so it survives rebuilds. Nothing to set. The libraries Chromium needs are still not included.

## 0.70.4-dev.20261120.3

- Removed Caddy and all URL-prefix handling for ingress, to test whether the Home Assistant panel works without it. The app listens on port 5000 directly.

## 0.70.4-dev.20261120.2

- Ingress and direct access now share port 5000 (`ingress_port` is 5000), so there is no separate ingress port any more.
- Only requests from the Supervisor can set the URL prefix; a client faking `X-Ingress-Path` is ignored.

## 0.70.4-dev.20261120.1

- Replaced nginx with Caddy. Automatic HTTPS and the admin API are off.
- Fixed "Bad Request: The CSRF session token is missing" when using the app through a reverse proxy after opening it from the Home Assistant panel. changedetection kept the ingress cookie path for every later request.

## 0.70.4-dev.20261120

- Now built from upstream's `dev` image (0.70.4 plus newer commits), pinned by digest.

## 0.70.4

- First release: the official changedetection.io image, shown in Home Assistant through ingress, with its data in the app's config folder and optional environment variables.
