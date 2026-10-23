# Sony audio compatibility worker — pilot pending

## Evidence and scope

Owner tested Attack on Titan S01E01 on Sony KD-65AF9 in native Jellyfin Android TV 0.19.10. Source: HEVC Main 10 video, English TrueHD 5.1 and Japanese TrueHD stereo. Adding two AC3 tracks while retaining TrueHD improved playback but still stuttered and the player aborted. Disabling subtitles did not solve it. A video+Japanese-AC3-only copy played smoothly but once aborted during seeking. A further remux retaining both AC3 tracks, original subtitles/chapters and other streams but removing both TrueHD tracks then worked with subtitles, audio switching and seeking. This supports removing TrueHD from the derived TV file; it does not prove a universal TrueHD bug or network cause for the earlier abort.

Prepared automation replaces each TrueHD track with AC3 in a derived MKV and archives the full original separately. It does not leave TrueHD in the TV file. Existing other codecs are copied. Mono/stereo use 192 kbit/s; 5.1 uses 640 kbit/s. TrueHD 7.1 is downmixed to AC3 5.1 only in the derivative; that channel layout has not been tested on the Sony. Other layouts are refused. Video payload is copied and SHA256-checked, subtitle streams and attachments are mapped, languages/chapter count/duration checked. The first actual worker-generated file still requires a Pi/Sony pilot: the manual successful test used a different stream ordering.

## Prepared files and private configuration

- `audio/bin/homepi-audio` -> `/usr/local/sbin/homepi-audio`, root-owned 0755.
- `audio/systemd/homepi-audio.service` and `.timer` -> `/etc/systemd/system/`, 0644.
- `/etc/homepi-audio/jellyfin.key`: dedicated Jellyfin API key created privately in Dashboard -> API Keys; root-owned 0600 inside a root-owned 0700 directory. Never paste the key into chat/Git. The key is sent only in an HTTP header to `127.0.0.1:8096`, redirects and environment proxies disabled. No admin UI is exposed.
- `/etc/homepi-audio/enabled`: absent by default. Automatic service execution requires this explicit enable marker as well as timer activation. Installation alone must not create the marker or enable the timer.
- Private scan cache: `/srv/appdata/homepi-audio/state.json` (included in existing appdata backup). No-TrueHD fingerprints are cached only in apply mode. Dry run does not cache or alter media; it acquires the shared lock and launches read-only probes.

## Behavior

Only imported `.mkv` files in `/srv/data/media/movies` and `/srv/data/media/tv` are candidates. Audio-test, torrent and archive folders are excluded. Symlinks, paths outside the roots and colon-containing paths are refused. Files younger than five minutes are deferred; the pre-commit fingerprint must still match. The source is mounted read-only in a disposable converter. It reuses the exact local running Jellyfin image ID with `--pull never`, network none, read-only container root, no capabilities, one CPU, 512 MiB RAM/no extra swap and a PID limit. There is no video encoder.

At most one TrueHD candidate is converted per apply invocation. The worker uses the existing exclusive `/run/lock/homepi-restic.lock` so it cannot overlap backup, maintenance or another worker; a busy lock defers the run. The timer checks five minutes after boot/last completed invocation. Old untouched TrueHD files are also eligible after enabling; this is intentionally a backlog scan, not only future downloads. A failing first candidate stops that invocation and may need a targeted fix to avoid starving later files. No unattended error email is configured for this new worker yet; inspect its systemd journal during the pilot.

The worker defers if Jellyfin reports any playing or paused item, including music, and checks again before replacement. API failures prevent replacement. This is a conservative best-effort guard, not an atomic reservation: a client can start playback in the small interval after the last API check. Do the pilot with all players stopped and validate live session behavior before enabling unattended processing.

Staging is outside the scanned libraries at `/srv/data/.homepi-audio-staging`. Output space must exceed 1.5 times source size plus a 2 GiB reserve. After validation, the original inode is hardlinked into a private timestamp/UUID directory under `/srv/data/media-originals/` with `original.mkv` and a source-path manifest. Then `os.replace` publishes the new inode at the original library pathname. Any torrent hardlink keeps original bytes; no shared inode is edited. The archive and staging must be on the same filesystem as the media. The archive hardlink still shares original bytes with any existing torrent link, so later external writes to that inode would also affect the archive.

The original archive is outside Jellyfin's `/media` mount and outside the current restic scope (`/srv/data` is excluded). It is a local rollback copy, not an independent backup. Keeping originals means roughly another library-file-sized allocation for each converted title; there is no automatic archive deletion. A new `.mkv` is created only after full success; a caught error removes temporary output. Power loss/SIGKILL can leave staging/manifest entries for manual review. Completed archives are never auto-cleaned. Replacement, Sonarr/Radarr imports and new client playback do not share an atomic application-level transaction; final fingerprints guard common source changes, but do not claim to eliminate every race.

Jellyfin is asked to rescan after replacement. A refresh failure after replacement reports failure while the archived original and converted file remain intact. The pathname stays unchanged; release filenames may still contain the old TrueHD label. Actual stream metadata must be used for playback decisions. Sonarr/Radarr metadata refresh/optional renaming after conversion remains a Pi pilot check; no quality profile changes are made.

## Installation and pilot sequence (not executed yet)

1. From a clean reviewed checkout, install the worker only. Preserve the existing older dirty checkout. Create the private key file via an editor with the permissions above. Do not install/enable automatic units yet.
2. With playback stopped, run `sudo /usr/local/sbin/homepi-audio --file 'EXACT_ORIGINAL_LIBRARY_PATH'`. This prints a plan and cannot replace media. Root is needed for the shared lock/private paths.
3. Review the plan. Run the same command with `--apply` for that one file. Verify archive manifest/original, the new AC3 tracks, unchanged video hash results, Jellyfin media refresh, Sony subtitles/audio switching/seeking and Sonarr file state. If playback/API checks defer, stop playback or resolve the API issue instead of bypassing the guard.
4. Run `sudo /usr/local/sbin/homepi-audio --scan` to inventory the whole eligible backlog without replacement. Review storage and scope. Only after the pilot should the units be installed, the enable marker created and the timer enabled. Confirm the next timer run and journal.
5. For rollback, stop the timer and wait for an active worker to finish (or stop the service with its cleanup). Read the private manifest and verify the original. With affected playback stopped, copy the archived original to a temporary sibling file and atomically rename it over the derivative; never restore by writing into a shared inode. Preserve the archive. Refresh Jellyfin and inspect Sonarr/Radarr metadata. The enabled marker can be removed to disable service activation without deleting any files.

## Validation already performed locally

`python3 -m unittest discover -s tests -p 'test_audio.py' -v`: 12 tests covering stream plans, 7.1 downmix choice, unsupported layout refusal, validation failures, actual atomic replacement with preserved archive/torrent hardlinks, source-change refusal, symlink/outside-root rejection, playback deferral and conversion/archive failure preservation.

A real native FFmpeg synthetic fixture with two TrueHD tracks, a subtitle, chapter and font attachment converted to AC3 5.1/stereo and passed validation; the encoded video SHA256 stayed identical. This is not a native Docker/Pi worker run. Pi installation, API-key guard, scheduling, unattended playback interaction, real worker replacement/rollback and Sony replay of its exact output remain unverified. The manual Sony result is one episode, not proof for all titles.
