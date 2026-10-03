# Storage and filesystem layout

## Host layout

```text
/opt/homelab/stacks   Compose definitions
/srv/appdata          persistent app state/config
/srv/data             media/download data
/srv/backups          future backups
```

## Media layout

```text
/srv/data/
├── torrents/
│   ├── movies/
│   ├── tv/
│   ├── incomplete/
│   │   ├── radarr/
│   │   └── sonarr/
│   └── test/
└── media/
    ├── movies/
    └── tv/
```

Containers see the same tree as `/data`.

## Why this matters

Sonarr/Radarr must be able to hardlink from `/data/torrents/...` to `/data/media/...`. If downloads and media are presented as separate Docker mounts/filesystems, hardlinks may fail and files will be copied instead.

## Hardlink behavior verified

During the real Sonarr test:

- torrent-side and media-side files shared the same inode and had `links=2`;
- deleting the torrent plus torrent-side data reduced the media file to `links=1` without deleting it;
- therefore storage was not duplicated while seeding.

## Capacity policy

Use the 2 TB NVMe first. Reconsider HDD capacity only after measuring actual sustained consumption.
