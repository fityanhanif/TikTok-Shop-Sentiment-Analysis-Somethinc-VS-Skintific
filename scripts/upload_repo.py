#!/usr/bin/env python3
"""Upload repo files via GitHub API"""
import requests, base64, os, sys, json

# Read token from env
token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
if not token:
    print("ERROR: GH_TOKEN not set")
    sys.exit(1)

headers = {"Accept": "application/vnd.github+json", "Authorization": f"Bearer {token}"}
owner = "fityanhanif"
repo = "somethinc-vs-skintific-sentiment"
proj = r"C:\Users\lenovo\Projects\somethinc-vs-skintific"

# Verify auth
r = requests.get("https://api.github.com/user", headers=headers)
if r.status_code != 200:
    print(f"AUTH FAILED: {r.status_code}")
    sys.exit(1)
print(f"Auth OK: {r.json().get('login')}")

# Check/delete repo
r = requests.get(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)
print(f"Repo exists: {r.status_code}")

if r.status_code == 200:
    branch = r.json().get("default_branch", "main")
else:
    # Create repo
    r = requests.post("https://api.github.com/user/repos", headers=headers, json={"name": repo, "description": "TikTok Shop Sentiment Analysis — Somethinc vs Skintific", "private": False})
    print(f"Create repo: {r.status_code}")
    branch = "main"

# Upload files
def upload(path_in_repo, local_path, msg="Add files"):
    if not os.path.exists(local_path):
        print(f"  SKIP {path_in_repo} (not found)")
        return False
    with open(local_path, "rb") as f:
        content = base64.b64encode(f.read()).decode()
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path_in_repo}"
    r = requests.put(url, headers=headers, json={"message": msg, "content": content, "branch": branch})
    ok = r.status_code in (200, 201)
    print(f"  {'OK' if ok else 'FAIL'} {path_in_repo} ({r.status_code})")
    if not ok:
        print(f"    {r.json().get('message', '')[:100]}")
    return ok

# Upload all files
files = [
    ("README.md", os.path.join(proj, "README.md")),
    (".gitignore", os.path.join(proj, ".gitignore")),
    ("vercel.json", os.path.join(proj, "vercel.json")),
    ("dashboard/index.html", os.path.join(proj, "dashboard/index.html")),
    ("dashboard/css/styles.css", os.path.join(proj, "dashboard/css/styles.css")),
    ("dashboard/js/app.js", os.path.join(proj, "dashboard/js/app.js")),
    ("dashboard/data/analysis_output.json", os.path.join(proj, "dashboard/data/analysis_output.json")),
]

for path_in_repo, local_path in files:
    upload(path_in_repo, local_path)

print(f"\n✅ Done! https://github.com/{owner}/{repo}")
