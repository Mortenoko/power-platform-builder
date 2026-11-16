#!/usr/bin/env python3
"""Read-only machine check for Power Platform work with Claude. Changes nothing.

    python3 doctor.py            # human-readable
    python3 doctor.py --json     # for Claude to read

Reports the OS, the tools (git, python, pac, dotnet, az, node), the active `pac` auth profile and
environment, the Azure CLI account, and which Claude Code plugins are installed. For every missing
tool it suggests an install command for this OS. Claude should ask the user before running any
install command, and should compare the environment with what the user said before changing anything.
"""
import json, platform, shutil, subprocess, sys

OS = {"Darwin": "mac", "Windows": "windows", "Linux": "linux"}.get(platform.system(), "other")

INSTALL = {
    "git":    {"mac": "brew install git", "windows": "winget install Git.Git", "linux": "sudo apt install git"},
    "python": {"mac": "brew install python", "windows": "winget install Python.Python.3.12", "linux": "sudo apt install python3"},
    "dotnet": {"mac": "brew install dotnet", "windows": "winget install Microsoft.DotNet.SDK.10", "linux": "see https://dotnet.microsoft.com/download"},
    "pac":    {"mac": "dotnet tool install --global Microsoft.PowerApps.CLI.Tool", "windows": "dotnet tool install --global Microsoft.PowerApps.CLI.Tool", "linux": "dotnet tool install --global Microsoft.PowerApps.CLI.Tool"},
    "az":     {"mac": "brew install azure-cli", "windows": "winget install Microsoft.AzureCLI", "linux": "see https://learn.microsoft.com/cli/azure/install-azure-cli-linux"},
    "node":   {"mac": "brew install node", "windows": "winget install OpenJS.NodeJS.LTS", "linux": "sudo apt install nodejs"},
}
# Which surface needs what, so Claude only sets up what the task requires.
NEEDED_FOR = {
    "git": "all", "python": "scripts (optional)", "dotnet": "canvas apps (authoring MCP) and pac",
    "pac": "environments and solutions (all surfaces)", "az": "scripts/deploy_schema.py and flow_tool.py (optional)",
    "node": "optional",
}


def run(cmd, timeout=30):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except Exception as e:  # missing binary, timeout
        return 1, str(e)


def which(name):
    return shutil.which(name) or (shutil.which("python3") if name == "python" else None)


def tool(name, cmd):
    path = which(name)
    if not path and name == "pac":
        import os
        cand = os.path.expanduser("~/.dotnet/tools/pac")
        path = cand if os.path.exists(cand) else None
    if not path:
        return {"installed": False, "needed_for": NEEDED_FOR[name], "install": INSTALL[name].get(OS)}
    rc, out = run(([path] + cmd[1:]) if cmd else [path, "--version"])
    first = next((l for l in out.splitlines() if l.strip()), "")
    return {"installed": True, "version": first[:80], "needed_for": NEEDED_FOR[name]}


r = {"os": OS}
r["tools"] = {
    "git": tool("git", ["git", "--version"]),
    "python": tool("python", ["python3", "--version"]),
    "dotnet": tool("dotnet", ["dotnet", "--list-sdks"]),
    "pac": tool("pac", ["pac", "help"]),
    "az": tool("az", ["az", "--version"]),
    "node": tool("node", ["node", "--version"]),
}
if r["tools"]["dotnet"].get("installed"):
    rc, out = run(["dotnet", "--list-sdks"])
    r["tools"]["dotnet"]["has_sdk_10"] = any(l.startswith("10.") for l in out.splitlines())

pacpath = which("pac") or ""
if r["tools"]["pac"].get("installed"):
    import os
    pacbin = shutil.which("pac") or os.path.expanduser("~/.dotnet/tools/pac")
    rc, out = run([pacbin, "org", "who"], 40)
    r["pac_environment"] = {"signed_in": rc == 0 and "Org URL" in out,
                            "details": [l.strip() for l in out.splitlines() if any(k in l for k in ("Connected as", "Friendly Name", "Org URL", "Environment ID"))]}
if r["tools"]["az"].get("installed"):
    rc, out = run(["az", "account", "show", "--query", "{user:user.name,tenant:tenantId}", "-o", "json"], 40)
    r["az_account"] = {"signed_in": rc == 0, "details": out[:200] if rc == 0 else "not signed in (az login)"}
if shutil.which("claude"):
    rc, out = run(["claude", "plugin", "list"], 40)
    names = [l.split("❯")[1].strip() for l in out.splitlines() if "❯" in l]
    wanted = ["power-platform-builder", "canvas-apps", "dataverse", "copilot-studio"]
    r["claude_plugins"] = {"installed": names, "missing": [w for w in wanted if not any(n.startswith(w + "@") for n in names)]}

if "--json" in sys.argv:
    print(json.dumps(r, indent=2))
else:
    print("OS:", r["os"])
    for k, v in r["tools"].items():
        extra = "" if v["installed"] else "  -> " + str(v["install"])
        print(f"  {'OK ' if v['installed'] else 'MISSING'} {k:7} {v.get('version','')}{extra}")
    for k in ("pac_environment", "az_account", "claude_plugins"):
        if k in r:
            print(k + ":", json.dumps(r[k]))
