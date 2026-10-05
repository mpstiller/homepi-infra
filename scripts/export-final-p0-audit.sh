#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-/tmp/homepi-final-p0}"
rm -rf "$OUT"
mkdir -p "$OUT"

python3 - "$OUT" <<'PY'
import json, pathlib, re, subprocess, sys, urllib.request, xml.etree.ElementTree as ET

out=pathlib.Path(sys.argv[1])

def write(name,obj):
    (out/name).write_text(json.dumps(obj,indent=2,sort_keys=True,ensure_ascii=False)+"\n")

def key(path):
    root=ET.parse(path).getroot()
    n=root.find("ApiKey")
    return n.text.strip()

def get(url,k=None):
    h={"Accept":"application/json"}
    if k: h["X-Api-Key"]=k
    with urllib.request.urlopen(urllib.request.Request(url,headers=h),timeout=10) as r:
        return json.load(r)

# Music Assistant compose, redacted while preserving structure.
src=pathlib.Path("/srv/appdata/compose.yaml")
if src.exists():
    text=src.read_text(errors="replace")
    secret_words=re.compile(r'(password|passwd|token|secret|private.?key|encryption.?key|api.?key|credential|cookie)',re.I)
    lines=[]
    for line in text.splitlines():
        m=re.match(r'^(\s*)([-]?[\s]*)(["\']?[^:#]+["\']?)\s*:\s*(.*)$',line)
        if m and secret_words.search(m.group(3)):
            v=m.group(4).strip()
            if v and not re.fullmatch(r'["\']?\$\{[A-Za-z_][A-Za-z0-9_]*\}["\']?',v):
                line=f"{m.group(1)}{m.group(2)}{m.group(3)}: <REDACTED>"
        m2=re.match(r'^(\s*-?\s*)([A-Za-z_][A-Za-z0-9_]*)(=)(.*)$',line)
        if m2 and secret_words.search(m2.group(2)):
            v=m2.group(4).strip()
            if v and not re.fullmatch(r'\$\{[A-Za-z_][A-Za-z0-9_]*\}',v):
                line=f"{m2.group(1)}{m2.group(2)}=<REDACTED>"
        lines.append(line)
    (out/"music-assistant-compose.yaml").write_text("\n".join(lines)+"\n")

for name,port in (("sonarr",8989),("radarr",7878)):
    k=key(f"/srv/appdata/{name}/config.xml")
    base=f"http://127.0.0.1:{port}/api/v3"
    result={}
    try:
        n=get(base+"/config/naming",k)
        # Naming data is safe and intentionally retained.
        result["naming"]=n
    except Exception as e:
        result["namingError"]=str(e)

    try:
        q=get(base+"/qualitydefinition",k)
        keep=[]
        for x in q:
            keep.append({kk:x.get(kk) for kk in (
                "id","title","weight","minSize","preferredSize","maxSize"
            ) if kk in x})
        result["qualityDefinitions"]=keep
    except Exception as e:
        result["qualityDefinitionsError"]=str(e)
    write(f"{name}-naming-quality.json",result)

# Exact HA version, no config.
try:
    v=subprocess.check_output([
        "docker","exec","homeassistant","python3","-c",
        "from homeassistant.const import __version__; print(__version__)"
    ],text=True).strip()
    write("homeassistant-version.json",{"version":v})
except Exception as e:
    write("homeassistant-version.json",{"error":str(e)})

# Jellyfin public server info requires no token.
try:
    write("jellyfin-public-info.json",get("http://127.0.0.1:8096/System/Info/Public"))
except Exception as e:
    write("jellyfin-public-info.json",{"error":str(e)})
PY

tar -C "$(dirname "$OUT")" -czf "${OUT}.tar.gz" "$(basename "$OUT")"
echo "Created: ${OUT}.tar.gz"
