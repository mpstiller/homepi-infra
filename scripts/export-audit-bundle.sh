#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-/tmp/homepi-audit}"
rm -rf "$OUT"
mkdir -p "$OUT/system" "$OUT/stacks"

redact_compose() {
  local src="$1"
  local dst="$2"
  python3 - "$src" "$dst" <<'PY'
import re, sys, pathlib
src, dst = map(pathlib.Path, sys.argv[1:3])
text = src.read_text(errors="replace")
secret_words = re.compile(r'(password|passwd|token|secret|private.?key|encryption.?key|api.?key|credential|cookie)', re.I)
out = []
for line in text.splitlines():
    # Redact common YAML key/value secrets while preserving indentation/key name.
    m = re.match(r'^(\s*)([-]?[\s]*)(["\']?[^:#]+["\']?)\s*:\s*(.*)$', line)
    if m and secret_words.search(m.group(3)):
        value = m.group(4).strip()
        # Preserve variable references such as ${FOO}; they contain no secret value.
        if value and not re.fullmatch(r'["\']?\$\{[A-Za-z_][A-Za-z0-9_]*\}["\']?', value):
            line = f"{m.group(1)}{m.group(2)}{m.group(3)}: <REDACTED>"
    # Also redact KEY=value style entries embedded in environment lists.
    m2 = re.match(r'^(\s*-?\s*)([A-Za-z_][A-Za-z0-9_]*)(=)(.*)$', line)
    if m2 and secret_words.search(m2.group(2)):
        v = m2.group(4).strip()
        if v and not re.fullmatch(r'\$\{[A-Za-z_][A-Za-z0-9_]*\}', v):
            line = f"{m2.group(1)}{m2.group(2)}=<REDACTED>"
    out.append(line)
dst.write_text("\n".join(out) + "\n")
PY
}

env_example() {
  local src="$1"
  local dst="$2"
  awk '
    /^[[:space:]]*#/ || /^[[:space:]]*$/ { print; next }
    /^[A-Za-z_][A-Za-z0-9_]*=/ {
      split($0,a,"=");
      key=a[1];
      if (key=="PUID" || key=="PGID" || key=="TZ") print $0;
      else print key "=<REDACTED>";
      next
    }
  ' "$src" > "$dst"
}

{
  echo "===== DATE ====="
  date -Is
  echo
  echo "===== OS ====="
  uname -a
  cat /etc/os-release
  echo
  echo "===== ROOT / STORAGE ====="
  findmnt /
  lsblk -o NAME,SIZE,MODEL,FSTYPE,MOUNTPOINTS
  df -h / /srv/data 2>/dev/null || true
  echo
  echo "===== RASPBERRY PI ====="
  vcgencmd measure_temp 2>/dev/null || true
  vcgencmd bootloader_config 2>/dev/null | grep BOOT_ORDER || true
  rpi-eeprom-update 2>/dev/null || true
  echo
  echo "===== DOCKER ====="
  docker version --format '{{.Server.Version}}' 2>/dev/null || docker version || true
  docker compose version || true
  docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
  echo
  echo "===== DIRECTORY USAGE ====="
  for p in /opt/homelab/stacks /srv/appdata /srv/data /srv/backups; do
    [ -e "$p" ] && du -sh "$p" 2>/dev/null || true
  done
  echo
  echo "===== MEDIA TREE ====="
  find /srv/data -maxdepth 3 -type d -print 2>/dev/null | sort || true
} > "$OUT/system/system-report.txt"

# Capture safe Docker networking facts without container environment variables.
docker network ls > "$OUT/system/docker-networks.txt" 2>&1 || true

# Redacted Compose files and variable-name-only env examples.
if [ -d /opt/homelab/stacks ]; then
  while IFS= read -r -d '' file; do
    rel="${file#/opt/homelab/stacks/}"
    mkdir -p "$OUT/stacks/$(dirname "$rel")"
    redact_compose "$file" "$OUT/stacks/$rel"
  done < <(find /opt/homelab/stacks -maxdepth 3 -type f \( -name 'compose.yaml' -o -name 'compose.yml' -o -name 'docker-compose.yml' -o -name 'docker-compose.yaml' \) -print0)

  while IFS= read -r -d '' file; do
    rel="${file#/opt/homelab/stacks/}"
    dst="$OUT/stacks/$(dirname "$rel")/.env.example"
    mkdir -p "$(dirname "$dst")"
    env_example "$file" "$dst"
  done < <(find /opt/homelab/stacks -maxdepth 3 -type f -name '.env' -print0)
fi

# Selected qBittorrent facts only; no credentials.
{
  echo "===== VERSION ====="
  docker exec gluetun sh -c 'wget -qO- http://127.0.0.1:8080/api/v2/app/version' 2>/dev/null || true
  echo
  echo "===== SELECTED PREFERENCES ====="
  docker exec gluetun sh -c 'wget -qO- http://127.0.0.1:8080/api/v2/app/preferences' 2>/dev/null |
    python3 -c 'import json,sys; d=json.load(sys.stdin); keys=["save_path","temp_path_enabled","temp_path","current_network_interface","current_interface_address","listen_port","torrent_content_layout","max_ratio","max_seeding_time","max_ratio_enabled","max_seeding_time_enabled","autorun_enabled"]; print(json.dumps({k:d.get(k) for k in keys if k in d}, indent=2))' || true
  echo
  echo "===== CATEGORIES ====="
  docker exec gluetun sh -c 'wget -qO- http://127.0.0.1:8080/api/v2/torrents/categories' 2>/dev/null || true
} > "$OUT/system/qbittorrent-safe.txt"

# Last Gluetun status lines are useful but do not include env/private keys.
docker logs gluetun --tail 80 > "$OUT/system/gluetun-tail.txt" 2>&1 || true

# Inventory filenames only for selected appdata locations; no DB/config contents.
for app in sonarr radarr prowlarr jellyfin homeassistant music-assistant qbittorrent gluetun; do
  if [ -d "/srv/appdata/$app" ]; then
    find "/srv/appdata/$app" -maxdepth 2 -type f -printf '%p\n' 2>/dev/null | sort > "$OUT/system/appdata-files-$app.txt" || true
  fi
done

tar -C "$(dirname "$OUT")" -czf "${OUT}.tar.gz" "$(basename "$OUT")"
echo "Created: ${OUT}.tar.gz"
echo "Review before sharing if desired. The script intentionally excludes .env values and app databases/config contents."
