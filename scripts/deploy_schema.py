#!/usr/bin/env python3
"""Idempotent schema-as-code deployer for Dataverse.

    python3 deploy_schema.py schema.json            # dry run: shows what would be created
    python3 deploy_schema.py schema.json --apply    # creates what is missing

Creates the publisher and solution if missing, then tables (primary name column), choice
columns and lookups, all inside the solution. Re-running changes nothing. The publisher
prefix is permanent: confirm it with the user before the first --apply.
See example_schema.json for the format.
"""
import json, sys, time
from dv import call, label, org

args = [a for a in sys.argv[1:] if not a.startswith("--")]
if not args:
    sys.exit(__doc__)
APPLY = "--apply" in sys.argv
S = json.load(open(args[0]))
SOL = {"MSCRM.SolutionUniqueName": S["solution"]["uniquename"]}
print(("APPLY" if APPLY else "DRY RUN"), "against", org())


def show(r):
    print("   ->", r[0], "" if r[0] < 300 else str(r[1])[:300])
    if r[0] >= 300:
        sys.exit("stopped on error")


def ensure_publisher_and_solution():
    p = S["publisher"]
    st, d, _ = call("GET", f"publishers?$filter=customizationprefix eq '{p['prefix']}'&$select=publisherid")
    pid = d["value"][0]["publisherid"] if st == 200 and d["value"] else None
    print("publisher", p["prefix"], "exists" if pid else "create")
    if not pid and APPLY:
        show(call("POST", "publishers", {"uniquename": p["uniquename"], "friendlyname": p["friendlyname"],
               "customizationprefix": p["prefix"], "customizationoptionvalueprefix": p["optionvalueprefix"]}))
        st, d, _ = call("GET", f"publishers?$filter=customizationprefix eq '{p['prefix']}'&$select=publisherid")
        pid = d["value"][0]["publisherid"]
    s = S["solution"]
    st, d, _ = call("GET", f"solutions?$filter=uniquename eq '{s['uniquename']}'&$select=solutionid")
    print("solution", s["uniquename"], "exists" if d["value"] else "create")
    if not d["value"] and APPLY and pid:
        show(call("POST", "solutions", {"uniquename": s["uniquename"], "friendlyname": s["friendlyname"],
               "version": s["version"], "publisherid@odata.bind": f"/publishers({pid})"}))


def table_exists(logical):
    return call("GET", f"EntityDefinitions(LogicalName='{logical}')?$select=LogicalName")[0] == 200


def attr_exists(table, logical):
    return call("GET", f"EntityDefinitions(LogicalName='{table}')/Attributes(LogicalName='{logical}')?$select=LogicalName")[0] == 200


ensure_publisher_and_solution()
for t in S["tables"]:
    lg = t["schema"].lower()
    if table_exists(lg):
        print("table", lg, "exists"); continue
    print("table", lg, "create")
    if not APPLY: continue
    col, col_disp = t["name_column"]
    show(call("POST", "EntityDefinitions", {
        "@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata", "SchemaName": t["schema"],
        "DisplayName": label(t["display"]), "DisplayCollectionName": label(t["plural"]),
        "OwnershipType": "UserOwned", "HasActivities": False, "HasNotes": False, "PrimaryNameAttribute": col.lower(),
        "Attributes": [{"@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata", "SchemaName": col,
                        "DisplayName": label(col_disp), "RequiredLevel": {"Value": "None"}, "MaxLength": 200,
                        "IsPrimaryName": True}]}, SOL))
for t in S["tables"]:
    for c in t.get("choices", []):
        tl = t["schema"].lower()
        if attr_exists(tl, c["schema"].lower()):
            print("choice", c["schema"], "exists"); continue
        print("choice", c["schema"], "create")
        if not APPLY: continue
        show(call("POST", f"EntityDefinitions(LogicalName='{tl}')/Attributes", {
            "@odata.type": "Microsoft.Dynamics.CRM.PicklistAttributeMetadata", "SchemaName": c["schema"],
            "DisplayName": label(c["display"]), "RequiredLevel": {"Value": "None"},
            "OptionSet": {"@odata.type": "Microsoft.Dynamics.CRM.OptionSetMetadata", "IsGlobal": False,
                          "OptionSetType": "Picklist",
                          "Options": [{"Value": v, "Label": label(k)} for k, v in c["options"].items()]}}, SOL))
for l in S.get("lookups", []):
    if attr_exists(l["from"], l["schema"].lower()):
        print("lookup", l["schema"], "exists"); continue
    print("lookup", l["from"], "->", l["to"], "create")
    if not APPLY: continue
    time.sleep(3)  # let the new tables settle before relating them
    show(call("POST", "RelationshipDefinitions", {
        "@odata.type": "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata",
        "SchemaName": f"{l['to']}_{l['from']}_{l['schema'].lower()}", "ReferencedEntity": l["to"],
        "ReferencingEntity": l["from"],
        "Lookup": {"SchemaName": l["schema"], "DisplayName": label(l["display"]), "RequiredLevel": {"Value": "None"}},
        "AssociatedMenuConfiguration": {"Behavior": "UseCollectionName", "Group": "Details", "Order": 10000},
        "CascadeConfiguration": {"Delete": "RemoveLink", "Assign": "NoCascade", "Share": "NoCascade",
                                 "Unshare": "NoCascade", "Reparent": "NoCascade", "Merge": "NoCascade"}}, SOL))
print("done" if APPLY else "dry run only; add --apply to create")
