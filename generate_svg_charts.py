#!/usr/bin/env python3
"""Generate SVG charts for AP Microeconomics lecture notes.

SVG offers resolution-independent, publication-grade typography for charts
dominated by text, rectangles, and simple geometry. One chart is generated
here; the rest remain in generate_charts.py (matplotlib).

Run: python generate_svg_charts.py
Output: charts/*.svg
"""
import os

OUT = 'charts'

# Color palette aligned with matplotlib charts (see generate_charts.py C dict)
C = {
    'D': '#2563EB', 'S': '#F97316', 'MC': '#059669', 'TEXT': '#334155',
    'MUTE': '#64748B', 'AXIS': '#1E293B', 'GRID': '#E2E8F0',
    'GREEN_BG': '#ECFDF5', 'RED_BG': '#FEF2F2', 'AMBER_BG': '#FFFBEB',
    'AMBER': '#D97706', 'BORDER': '#CBD5E1',
}


def write_svg(name, svg_body, width, height):
    """Wrap body in <svg> root and write to charts/<name>."""
    path = os.path.join(OUT, name)
    full = (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" '
        f'font-family="Microsoft YaHei, Noto Sans SC, Inter, sans-serif">\n'
        f'{svg_body}\n</svg>\n'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(full)
    print(f'  OK {name}')


# ═══════════════════════════════════════════════════════════════
# u4_game_theory.svg — 2x2 payoff matrix (prisoner's dilemma)
# ═══════════════════════════════════════════════════════════════
def u4_game_theory_svg():
    W, H = 760, 420
    # Layout
    x0, y0 = 140, 80         # top-left of matrix
    cw, ch = 280, 160        # cell width/height
    body = []

    # Title
    body.append(f'<text x="{W/2}" y="36" text-anchor="middle" font-size="20" '
                f'font-weight="800" fill="{C["TEXT"]}">Prisoner\'s Dilemma — Pricing Game</text>')

    # Column headers (Firm B)
    body.append(f'<text x="{x0 + cw/2}" y="{y0 - 18}" text-anchor="middle" '
                f'font-size="14" font-weight="700" fill="{C["S"]}">Firm B: High Price</text>')
    body.append(f'<text x="{x0 + 1.5*cw}" y="{y0 - 18}" text-anchor="middle" '
                f'font-size="14" font-weight="700" fill="{C["D"]}">Firm B: Low Price</text>')

    # Row headers (Firm A) — rotated
    body.append(f'<text x="{x0 - 60}" y="{y0 + ch/2}" text-anchor="middle" '
                f'font-size="14" font-weight="700" fill="{C["S"]}" '
                f'transform="rotate(-90 {x0 - 60} {y0 + ch/2})">Firm A: High Price</text>')
    body.append(f'<text x="{x0 - 60}" y="{y0 + 1.5*ch}" text-anchor="middle" '
                f'font-size="14" font-weight="700" fill="{C["D"]}" '
                f'transform="rotate(-90 {x0 - 60} {y0 + 1.5*ch})">Firm A: Low Price</text>')

    # Cells: (col, row, fill, A payoff, B payoff, note, border_color)
    cells = [
        (0, 0, C['GREEN_BG'], '$50', '$50', 'Cooperation', None),
        (1, 0, C['RED_BG'],   '$20', '$80', '',            None),
        (0, 1, C['RED_BG'],   '$80', '$20', '',            None),
        (1, 1, C['AMBER_BG'], '$30', '$30', 'Nash Equilibrium', C['AMBER']),
    ]
    for col, row, fill, a, b, note, border in cells:
        cx = x0 + col * cw
        cy = y0 + row * ch
        bw = 2 if border else 1.2
        bc = border or C['BORDER']
        body.append(f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" '
                    f'fill="{fill}" stroke="{bc}" stroke-width="{bw}" />')
        # Payoffs displayed horizontally: "A payoff, B payoff"
        body.append(f'<text x="{cx + cw/2}" y="{cy + ch/2 + 4}" text-anchor="middle" '
                    f'font-size="22" font-weight="800" fill="{C["TEXT"]}">{a}, {b}</text>')
        if note:
            ncolor = C['AMBER'] if 'Nash' in note else C['MUTE']
            body.append(f'<text x="{cx + cw/2}" y="{cy + ch - 14}" text-anchor="middle" '
                        f'font-size="11" font-weight="700" fill="{ncolor}">{note}</text>')

    write_svg('u4_game_theory.svg', '\n'.join(body), W, H)


# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    print('Generating SVG charts...')
    u4_game_theory_svg()
    print('Done! 1 SVG chart saved to', OUT + '/')
