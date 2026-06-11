#!/usr/bin/env python3
"""Generate pilot-11-cosleeping with the dynamic long-form carousel template."""

from hf_dynamic_carousel import render_pilot
from recent_pilots import RECENT_PILOTS


if __name__ == "__main__":
    target = render_pilot(RECENT_PILOTS["pilot-11-cosleeping"])
    print(f"generated {target}")
