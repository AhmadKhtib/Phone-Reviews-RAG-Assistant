#!/usr/bin/env bash
set -e

export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

TARGET="openai_mobile_review_embeddings/chroma.sqlite3"


if [ ! -f "$TARGET" ]; then
  echo "Embeddings not found. Downloading via GitHub API..."

  python - <<'PY'
import os, json, urllib.request, zipfile

owner = os.environ.get("GITHUB_OWNER", "AhmadKhtib")
repo  = os.environ.get("GITHUB_REPO", "Phone-Reviews-Assistant")
tag   = os.environ.get("RELEASE_TAG", "embeddings-v1")
asset_name = os.environ.get("ASSET_NAME", "openai_mobile_review_embeddings.zip")
token = os.environ["GITHUB_TOKEN"]

release_url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"
req = urllib.request.Request(
    release_url,
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "render",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)
with urllib.request.urlopen(req) as r:
    release = json.load(r)

assets = release.get("assets", [])
asset = next((a for a in assets if a.get("name") == asset_name), None)
if not asset:
    names = [a.get("name") for a in assets]
    raise SystemExit(f"ERROR: asset '{asset_name}' not found. Available: {names}")

asset_api_url = asset["url"]

download_req = urllib.request.Request(
    asset_api_url,
    headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/octet-stream",
        "User-Agent": "render",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)

zip_path = "/tmp/embeddings.zip"
with urllib.request.urlopen(download_req) as r, open(zip_path, "wb") as f:
    f.write(r.read())

print("Downloaded:", zip_path)

with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(".")

target = "openai_mobile_review_embeddings/chroma.sqlite3"
if not os.path.exists(target):
    raise SystemExit(f"ERROR: expected {target} not found after extraction. Check zip structure.")
print("Extraction OK.")
PY
fi

set -e
exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
