import os
import pathlib
import urllib.parse

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://imagewatch.dell.com/"
OUT_DIR = pathlib.Path("imagewatch_static")
OUT_DIR.mkdir(exist_ok=True)

session = requests.Session()

def download_file(url, rel_path):
    """Download a single file to OUT_DIR / rel_path."""
    rel_path = pathlib.Path(rel_path)
    dest = OUT_DIR / rel_path
    dest.parent.mkdir(parents=True, exist_ok=True)

    print(f"Downloading {url} -> {dest}")
    resp = session.get(url)
    resp.raise_for_status()
    dest.write_bytes(resp.content)

# 1. Download the base HTML
resp = session.get(BASE_URL)
resp.raise_for_status()
html = resp.text

soup = BeautifulSoup(html, "html.parser")

# 2. Collect CSS and JS URLs
asset_map = {}  # original_url -> local_relative_path

def absolutize(src):
    return urllib.parse.urljoin(BASE_URL, src)

# CSS
for link in soup.find_all("link", rel="stylesheet"):
    href = link.get("href")
    if not href:
        continue
    full = absolutize(href)
    # Determine local path from URL path
    path = urllib.parse.urlparse(full).path.lstrip("/")
    if not path:
        # fallback
        path = "styles.css"
    asset_map[full] = path

# JS
for script in soup.find_all("script", src=True):
    src = script["src"]
    full = absolutize(src)
    path = urllib.parse.urlparse(full).path.lstrip("/")
    if not path:
        path = "script.js"
    asset_map[full] = path

# 3. Download assets
for full_url, local_path in asset_map.items():
    download_file(full_url, local_path)

# 4. Rewrite HTML to point to local copies
for link in soup.find_all("link", rel="stylesheet"):
    href = link.get("href")
    if not href:
        continue
    full = absolutize(href)
    if full in asset_map:
        link["href"] = asset_map[full]

for script in soup.find_all("script", src=True):
    src = script["src"]
    full = absolutize(src)
    if full in asset_map:
        script["src"] = asset_map[full]

# 5. Save modified HTML locally
(OUT_DIR / "index.html").write_text(str(soup), encoding="utf-8")
print("Saved:", OUT_DIR / "index.html")