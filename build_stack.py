#!/usr/bin/env python3
"""Custom animated tech/design icon system + composed Stack panel (dark+light).
Every glyph is ORIGINAL geometry on a 46px chip grid. No trademarked logos."""
import math

# ---- individual icon glyphs (centered at cx,cy; ~±14 art radius) ----------
def react(cx,cy):
    orb=f'<g transform="rotate(0 {cx} {cy})"><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="7s" repeatCount="indefinite"/><circle cx="{cx+14}" cy="{cy}" r="2" class="dot"/></g>'
    return (f'<ellipse cx="{cx}" cy="{cy}" rx="14" ry="5.5" class="ic" transform="rotate(-22 {cx} {cy})"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="14" ry="5.5" class="ic" transform="rotate(22 {cx} {cy})"/>'
            f'<circle cx="{cx}" cy="{cy}" r="2.6" class="fic"/>{orb}')
def nextjs(cx,cy):
    return (f'<path class="ic" d="M{cx-12},{cy+12} A12,12 0 1 1 {cx+11},{cy+6}"/>'
            f'<path class="ic" d="M{cx-6},{cy+10} V{cy-10} L{cx+9},{cy+11}"/>'
            f'<path class="ic" d="M{cx+8},{cy-10} V{cy-2}"/>')
def typescript(cx,cy):
    return (f'<path class="ic" d="M{cx-13},{cy-11} H{cx+3}"/>'
            f'<path class="ic" d="M{cx-5},{cy-11} V{cy+12}"/>'
            f'<path class="ic" d="M{cx+6},{cy+12} q7,0 7,-6 0,-5 -6,-6 -6,-1 -6,-6 0,-6 7,-6"/>')
def javascript(cx,cy):
    return (f'<path class="ic" d="M{cx-4},{cy-12} q-6,0 -6,6 v3 q0,6 -5,6 5,0 5,6 v3 q0,6 6,6"/>'
            f'<path class="ic" d="M{cx+4},{cy-12} q6,0 6,6 v3 q0,6 5,6 -5,0 -5,6 v3 q0,6 -6,6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="1.6" class="fic"/>')
def node(cx,cy):
    pts=" ".join(f"{cx+13*math.cos(math.radians(a)):.1f},{cy+13*math.sin(math.radians(a)):.1f}" for a in range(-90,270,60))
    return f'<polygon points="{pts}" class="ic"/><circle cx="{cx}" cy="{cy}" r="2.4" class="fic"/>'
def prisma(cx,cy):
    return (f'<path class="ic" d="M{cx},{cy-13} L{cx+12},{cy+12} H{cx-12} Z"/>'
            f'<path class="ic" d="M{cx},{cy-13} V{cy+12}"/>'
            f'<path class="dic" d="M{cx},{cy-13} L{cx-7},{cy+12}"/>')
def postgres(cx,cy):
    return (f'<ellipse cx="{cx}" cy="{cy-9}" rx="12" ry="4.5" class="ic"/>'
            f'<path class="ic" d="M{cx-12},{cy-9} V{cy+9} q0,4.5 12,4.5 12,0 12,-4.5 V{cy-9}"/>'
            f'<path class="ic" d="M{cx-12},{cy} q0,4.5 12,4.5 12,0 12,-4.5"/>')
def tailwind(cx,cy):
    return (f'<path class="ic" d="M{cx-13},{cy-3} q4,-8 8,-4 3,3 5,3 4,0 5,-4 -3,8 -8,4 -3,-3 -5,-3 -4,0 -5,4 Z" opacity=".85"/>'
            f'<path class="ic" d="M{cx-13},{cy+7} q4,-8 8,-4 3,3 5,3 4,0 5,-4 -3,8 -8,4 -3,-3 -5,-3 -4,0 -5,4 Z"/>')
def figma(cx,cy):
    return (f'<circle cx="{cx-4}" cy="{cy-6}" r="7" class="ic"/>'
            f'<rect x="{cx-2}" y="{cy-1}" width="13" height="13" rx="2" class="ic"/>')
def framer(cx,cy):
    return (f'<path class="ic" d="M{cx-10},{cy-12} H{cx+10} L{cx},{cy} H{cx-10} Z"/>'
            f'<path class="ic" d="M{cx-10},{cy} H{cx} L{cx+10},{cy+12} H{cx},{cy}"/>')
