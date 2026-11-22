# Rules for every app in this repository

1. **Never build your own image.** Inherit an upstream image (`FROM ...`) and
   patch on top. Fall back to a base image + package install only when no
   maintained upstream image exists. Pin everything that matters: base images by
   tag and digest (`FROM image:tag@sha256:...`, look it up with
   `regctl image digest`) and Python packages with `==`.
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
5. **Web UIs use ingress** (Home Assistant handles auth): set `ingress_port`
   to the app's own port, only trust `X-Ingress-Path` from `172.30.32.2`, and
   keep host ports off by default (`ports: {5000/tcp: null}`). Test with a
   Docker network on `172.30.32.0/23` and a client at `172.30.32.2`. When a
   proxy is needed, use Caddy
   (`COPY --from=caddy:2@sha256:... /usr/bin/caddy`, never nginx) and always set
   `auto_https off` and `admin off`: no Let's Encrypt, no admin API.
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
13. **Bump `version` on every change to an app.** Any change to its
    `config.yaml`, `Dockerfile`, scripts or translations bumps `version` in
    `config.yaml` in the same commit, with a `CHANGELOG.md` entry (docs-only
    changes don't). Without a bump users never get the change: the Supervisor
    offers an update when `version` differs from the installed one (a plain
    string comparison in `supervisor/apps/app.py`, not an ordering) and rebuilds
    from the Dockerfile when they update.
    - Scheme: `<upstream version>[-dev.<YYYYMMDD>].<revision>`.
    - The upstream version is the one of the pinned image or package the app
      wraps (changedetection `0.70.4-dev.20261120.2`, Botasaurus `4.0.97.1`,
      CloakBrowser `0.7.3.1`).
    - `-dev.<YYYYMMDD>` is added only when tracking a moving tag like `dev`; the
      date is the one of the pinned image.
    - The revision starts at 1 and resets whenever the upstream part changes.
    - Ordering is not reliable with this scheme, so don't use `breaking_versions`
      without checking it first.
14. **`CHANGELOG.md` is read by pattern.** When an update is available, Home
    Assistant Core (`async_release_notes`, `components/hassio/update.py`) shows
    the part of the file found with `^#* <latest>\n` up to the first line that
    starts with `#* <installed>`; the Supervisor only serves the raw file.
    So: newest version first; every heading is exactly `## <version>` and
    nothing else on the line (no brackets, dates or links — Keep a Changelog
    headings like `## [1.0.0] - 2026-01-01` don't match, and then users get the
    whole file); a version that is a text prefix of newer ones (`0.70.4` against
    `0.70.4-dev…`, `.1` against `.10`) cuts the notes short; put
    backward-incompatible changes at the top of the newest entry.
