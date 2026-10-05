#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-/tmp/homepi-live-config}"
rm -rf "$OUT"
mkdir -p "$OUT"

python3 - "$OUT" <<'PY'
import json, os, pathlib, re, subprocess, sys, urllib.request, urllib.error
import xml.etree.ElementTree as ET

out = pathlib.Path(sys.argv[1])

def write(name, obj):
    (out / name).write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")

def api_key(path):
    root = ET.parse(path).getroot()
    node = root.find("ApiKey")
    if node is None or not node.text:
        raise RuntimeError(f"No ApiKey in {path}")
    return node.text.strip()

def http_json(url, key=None):
    headers = {"Accept":"application/json"}
    if key:
        headers["X-Api-Key"] = key
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)

def safe_status(x):
    keys = [
        "appName","instanceName","version","buildTime","startupPath","appData",
        "osName","osVersion","isDocker","isLinux","isOsx","isWindows",
        "runtimeName","runtimeVersion","databaseType","databaseVersion"
    ]
    return {k:x.get(k) for k in keys if k in x}

def get_field(item, name):
    for f in item.get("fields", []) or []:
        if f.get("name") == name:
            return f.get("value")
    return None

def arr_dump(name, port):
    key = api_key(f"/srv/appdata/{name}/config.xml")
    base = f"http://127.0.0.1:{port}/api/v3"
    result = {}
    result["status"] = safe_status(http_json(base + "/system/status", key))

    try:
        result["rootFolders"] = [
            {k:r.get(k) for k in ("id","path","freeSpace","unmappedFolders") if k in r}
            for r in http_json(base + "/rootfolder", key)
        ]
    except Exception as e:
        result["rootFoldersError"] = str(e)

    cfs = []
    cf_names = {}
    try:
        for x in http_json(base + "/customformat", key):
            safe = {k:x.get(k) for k in ("id","name","includeCustomFormatWhenRenaming") if k in x}
            cfs.append(safe)
            if "id" in x and "name" in x:
                cf_names[x["id"]] = x["name"]
        result["customFormats"] = cfs
    except Exception as e:
        result["customFormatsError"] = str(e)

    try:
        profiles = []
        for p in http_json(base + "/qualityprofile", key):
            q = {k:p.get(k) for k in (
                "id","name","upgradeAllowed","cutoff","minFormatScore",
                "cutoffFormatScore","minUpgradeFormatScore"
            ) if k in p}
            if "formatItems" in p:
                q["formatScores"] = [
                    {"id":f.get("format"), "name":cf_names.get(f.get("format")), "score":f.get("score")}
                    for f in p.get("formatItems", [])
                ]
            # Preserve enabled quality hierarchy names only, without dumping unrelated metadata.
            def walk(items):
                result_items=[]
                for i in items or []:
                    entry={"allowed":i.get("allowed")}
                    ql=i.get("quality")
                    if isinstance(ql, dict):
                        entry["quality"]=ql.get("name")
                    its=i.get("items")
                    if its:
                        entry["group"]=i.get("name")
                        entry["items"]=walk(its)
                    result_items.append(entry)
                return result_items
            if p.get("items"):
                q["qualities"] = walk(p["items"])
            profiles.append(q)
        result["qualityProfiles"] = profiles
    except Exception as e:
        result["qualityProfilesError"] = str(e)

    try:
        mm = http_json(base + "/config/mediamanagement", key)
        allowed = [
            "renameEpisodes","renameMovies","replaceIllegalCharacters",
            "standardEpisodeFormat","dailyEpisodeFormat","animeEpisodeFormat",
            "seriesFolderFormat","seasonFolderFormat","multiEpisodeStyle",
            "movieFolderFormat","createEmptySeriesFolders","deleteEmptyFolders",
            "copyUsingHardlinks","importExtraFiles","extraFileExtensions",
            "enableMediaInfo","rescanAfterRefresh","propersRepacks"
        ]
        result["mediaManagement"] = {k:mm.get(k) for k in allowed if k in mm}
    except Exception as e:
        result["mediaManagementError"] = str(e)

    try:
        dc = http_json(base + "/downloadclient", key)
        result["downloadClients"] = [{
            **{k:d.get(k) for k in ("id","name","implementation","protocol","enable","priority","removeCompletedDownloads","removeFailedDownloads") if k in d},
            **({"category": get_field(d, "category")} if get_field(d, "category") is not None else {})
        } for d in dc]
    except Exception as e:
        result["downloadClientsError"] = str(e)

    try:
        cfg = http_json(base + "/config/downloadclient", key)
        keep = ["enableCompletedDownloadHandling","autoRedownloadFailed","removeFailedDownloads","redownloadAfterRefresh"]
        result["downloadClientConfig"] = {k:cfg.get(k) for k in keep if k in cfg}
    except Exception as e:
        result["downloadClientConfigError"] = str(e)

    try:
        idx = http_json(base + "/indexer", key)
        result["indexers"] = [{k:i.get(k) for k in (
            "id","name","implementation","protocol","enableRss",
            "enableAutomaticSearch","enableInteractiveSearch","priority","tags"
        ) if k in i} for i in idx]
    except Exception as e:
        result["indexersError"] = str(e)

    write(f"{name}.json", result)

