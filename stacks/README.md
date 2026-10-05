# Runtime stacks

This directory is being converted from reconstructed documentation into the checked-in runtime configuration source.

## Verified from the live Pi on 2026-10-05

Live Compose files have been synchronized for:

- `arcane/`
- `homepage/`
- `homeassistant/`
- `jellyfin/`
- `media/`

The checked-in files were exported from `/opt/homelab/stacks` and reviewed so secret values remain external.

## Still to resolve

The running `music-assistant` container did not have a Compose file captured from the expected `/opt/homelab/stacks` tree in the first audit. Do not reconstruct it from memory. The second runtime audit will inspect Docker Compose labels, mounts and image metadata to determine its actual deployment source.

## Secrets

Real `.env` files stay on the Pi. Only `.env.example` files belong in Git.

If live files and prose documentation disagree, verify the live system and update the documentation rather than silently changing a known-good runtime file.
