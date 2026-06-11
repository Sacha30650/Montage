# HyperFrames Composition Project

## Skills — USE THESE FIRST

**Always invoke the relevant skill before writing or modifying compositions.** Skills encode framework-specific patterns (e.g., `window.__timelines` registration, `data-*` attribute semantics, shader-compatible CSS rules) that are NOT in generic web docs. Skipping them produces broken compositions.

| Skill                      | Command                   | When to use                                                                                       |
| -------------------------- | ------------------------- | ------------------------------------------------------------------------------------------------- |
| **hyperframes**            | `/hyperframes`            | Creating or editing HTML compositions, captions, TTS, audio-reactive animation, marker highlights |
| **hyperframes-cli**        | `/hyperframes-cli`        | Dev-loop CLI: init, lint, inspect, preview, render, doctor                                        |
| **hyperframes-media**      | `/hyperframes-media`      | Asset preprocessing: tts (Kokoro), transcribe (Whisper), remove-background (u2net)                |
| **hyperframes-registry**   | `/hyperframes-registry`   | Installing blocks and components via `hyperframes add`                                            |
| **website-to-hyperframes** | `/website-to-hyperframes` | Capturing a URL and turning it into a video — full website-to-video pipeline                      |
| **tailwind**               | `/tailwind`               | Tailwind v4 browser-runtime styles for projects created with `hyperframes init --tailwind`        |
| **gsap**                   | `/gsap`                   | GSAP animations for HyperFrames — tweens, timelines, easing, performance                          |
| **animejs**                | `/animejs`                | Anime.js animations registered on `window.__hfAnime`                                              |
| **css-animations**         | `/css-animations`         | CSS keyframes that HyperFrames can pause and seek                                                 |
| **lottie**                 | `/lottie`                 | `lottie-web` and dotLottie players registered on `window.__hfLottie`                              |
| **three**                  | `/three`                  | Three.js scenes rendered from HyperFrames `hf-seek` events                                        |
| **waapi**                  | `/waapi`                  | Web Animations API motion driven through `document.getAnimations()`                               |

> **Skills not available?** Ask the user to run `npx hyperframes skills` and restart their
> agent session, or install manually: `npx skills add heygen-com/hyperframes`.

## Commands

```bash
npm run dev          # preview in browser (studio editor)
npm run check        # lint + validate + inspect + timeline audit
npm run audit        # overlap + long-form pacing density audit
npm run generate:recent # regenerate pilots 09-14 and root index.html
npm run render       # render to MP4
npm run publish      # publish and get a shareable link
npx hyperframes lint --verbose  # include info-level findings
npx hyperframes lint --json     # machine-readable output for CI
npx hyperframes docs <topic> # reference docs in terminal
```

## Documentation

**For quick reference**, use the local CLI docs command (no network required):

```bash
npx hyperframes docs <topic>
```

Topics: `data-attributes`, `gsap`, `compositions`, `rendering`, `examples`, `troubleshooting`

**For full documentation**, discover pages via the machine-readable index — do NOT guess URLs:

```
https://hyperframes.heygen.com/llms.txt
```

## Project Structure

- `index.html` — main composition (root timeline)
- `compositions/` — sub-compositions referenced via `data-composition-src`
- `meta.json` — project metadata (id, name)
- `transcript.json` — whisper word-level transcript (if generated)

## Linting — ALWAYS RUN AFTER CHANGES

After creating or editing any `.html` composition, **always** run the full check before considering the task complete:

```bash
npm run check
```

Fix all errors before presenting the result. Inspect warnings should be reviewed before rendering.

## Long-Form Reels/TikTok Guardrails

Videos over 60s should be generated through `scripts/hf_dynamic_carousel.py` via `npm run generate:recent` or the `gen_p09`-`gen_p14` wrappers. The template keeps carousel assets but adds 2-3s cuts, transcript-derived captions, a music bed, SFX beats, flashes, shakes, and rounded timings with tiny gaps so same-track float overlaps do not reappear.

`npm run audit` checks `index.html` plus pilots 09-14 for overlaps, missing `clip` classes, cut/caption density, max image hold, music presence, SFX count, and voiceover duration drift.

## Key Rules

1. Every timed element needs `data-start`, `data-duration`, and `data-track-index`
2. Elements with timing **MUST** have `class="clip"` — the framework uses this for visibility control
3. Timelines must be paused and registered on `window.__timelines`:
   ```js
   window.__timelines = window.__timelines || {};
   window.__timelines["composition-id"] = gsap.timeline({ paused: true });
   ```
4. Videos use `muted` with a separate `<audio>` element for the audio track
5. Sub-compositions use `data-composition-src="compositions/file.html"` to reference other HTML files
6. Only deterministic logic — no `Date.now()`, no `Math.random()`, no network fetches
