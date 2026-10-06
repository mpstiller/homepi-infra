# Remote access

## Current solution: Tailscale

Tailscale is installed directly on the HomePi host and is the private remote-access layer.

Current HomePi Tailscale identity:

```text
Hostname: homepi
Tailscale IPv4: 100.72.110.114
```

No router port forwarding is required. This is particularly suitable for the current O2 / FRITZ!Box DS-Lite connection.

## Access model

Remote client devices join the same Tailnet with the Tailscale client.

Examples:

```text
SSH              -> 100.72.110.114:22
Homepage         -> 100.72.110.114:3000
Arcane           -> 100.72.110.114:3552
Seerr            -> 100.72.110.114:5055
Radarr           -> 100.72.110.114:7878
qBittorrent UI   -> 100.72.110.114:8080
Music Assistant  -> 100.72.110.114:8095
Jellyfin         -> 100.72.110.114:8096
Home Assistant   -> 100.72.110.114:8123
Sonarr           -> 100.72.110.114:8989
Prowlarr         -> 100.72.110.114:9696
```

MagicDNS short-name access also works as `homepi:<port>` on clients that resolve short Tailnet hostnames correctly.

For third-party apps and browsers that may interpret a single-label hostname such as `homepi` as a search term, prefer either:

- the Tailscale IPv4 address, or
- the full MagicDNS FQDN once recorded.

## Homepage host validation

Homepage explicitly allows:

```text
homepi.local:3000
homepi:3000
100.72.110.114:3000
```

Do not replace this with a wildcard unless there is a deliberate reason.

## Security boundaries

- Do not expose SSH or admin UIs directly through FRITZ!Box port forwarding.
- Tailscale is for private administrative/device access.
- qBittorrent Internet traffic remains isolated through Gluetun + Proton VPN.
- Installing Tailscale on the host does not replace or bypass the Gluetun network namespace used by qBittorrent.
- Public application access, if added later, should be designed separately with a controlled tunnel/reverse proxy.
