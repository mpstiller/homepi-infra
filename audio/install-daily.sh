#!/usr/bin/env bash
set -Eeuo pipefail
umask 077
[[ $EUID == 0 ]] || { echo 'Run this installer with sudo.'; exit 1; }
payload=${1:?Usage: install-daily.sh VERIFIED_PAYLOAD_DIRECTORY}
[[ $payload == /* && -d $payload ]] || { echo 'STOP: payload must be an absolute directory.'; exit 1; }

exec 9>/run/lock/homepi-restic.lock
flock -n -x 9 || { echo 'STOP: Backup/Wartung/Audio ist beschäftigt. Später erneut versuchen.'; exit 1; }
test "$(systemctl show homepi-audio.service -p ActiveState --value)" = inactive
test "$(systemctl is-active homepi-audio.timer || true)" = inactive

sha256sum --quiet -c <<'BASELINE'
17a2c935df16cb8f5c3747d2733e1d238cabae06b4ce9d5f673b0ef1bfef7d2f  /usr/local/sbin/homepi-audio
a0abaa5f3981bf5ade22700117caf3236deadc704d2529157e083df723550d00  /etc/systemd/system/homepi-audio.service
a54bb6c1649c11262859838bcb9a854ac2894d1222e3c22b5c2a1041c71fc8d1  /etc/systemd/system/homepi-audio.timer
e3c4d12944aaaf613a477c3b7deedff070a68cb6931b84e90acf4b72083b9c35  /usr/local/sbin/homepi-status
BASELINE

rollback=$(mktemp -d /root/homepi-audio-daily-rollback.XXXXXXXX)
echo "Rollback: $rollback"
cp -a "$payload" "$rollback/payload"
cd "$rollback/payload"
sha256sum --quiet -c <<'PAYLOAD'
c8780993d911dc56c4d72ada6106c4ae520ede2fcf5872f839dd6bbcfc183480  audio/bin/homepi-audio
039d14c8df8bafc5793bc71a130360160c03917d7d26e06b1580790d457dd8d5  audio/systemd/homepi-audio.service
3b4e9c864ee1842e9f50141339abe8f6df5a05222024b1f3c49292e3f1ac740e  audio/systemd/homepi-audio.timer
cf31b70bffc04064138443517d835a9bad205f44210655ca47f10d296e96a0ab  operations/homepi-status
PAYLOAD
python3 -c 'import ast; from pathlib import Path; [ast.parse(Path(p).read_text()) for p in ["audio/bin/homepi-audio", "operations/homepi-status"]]'
systemd-analyze verify audio/systemd/homepi-audio.service audio/systemd/homepi-audio.timer

cp -a /usr/local/sbin/homepi-audio "$rollback/homepi-audio"
cp -a /usr/local/sbin/homepi-status "$rollback/homepi-status"
cp -a /etc/systemd/system/homepi-audio.service "$rollback/homepi-audio.service"
cp -a /etc/systemd/system/homepi-audio.timer "$rollback/homepi-audio.timer"
status_active=$(systemctl is-active homepi-status.timer || true)
changed=0
success=0
cleanup() {
  code=$?
  trap - EXIT
  set +e
  if ((success == 0)); then
    if ((changed)); then
      cp -a "$rollback/homepi-audio" /usr/local/sbin/homepi-audio
      cp -a "$rollback/homepi-status" /usr/local/sbin/homepi-status
      cp -a "$rollback/homepi-audio.service" /etc/systemd/system/homepi-audio.service
      cp -a "$rollback/homepi-audio.timer" /etc/systemd/system/homepi-audio.timer
      systemctl daemon-reload
    fi
    [[ $status_active == active ]] && systemctl start homepi-status.timer
    systemctl start homepi-audio.timer
    echo "Installation abgebrochen; bisherige Dateien wiederhergestellt. Rollback: $rollback"
  fi
  exit "$code"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

systemctl stop homepi-status.timer
systemctl stop homepi-status.service
changed=1
install -m 755 audio/bin/homepi-audio /usr/local/sbin/homepi-audio
install -m 755 operations/homepi-status /usr/local/sbin/homepi-status
install -m 644 audio/systemd/homepi-audio.service /etc/systemd/system/homepi-audio.service
install -m 644 audio/systemd/homepi-audio.timer /etc/systemd/system/homepi-audio.timer
systemctl daemon-reload
systemctl start homepi-status.service
if [[ $status_active == active ]]; then systemctl start homepi-status.timer; fi
systemctl start homepi-audio.timer
success=1
echo 'Installiert. Audio startet künftig täglich um 07:00 Uhr Europe/Berlin.'
systemctl list-timers homepi-audio.timer --all --full --no-pager
