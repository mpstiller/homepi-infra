#!/usr/bin/env bash
set -euo pipefail

# Read-only system snapshot. Intentionally does NOT print .env files, API keys,
# container environment variables, or application databases.

section() { printf '\n\n===== %s =====\n' "$1"; }

section "DATE"
date -Is

section "OS"
uname -a
cat /etc/os-release

section "BOOT / STORAGE"
findmnt /
lsblk -o NAME,SIZE,MODEL,FSTYPE,MOUNTPOINTS
df -h / /srv/data 2>/dev/null || true

section "RASPBERRY PI"
vcgencmd measure_temp 2>/dev/null || true
vcgencmd bootloader_config 2>/dev/null | grep BOOT_ORDER || true
rpi-eeprom-update 2>/dev/null || true

section "DOCKER"
docker version --format '{{.Server.Version}}' 2>/dev/null || docker version || true
docker compose version || true
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'

section "DIRECTORIES"
for p in /opt/homelab/stacks /srv/appdata /srv/data /srv/backups; do
  if [ -e "$p" ]; then
    du -sh "$p" 2>/dev/null || true
  fi
done

section "MEDIA TREE"
find /srv/data -maxdepth 3 -type d -print 2>/dev/null | sort || true
