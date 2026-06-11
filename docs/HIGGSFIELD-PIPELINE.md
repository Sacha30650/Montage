# Higgsfield → HyperFrames b-roll pipeline

Goal: replace the carousel-slide "b-roll" (1:1 images with baked-in text) with
premium, full-bleed 9:16 photographic visuals generated on Higgsfield, without
breaking the dynamic template, the audit, or the fallback path.

## How it is wired

1. **Visual plan** — `assets/visual-plans/<pilot>.json`
   One entry per scene: voiceover excerpt, time range, target filename, and the
   exact Higgsfield prompt (style DNA + composition rules included at the top of
   the file). Prompts always end with "no text, no watermark" and keep faces in
   the upper half of the frame (captions render at ~62–78% height).

2. **Job tracking** — `assets/visual-plans/<pilot>.jobs.json`
   Maps target filenames to Higgsfield job ids and result URLs.

3. **Generation** (Hermes / any agent with the Higgsfield MCP):
   - model `soul_2`, `aspect_ratio: "9:16"`, `quality: "2k"` (≈0.12 credit/image)
   - one `generate_image` call per shot, prompts copied verbatim from the plan
   - poll `job_status` (sync:true) → grab `results.rawUrl`
   - **NSFW false positives**: soul_2's filter sometimes flags innocent
     child/bedroom scenes. Reword (child seen from behind, "small hand" instead
     of close-up child, living room instead of bed) and retry — this resolved
     all 3 cases for pilot-14.

4. **Download** — paste the rawUrls into the jobs file, then:
   ```bash
   python3 scripts/fetch_higgsfield_broll.py assets/visual-plans/<pilot>.jobs.json
   ```
   Files land in `pilots/<pilot>/assets/broll-hf/`.

5. **Mapping into HyperFrames** — `scripts/recent_pilots.py`
   The pilot config gets `hf_broll_dir` + `hf_slides` (filename, start, duration).
   `scripts/hf_dynamic_carousel.py::resolve_slides` uses the Higgsfield set only
   when **every** listed file exists; otherwise it falls back to the legacy
   carousel `slides` — so a partial batch never breaks generation.

6. **Regenerate + verify + render**
   ```bash
   npm run generate:recent
   npm run check
   cd pilots/<pilot> && npx --yes hyperframes@0.6.91 render
   ```

## Template behaviour with Higgsfield assets (full-bleed mode)

- Images are drawn full-frame (`object-fit: cover`, 1080×1920) — no more
  letterboxed slide on a blurred background.
- The heavy carousel scrim is replaced by a light cinematic grade: subtle
  vignette + soft bottom gradient, so the photography stays visible while
  captions (which carry their own black/yellow boxes) remain readable.
- Ken Burns moves, stutter zooms, flashes, shakes, SFX and caption timing are
  unchanged — pacing already passes `npm run audit`.

## Safe zones (encoded in every prompt)

- Captions: y 62–78% → keep key subjects in the upper 55%, lower third calm.
- TikTok UI: avoid critical detail in the right 12% and bottom 20%.
- Ken Burns zooms up to 1.16x → leave headroom around faces.

## Extending to other pilots (09–13)

Copy `assets/visual-plans/pilot-14-parle-tard.json` as the template: keep the
`style_dna` and `composition_rules`, rewrite the scene prompts from that pilot's
`scripts/full.txt` voiceover, add `hf_slides` to its config in
`scripts/recent_pilots.py` (2 shots per scene >8s, scene boundaries = existing
slide timings), then run the steps above.

## Upgrade path: animated b-roll

When video generation is available (MCP `generate_video`), the highest-impact
upgrades are: S1 hook (slow push-in on the child's face), S5 bamboo time-lapse
growth, S7 golden-hour lift. Use `seedance_2_0` or `kling3_0`, 9:16, 3–6s clips,
same prompts as the stills; the template needs a video-slide variant before
wiring them in (`<video muted>` + separate audio rule per CLAUDE.md).
