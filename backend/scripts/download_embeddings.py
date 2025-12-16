import os, json, urllib.request, zipfile, pathlib

OWNER = os.environ["GITHUB_OWNER"]
REPO  = os.environ["GITHUB_REPO"]
TAG   = os.environ["RELEASE_TAG"]
ASSET = os.environ["ASSET_NAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

ROOT = pathlib.Path(__file__).resolve().parents[2]
TARGET = ROOT / "openai_mobile_review_embeddings" / "chroma.sqlite3"

if TARGET.exists():
    print("Embeddings already exist:", TARGET)
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

asset = next(a for a in release["assets"] if a["name"] == ASSET)

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
    z.extractall(ROOT)

if not TARGET.exists():
    raise RuntimeError("chroma.sqlite3 not found after extraction")

print("Embeddings downloaded and ready.")
