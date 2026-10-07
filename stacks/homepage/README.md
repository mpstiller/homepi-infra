# Homepage

The verified runtime Compose definition is checked in as `compose.yaml`.

Persistent Homepage configuration lives on the Pi under:

```text
/srv/appdata/homepage
```

Important live config files include:

```text
services.yaml
settings.yaml
widgets.yaml
docker.yaml
```

As of 2026-10-07, the dashboard service-group layout is implemented and the Sonarr native widget is confirmed working. Its API key is stored only in the local Homepage `.env`.

The live YAML dashboard files are not yet synchronized into this repository. Do not reconstruct or overwrite them from memory when the live files are available. Once the widget rollout is stable, capture a sanitized version/structure here without committing API keys or other secrets.
