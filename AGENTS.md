# Rules for every app in this repository

1. **Never build your own image.** Inherit an upstream image (`FROM ...`) and
   patch on top. Fall back to a base image + package install only when no
   maintained upstream image exists. Pin everything that matters: base images by
   tag and digest (`FROM image:tag@sha256:...`, look it up with
   `regctl image digest`) and Python packages with `==`.
   Don't hand-write a list of system libraries: derive it from what already
   knows it, for example the `Depends` of Debian's `chromium` package through
   `apt-cache depends`, and check the result with `ldd` or `ldconfig -p`.
2. **Modern app conventions.** Use the current app manifest keys
   (`homeassistant_api`/`hassio_api` where the app talks to Home Assistant),
   the app's own data, and the new `map` names: `app_config` (not the
   deprecated `addon_config`), `homeassistant_config` (not `config`),
   `all_app_configs` (mounted at `/app_configs`). Use the `map` list form
   (`type`/`read_only`/`path`), not the old short form.
   Need a persistent folder for something else (a cache, a download)? Point the
   software at one under `/data` with an environment variable. `map` can't add
   a folder: it keeps one entry per type, and `type: data` with a `path` moves
   `/data` instead of adding a mount. A symlink also works, but the variable
   needs no extra step.
3. **BuildKit is available** — use modern Dockerfile syntax (`RUN --mount`,
   `COPY --chmod`, heredocs). Put small configs and scripts inline with
   `COPY <<'EOF' /path` instead of extra files. For files that live in git, set
   exec bits with `git add --chmod=+x`, not `RUN chmod`.
4. **Less is more.** Fewest files and moving parts. Keep `icon.png` and
   `logo.png`; skip CI and other boilerplate unless it earns its place. Stay
   agnostic to optional plugins: no settings for them in the app, users add
   those through the environment variables option.
5. **Web UIs use ingress** (Home Assistant handles auth): set `ingress_port`
   to the app's own port, only trust `X-Ingress-Path` from `172.30.32.2`, and
   keep host ports off by default (`ports: {5000/tcp: null}`). Test with a
   Docker network on `172.30.32.0/23` and a client at `172.30.32.2`. When a
   proxy is needed, use Caddy
   (`COPY --from=caddy:2@sha256:... /usr/bin/caddy`, never nginx) and always set
   `auto_https off` and `admin off`: no Let's Encrypt, no admin API.
6. **Set `init` by what the image has.** Images without a real init system
   (most upstream images; Python, Node and browser apps) use `init: true`, which
   is the default, so leave the key out: Docker's init then reaps child
   processes and forwards stop signals. Images that bake in their own init,
   like s6-overlay (Home Assistant base images, linuxserver.io), must set
   `init: false`. Use a `tcp://` watchdog, so an app login redirect can't look
   unhealthy.
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
15. **Deploy and verify on the user's Home Assistant yourself.** The ssh MCP
    (profile `homeassistant`, tool `ssh:run-command`) gives a shell on the
    instance, where the `ha` CLI manages apps. Slugs are `72547810_<folder>`,
    hostnames `72547810-<folder>`, containers `app_72547810_<folder>`.
    - After pushing run `ha store reload`. Without it `version_latest` stays on
      an older commit and a pending update can look absent.
    - Check with `ha apps info <slug> | grep -E '^(state|version|version_latest|update_available):'`;
      `version_latest` must match `config.yaml`.
    - Deploy with `ha apps update <slug>` (`ha apps rebuild <slug>` for the same
      version). It prints nothing until it finishes and can take many minutes,
      because the Supervisor builds in a helper container and the first pull of
      a base image is slow on this host (about 0.2 MB/s observed).
    - The ssh tool gives up after about a minute: start long commands with
      `nohup … > /tmp/x.log 2>&1 &`, then poll with short commands (`sleep`
      at most 40).
    - Follow a build with `docker logs app_builder_<slug> --tail 3` and
      `ha jobs info | grep -E 'name:|done:'` (an `app_update` job with
      `done: false` is still running).
    - It is done when the builder container is gone, the log file says "Command
      completed successfully.", `ha apps info` shows `update_available: false`,
      and `docker ps` shows the image `72547810/<arch>-addon-<folder>:<version>`.
    - Afterwards: `ha apps logs <slug>`, `docker logs app_<slug> --tail 30`, and
      `ha apps changelog <slug>` (what users will be offered).
