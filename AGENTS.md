# Rules for every app in this repository

1. **Never build your own image.** Inherit an upstream image (`FROM ...`) and
   patch on top. Fall back to a base image + package install only when no
   maintained upstream image exists.
2. **Modern app conventions.** Use the current app manifest keys
   (`homeassistant_api`/`hassio_api` where the app talks to Home Assistant),
   the app's own `/data` folder, and the new `map` names: `app_config` (not the
   deprecated `addon_config`), `homeassistant_config` (not `config`),
   `all_app_configs` (mounted at `/app_configs`). Use the `map` list form
   (`type`/`read_only`/`path`), not the old short form.
3. **BuildKit is available** — use modern Dockerfile syntax (`RUN --mount`,
   `COPY --chmod`). Set script exec bits with `git add --chmod=+x`, not
   `RUN chmod`.
4. **Less is more.** Fewest files and moving parts: no CI, no icons, no
   boilerplate unless it earns its place.
5. **Docs live per-app.** The root README does not document individual apps.
   Each app has `DOCS.md` and a `README.md` symlinked to it (HA renders it).
6. **No manual install steps.** Never write "add this repository" or "install
   this app" instructions — use a `my.home-assistant.io` button instead.
7. **Always use the latest conventions.** Check
   <https://contributors.home-assistant.io/apps/> (and the configuration
   reference) before writing an app; prefer the newest keys and names (e.g.
   `app_config`, not the deprecated `addon_config`).