for name, port in (("sonarr",8989),("radarr",7878)):
    try:
        arr_dump(name, port)
    except Exception as e:
        write(f"{name}.json", {"fatalError":str(e)})

# Prowlarr safe inventory: names/capabilities only, never connection fields/API keys.
try:
    key = api_key("/srv/appdata/prowlarr/config.xml")
    base = "http://127.0.0.1:9696/api/v1"
    result = {"status": safe_status(http_json(base + "/system/status", key))}
    try:
        result["indexers"] = [{k:i.get(k) for k in (
            "id","name","implementation","protocol","privacy","enable","priority","tags"
        ) if k in i} for i in http_json(base + "/indexer", key)]
    except Exception as e:
        result["indexersError"] = str(e)
    try:
        result["applications"] = [{k:a.get(k) for k in (
            "id","name","implementation","syncLevel","tags"
        ) if k in a} for a in http_json(base + "/applications", key)]
    except Exception as e:
        result["applicationsError"] = str(e)
    try:
        result["indexerProxies"] = [{k:p.get(k) for k in (
            "id","name","implementation","tags"
        ) if k in p} for p in http_json(base + "/indexerProxy", key)]
    except Exception as e:
        result["indexerProxiesError"] = str(e)
    write("prowlarr.json", result)
except Exception as e:
    write("prowlarr.json", {"fatalError":str(e)})

# Home Assistant integration inventory without config-entry data/tokens/unique IDs.
try:
    p=pathlib.Path("/srv/appdata/homeassistant/.storage/core.config_entries")
    d=json.loads(p.read_text())
    entries=d.get("data",{}).get("entries",[])
    safe=[]
    for e in entries:
        safe.append({k:e.get(k) for k in (
            "domain","title","state","source","disabled_by","version","minor_version"
        ) if k in e})
    write("homeassistant-integrations.json", safe)
except Exception as e:
    write("homeassistant-integrations.json", {"fatalError":str(e)})

# Seerr safe settings, if present. No API keys/tokens/user records.
try:
    candidates=[
        pathlib.Path("/srv/appdata/seerr/settings.json"),
        pathlib.Path("/srv/appdata/seerr/config/settings.json"),
    ]
    p=next((x for x in candidates if x.exists()), None)
    if p:
        d=json.loads(p.read_text())
        safe={}
        main=d.get("main")
        if isinstance(main,dict):
            safe["main"]={k:main.get(k) for k in (
                "applicationTitle","applicationUrl","trustProxy","locale",
                "cacheImages","defaultPermissions","hideAvailable","localLogin",
                "discoverRegion","originalLanguage","mediaServerType"
            ) if k in main}
        for sec in ("jellyfin","plex"):
            x=d.get(sec)
            if isinstance(x,dict):
                safe[sec]={k:x.get(k) for k in (
                    "name","ip","hostname","port","useSsl","externalHostname","libraries"
                ) if k in x}
        for sec in ("radarr","sonarr"):
            vals=d.get(sec)
            if isinstance(vals,list):
                safe[sec]=[{k:x.get(k) for k in (
                    "id","name","hostname","port","useSsl","baseUrl","activeProfileId",
                    "activeProfileName","activeDirectory","is4k","isDefault",
                    "externalUrl","syncEnabled"
                ) if k in x} for x in vals if isinstance(x,dict)]
        write("seerr.json", safe)
    else:
        write("seerr.json", {"status":"settings.json not found at expected paths"})
