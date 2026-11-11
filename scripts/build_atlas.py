#!/usr/bin/env python3
"""Build the dependency-free atlas data file from canonical project catalog."""
import json
from pathlib import Path
root=Path(__file__).resolve().parents[1]
projects=json.loads((root/"data/projects.json").read_text(encoding="utf-8"))
out=[]
for p in projects:
    prof=p.get("profile",{})
    out.append({"name":p["name"],"url":p["url"],"category":p["category"],"summary":prof.get("summary",p["note"]),"mechanism":prof.get("mechanism",p["category"]),"platforms":prof.get("platforms",[]),"level":prof.get("level","not-reviewed"),"limits":prof.get("limits",""),"reviewed":prof.get("reviewed_on"),"minimum":prof.get("min_ram_gb"),"reports":prof.get("reports",[])})
content="/* Generated snapshot from data/projects.json. See scripts/build_atlas.py */\\n".replace("\\n","\n")+"window.ATLAS_DATA = "+json.dumps(out,ensure_ascii=False,separators=(",",":")).replace("<","\\u003c")+";\n"
path=root/"docs/catalog.js"
if __import__("sys").argv[1:]==["--check"]:
    assert path.exists() and path.read_text(encoding="utf-8")==content, "Atlas catalog is stale; run python scripts/build_atlas.py"
    print("Atlas data is synchronized.")
else:
    path.parent.mkdir(exist_ok=True)
    path.write_text(content,encoding="utf-8")
    print(f"Generated {path} for {len(out)} projects.")
