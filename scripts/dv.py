"""Tiny Dataverse / Power Automate Web API helper. Standard library only.

Auth: a bearer token from the Azure CLI (`az login` with the same account as `pac`).
Environment URL comes from the DATAVERSE_URL environment variable, e.g.
    export DATAVERSE_URL=https://<org>.<region>.dynamics.com
"""
import json, os, subprocess, sys, urllib.error, urllib.request


def org():
    url = os.environ.get("DATAVERSE_URL", "").rstrip("/")
    if not url:
        sys.exit("Set DATAVERSE_URL to the environment URL (and confirm it with `pac org who`).")
    return url


def token(resource=None):
    return subprocess.check_output(
        ["az", "account", "get-access-token", "--resource", resource or org(),
         "--query", "accessToken", "-o", "tsv"], text=True).strip()


def call(method, path, body=None, headers=None):
    """Dataverse Web API call. Returns (status, parsed_body_or_text, response_headers)."""
    h = {"Authorization": "Bearer " + token(), "Content-Type": "application/json",
         "Accept": "application/json", "OData-Version": "4.0"}
    h.update(headers or {})
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(org() + "/api/data/v9.2/" + path.replace(" ", "%20"),
                                 data=data, method=method, headers=h)
    try:
        with urllib.request.urlopen(req) as r:
            text = r.read().decode()
            return r.status, (json.loads(text) if text else {}), r.headers
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(), None


def label(text):
    return {"@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [
        {"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": text, "LanguageCode": 1033}]}
