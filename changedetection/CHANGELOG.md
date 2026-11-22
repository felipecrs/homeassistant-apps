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
