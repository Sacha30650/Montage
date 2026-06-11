#!/usr/bin/env python3
"""Generate pilot-14-parle-tard and root index.html with the dynamic template."""

from hf_dynamic_carousel import render_pilot
from recent_pilots import RECENT_PILOTS


if __name__ == "__main__":
    target = render_pilot(RECENT_PILOTS["pilot-14-parle-tard"], write_root=True)
    print(f"generated {target} and index.html")
