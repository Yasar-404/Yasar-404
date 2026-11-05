"""One request travelling through every layer, followed by its distributed trace."""

from __future__ import annotations

from ..svg import EASE, MARGIN, WIDTH, Doc
from ..theme import Theme

HEIGHT = 500
LOOP = 12
NODE_W, NODE_H, NODE_GAP = 180, 176, 48
NODE_Y = 68
NODES = (
    ("DESIGN", "Figma, Framer", "tokens, prototypes"),
    ("CLIENT", "React, Next.js", "TypeScript, Tailwind"),
    ("SERVICES", "Python, Java", "Node.js, Go, REST"),
    ("DATA", "SQL, PostgreSQL", "schemas, indexes"),
)
# Span label, start and end as a fraction of the trace, depth.
SPANS = (
    ("GET /api/renewals", 0.00, 1.00, 0),
    ("auth.verifyToken", 0.03, 0.14, 1),
    ("RenewalService.findDue", 0.15, 0.82, 1),
    ("SELECT members JOIN attendance", 0.22, 0.62, 2),
    ("churn_risk.score", 0.64, 0.79, 2),
    ("render <RenewalTable/>", 0.84, 0.99, 1),
)


def _vignette(doc: Doc, index: int) -> str:
    """A tiny looping scene (140 x 60, origin at top left) showing the layer at work."""
    t = doc.theme
    if index == 0:  # A selected frame with a designer's cursor.
        handles = "".join(
            f'<rect x="{x - 2.5}" y="{y - 2.5}" width="5" height="5" fill="{t.bg}" '
            f'stroke="{t.accent}"/>'
            for x, y in ((14, 8), (100, 8), (14, 50), (100, 50))
        )
        return (
            f'<rect x="14" y="8" width="86" height="42" stroke="{t.accent}"/>'
            f'<rect x="24" y="18" width="40" height="5" rx="2.5" fill="{t.muted}"/>'
            f'<rect x="24" y="30" width="62" height="10" rx="3" fill="{t.iris}" opacity=".6"/>'
            f"{handles}"
            f'<path class="cur" d="M0 0 l0 13 l3.6 -3 l2.4 5.4 l2 -1 l-2.3 -5.2 l4.6 -.4 z" '
            f'fill="{t.ink}"/>'
        )
    if index == 1:  # Skeleton rows hydrating into content.
        rows = "".join(
            f'<rect x="10" y="{8 + i * 15}" width="120" height="8" rx="4" fill="{t.stroke}"/>'
            f'<rect class="fillbar" x="10" y="{8 + i * 15}" width="{w}" height="8" rx="4" '
            f'fill="{c}" style="animation-delay:{i * 0.35 + 1.2}s"/>'
            for i, (w, c) in enumerate(((120, t.accent), (84, t.iris), (104, t.mint)))
        )
        return rows
    if index == 2:  # Handlers lighting up in turn.
        cells = "".join(
            f'<rect x="{8 + i * 44}" y="10" width="36" height="36" rx="8" stroke="{t.faint}"/>'
            f'<rect class="svc" x="{8 + i * 44}" y="10" width="36" height="36" rx="8" '
            f'fill="{t.accent}" fill-opacity=".3" stroke="{t.accent}" '
            f'style="animation-delay:{2.5 + i * 0.6}s"/>'
            f'<circle cx="{26 + i * 44}" cy="28" r="3" fill="{t.ink}"/>'
            for i in range(3)
        )
        return cells
    rows = "".join(  # A table scan settling on the matching row.
        f'<line x1="10" y1="{8 + i * 12}" x2="130" y2="{8 + i * 12}" stroke="{t.stroke}"/>'
        for i in range(5)
    )
    columns = "".join(
        f'<line x1="{x}" y1="8" x2="{x}" y2="56" stroke="{t.stroke}"/>' for x in (10, 50, 90, 130)
    )
    return (
        f"{rows}{columns}"
        f'<rect class="scan" x="10" y="8" width="120" height="12" fill="{t.mint}" '
        f'fill-opacity=".35"/>'
    )


