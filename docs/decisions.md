# Architecture Decision Log

## ADR-001 — Use NVMe as the primary system disk

**Decision:** Boot and run the Pi directly from the Samsung 990 EVO Plus 2 TB NVMe.

**Reason:** better durability/performance than the temporary microSD and enough capacity to learn actual usage.

## ADR-002 — Do not buy a large HDD yet

**Decision:** Use the 2 TB NVMe for OS, appdata, downloads, and media for now.

**Reason:** actual storage demand is unknown; avoid unnecessary cost, noise, power, and complexity.

**Revisit when:** sustained real usage approaches a meaningful capacity threshold or retention needs become clear.

## ADR-003 — Preserve a common `/data` mount for media automation

**Decision:** qBittorrent, Sonarr, and Radarr share the same `/data` filesystem view.

**Reason:** enables hardlinks and atomic/efficient imports.

## ADR-004 — qBittorrent only goes through VPN

**Decision:** qBittorrent shares Gluetun's network namespace; the rest of the stack does not use the VPN by default.

**Reason:** strong isolation and kill-switch behavior without unnecessarily routing Home Assistant/Jellyfin/etc. through the VPN.

## ADR-005 — Proton VPN + WireGuard + port forwarding

**Decision:** Proton paid plan, WireGuard, NAT-PMP/port-forwarding configuration, Gluetun integration.

**Reason:** supports inbound peer connectivity while keeping qBittorrent isolated. Kill-switch and IP isolation were validated.

## ADR-006 — 1080p V1 media profile

**Decision:** prioritize good 1080p Bluray/WEB encodes; no 4K, 720p, or 1080p remux in the default V1 profile.

**Reason:** balance quality, 65-inch OLED viewing, Pi Direct Play, and 2 TB storage constraints. 4K can be a separate future profile.

## ADR-007 — German dual-language is the preferred media outcome

**Decision:** prefer German DL, then German, while permitting English/original as fallback through Custom Format scoring.

## ADR-008 — Home Assistant supplements Google Home

**Decision:** keep existing Google Home voice usability and use Home Assistant as the richer backend/automation layer.

## ADR-009 — Defer heavy photo-cloud stack

**Decision:** do not add Immich yet on the 4 GB Pi.

**Reason:** stabilize current workloads and understand resource headroom first.

## ADR-010 — Keep existing web apps on Vercel/Supabase for now

**Decision:** do not move current production `planner` / `quoernchenkueche` apps to the Pi merely for the sake of self-hosting.

**Reason:** current cloud deployment is appropriate; Pi may later host staging/new small apps.
