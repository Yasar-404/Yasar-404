#!/usr/bin/env python3
"""Emit hero-dark.svg and hero-light.svg from a single template (no CSS var()
so it renders identically in every SVG engine, GitHub camo included)."""

TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="380" viewBox="0 0 1280 380" fill="none" role="img" aria-label="Yasar K — Design Engineer, Chennai">
  <title>Yasar K — Design Engineer</title>
  <defs>
    <linearGradient id="aurora" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6E8BFF"/><stop offset="0.5" stop-color="#7C7BF7"/><stop offset="1" stop-color="#43E7C4"/>
    </linearGradient>
    <linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1="80" y1="0" x2="640" y2="0">
      <stop offset="0" stop-color="{ink}"/><stop offset="0.42" stop-color="{ink}"/>
      <stop offset="0.5" stop-color="{gleam}"/><stop offset="0.58" stop-color="{ink}"/>
      <stop offset="1" stop-color="{ink}"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        values="-620 0; 620 0; -620 0" dur="7s" begin="0.6s" keyTimes="0;0.5;1"
        calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1" repeatCount="indefinite"/>
    </linearGradient>
    <radialGradient id="atmos" cx="0.5" cy="0.35" r="0.75">
      <stop offset="0" stop-color="{halo}" stop-opacity="{h0}"/>
      <stop offset="0.4" stop-color="#7C7BF7" stop-opacity="{h1}"/>
      <stop offset="1" stop-color="{halo}" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse">
      <circle cx="1.1" cy="1.1" r="1.1" fill="{dot}"/>
    </pattern>
    <style>
      .word{{font:300 92px/1 ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;letter-spacing:-2px;fill:url(#sheen)}}
      .eyebrow{{font:500 15px/1 ui-monospace,"SF Mono","JetBrains Mono",Menlo,monospace;letter-spacing:6px;fill:{muted}}}
      .role{{font:400 19px/1 ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;fill:{muted}}}
      .status{{font:500 13px/1 ui-monospace,"SF Mono","JetBrains Mono",Menlo,monospace;letter-spacing:2px;fill:{muted}}}
      .grid{{animation:breathe 6s ease-in-out infinite}}
      @keyframes breathe{{0%,100%{{opacity:.55}}50%{{opacity:1}}}}
      @media (prefers-reduced-motion: reduce){{.grid{{animation:none}}}}
    </style>
  </defs>
  <rect width="1280" height="380" fill="{bg}"/>
  <rect width="1280" height="380" fill="url(#atmos)"/>
  <rect class="grid" width="1280" height="380" fill="url(#dots)"/>
  <g stroke="{mark}" stroke-width="1.4">
    <g transform="translate(48,48)"><line x1="0" y1="0" x2="18" y2="0"/><line x1="0" y1="0" x2="0" y2="18"/></g>
    <g transform="translate(1232,48)"><line x1="0" y1="0" x2="-18" y2="0"/><line x1="0" y1="0" x2="0" y2="18"/></g>
    <g transform="translate(48,332)"><line x1="0" y1="0" x2="18" y2="0"/><line x1="0" y1="0" x2="0" y2="-18"/></g>
    <g transform="translate(1232,332)"><line x1="0" y1="0" x2="-18" y2="0"/><line x1="0" y1="0" x2="0" y2="-18"/></g>
  </g>
  <text class="eyebrow" x="82" y="132">DESIGN ENGINEER &#160;·&#160; CHENNAI, IN</text>
  <text class="word" x="80" y="228">YASAR K</text>
  <g filter="url(#glow)">
    <line x1="82" y1="266" x2="640" y2="266" stroke="url(#aurora)" stroke-width="2" stroke-linecap="round"
          stroke-dasharray="560" stroke-dashoffset="560">
      <animate attributeName="stroke-dashoffset" from="560" to="0" dur="1.6s" begin="0.3s"
               fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
    </line>
    <circle r="3.4" fill="#FFFFFF">
      <animate attributeName="cx" values="82;640;82" dur="7s" begin="1.9s" keyTimes="0;0.5;1"
               calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;1;0" dur="7s" begin="1.9s"
               keyTimes="0;0.05;0.5;0.95;1" repeatCount="indefinite"/>
    </circle>
  </g>
  <text class="role" x="82" y="306">Product &amp; UX design, engineered end to end — Figma to shipped interface.</text>
  <g transform="translate(82,338)">
    <circle cx="4" cy="-4" r="4" fill="#43E7C4"><animate attributeName="opacity" values="1;0.35;1" dur="2.2s" repeatCount="indefinite"/></circle>
    <circle cx="4" cy="-4" r="4" fill="none" stroke="#43E7C4" stroke-width="1.4">
      <animate attributeName="r" values="4;11" dur="2.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.6;0" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <text class="status" x="20" y="0">OPEN TO SENIOR PRODUCT / UX ROLES</text>
  </g>
</svg>
'''

DARK = dict(bg="#0A0A0B", ink="#EDEDF0", gleam="#FFFFFF", muted="#8A8A94",
            dot="rgba(255,255,255,0.06)", mark="rgba(255,255,255,0.22)",
            halo="#6E8BFF", h0="0.22", h1="0.08")
LIGHT = dict(bg="#FBFBFD", ink="#16161A", gleam="#5B6BFF", muted="#6B6B76",
             dot="rgba(0,0,0,0.05)", mark="rgba(0,0,0,0.28)",
             halo="#6E8BFF", h0="0.16", h1="0.05")

for name, c in (("hero-dark", DARK), ("hero-light", LIGHT)):
    with open(f"assets/{name}.svg", "w") as f:
        f.write(TEMPLATE.format(**c))
    print(f"wrote assets/{name}.svg")
