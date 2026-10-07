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


## Hardening

The Tailnet has been hardened beyond the default unrestricted policy:

- Device Approval is enabled.
- The default allow-all grant has been removed.
- Only the tailnet owner may access HomePi over Tailscale.
- Access is restricted to the explicitly required HomePi ports plus ICMP.
- Tailscale SSH is not used; normal OpenSSH on TCP 22 remains the SSH authentication layer.
- Key expiry is disabled for the headless `homepi` node to avoid losing unattended remote access.
- The identity provider is a Google account protected with a passkey.
- Tailscale auto-update is enabled on HomePi.

Allowed Tailscale ports:

```text
22    SSH
3000  Homepage
3552  Arcane
5055  Seerr
7878  Radarr
8080  qBittorrent WebUI
8095  Music Assistant
8096  Jellyfin
8123  Home Assistant
8989  Sonarr
9696  Prowlarr
```

The Tailnet policy is deny-by-default for all other HomePi ports.


### Known issue: Jellyfin remote connection

A remote MacBook on the Tailnet can open the Jellyfin web client at `http://homepi:8096`, but the client currently cannot connect to the HomePi Jellyfin server. Automatic discovery is not expected to work across the Tailscale overlay, and manually adding `http://homepi:8096` also fails.

This is an unresolved Jellyfin-specific remote-access issue. Other HomePi services remain reachable through Tailscale/MagicDNS, so it should be debugged independently from Homepage.
