# Runtime stacks

The actual Compose files running on the Pi have **not yet been synchronized** into this repository.

When Pi access is available, copy and review the files from:

```text
/opt/homelab/stacks/arcane
/opt/homelab/stacks/homepage
/opt/homelab/stacks/homeassistant
/opt/homelab/stacks/music-assistant
/opt/homelab/stacks/jellyfin
/opt/homelab/stacks/media
```

Before committing:

- remove/redact secrets;
- replace local secret values with `${VARIABLE}` references where necessary;
- create matching `.env.example` files with variable names only;
- compare live config with `LLM_CONTEXT.md` and resolve discrepancies in favor of the live, verified system.