def motion(cx,cy):
    dots="".join(f'<circle cx="{cx-14+i*5}" cy="{cy+6}" r="{1.8-i*0.4}" class="dot"><animate attributeName="opacity" values="0;.9;0" dur="2.2s" begin="{i*0.25}s" repeatCount="indefinite"/></circle>' for i in range(3))
    return (f'<path class="ic" d="M{cx-13},{cy+2} q10,-16 26,-10"/>'
            f'<path class="dic" d="M{cx+9},{cy-11} l4,1 -1,4"/>{dots}')
def git(cx,cy):
    return (f'<path class="ic" d="M{cx-8},{cy+11} V{cy-6} q0,-6 8,-6 h4"/>'
            f'<path class="dic" d="M{cx-8},{cy-2} h8 q6,0 6,-6"/>'
            f'<circle cx="{cx-8}" cy="{cy+11}" r="2.6" class="fic"/>'
            f'<circle cx="{cx+6}" cy="{cy-11}" r="2.6" class="fic"/>'
            f'<circle cx="{cx+6}" cy="{cy-2}" r="2.4" class="dic-f"/>')
def github(cx,cy):
    spokes=""
    for a in (-90,-18,54,126,198):
        x=cx+12*math.cos(math.radians(a)); y=cy+12*math.sin(math.radians(a))
        mx=cx+7*math.cos(math.radians(a)); my=cy+7*math.sin(math.radians(a))
        spokes+=f'<line x1="{mx:.1f}" y1="{my:.1f}" x2="{x:.1f}" y2="{y:.1f}" class="ic"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2" class="dic-f"/>'
    return f'<circle cx="{cx}" cy="{cy}" r="5" class="ic"/><circle cx="{cx}" cy="{cy}" r="1.8" class="fic"/>{spokes}'
def terminal(cx,cy):
    return (f'<path class="ic" d="M{cx-11},{cy-6} l7,6 -7,6"/>'
            f'<rect x="{cx-1}" y="{cy+8}" width="12" height="2.2" rx="1" class="fic"><animate attributeName="opacity" values="1;0;1" dur="1.4s" repeatCount="indefinite"/></rect>')

ENG=[("React",react),("Next.js",nextjs),("TypeScript",typescript),("JavaScript",javascript),
     ("Node.js",node),("Prisma",prisma),("PostgreSQL",postgres),("Tailwind",tailwind)]
DES=[("Figma",figma),("Framer",framer),("Motion",motion),("Git",git),("GitHub",github),("Terminal",terminal)]

def chip(cx,cy,glyph,label,delay):
    return (f'<g class="chip" style="animation-delay:{delay:.2f}s">'
            f'<rect x="{cx-23}" y="{cy-23}" width="46" height="46" rx="13" class="tile"/>'
            f'<circle cx="{cx+16}" cy="{cy-16}" r="1.8" class="dot"/>'
            f'{glyph(cx,cy)}</g>'
            f'<text class="lbl" x="{cx}" y="{cy+40}">{label}</text>')

def row(items,cy,y0):
    n=len(items); cw=1280/n; out=[]
    for i,(lbl,g) in enumerate(items):
        cx=cw*(i+0.5); out.append(chip(cx,cy,g,lbl,y0+i*0.09))
    return "".join(out)