def render(theme: Theme) -> str:
    doc = Doc(
        theme,
        "Architecture: a request moves from design through client and services to data and back",
        HEIGHT,
    )
    t = theme
    xs = [MARGIN + i * (NODE_W + NODE_GAP) for i in range(4)]
    wire_y = NODE_Y + NODE_H / 2
    travel = xs[3] - xs[0]

    doc.style(
        f".req{{animation:req {LOOP}s linear infinite;offset-rotate:0deg}}"
        f"@keyframes req{{0%{{transform:translateX(0);opacity:1}}42%{{transform:translateX({travel}px);"
        f"opacity:1}}43%,100%{{transform:translateX({travel}px);opacity:0}}}}"
        f".res{{animation:res {LOOP}s linear infinite}}"
        f"@keyframes res{{0%,44%{{transform:translateX({travel}px);opacity:0}}"
        f"45%{{transform:translateX({travel}px);opacity:1}}"
        "85%{transform:translateX(0);opacity:1}86%,100%{transform:translateX(0);opacity:0}}"
        f".hit{{opacity:0;animation:hit {LOOP}s ease-out infinite}}"
        "@keyframes hit{0%{opacity:1}12%,100%{opacity:0}}"
        f".cur{{animation:cur {LOOP}s {EASE} infinite}}"
        "@keyframes cur{0%,100%{transform:translate(110px,44px)}"
        "20%,60%{transform:translate(76px,30px)}}"
        f".fillbar{{transform-box:fill-box;transform-origin:left;"
        f"animation:fillbar {LOOP}s {EASE} infinite}}"
        "@keyframes fillbar{0%{transform:scaleX(0)}10%,88%{transform:scaleX(1)}"
        "96%,100%{transform:scaleX(0)}}"
        f".svc{{opacity:0;animation:svc {LOOP}s ease-in-out infinite}}"
        "@keyframes svc{0%,14%{opacity:1}24%,100%{opacity:0}}"
        f".scan{{animation:scan {LOOP}s steps(1) infinite}}"
        "@keyframes scan{0%,30%{transform:translateY(0)}34%{transform:translateY(12px)}"
        "38%{transform:translateY(24px)}42%,70%{transform:translateY(12px)}"
        "74%,100%{transform:translateY(0)}}"
        f".span{{transform-box:fill-box;transform-origin:left;"
        f"animation:span {LOOP}s {EASE} infinite}}"
        "@keyframes span{0%,1%{transform:scaleX(0);opacity:1}"
        "100%{transform:scaleX(1);opacity:1}}",
        ".req,.res,.hit,.cur,.fillbar,.svc,.scan,.span{animation:none}"
        ".req,.res,.hit,.svc{opacity:0}",
    )
    # Per-span timings: each bar grows during its own slice of the first 80% of the loop.
    for i, (_, start, end, _) in enumerate(SPANS):
        a, b = 5 + start * 75, 5 + end * 75
        doc.style(
            f"@keyframes s{i}{{0%,{a:.1f}%{{transform:scaleX(0)}}{b:.1f}%,92%{{transform:scaleX(1)}}"
            f"97%,100%{{transform:scaleX(0)}}}}.s{i}{{animation-name:s{i}}}"
        )

    doc.add(doc.section_header("01", "ONE REQUEST, EVERY LAYER", "ANIMATED REFERENCE ARCHITECTURE"))
    doc.add(
        f'<line class="rule" x1="{xs[0] + NODE_W / 2}" y1="{wire_y}" '
        f'x2="{xs[3] + NODE_W / 2}" y2="{wire_y}"/>',
        f'<circle class="req" cx="{xs[0] + NODE_W / 2}" cy="{wire_y - 5}" r="3.5" '
        f'fill="{t.accent}"/>',
        f'<circle class="res" cx="{xs[0] + NODE_W / 2}" cy="{wire_y + 5}" r="3.5" fill="{t.mint}"/>',
    )
    for i, (title, line1, line2) in enumerate(NODES):
        x = xs[i]
        # Moments the request (going right) or the response (coming back) reach this node.
        hits = [i / 3 * 42] + ([45 + (3 - i) / 3 * 40] if i < 3 else [])
        pulses = "".join(
            f'<rect class="hit" x="{x}" y="{NODE_Y}" width="{NODE_W}" height="{NODE_H}" rx="12" '
            f'stroke="{t.accent if n == 0 else t.mint}" stroke-width="1.5" '
            f'style="animation-delay:{p / 100 * LOOP:.2f}s"/>'
            for n, p in enumerate(hits)
        )
        doc.add(
            f'<rect class="card" x="{x}" y="{NODE_Y}" width="{NODE_W}" height="{NODE_H}" rx="12"/>',
            pulses,
            doc.label_text(x + 18, NODE_Y + 28, title, "muted", size=11, track=2.4),
            f'<g transform="translate({x + 20} {NODE_Y + 42})">{_vignette(doc, i)}</g>',
            doc.text(x + 18, NODE_Y + 130, line1, "sans", 500, 14, "ink"),
            doc.text(x + 18, NODE_Y + 151, line2, "sans", 400, 13, "muted"),
        )

    # Trace waterfall.
    top = NODE_Y + NODE_H + 24
    label_w = 262
    track_x, track_w = MARGIN + 18 + label_w, WIDTH - 2 * MARGIN - 36 - label_w
    doc.add(
        f'<rect class="card" x="{MARGIN}" y="{top}" width="{WIDTH - 2 * MARGIN}" height="210" '
        'rx="12"/>',
        doc.label_text(MARGIN + 18, top + 28, "REQUEST TRACE", "muted", size=11, track=2.4),
        doc.label_text(WIDTH - MARGIN - 18, top + 28, "ILLUSTRATIVE", "faint", "end", 10, 1.6),
    )
    for i, (name, start, end, depth) in enumerate(SPANS):
        y = top + 54 + i * 25
        colour = (t.accent, t.iris, t.mint)[depth]
        doc.add(
            doc.text(
                MARGIN + 18 + depth * 14,
                y + 10,
                name,
                "mono",
                400,
                12,
                "ink" if depth == 0 else "muted",
            ),
            f'<rect x="{track_x}" y="{y}" width="{track_w}" height="12" rx="3" fill="{t.dot}"/>',
            f'<rect class="span s{i}" x="{track_x + start * track_w:.1f}" y="{y}" '
            f'width="{(end - start) * track_w:.1f}" height="12" rx="3" fill="{colour}"/>',
        )
    return doc.render()
