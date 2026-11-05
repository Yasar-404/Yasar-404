# Engineering notes

The profile README is generated. `studio` is a small Python package with one runtime
dependency (fontTools, for outlining type), and everything else is the standard library.

## Commands

```bash
pip install -e ".[dev]"
python -m studio   # render assets/*.svg
pytest
ruff check .
```

## Layout

| Path | Responsibility |
|---|---|
| `studio/content.py` | All copy: headline, stack, projects, code snippets |
| `studio/theme.py` | Design tokens for the dark and light themes |
| `studio/typography.py`, `studio/svg.py` | Outlined text and the SVG document builder |
| `studio/sections/` | One renderer per part of the page |
| `.github/workflows/ci.yml` | Runs tests and lint on each push |

## Decisions

**Outlined type.** GitHub's image sandbox blocks web fonts, and system font stacks change
text widths per OS. Each glyph is defined once per file and reused with `<use>`, which keeps
even the code panel small.

**Looping, CSS-only motion.** README images only animate from page load, so a one-shot
entrance below the fold would finish before anyone scrolls to it. Only the hero has an
entrance. Everything is CSS because `prefers-reduced-motion` cannot stop SMIL animation.

**A 960px canvas.** GitHub's profile column is roughly 830px wide on desktop. Drawing near
that size keeps small labels legible, where a 1280px canvas would shrink them by a third.

**Direct image URLs.** Relative README images load through a `github.com/.../raw/` redirect
for every file, so any slowness on github.com delays each image. Absolute
`raw.githubusercontent.com` URLs skip it.

**A budget for motion.** A running animation makes the browser redo work for that image on
every frame, even when the change is tiny. Continuous motion is kept to the elements that
carry meaning, and small decorative loops stay static.

## Limits

SVG images can't hold hyperlinks or hover states on GitHub, so links wrap the images in the
README, and alt text carries the content for screen readers.

## Fonts

Inter, JetBrains Mono and Unbounded, under the SIL Open Font License. See `fonts/`.