TEMPLATE='''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="392" viewBox="0 0 1280 392" fill="none" role="img" aria-label="Technology and design stack">
  <title>Stack</title>
  <defs><style>
    .tile{{fill:{tile};stroke:{stroke};stroke-width:1.3}}
    .ic{{fill:none;stroke:{ink};stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
    .dic{{fill:none;stroke:#6E8BFF;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
    .fic{{fill:{ink};stroke:none}}
    .dic-f{{fill:#6E8BFF;stroke:none}}
    .dot{{fill:#43E7C4}}
    .lbl{{font:500 12px/1 ui-monospace,"SF Mono","JetBrains Mono",Menlo,monospace;letter-spacing:1.5px;fill:{muted};text-anchor:middle}}
    .idx{{font:600 13px/1 ui-monospace,Menlo,monospace;letter-spacing:2px;fill:#6E8BFF}}
    .eyebrow{{font:500 14px/1 ui-monospace,Menlo,monospace;letter-spacing:5px;fill:{muted}}}
    .rowlbl{{font:600 11px/1 ui-monospace,Menlo,monospace;letter-spacing:3px;fill:{faint}}}
    .rule{{stroke:{stroke};stroke-width:1}}
    .chip{{transform-box:fill-box;transform-origin:center;opacity:0;animation:pop .6s cubic-bezier(.2,.75,.25,1) forwards}}
    .draw{{stroke-dasharray:1;stroke-dashoffset:1;animation:draw 1.1s ease forwards}}
    @keyframes pop{{0%{{opacity:0;transform:translateY(9px) scale(.92)}}100%{{opacity:1;transform:none}}}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}}
    @media (prefers-reduced-motion:reduce){{.chip{{animation:none;opacity:1}}.draw{{animation:none;stroke-dashoffset:0}}}}
  </style></defs>

  <text class="idx" x="40" y="46">02</text>
  <line class="rule draw" x1="66" y1="42" x2="120" y2="42" pathLength="1"/>
  <text class="eyebrow" x="134" y="47">STACK</text>
  <text class="rowlbl" x="1240" y="47" text-anchor="end">ORIGINAL SVG ICON SYSTEM · NO EXTERNAL ICONS</text>

  <text class="rowlbl" x="40" y="96">ENGINEERING</text>
  <line class="rule" x1="150" y1="92" x2="1240" y2="92"/>
  {ENG}

  <text class="rowlbl" x="40" y="248">DESIGN &amp; TOOLS</text>
  <line class="rule" x1="150" y1="244" x2="1240" y2="244"/>
  {DES}
</svg>
'''
DARK=dict(tile="rgba(255,255,255,0.02)",stroke="rgba(255,255,255,0.12)",ink="#D6D6DE",muted="#8A8A94",faint="#5B5B63")
LIGHT=dict(tile="rgba(0,0,0,0.015)",stroke="rgba(0,0,0,0.11)",ink="#33333B",muted="#6B6B76",faint="#9A9AA4")
eng=row(ENG,150,0.15); des=row(DES,302,0.7)
for name,c in (("stack-dark",DARK),("stack-light",LIGHT)):
    open(f"assets/{name}.svg","w").write(TEMPLATE.format(ENG=eng,DES=des,**c))
    print("wrote assets/"+name+".svg")

# ---- also emit reusable single-icon files (theme-adaptive, self-contained) ----
ICON='''<svg xmlns="http://www.w3.org/2000/svg" width="64" height="64" viewBox="0 0 64 64" fill="none" role="img" aria-label="{name}">
  <defs><style>
    .tile{{fill:rgba(255,255,255,0.02);stroke:rgba(255,255,255,0.12);stroke-width:1.3}}
    .ic{{fill:none;stroke:#D6D6DE;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
    .dic{{fill:none;stroke:#6E8BFF;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
    .fic{{fill:#D6D6DE}} .dic-f{{fill:#6E8BFF}} .dot{{fill:#43E7C4}}
    @media(prefers-color-scheme:light){{.tile{{fill:rgba(0,0,0,0.015);stroke:rgba(0,0,0,0.11)}}.ic{{stroke:#33333B}}.fic{{fill:#33333B}}}}
    .g{{transform-box:fill-box;transform-origin:center;animation:pop .6s cubic-bezier(.2,.75,.25,1)}}
    @keyframes pop{{0%{{opacity:0;transform:scale(.9)}}100%{{opacity:1;transform:none}}}}
    @media(prefers-reduced-motion:reduce){{.g{{animation:none}}}}
  </style></defs>
  <g class="g"><rect x="9" y="9" width="46" height="46" rx="13" class="tile"/><circle cx="48" cy="16" r="1.8" class="dot"/>{glyph}</g>
</svg>
'''
slug={"Next.js":"nextjs","Node.js":"nodejs","PostgreSQL":"postgresql"}
for lbl,g in ENG+DES:
    fn=slug.get(lbl, lbl.lower())
    open(f"assets/icons/{fn}.svg","w").write(ICON.format(name=lbl,glyph=g(32,32)))
print("emitted", len(ENG+DES), "reusable icons to assets/icons/")
