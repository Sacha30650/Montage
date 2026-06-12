#!/usr/bin/env python3
"""Generate full-bleed 9:16 abstract cinematic b-roll for pilot-15-ennui.

Pure local PIL/numpy gradients — no text, no watermark. Deterministic (fixed seeds).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "pilots/pilot-15-ennui/assets/broll-hf"
W, H = 1080, 1920

YY, XX = np.mgrid[0:H, 0:W].astype(np.float32)
NX = (XX / W) * 2 - 1
NY = (YY / H) * 2 - 1


def vertical_gradient(stops: list[tuple[float, tuple[int, int, int]]]) -> np.ndarray:
    img = np.zeros((H, W, 3), dtype=np.float32)
    t = YY / H
    for (p0, c0), (p1, c1) in zip(stops, stops[1:]):
        mask = np.clip((t - p0) / max(p1 - p0, 1e-6), 0, 1)
        smooth = mask * mask * (3 - 2 * mask)
        for ch in range(3):
            seg = c0[ch] + (c1[ch] - c0[ch]) * smooth
            img[..., ch] = np.where(t < p0, img[..., ch], seg)
    for ch in range(3):
        img[..., ch] = np.where(t < stops[0][0], stops[0][1][ch], img[..., ch])
    return img


def add_glow(img: np.ndarray, cx: float, cy: float, radius: float,
             color: tuple[int, int, int], strength: float = 1.0, aspect: float = 1.0) -> None:
    d2 = ((NX - cx) / aspect) ** 2 + (NY - cy) ** 2
    fall = np.exp(-d2 / (2 * radius * radius)) * strength
    for ch in range(3):
        img[..., ch] += color[ch] * fall


def add_bokeh(img: np.ndarray, rng: np.random.Generator, n: int,
              color: tuple[int, int, int], rmin: float = 0.01, rmax: float = 0.05,
              ymin: float = -1.0, ymax: float = 1.0, strength: float = 0.5) -> None:
    for _ in range(n):
        cx = rng.uniform(-0.95, 0.95)
        cy = rng.uniform(ymin, ymax)
        r = rng.uniform(rmin, rmax)
        s = rng.uniform(0.3, 1.0) * strength
        add_glow(img, cx, cy, r, color, s)


def add_network(img: np.ndarray, rng: np.random.Generator, n: int,
                color: tuple[int, int, int]) -> None:
    pts = [(rng.uniform(-0.8, 0.8), rng.uniform(-0.75, 0.75)) for _ in range(n)]
    for i, (ax, ay) in enumerate(pts):
        for bx, by in pts[i + 1:]:
            if (ax - bx) ** 2 + (ay - by) ** 2 > 0.42:
                continue
            for t in np.linspace(0, 1, 22):
                add_glow(img, ax + (bx - ax) * t, ay + (by - ay) * t, 0.008, color, 0.16)
        add_glow(img, ax, ay, 0.018, color, 1.5)
        add_glow(img, ax, ay, 0.07, color, 0.35)


def add_streaks(img: np.ndarray, rng: np.random.Generator, n: int,
                color: tuple[int, int, int], strength: float = 0.3) -> None:
    for _ in range(n):
        cx = rng.uniform(-1, 1)
        cy = rng.uniform(-0.9, 0.9)
        length = rng.uniform(0.08, 0.3)
        for t in np.linspace(0, 1, 14):
            add_glow(img, cx, cy + length * t, 0.006, color, strength * (1 - t))


def vignette(img: np.ndarray, power: float = 0.55) -> None:
    d = np.sqrt((NX * 0.78) ** 2 + (NY * 0.62) ** 2)
    mask = 1 - power * np.clip(d - 0.45, 0, 1) ** 1.6
    img *= mask[..., None]


def finish(img: np.ndarray, name: str, seed: int, blur: float = 3.0) -> None:
    rng = np.random.default_rng(seed + 1000)
    pil = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    pil = pil.filter(ImageFilter.GaussianBlur(blur))
    arr = np.asarray(pil).astype(np.float32)
    arr += rng.normal(0, 2.6, arr.shape).astype(np.float32)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(OUT / name, optimize=True)
    print(f"wrote {name}")


def scene_hook_a() -> None:
    # dusk room: deep teal-navy, one warm window glow upper third
    img = vertical_gradient([(0.0, (10, 18, 34)), (0.45, (16, 32, 52)), (1.0, (6, 10, 18))])
    rng = np.random.default_rng(151)
    add_glow(img, 0.32, -0.42, 0.22, (215, 150, 70), 0.85, aspect=0.7)
    add_glow(img, 0.32, -0.42, 0.07, (255, 205, 120), 1.0, aspect=0.65)
    add_glow(img, -0.55, 0.55, 0.5, (20, 60, 80), 0.5)
    add_bokeh(img, rng, 10, (90, 140, 170), 0.008, 0.02, -0.2, 0.9, 0.35)
    vignette(img)
    finish(img, "01_hook_a.png", 151)


def scene_hook_b() -> None:
    # the gift: warm amber radial burst on near-black
    img = vertical_gradient([(0.0, (16, 10, 8)), (0.5, (28, 16, 12)), (1.0, (8, 5, 6))])
    rng = np.random.default_rng(152)
    add_glow(img, 0.0, -0.05, 0.34, (235, 150, 50), 0.95)
    add_glow(img, 0.0, -0.05, 0.12, (255, 215, 130), 1.1)
    add_glow(img, 0.0, -0.05, 0.035, (255, 245, 210), 1.2)
    add_bokeh(img, rng, 16, (255, 190, 90), 0.006, 0.018, -0.7, 0.6, 0.5)
    vignette(img, 0.6)
    finish(img, "01_hook_b.png", 152)


def scene_empathy_a() -> None:
    # muted blue-grey with soft falling streaks (the "je sais pas quoi faire" mood)
    img = vertical_gradient([(0.0, (30, 38, 52)), (0.55, (44, 52, 68)), (1.0, (16, 20, 30))])
    rng = np.random.default_rng(153)
    add_streaks(img, rng, 26, (120, 140, 170), 0.32)
    add_glow(img, 0.0, -0.25, 0.45, (70, 90, 120), 0.45)
    vignette(img)
    finish(img, "02_empathy_a.png", 153)


def scene_empathy_b() -> None:
    # cold screen-glow rising from bottom of a dark room
    img = vertical_gradient([(0.0, (8, 10, 16)), (0.6, (14, 18, 28)), (1.0, (22, 34, 56))])
    rng = np.random.default_rng(154)
    add_glow(img, 0.0, 0.78, 0.3, (70, 140, 220), 0.95, aspect=1.4)
    add_glow(img, 0.0, 0.85, 0.12, (140, 200, 255), 0.8, aspect=1.6)
    add_bokeh(img, rng, 8, (60, 110, 180), 0.008, 0.02, -0.4, 0.4, 0.3)
    vignette(img)
    finish(img, "02_empathy_b.png", 154)


def scene_science_a() -> None:
    # default mode network: indigo field with glowing connected nodes
    img = vertical_gradient([(0.0, (14, 10, 38)), (0.5, (26, 18, 60)), (1.0, (8, 6, 24))])
    rng = np.random.default_rng(155)
    add_glow(img, 0.0, 0.0, 0.5, (40, 30, 100), 0.55)
    add_network(img, rng, 11, (150, 170, 255))
    vignette(img, 0.5)
    finish(img, "03_science_a.png", 155)


def scene_science_b() -> None:
    # imagination nebula: violet-magenta bloom
    img = vertical_gradient([(0.0, (20, 8, 36)), (0.5, (44, 16, 64)), (1.0, (10, 4, 22))])
    rng = np.random.default_rng(156)
    add_glow(img, -0.3, -0.3, 0.35, (190, 70, 200), 0.7)
    add_glow(img, 0.4, 0.25, 0.3, (90, 60, 220), 0.65)
    add_glow(img, 0.05, -0.05, 0.14, (255, 160, 230), 0.6)
    add_bokeh(img, rng, 22, (220, 160, 255), 0.005, 0.015, -0.9, 0.9, 0.5)
    vignette(img, 0.5)
    finish(img, "03_science_b.png", 156)


def scene_observe_a() -> None:
    # quiet warm room: amber lamp pools, patience
    img = vertical_gradient([(0.0, (30, 22, 18)), (0.5, (52, 36, 26)), (1.0, (14, 10, 10))])
    rng = np.random.default_rng(157)
    add_glow(img, -0.35, -0.3, 0.2, (230, 160, 80), 0.8)
    add_glow(img, 0.5, 0.4, 0.28, (180, 110, 60), 0.5)
    add_bokeh(img, rng, 10, (240, 180, 100), 0.007, 0.02, -0.6, 0.8, 0.4)
    vignette(img)
    finish(img, "04_observe_a.png", 157)


def scene_observe_b() -> None:
    # the spark: sunrise burst, play ignites
    img = vertical_gradient([(0.0, (40, 14, 40)), (0.45, (90, 34, 50)), (1.0, (20, 8, 24))])
    rng = np.random.default_rng(158)
    add_glow(img, 0.0, 0.1, 0.4, (255, 120, 60), 0.85)
    add_glow(img, 0.0, 0.05, 0.16, (255, 200, 110), 1.0)
    add_glow(img, 0.0, 0.0, 0.05, (255, 250, 220), 1.1)
    add_bokeh(img, rng, 18, (255, 170, 110), 0.006, 0.02, -0.8, 0.8, 0.55)
    vignette(img, 0.5)
    finish(img, "04_observe_b.png", 158)


def scene_jachere_a() -> None:
    # fallow field at dusk: ochre/olive horizon
    img = vertical_gradient([
        (0.0, (60, 52, 40)), (0.42, (120, 96, 56)), (0.5, (70, 60, 34)),
        (0.62, (44, 40, 24)), (1.0, (16, 14, 10)),
    ])
    rng = np.random.default_rng(159)
    add_glow(img, 0.0, -0.12, 0.25, (255, 200, 110), 0.7, aspect=2.2)
    add_streaks(img, rng, 14, (140, 120, 70), 0.22)
    vignette(img)
    finish(img, "05_jachere_a.png", 159)


def scene_jachere_b() -> None:
    # under the soil: deep brown with golden root-glow veins
    img = vertical_gradient([(0.0, (26, 18, 12)), (0.5, (38, 26, 16)), (1.0, (12, 8, 6))])
    rng = np.random.default_rng(160)
    add_network(img, rng, 8, (235, 170, 70))
    add_glow(img, 0.0, 0.3, 0.4, (120, 80, 30), 0.45)
    vignette(img)
    finish(img, "05_jachere_b.png", 160)


def scene_advice_a() -> None:
    # calm sage green: space left open on the agenda
    img = vertical_gradient([(0.0, (24, 38, 32)), (0.5, (44, 66, 54)), (1.0, (12, 20, 16))])
    rng = np.random.default_rng(161)
    add_glow(img, -0.2, -0.35, 0.3, (140, 200, 160), 0.55)
    add_glow(img, 0.45, 0.3, 0.35, (60, 110, 90), 0.5)
    add_bokeh(img, rng, 12, (170, 220, 180), 0.006, 0.018, -0.7, 0.8, 0.35)
    vignette(img)
    finish(img, "06_advice_a.png", 161)


def scene_advice_b() -> None:
    # simple objects: warm neutral bokeh, paper / carton / string tones
    img = vertical_gradient([(0.0, (44, 38, 32)), (0.5, (70, 58, 44)), (1.0, (20, 16, 14))])
    rng = np.random.default_rng(162)
    add_bokeh(img, rng, 20, (235, 200, 150), 0.012, 0.05, -0.7, 0.8, 0.5)
    add_glow(img, 0.0, -0.1, 0.4, (160, 130, 90), 0.45)
    vignette(img)
    finish(img, "06_advice_b.png", 162)


def scene_cta_a() -> None:
    # holding on: charcoal with a slow rising glow
    img = vertical_gradient([(0.0, (14, 14, 18)), (0.6, (24, 22, 28)), (1.0, (8, 8, 12))])
    rng = np.random.default_rng(163)
    add_glow(img, 0.0, 0.55, 0.35, (200, 140, 70), 0.6, aspect=1.5)
    add_glow(img, 0.0, 0.7, 0.14, (255, 200, 120), 0.7, aspect=1.4)
    add_bokeh(img, rng, 8, (200, 160, 110), 0.006, 0.015, -0.2, 0.6, 0.3)
    vignette(img)
    finish(img, "07_cta_a.png", 163)


def scene_cta_b() -> None:
    # the secret workshop: golden radial light with sparkle bokeh
    img = vertical_gradient([(0.0, (24, 14, 8)), (0.5, (46, 26, 12)), (1.0, (12, 7, 5))])
    rng = np.random.default_rng(164)
    add_glow(img, 0.0, -0.1, 0.38, (240, 160, 60), 0.9)
    add_glow(img, 0.0, -0.1, 0.15, (255, 215, 130), 1.05)
    add_glow(img, 0.0, -0.1, 0.045, (255, 248, 220), 1.15)
    add_bokeh(img, rng, 26, (255, 210, 120), 0.005, 0.02, -0.9, 0.9, 0.6)
    vignette(img, 0.55)
    finish(img, "07_cta_b.png", 164)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for fn in (
        scene_hook_a, scene_hook_b, scene_empathy_a, scene_empathy_b,
        scene_science_a, scene_science_b, scene_observe_a, scene_observe_b,
        scene_jachere_a, scene_jachere_b, scene_advice_a, scene_advice_b,
        scene_cta_a, scene_cta_b,
    ):
        fn()


if __name__ == "__main__":
    main()
