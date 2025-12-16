import os, json, urllib.request, zipfile, pathlib

OWNER = os.environ.get("GITHUB_OWNER", "AhmadKhtib")
REPO  = os.environ.get("GITHUB_REPO", "Phone-Reviews-Assistant")
TAG   = os.environ.get("RELEASE_TAG", "embeddings-v1")
ASSET = os.environ.get("ASSET_NAME", "openai_mobile_review_embeddings.zip")
TOKEN = os.environ["GITHUB_TOKEN"]

target_sqlite = pathlib.Path("openai_mobile_review_embeddings") / "chroma.sqlite3"
if target_sqlite.exists():
    print("Embeddings already present:", target_sqlite)
    raise SystemExit(0)

release_url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/tags/{TAG}"
req = urllib.request.Request(
    release_url,
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "User-Agent": "render-build",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)
with urllib.request.urlopen(req) as r:
    release = json.load(r)

asset = next((a for a in release.get("assets", []) if a.get("name") == ASSET), None)
if not asset:
    names = [a.get("name") for a in release.get("assets", [])]
    raise SystemExit(f"ERROR: asset '{ASSET}' not found. Available: {names}")

download_req = urllib.request.Request(
    asset["url"],
    headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/octet-stream",
        "User-Agent": "render-build",
        "X-GitHub-Api-Version": "2022-11-28",
    },
)

zip_path = "/tmp/embeddings.zip"
with urllib.request.urlopen(download_req) as r, open(zip_path, "wb") as f:
    f.write(r.read())

with zipfile.ZipFile(zip_path, "r") as z:
    z.extractall(".")

if not target_sqlite.exists():
    raise SystemExit("ERROR: chroma.sqlite3 not found after extraction. Check zip structure.")

print("Embeddings downloaded and extracted successfully.")
