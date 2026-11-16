#!/usr/bin/env python3
"""Create, update, turn on and run a solution-aware Power Automate flow from code.

    python3 flow_tool.py create   --name "My Flow" --solution MySolution --file flow.json   # created OFF
    python3 flow_tool.py update   --name "My Flow" --file flow.json                         # flow must be off
    python3 flow_tool.py on       --name "My Flow"                                          # ask the user first
    python3 flow_tool.py run      --name "My Flow" --env-id <environment id>                # manual trigger
    python3 flow_tool.py runs     --name "My Flow" --env-id <environment id>                # run + action status

flow.json is the `clientdata` object: {"properties": {"connectionReferences": {...},
"definition": {...}}, "schemaVersion": "1.0.0.0"}. Generate it from a builder script and keep
the builder in the repo. Needs DATAVERSE_URL and `az login` (see dv.py).
"""
import argparse, json, subprocess, sys, urllib.request
from dv import call, token

p = argparse.ArgumentParser()
p.add_argument("cmd", choices=["create", "update", "on", "off", "run", "runs"])
p.add_argument("--name", required=True)
p.add_argument("--solution")
p.add_argument("--file")
p.add_argument("--env-id")
a = p.parse_args()


def find():
    st, d, _ = call("GET", f"workflows?$filter=name eq '{a.name}' and category eq 5&$select=workflowid,statecode")
    return d["value"][0] if st == 200 and d["value"] else None


def flow_api(method, path):
    req = urllib.request.Request(
        f"https://api.flow.microsoft.com/providers/Microsoft.ProcessSimple/environments/{a.env_id}/flows/{path}api-version=2016-11-01",
        method=method, data=b"{}" if method == "POST" else None,
        headers={"Authorization": "Bearer " + token("https://service.flow.microsoft.com/"), "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        t = r.read().decode()
        return json.loads(t) if t else {}


w = find()
if a.cmd == "create":
    if w: sys.exit("flow already exists")
    if not (a.solution and a.file): sys.exit("--solution and --file are required")
    r = call("POST", "workflows", {"name": a.name, "category": 5, "type": 1, "primaryentity": "none",
             "statecode": 0, "statuscode": 1, "clientdata": json.dumps(json.load(open(a.file)))},
             {"MSCRM.SolutionUniqueName": a.solution})
    print(r[0], "" if r[0] < 300 else r[1])
elif not w:
    sys.exit("flow not found")
elif a.cmd == "update":
    r = call("PATCH", f"workflows({w['workflowid']})", {"clientdata": json.dumps(json.load(open(a.file)))})
    print(r[0], "" if r[0] < 300 else r[1])
elif a.cmd in ("on", "off"):
    on = a.cmd == "on"
    r = call("PATCH", f"workflows({w['workflowid']})", {"statecode": 1 if on else 0, "statuscode": 2 if on else 1})
    print(r[0], "" if r[0] < 300 else r[1])
elif a.cmd == "run":
    print(flow_api("POST", f"{w['workflowid']}/triggers/manual/run?") or "run requested")
elif a.cmd == "runs":
    runs = flow_api("GET", f"{w['workflowid']}/runs?").get("value", [])
    for r in runs[:5]:
        print(r["name"], r["properties"]["status"])
        for act in flow_api("GET", f"{w['workflowid']}/runs/{r['name']}/actions?").get("value", []):
            print("   ", act["name"], act["properties"]["status"], act["properties"].get("code", ""))
