#!/usr/bin/env bash
# Install only from the reviewed, pinned repository bundle. Run on HomePi as root.
set -Eeuo pipefail
umask 077
cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.."
[[ $EUID == 0 ]] || { echo 'Run this installer with sudo.' >&2; exit 1; }

check_baseline() {
  local actual
  actual=$(sha256sum "$1")
  actual=${actual%% *}
  shift
  local expected
  for expected in "$@"; do
    [[ $actual == "$expected" ]] && return 0
  done
  echo 'STOP: installed Homepage configuration differs from reviewed baseline; no installation performed.' >&2
  return 1
}

check_baseline /opt/homelab/stacks/homepage/compose.yaml \
  2b19faa5afec09342a3ed92d20a2a490dc17f0a98fa42d4870aecb7e75fbeae7 \
  2542333af06019c0f681b2b2611aa1337adec4386dab84448f8f96e76c672b72
check_baseline /srv/appdata/homepage/services.yaml \
  0ddcff664891cc484294fb3b5effde1092b89d01db21fc54cc4f01ac6a5f9932
check_baseline /srv/appdata/homepage/settings.yaml \
  9740d56bbef7ab560641e246a3208b0a098c85ba6f8d4656924f356ec6ce2ae2
[[ ! -e /usr/local/sbin/homepi-status && ! -e /etc/systemd/system/homepi-status.service &&
   ! -e /etc/systemd/system/homepi-status.timer && ! -e /srv/appdata/homepi-status ]] || {
  echo 'STOP: a status installation already exists; review before updating.' >&2; exit 1;
}
sha256sum --quiet -c operations/SHA256SUMS
docker compose --project-directory /opt/homelab/stacks/homepage \
  -f stacks/homepage/compose.yaml config --quiet
# Only the new small status image is pulled; existing application images are retained.
docker compose --project-directory /opt/homelab/stacks/homepage \
  -f stacks/homepage/compose.yaml pull operations-status
exec 9>/run/lock/homepi-restic.lock
flock -n -x 9 || {
  echo 'STOP: backup/maintenance/audio is busy. Wait for completion and retry.' >&2; exit 1;
}

rollback=$(mktemp -d /root/homepi-status-rollback.XXXXXXXX)
cp -a /opt/homelab/stacks/homepage/compose.yaml "$rollback/compose.yaml"
cp -a /srv/appdata/homepage/services.yaml "$rollback/services.yaml"
cp -a /srv/appdata/homepage/settings.yaml "$rollback/settings.yaml"
echo "Rollback configuration: $rollback"
trap 'echo "Installation interrupted. Retained rollback: $rollback; see operations/README.md" >&2' ERR
install -d -m 755 /srv/appdata/homepi-status
install -m 755 operations/homepi-status /usr/local/sbin/homepi-status
install -m 644 operations/systemd/homepi-status.{service,timer} /etc/systemd/system/
systemd-analyze verify /etc/systemd/system/homepi-status.{service,timer}
systemctl daemon-reload
systemctl start homepi-status.service
# Do not publish widgets until a complete first collection exists.
test -s /srv/appdata/homepi-status/status.json
install -m 644 stacks/homepage/compose.yaml /opt/homelab/stacks/homepage/compose.yaml
# Preserve Homepage config owner/group so its existing PUID/PGID can read it.
cat stacks/homepage/config/services.yaml > /srv/appdata/homepage/services.yaml
cat stacks/homepage/config/settings.yaml > /srv/appdata/homepage/settings.yaml
systemctl enable --now homepi-status.timer
docker compose --project-directory /opt/homelab/stacks/homepage \
  -f /opt/homelab/stacks/homepage/compose.yaml up -d --no-deps --pull never operations-status homepage
echo 'Installed. Verify the three Betriebsstatus cards on Homepage.'
echo "If any step failed, retained rollback files: $rollback"