except Exception as e:
    write("seerr.json", {"fatalError":str(e)})

# Docker runtime deployment metadata. Do not export container environments.
try:
    names=subprocess.check_output(["docker","ps","-a","--format","{{.Names}}"], text=True).splitlines()
    containers=[]
    image_ids=set()
    for name in names:
        raw=json.loads(subprocess.check_output(["docker","inspect",name], text=True))[0]
        image_ids.add(raw.get("Image"))
        labels=raw.get("Config",{}).get("Labels") or {}
        containers.append({
            "name": name,
            "image": raw.get("Config",{}).get("Image"),
            "imageId": raw.get("Image"),
            "created": raw.get("Created"),
            "restartPolicy": raw.get("HostConfig",{}).get("RestartPolicy",{}).get("Name"),
            "networkMode": raw.get("HostConfig",{}).get("NetworkMode"),
            "ports": raw.get("NetworkSettings",{}).get("Ports"),
            "mounts": [
                {"source":m.get("Source"),"destination":m.get("Destination"),"mode":m.get("Mode"),"type":m.get("Type")}
                for m in raw.get("Mounts",[])
            ],
            "compose": {
                "project": labels.get("com.docker.compose.project"),
                "workingDir": labels.get("com.docker.compose.project.working_dir"),
                "configFiles": labels.get("com.docker.compose.project.config_files"),
                "service": labels.get("com.docker.compose.service"),
            }
        })
    write("docker-containers.json", containers)

    images=[]
    for iid in image_ids:
        if not iid: continue
        raw=json.loads(subprocess.check_output(["docker","image","inspect",iid], text=True))[0]
        images.append({
            "id":raw.get("Id"),"repoTags":raw.get("RepoTags"),"repoDigests":raw.get("RepoDigests"),
            "created":raw.get("Created"),"architecture":raw.get("Architecture"),"os":raw.get("Os")
        })
    write("docker-images.json", images)
except Exception as e:
    write("docker-runtime.json", {"fatalError":str(e)})

# qBittorrent selected non-secret preferences, including the share-limit action.
try:
    raw=subprocess.check_output([
        "docker","exec","gluetun","sh","-c",
        "wget -qO- http://127.0.0.1:8080/api/v2/app/preferences"
    ], text=True)
    d=json.loads(raw)
    keys=[
        "save_path","temp_path_enabled","temp_path","current_network_interface",
        "current_interface_address","listen_port","torrent_content_layout",
        "max_ratio","max_ratio_enabled","max_ratio_act",
        "max_seeding_time","max_seeding_time_enabled",
        "max_inactive_seeding_time","max_inactive_seeding_time_enabled",
        "queueing_enabled","max_active_downloads","max_active_uploads","max_active_torrents",
        "dht","pex","lsd","upnp","random_port","autorun_enabled"
    ]
    write("qbittorrent-preferences.json",{k:d.get(k) for k in keys if k in d})
except Exception as e:
    write("qbittorrent-preferences.json",{"fatalError":str(e)})
PY

tar -C "$(dirname "$OUT")" -czf "${OUT}.tar.gz" "$(basename "$OUT")"
echo "Created: ${OUT}.tar.gz"
echo "This audit intentionally omits API keys, passwords, container environments, application databases and Home Assistant config-entry data."
