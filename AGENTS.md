# Rules for every app in this repository

1. **Never build your own image.** Inherit an upstream image (`FROM ...`) and
   patch on top. Fall back to a base image + package install only when no
   maintained upstream image exists.
2. **Modern app conventions.** Use the current app manifest, `homeassistant_api`
   where the app talks to Home Assistant, and the native `/data`
   (`/addon_configs/<slug>`) path — never `map: config`.
3. **BuildKit is available** — use modern Dockerfile syntax (`RUN --mount`,
   `COPY --chmod`). Set script exec bits with `git add --chmod=+x`, not
   `RUN chmod`.
4. **Less is more.** Fewest files and moving parts: no CI, no icons, no
   boilerplate unless it earns its place.
5. **Docs live per-app.** The root README does not document individual apps.
   Each app has `DOCS.md` and a `README.md` symlinked to it (HA renders it).
6. **No manual install steps.** Never write "add this repository" or "install
   this app" instructions — use a `my.home-assistant.io` button instead.
7. **Use the most modern thing available.**
