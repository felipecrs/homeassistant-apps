# Rules for every app in this repository

1. **Never build your own image.** Inherit an upstream image (`FROM ...`) and
   patch on top. Fall back to a base image + package install only when no
   maintained upstream image exists. Pin the base by tag and digest
   (`FROM image:tag@sha256:...`, look it up with `regctl image digest`), and
   bump `version` in `config.yaml` whenever the digest changes.
2. **Modern app conventions.** Use the current app manifest keys
   (`homeassistant_api`/`hassio_api` where the app talks to Home Assistant),
   the app's own data, and the new `map` names: `app_config` (not the
   deprecated `addon_config`), `homeassistant_config` (not `config`),
   `all_app_configs` (mounted at `/app_configs`). Use the `map` list form
   (`type`/`read_only`/`path`), not the old short form.
3. **BuildKit is available** — use modern Dockerfile syntax (`RUN --mount`,
   `COPY --chmod`, heredocs). Put small configs and scripts inline with
   `COPY <<'EOF' /path` instead of extra files. For files that live in git, set
   exec bits with `git add --chmod=+x`, not `RUN chmod`.
4. **Less is more.** Fewest files and moving parts. Keep `icon.png` and
   `logo.png`; skip CI and other boilerplate unless it earns its place.
5. **Web UIs use ingress** (Home Assistant handles auth): accept only
   `172.30.32.2`, read the `X-Ingress-Path` header, and keep host ports off by
   default (`ports: {5000/tcp: null}`).
6. **Leave `init` at its default** unless the base image has its own init. Use a
   `tcp://` watchdog, so an app login redirect can't look unhealthy.
7. **Options get `translations/en.yaml`** (names, descriptions, ports).
8. **Docs live per-app.** The root README does not document individual apps.
   Each app has `DOCS.md` and a `README.md` symlinked to it (HA renders it).
9. **No manual install steps.** Never write "add this repository" or "install
   this app" instructions — use a `my.home-assistant.io` button instead.
10. **Always use the latest conventions.** Check
    <https://contributors.home-assistant.io/apps/> (and the configuration
    reference) before writing an app; prefer the newest keys and names.
11. **Say "app", never "add-on".**
12. **Test the build locally** before pushing: `wsl.exe docker build`, and
    smoke-test the container.
