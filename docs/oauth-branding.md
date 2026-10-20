# Google OAuth branding for HomePi Backup

Prepared static pages: `docs/index.html` and `docs/privacy.html`. No analytics, scripts, remote fonts, secrets or public login are included.

## Recovery result — 2026-10-20

PR #9 merged. Owner reported GitHub Pages/Branding setup ready, then confirmed OAuth publishing status In production. Pages public reachability was not independently verified by the assistant. Reconnected existing gdrive using /etc/rclone/homepi.conf and Mac browser authorization, selecting no Shared Drive. Repository 475950f8 opened and expected snapshots were listed. Real maintenance completed 17:05:40 CEST with Result=success, exit 0; prune and standard check of eight snapshots found no errors. Renewed recovery configuration replaced the password-manager attachment. Monthly monitoring green state and final timer scheduling were subsequently owner-confirmed. Temporary-copy deletion remains unconfirmed. Installed monitoring helpers/drop-ins are captured in backup/; see backup/monitoring.md. No future token-expiry guarantee or independent-host recovery is claimed.

## Deployment reference

After merging the PR, select repository Settings → Pages → Deploy from a branch → main → /docs and Save. The existing sanitized docs folder is the published source; `.nojekyll` disables Jekyll processing. Check GitHub's actual deployed URL and confirm both pages return successfully before entering them in Google.

Expected project URLs (not yet verified as deployed):

- Homepage: https://mpstiller.github.io/homepi-infra/
- Privacy: https://mpstiller.github.io/homepi-infra/privacy.html
- Authorized domain for that Pages host: `mpstiller.github.io` (enter no scheme/path; follow any domain ownership prompt Google actually presents).

In Google Auth Platform → Branding keep the existing client/project; use HomePi Backup as the app name if desired, the owner's actual support/developer emails, and the verified page URLs. Do not invent a contact email or use unrelated privacy pages. Save, then switch Audience from Testing to In production. Publishing and verification are distinct; additional Google requirements must be handled if presented, not assumed bypassed.

Once published, reconnect the existing gdrive remote with the explicit configuration path. The expired token is not repaired by publishing alone. Use the headless rclone authorization flow as prompted; do not paste tokens, client secrets or authorize output into chat/Git. Update the private recovery copy after successful authorization. Verify access without writing/deleting backup data, then rerun the maintenance systemd service and confirm both exit status and the Healthchecks result.

References: https://rclone.org/drive/#making-your-own-client-id ; https://developers.google.com/identity/protocols/oauth2/ ; https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
