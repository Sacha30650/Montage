#!/usr/bin/env python3
"""Download Higgsfield generation results to assets/broll/.

Usage:
  python3 scripts/download_broll.py <url> <dest_filename>

In practice this script is called after job_display returns a results array
with a URL. The MCP server exposes the URL via `results[].results[].url` once
status == "completed".
"""
import sys, urllib.request
from pathlib import Path

def main() -> None:
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    url, dest = sys.argv[1], Path(sys.argv[2])
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "montage-pilot/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        data = r.read()
    dest.write_bytes(data)
    print(f"wrote {dest} ({len(data):,} bytes)")

if __name__ == "__main__":
    main()
