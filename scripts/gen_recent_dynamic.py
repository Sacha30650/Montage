#!/usr/bin/env python3
"""Regenerate the recent long pilots with the dynamic carousel template."""

from hf_dynamic_carousel import render_pilot
from recent_pilots import RECENT_ORDER, RECENT_PILOTS


ROOT_SLUG = "pilot-14-parle-tard"


def main() -> None:
    for slug in RECENT_ORDER:
        target = render_pilot(RECENT_PILOTS[slug], write_root=(slug == ROOT_SLUG))
        root_note = " + root index.html" if slug == ROOT_SLUG else ""
        print(f"generated {target.relative_to(target.parents[2])}{root_note}")


if __name__ == "__main__":
    main()
