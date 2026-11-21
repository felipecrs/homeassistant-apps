#!/usr/bin/env bash
set -euo pipefail

opt() {
  python3 -c 'import json,sys;print(json.load(open(sys.argv[1])).get(sys.argv[2],""))' \
    /data/options.json "$1"
}

export CLOAKBROWSER_LICENSE_KEY="$(opt license_key)"

args=(cloakserve --data-dir=/data/profiles --keep-profiles)
[ "$(opt headless)" = "False" ] && args+=(--headless=false)

exec "${args[@]}"
