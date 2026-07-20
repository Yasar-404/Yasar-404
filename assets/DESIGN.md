# Design System — Yasar-404 profile

The single source of truth for every asset in this repo. Nothing is invented per-file;
each SVG derives its values from here so the profile reads as one designed object.

## Color — Dark (default)

| Token        | Hex / value                | Use                          |
|--------------|----------------------------|------------------------------|
| `bg`         | `#0A0A0B`                  | Canvas                       |
| `panel`      | `#0E0E11`                  | Raised surfaces              |
| `ink`        | `#EDEDF0`                  | Primary text / wordmark      |
| `gleam`      | `#FFFFFF`                  | Sheen highlight band         |
| `muted`      | `#8A8A94`                  | Labels, captions, sublines   |
| `stroke`     | `rgba(255,255,255,0.10)`   | Hairline dividers, borders   |
| `dot`        | `rgba(255,255,255,0.06)`   | Grid pattern                 |
| `mark`       | `rgba(255,255,255,0.22)`   | Registration / crop marks    |

## Color — Light

| Token        | Hex / value                |
|--------------|----------------------------|
| `bg`         | `#FBFBFD`                  |
| `panel`      | `#F4F4F7`                  |
| `ink`        | `#16161A`                  |
| `gleam`      | `#5B6BFF`                  |
| `muted`      | `#6B6B76`                  |
| `stroke`     | `rgba(0,0,0,0.09)`         |
| `dot`        | `rgba(0,0,0,0.05)`         |
| `mark`       | `rgba(0,0,0,0.28)`         |

## Accent — Aurora (shared across themes)

A single restrained gradient. Never acid-green, never vermilion.

```
#6E8BFF  periwinkle   →   #7C7BF7  iris   →   #43E7C4  mint-cyan
```

- `#43E7C4` alone signals **live / available** (status pulse).
- Halo behind hero uses `#6E8BFF` at 0.22 (dark) / 0.16 (light) opacity.

## Type

| Role     | Stack                                                                 | Treatment              |
|----------|-----------------------------------------------------------------------|------------------------|
| Display  | **Unbounded 800**, outlined to vector paths (see `build_hero.py`)      | logotype, `-1.5%` track |
| Body     | same sans stack                                                       | weight 400             |
| Label    | `ui-monospace, "SF Mono", "JetBrains Mono", Menlo, monospace`         | tracked `+6px`, uppercase |

System stacks only — they render consistently through GitHub's image proxy without
embedding font binaries. Elegance comes from weight, spacing, and hierarchy, not a webfont.

## Motion

| Curve            | Value                          | Use                        |
|------------------|--------------------------------|----------------------------|
| Signature ease   | `cubic-bezier(0.4, 0, 0.2, 1)` | draws, sweeps, travels     |
| Breathe          | `ease-in-out`, 6s              | grid opacity               |
| Pulse            | linear, 2.2s                   | availability dot           |

Rules: nothing faster than 1.6s on a primary element; every loop returns to its
start state seamlessly; `prefers-reduced-motion` disables ambient loops.

## Platform constraints (why the system looks the way it does)

GitHub READMEs sanitize Markdown: **no `<script>`, no page `<style>`, no `:hover`,
no JS.** Every asset is therefore a self-contained SVG referenced as an image, where
internal `<style>`, `@keyframes`, SMIL, filters and gradients all animate. Theme
switching is done with `<picture>` + `prefers-color-scheme`, not CSS toggles.

## Accessibility (Sprint 4 audit)

Every asset passes an automated audit:
- `role="img"`, `aria-label`, and `<title>` on all 28 SVGs (screen-reader name + tooltip).
- **All motion is CSS** — there are zero infinite SMIL loops. This matters because
  `@media (prefers-reduced-motion: reduce)` cannot stop SMIL animation; it can only
  gate CSS. Every animated file therefore honors reduced-motion, collapsing to a calm
  resting state (no orbit, pulse, drift, sweep, or blink) for users who ask for it.
- README `<img>`/`<picture>` all carry descriptive `alt` text; decorative dividers use
  empty `alt=""` so screen readers skip them.
- Clickable contact links live in the README markdown (an SVG embedded as an image
  cannot expose working hyperlinks on GitHub).
