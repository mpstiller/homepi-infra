# Google OAuth branding for HomePi Backup

Prepared static pages: `docs/index.html` and `docs/privacy.html`. No analytics, scripts, remote fonts, secrets or public login are included.

## Deployment (owner action pending)

After merging the PR, select repository Settings → Pages → Deploy from a branch → main → /docs and Save. The existing sanitized docs folder is the published source; `.nojekyll` disables Jekyll processing. Check GitHub's actual deployed URL and confirm both pages return successfully before entering them in Google.

Expected project URLs (not yet verified as deployed):

- Homepage: https://mpstiller.github.io/homepi-infra/
- Privacy: https://mpstiller.github.io/homepi-infra/privacy.html
- Authorized domain for that Pages host: `mpstiller.github.io` (enter no scheme/path; follow any domain ownership prompt Google actually presents).

In Google Auth Platform → Branding keep the existing client/project; use HomePi Backup as the app name if desired, the owner's actual support/developer emails, and the verified page URLs. Do not invent a contact email or use unrelated privacy pages. Save, then switch Audience from Testing to In production. Publishing and verification are distinct; additional Google requirements must be handled if presented, not assumed bypassed.

Once published, reconnect the existing gdrive remote with the explicit configuration path. The expired token is not repaired by publishing alone. Use the headless rclone authorization flow as prompted; do not paste tokens, client secrets or authorize output into chat/Git. Update the private recovery copy after successful authorization. Verify access without writing/deleting backup data, then rerun the maintenance systemd service and confirm both exit status and the Healthchecks result.

References: https://rclone.org/drive/#making-your-own-client-id ; https://developers.google.com/identity/protocols/oauth2/ ; https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
