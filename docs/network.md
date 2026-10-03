# Network

## Current environment

- FRITZ!Box 6690 Cable.
- O2 cable connection with DS-Lite.
- IPv6 available; no conventional inbound public IPv4 assumption.
- Final server connection should be Ethernet near the router; Wi-Fi was used during setup/testing.
- mDNS hostname: `homepi.local`.

## Security / exposure

- Do not expose Arcane, Docker socket, Home Assistant admin, qBittorrent WebUI, or FlareSolverr directly to the public Internet.
- Router UPnP/automatic public port mapping is not part of the design.
- Future admin access should use a private overlay network.
- Future public apps should use a deliberate tunnel/reverse-proxy architecture.

## qBittorrent VPN boundary

qBittorrent has no independent normal network stack in the Compose design; it uses `network_mode: service:gluetun`. This is deliberate so Gluetun's firewall acts as the kill switch.
