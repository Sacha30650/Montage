#!/usr/bin/env python3
"""Download Higgsfield-generated b-roll into a pilot's assets/broll-hf directory.

Usage:
    python3 scripts/fetch_higgsfield_broll.py assets/visual-plans/pilot-14-parle-tard.jobs.json

The jobs file maps target filenames to Higgsfield job ids and, once known, result
URLs. The MCP `job_status` tool (or the Higgsfield UI) gives the CDN `rawUrl` for a
completed job; paste it into the "urls" section below and re-run this script.

Expected jobs.json shape:
{
  "pilot": "pilot-14-parle-tard",
  "target_dir": "pilots/pilot-14-parle-tard/assets/broll-hf",
  "jobs":  { "01_hook_a.png": "<job-uuid>", ... },
  "urls":  { "01_hook_a.png": "https://...cloudfront.net/....png", ... }
}

Files already present in target_dir are kept unless --force is passed, so partial
batches can be completed incrementally. After downloading, regenerate with
`npm run generate:recent` — hf_dynamic_carousel switches to the full-bleed
Higgsfield template automatically once every file listed in the pilot's
"hf_slides" (scripts/recent_pilots.py) exists.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jobs_file", help="path to a *.jobs.json visual-plan companion file")
    parser.add_argument("--force", action="store_true", help="re-download files that already exist")
    args = parser.parse_args()

    data = json.loads(Path(args.jobs_file).read_text())
    target_dir = ROOT / data["target_dir"]
    target_dir.mkdir(parents=True, exist_ok=True)
    urls: dict[str, str] = data.get("urls", {})
    jobs: dict[str, str] = data.get("jobs", {})

    missing_urls = [name for name in jobs if name not in urls]
    downloaded = skipped = 0
    for name, url in urls.items():
        destination = target_dir / name
        if destination.exists() and not args.force:
            skipped += 1
            continue
        print(f"downloading {name} ...")
        with urllib.request.urlopen(url) as response:
            destination.write_bytes(response.read())
        downloaded += 1

    print(f"done: {downloaded} downloaded, {skipped} kept, target={target_dir}")
    if missing_urls:
        print(
            "still missing result URLs for: " + ", ".join(missing_urls) + "\n"
            "→ check the jobs with the Higgsfield MCP `job_status` tool and add the "
            "rawUrl values to the \"urls\" section of " + args.jobs_file,
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
