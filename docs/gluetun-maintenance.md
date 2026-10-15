# Gluetun pinning and maintenance

## Applied state — 2026-10-15

The owner executed the Pi commands and supplied the results. The active file is `/opt/homelab/stacks/media/compose.yaml`; its Docker Compose labels confirmed this source. The only intended runtime configuration change is the Gluetun image reference:

```yaml
image: qmcgaw/gluetun@sha256:12df8b20528d4cd5e9b6e827d40f2886cf78e53e7e9afc750050648c31183793
```

This is the image already validated in the October 14 inventory. It is not a version upgrade. Before applying it, the owner confirmed running/local image IDs and RepoDigest, Linux/arm64, valid Compose, inactive backup/maintenance services, and qBittorrent's namespace reference matching Gluetun's container ID. A timestamped Compose backup was created before editing; VERIFY ON PI: its exact filename. No image was pulled. Persistent mounts, VPN credentials, firewall, forwarding hooks and other service definitions were unchanged.

## Verification and recovery evidence

- Gluetun and qBittorrent were recreated together with `--pull never`; Compose reported success. Subsequent inspect output confirmed the pinned Gluetun image and qBittorrent pointing to its new container ID.
- qBittorrent used `tun0`, bind address `0.0.0.0`, and the same port as `/tmp/gluetun/forwarded_port`. Host and shared VPN namespace public IPv4 addresses differed (owner comparison).
- Tunnel-down test: `http://1.1.1.1/cdn-cgi/trace` was reachable first. After `ip link set tun0 down`, a fresh request to the same fixed IPv4 target failed, with `tun0` still DOWN before and after that request. A shell EXIT trap raised the interface afterward.
- Raising the interface alone left Gluetun healthy but qBittorrent bound to `lo` / port `0`, consistent with the configured forwarding-down hook. The forwarded-port command supplied no value in the reported output.
- A Gluetun-only `docker restart` did not restore the qBittorrent API path: the preferences request supplied no parseable JSON. A stale qBittorrent network namespace is a possible explanation, not a proven root cause; namespace identities were not measured at this failure point. Identical container IDs alone do not establish that two processes still share a kernel network namespace after a restart.
- Joint recreation restored qBittorrent API HTTP 200, version `v5.2.4`, `tun0` / `0.0.0.0`, matching forwarded/listen port `33266`, and a successful outbound IP request. Ports previously observed during this session were `43695` and `38344`; all are historical, dynamic values. Never hardcode them.

Scope: this is one targeted IPv4 blocking test plus manual recovery. It does not establish all IPv4 destinations/protocols, IPv6/DNS leak behavior, ordinary automatic reconnection, full-host reboot recovery or end-to-end torrent transfers. The host/VPN IP difference was checked before the interruption; a final VPN IP request succeeded after recovery, without a new host/VPN comparison. Gluetun health alone is insufficient to confirm qBittorrent API/binding/forwarding health.

## Planned joint recreation

This interrupts downloads briefly. The owner runs terminal commands. Before starting, confirm backup/maintenance are inactive, validate Compose with `docker compose config --quiet`, and review the configuration against the running deployment. Check that the local qBittorrent image still matches its running image; `--pull never` prevents downloads but does not prevent using a previously changed local tag.

Joint recreation was used successfully on the Pi. For future runs, use this guard, which also aborts if either image inspection fails:

```bash
cd /opt/homelab/stacks/media

if homepi_qbit_running_image=$(docker inspect qbittorrent --format '{{.Image}}') &&
   homepi_qbit_local_image=$(docker image inspect lscr.io/linuxserver/qbittorrent:latest --format '{{.Id}}') &&
   [ -n "$homepi_qbit_running_image" ] &&
   [ "$homepi_qbit_running_image" = "$homepi_qbit_local_image" ]; then
  docker compose stop qbittorrent &&
  docker compose up -d --no-deps --pull never --force-recreate \
    --wait --wait-timeout 120 gluetun qbittorrent
else
  echo "Abort: image inspection failed or local qBittorrent image differs."
fi
```

If either inspection fails, stop and review its error before proceeding. If Compose fails/times out, inspect selected status/error evidence; do not repeatedly restart Gluetun alone or remove the VPN boundary. This procedure is for planned maintenance/recovery, not a replacement for normal system shutdown or every automatic VPN reconnect. Stop if backup/maintenance becomes active; the commands above do not acquire the shared backup lock.

After startup, allow forwarding to initialize, then verify:

1. Gluetun healthy; qBittorrent running and its API reachable from Gluetun.
2. Pinned image unchanged; qBittorrent's `container:...` reference matches Gluetun's current ID after joint recreation.
3. qBittorrent API version unchanged and preferences `tun0` / `0.0.0.0`.
4. Its listen port matches the current nonzero `/tmp/gluetun/forwarded_port` value.
5. Outbound access works through the shared namespace and its public IPv4 differs from the host's normal public IPv4.

Do not publish full preferences, environments or raw configuration containing keys. Record selected fields only. The October 15 recovery confirmed items 1, 3, 4 and outbound access; the namespace and host/VPN comparison were confirmed during the initial joint recreation, before the disruption.

## Rollback and further work

The original Compose file is retained on the Pi under its timestamped backup name. Returning to `latest` would undo the protection against a moving tag; it does not by itself select an older software version. If reverting the file becomes necessary, review its diff, validate Compose and use the same controlled joint recreation and postchecks. Do not pull `latest` as a recovery shortcut. No rollback was applied in this session.

The forwarding hooks remain unchanged. Whether automatic failure recovery needs improvement is a separate diagnostic task; preserve the observed fail-closed behavior. The next roadmap work is independent recovery secrets and lightweight backup failure/staleness visibility.

References: [Gluetun firewall](https://github.com/qdm12/gluetun-wiki/blob/main/faq/firewall.md), [Gluetun healthcheck and automatic recovery](https://github.com/qdm12/gluetun-wiki/blob/main/faq/healthcheck.md), [Docker Compose up](https://docs.docker.com/reference/cli/docker/compose/up/).
