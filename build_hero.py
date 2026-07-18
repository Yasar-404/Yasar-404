#!/usr/bin/env python3
"""Build hero-dark.svg + hero-light.svg.
Wordmark is OUTLINED to vector paths (renders identically everywhere, no webfont
dependency) and animated glyph-by-glyph. Swap FONT to restyle the wordmark."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.varLib.instancer import instantiateVariableFont

# --- pick the wordmark face here -------------------------------------------
FONT   = ("fonts/Unbounded.ttf", {"wght": 800})          # unique + bold logotype
# FONT = ("fonts/Bricolage.ttf", {"wght":800,"opsz":48,"wdth":100})  # editorial
# FONT = ("fonts/SpaceGrotesk.ttf", {"wght":700})                    # techy
WORD, SIZE, TRACK = "YASAR K", 112, -0.015
X0, BASE = 82, 232          # wordmark origin (x, baseline y)
# ---------------------------------------------------------------------------

def outline():
    path, axes = FONT
    f = TTFont(path); instantiateVariableFont(f, axes, inplace=True)
    gs = f.getGlyphSet(); cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm; hmtx = f["hmtx"]; s = SIZE / upm
    x = 0.0; out = []
    for ch in WORD:
        g = cmap.get(ord(ch)); adv = hmtx[g][0] if g else int(upm*0.32)
        if g and ch != " ":
            pen = SVGPathPen(gs); gs[g].draw(pen); d = pen.getCommands()
            if d: out.append((d, X0 + x*s, s))
        x += adv + TRACK*upm
    return out, x*s

GLYPHS, WORD_W = outline()
THREAD_X2 = X0 + WORD_W

def glyph_paths():
    p = []
    for i,(d,tx,s) in enumerate(GLYPHS):
        p.append(
            f'<path class="g" pathLength="1" vector-effect="non-scaling-stroke" '
            f'style="animation-delay:{0.25+i*0.13:.2f}s" '
            f'transform="translate({tx:.1f},{BASE}) scale({s:.5f},{-s:.5f})" d="{d}"/>')
    return "".join(p)

TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="380" viewBox="0 0 1280 380" fill="none" role="img" aria-label="Yasar K — Design Engineer, Chennai">
  <title>Yasar K — Design Engineer</title>
  <defs>
    <linearGradient id="aurora" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#6E8BFF"/><stop offset="0.5" stop-color="#7C7BF7"/><stop offset="1" stop-color="#43E7C4"/>
    </linearGradient>
    <linearGradient id="sheen" gradientUnits="userSpaceOnUse" x1="{X0}" y1="0" x2="{TX2}" y2="0">
      <stop offset="0" stop-color="{ink}"/><stop offset="0.40" stop-color="{ink}"/>
      <stop offset="0.5" stop-color="{gleam}"/><stop offset="0.60" stop-color="{ink}"/>
      <stop offset="1" stop-color="{ink}"/>
      <animateTransform attributeName="gradientTransform" type="translate"
        values="-{W} 0; {W} 0; -{W} 0" dur="6s" begin="2.4s" keyTimes="0;0.5;1"
        calcMode="spline" keySplines="0.4 0 0.2 1; 0.4 0 0.2 1" repeatCount="indefinite"/>
    </linearGradient>
    <radialGradient id="atmos" cx="0.5" cy="0.35" r="0.75">
      <stop offset="0" stop-color="#6E8BFF" stop-opacity="{h0}"/>
      <stop offset="0.4" stop-color="#7C7BF7" stop-opacity="{h1}"/>
      <stop offset="1" stop-color="#6E8BFF" stop-opacity="0"/>
    </radialGradient>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="3.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1.1" cy="1.1" r="1.1" fill="{dot}"/></pattern>
    <style>
      .g{{fill:url(#sheen);fill-opacity:0;stroke:#6E8BFF;stroke-opacity:.85;stroke-width:1.2;
         stroke-dasharray:1;stroke-dashoffset:1;animation:rev 2s cubic-bezier(.4,0,.2,1) forwards}}
      @keyframes rev{{0%{{stroke-dashoffset:1;fill-opacity:0}}45%{{stroke-dashoffset:0;fill-opacity:0}}
         72%{{fill-opacity:1;stroke-opacity:.6}}100%{{stroke-dashoffset:0;fill-opacity:1;stroke-opacity:0}}}}
      .eyebrow{{font:500 15px/1 ui-monospace,"SF Mono","JetBrains Mono",Menlo,monospace;letter-spacing:6px;fill:{muted}}}
      .role{{font:400 19px/1 ui-sans-serif,-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;fill:{muted}}}
      .status{{font:500 13px/1 ui-monospace,"SF Mono","JetBrains Mono",Menlo,monospace;letter-spacing:2px;fill:{muted}}}
      .grid{{animation:breathe 6s ease-in-out infinite}}
      .halo{{animation:drift 20s ease-in-out infinite}}
      .fade{{opacity:0;animation:fin 1s ease 1.4s forwards}}
      @keyframes breathe{{0%,100%{{opacity:.5}}50%{{opacity:1}}}}
      @keyframes drift{{0%,100%{{transform:translate(0,0)}}50%{{transform:translate(26px,-14px)}}}}
      @keyframes fin{{to{{opacity:1}}}}
      @media (prefers-reduced-motion: reduce){{
        .grid,.halo{{animation:none}} .g{{animation:none;fill-opacity:1;stroke-opacity:0}} .fade{{animation:none;opacity:1}}
      }}
    </style>
  </defs>

  <rect width="1280" height="380" fill="{bg}"/>
  <g class="halo"><rect x="-40" y="-40" width="1360" height="460" fill="url(#atmos)"/></g>
  <rect class="grid" width="1280" height="380" fill="url(#dots)"/>

  <!-- floating particles -->
  <g fill="#7C7BF7">
    <circle cx="880" cy="250" r="1.6"><animate attributeName="cy" values="260;70" dur="11s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.7;0" dur="11s" repeatCount="indefinite"/></circle>
    <circle cx="970" cy="300" r="1.2" fill="#43E7C4"><animate attributeName="cy" values="300;110" dur="14s" begin="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.6;0" dur="14s" begin="2s" repeatCount="indefinite"/></circle>
    <circle cx="1080" cy="280" r="1.5"><animate attributeName="cy" values="290;90" dur="12s" begin="4s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.5;0" dur="12s" begin="4s" repeatCount="indefinite"/></circle>
    <circle cx="1160" cy="320" r="1.1" fill="#6E8BFF"><animate attributeName="cy" values="320;120" dur="15s" begin="1s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.6;0" dur="15s" begin="1s" repeatCount="indefinite"/></circle>
    <circle cx="1015" cy="240" r="1.3"><animate attributeName="cy" values="250;80" dur="13s" begin="6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;.5;0" dur="13s" begin="6s" repeatCount="indefinite"/></circle>
  </g>

  <g stroke="{mark}" stroke-width="1.4" class="fade">
    <g transform="translate(48,48)"><line x1="0" y1="0" x2="18" y2="0"/><line x1="0" y1="0" x2="0" y2="18"/></g>
    <g transform="translate(1232,48)"><line x1="0" y1="0" x2="-18" y2="0"/><line x1="0" y1="0" x2="0" y2="18"/></g>
    <g transform="translate(48,332)"><line x1="0" y1="0" x2="18" y2="0"/><line x1="0" y1="0" x2="0" y2="-18"/></g>
    <g transform="translate(1232,332)"><line x1="0" y1="0" x2="-18" y2="0"/><line x1="0" y1="0" x2="0" y2="-18"/></g>
  </g>

  <text class="eyebrow fade" x="{X0}" y="120">DESIGN ENGINEER &#160;·&#160; CHENNAI, IN</text>

  <!-- outlined animated wordmark -->
  {GLYPHS}

  <!-- aurora thread + travelling pulse + echo -->
  <g filter="url(#glow)">
    <line x1="{X0}" y1="266" x2="{TX2}" y2="266" stroke="url(#aurora)" stroke-width="2" stroke-linecap="round"
          stroke-dasharray="{W}" stroke-dashoffset="{W}">
      <animate attributeName="stroke-dashoffset" from="{W}" to="0" dur="1.6s" begin="1.9s" fill="freeze" calcMode="spline" keySplines="0.4 0 0.2 1"/>
    </line>
    <circle r="3.6" fill="#FFFFFF">
      <animate attributeName="cx" values="{X0};{TX2};{X0}" dur="7s" begin="3.5s" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;1;0" dur="7s" begin="3.5s" keyTimes="0;0.05;0.5;0.95;1" repeatCount="indefinite"/>
    </circle>
    <circle r="2.2" fill="#43E7C4">
      <animate attributeName="cx" values="{X0};{TX2};{X0}" dur="7s" begin="4.4s" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;.7;.7;.7;0" dur="7s" begin="4.4s" keyTimes="0;0.05;0.5;0.95;1" repeatCount="indefinite"/>
    </circle>
  </g>

  <text class="role fade" x="{X0}" y="306">Where product thinking meets engineering excellence.</text>

  <g transform="translate({X0},338)" class="fade">
    <circle cx="4" cy="-4" r="4" fill="#43E7C4"><animate attributeName="opacity" values="1;.35;1" dur="2.2s" repeatCount="indefinite"/></circle>
    <circle cx="4" cy="-4" r="4" fill="none" stroke="#43E7C4" stroke-width="1.4">
      <animate attributeName="r" values="4;11" dur="2.2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0" dur="2.2s" repeatCount="indefinite"/>
    </circle>
    <text class="status" x="20" y="0">OPEN TO SENIOR PRODUCT / UX ROLES</text>
  </g>
</svg>
'''

DARK  = dict(bg="#0A0A0B", ink="#EDEDF0", gleam="#FFFFFF", muted="#8A8A94",
             dot="rgba(255,255,255,0.06)", mark="rgba(255,255,255,0.22)", h0="0.22", h1="0.08")
LIGHT = dict(bg="#FBFBFD", ink="#1A1A20", gleam="#5B6BFF", muted="#6B6B76",
             dot="rgba(0,0,0,0.05)", mark="rgba(0,0,0,0.28)", h0="0.16", h1="0.05")

common = dict(X0=X0, TX2=round(THREAD_X2,1), W=round(WORD_W,1), GLYPHS=glyph_paths())
for name,c in (("hero-dark",DARK),("hero-light",LIGHT)):
    open(f"assets/{name}.svg","w").write(TEMPLATE.format(**{**c,**common}))
    print(f"wrote assets/{name}.svg   wordmark width={WORD_W:.0f}px  thread x2={THREAD_X2:.0f}")
