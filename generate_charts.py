#!/usr/bin/env python3
"""Generate all 38 PNG charts for AP Microeconomics lecture notes.
Style: classic textbook — white bg, arrow axes, smooth curves, precise intersections.
"""
import os, warnings, numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ═══════════════════════════════════════════════════════════════
# STYLE
# ═══════════════════════════════════════════════════════════════
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 11
plt.rcParams['figure.dpi'] = 800
plt.rcParams['savefig.dpi'] = 800
plt.rcParams['lines.solid_capstyle'] = 'round'
plt.rcParams['lines.solid_joinstyle'] = 'round'

OUT = 'charts'
DPI = 800
FIGSIZE = (7.2, 5.0)

C = {
    'D':'#2563EB','S':'#F97316','MC':'#059669','ATC':'#D97706','AVC':'#F59E0B',
    'AFC':'#94A3B8','MR':'#7C3AED','MRP':'#2563EB','MFC':'#F97316','MFCCURVE':'#B91C1C',
    'MSC':'#059669','MSB':'#2563EB','TP':'#059669','MP':'#DC2626','AP':'#2563EB',
    'AXIS':'#1E293B','TEXT':'#334155','MUTE':'#64748B','DASH':'#94A3B8',
    'ALERT':'#DC2626',
    'DWL':'#FCA5A5','DWL_TEXT':'#EF4444',
    'CS':'#DBEAFE','CS_TEXT':'#2563EB','PS':'#DCFCE7','PS_TEXT':'#16A34A',
    'TAX':'#F97316','PROFIT':'#10B981','LOSS':'#EF4444',
}
DASH = (5,3)
POINT_SIZE = 7.5
POINT_EDGE = 1.6
LABEL_OFFSET_SCALE = 18
AXIS_HEADROOM = 1.18
LABEL_FONTSIZE = 10

# ═══════════════════════════════════════════════════════════════
# UTILS
# ═══════════════════════════════════════════════════════════════

def expand_limits(lim, factor=AXIS_HEADROOM):
    lo, hi = lim
    return (lo, lo + (hi - lo) * factor)

def axis_with_headroom(xmax, ymax, xmin=0, ymin=0, factor=AXIS_HEADROOM):
    """Return axis limits with room beyond the plotted economic range."""
    return expand_limits((xmin, xmax), factor), expand_limits((ymin, ymax), factor)

def setup_axes(ax, xlabel='Quantity', ylabel='Price', xlim=(0,10), ylim=(0,10), add_headroom=True):
    """Draw arrow-style axes longer than the economic graph area."""
    if add_headroom:
        xlim = expand_limits(xlim)
        ylim = expand_limits(ylim)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.margins(x=0.03, y=0.04)
    for sp in ax.spines.values(): sp.set_visible(False)
    ax.set_xticks([]); ax.set_yticks([])
    # X axis arrow extends past plotted geometry; labels sit outside the graph area.
    x_arr = xlim[0] + (xlim[1]-xlim[0]) * 0.92
    ax.annotate('', xy=(x_arr, 0), xytext=(xlim[0]-0.3, 0),
                arrowprops=dict(arrowstyle='-|>', color=C['AXIS'], lw=1.5,
                                shrinkA=0, shrinkB=0))
    # Y axis arrow extends past plotted geometry.
    y_arr = ylim[0] + (ylim[1]-ylim[0]) * 0.92
    ax.annotate('', xy=(0, y_arr), xytext=(0, ylim[0]-0.3),
                arrowprops=dict(arrowstyle='-|>', color=C['AXIS'], lw=1.5,
                                shrinkA=0, shrinkB=0))
    ax.text(x_arr, ylim[0] - (ylim[1]-ylim[0])*0.055, xlabel,
            ha='right', va='top', fontsize=11, color=C['TEXT'])
    ax.text(xlim[0] - (xlim[1]-xlim[0])*0.04, y_arr, ylabel,
            ha='right', va='top', fontsize=11, color=C['TEXT'], rotation=90)

def save(fig, name):
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', UserWarning)
        try:
            fig.tight_layout(pad=0.8)
        except Exception:
            pass
    fig.savefig(os.path.join(OUT, name), dpi=DPI, bbox_inches='tight',
                facecolor='white', edgecolor='none', pad_inches=0.36)
    plt.close(fig); print(f'  OK {name}')

def intersect(f, g, qmin, qmax, n=2000):
    """Numerically find all q in (qmin, qmax) where f(q) == g(q).
    Returns a list of q values (linear interpolation between sign changes)."""
    q = np.linspace(qmin, qmax, n)
    diff = f(q) - g(q)
    roots = []
    for i in range(len(q)-1):
        if diff[i] == 0:
            roots.append(q[i])
        elif diff[i] * diff[i+1] < 0:
            # linear interpolation for the root
            q0, q1 = q[i], q[i+1]
            d0, d1 = diff[i], diff[i+1]
            roots.append(q0 - d0 * (q1 - q0) / (d1 - d0))
    return roots

def min_of(f, qmin, qmax, n=4000):
    """Return (q*, f(q*)) minimizing f over [qmin, qmax] by dense sampling."""
    q = np.linspace(qmin, qmax, n)
    vals = f(q)
    i = int(np.argmin(vals))
    return q[i], vals[i]

def point_on_curve(ax, f, q, color, label=None, dx=0.35, dy=0.35,
                   fontsize=LABEL_FONTSIZE, ha='left', va='bottom'):
    """Marker guaranteed on curve y=f(q); label offset in screen points."""
    y = f(q)
    return pt(ax, q, y, color, label, dx, dy, fontsize, ha, va)

def dashed_h(ax, y, x0=0, x1=None, color=None, label=None, lx=None, ly=None):
    if x1 is None: x1 = ax.get_xlim()[1] * 0.92
    ax.plot([x0, x1], [y, y], ls='--', color=color or C['DASH'], lw=1, zorder=2)
    if label:
        ax.text(lx if lx is not None else 0.3, ly if ly is not None else y + 0.15,
                label, fontsize=10, color=color or C['DASH'], ha='left', fontweight='bold')

def dashed_v(ax, x, y0=0, y1=None, color=None):
    if y1 is None: y1 = ax.get_ylim()[1] * 0.92
    ax.plot([x, x], [y0, y1], ls='--', color=color or C['DASH'], lw=1, zorder=2)

def pt(ax, x, y, color, label=None, dx=0.35, dy=0.35, fontsize=LABEL_FONTSIZE, ha='left', va='bottom'):
    """Draw a visible point and offset its label in screen points."""
    ax.plot(x, y, 'o', color=color, ms=POINT_SIZE, zorder=7,
            markeredgecolor='white', markeredgewidth=POINT_EDGE)
    if label:
        ox = dx * LABEL_OFFSET_SCALE
        oy = dy * LABEL_OFFSET_SCALE
        if ha == 'right' and ox > 0:
            ox = -ox
        if va == 'top' and oy > 0:
            oy = -oy
        ax.annotate(label, xy=(x, y), xytext=(ox, oy), textcoords='offset points',
                    fontsize=fontsize, color=color, fontweight='bold',
                    ha=ha, va=va, zorder=8,
                    bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.72))

def label_curve_end(ax, x, y, text, color, fontsize=LABEL_FONTSIZE, dx=10, dy=0, ha='left', va='center'):
    """Place a curve label near its end without sitting on top of the curve."""
    label_at(ax, x, y, text, color, dx=dx, dy=dy, fontsize=fontsize, ha=ha, va=va)

def label_at(ax, x, y, text, color, dx=8, dy=8, fontsize=LABEL_FONTSIZE, ha='left', va='bottom'):
    """Place a label near a data point using a fixed screen offset."""
    ax.annotate(text, xy=(x, y), xytext=(dx, dy), textcoords='offset points',
                fontsize=fontsize, color=color, fontweight='bold',
                ha=ha, va=va, zorder=8,
                bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.70))

def shade_rect(ax, x0, x1, y0, y1, color, alpha=0.18, zorder=1):
    ax.fill([x0, x1, x1, x0], [y0, y0, y1, y1],
            color=color, alpha=alpha, zorder=zorder)

def shade_poly(ax, points, color, alpha=0.14):
    xs, ys = zip(*points)
    ax.fill(xs, ys, color=color, alpha=alpha, zorder=1)

def price_label(ax, y, text, color=None, x0=0, x1=None):
    """Extend a price guide to the vertical axis and label it."""
    dashed_h(ax, y, x0, x1, color or C['DASH'])
    ax.text(-0.5, y, text, ha='right', va='center', fontsize=LABEL_FONTSIZE,
            color=color or C['MUTE'], fontweight='bold')

def q_label(ax, x, text='Q*', color=None):
    """Place a Q label just below the x-axis using screen offset."""
    ax.annotate(text, xy=(x, 0), xytext=(0, -18), textcoords='offset points',
                ha='center', va='top', fontsize=10, color=color or C['MUTE'],
                fontweight='bold', zorder=8)

def h_bracket(ax, x0, x1, y, text, color, dy=10):
    """Mark a horizontal quantity gap without implying an area."""
    # Background blur: semi-transparent white line behind arrow for visual separation
    ax.plot([x0, x1], [y, y], color='white', lw=7, alpha=0.7, zorder=2, solid_capstyle='round')
    ax.annotate('', xy=(x1, y), xytext=(x0, y),
                arrowprops=dict(arrowstyle='<|-|>', color=color, lw=1.6,
                                shrinkA=0, shrinkB=0), zorder=4)
    ax.annotate(text, xy=((x0+x1)/2, y), xytext=(0, dy), textcoords='offset points',
                ha='center', va='bottom', fontsize=10, color=color,
                fontweight='bold', zorder=8,
                bbox=dict(boxstyle='round,pad=0.16', fc='white', ec='none', alpha=0.75))

def arrow_bg(ax, x0, y0, x1, y1, lw=7, alpha=0.7):
    """Draw a semi-transparent white background behind a double arrow for visual separation."""
    ax.plot([x0, x1], [y0, y1], color='white', lw=lw, alpha=alpha,
            zorder=2, solid_capstyle='round')

# Cost function used across Unit 3 & 4. MC is derived from TVC, so it
# crosses AVC and ATC at their minimum points.
TFC = 8.0
_A = 0.35
_B = -2.6
_C = 8.0
def AVC(q): return _A*q**2 + _B*q + _C
def AFC(q): return TFC / q
def ATC(q): return AVC(q) + AFC(q)
def MC(q):  return 3*_A*q**2 + 2*_B*q + _C
Q_RANGE = np.linspace(1.0, 9.0, 400)
PC_YMAX = 16.0

# ═══════════════════════════════════════════════════════════════
# UNIT 0 — Exam Overview
# ═══════════════════════════════════════════════════════════════
# ═══════════════════════════════════════════════════════════════
# UNIT 1 — Basic Economic Concepts
# ═══════════════════════════════════════════════════════════════
def u1_ppc():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    ppc_max = 10
    x = np.linspace(0, ppc_max, 400)
    y = ppc_max*np.sqrt(np.maximum(0, 1-(x/ppc_max)**2))
    ax.plot(x, y, color=C['MC'], lw=2.5)
    ax.fill_between(x, 0, y, alpha=0.05, color=C['MC'])
    ya = ppc_max*np.sqrt(1-(3/ppc_max)**2)
    yb = ppc_max*np.sqrt(1-(7/ppc_max)**2)
    pt(ax, 3, ya, C['MC'], 'A (Efficient)', 0.4, 0.55)
    pt(ax, 7, yb, C['MC'], 'B (Efficient)', 0.55, 0.35)
    pt(ax, 4.4, 4.5, C['ALERT'], 'C (Inefficient)', 0.5, -0.45)
    pt(ax, 8.4, 8.4, C['MUTE'], 'D (Unattainable)', 0.55, 0.2)
    setup_axes(ax, 'Good X (Consumer Goods)', 'Good Y (Capital Goods)', (0, ppc_max), (0, ppc_max))
    save(fig, 'u1_ppc.png')

def u1_ppc_growth():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    ppc0, ppc1 = 10, 11.5
    x0 = np.linspace(0, ppc0, 400)
    x1 = np.linspace(0, ppc1, 400)
    y0 = ppc0*np.sqrt(np.maximum(0, 1-(x0/ppc0)**2))
    y1 = ppc1*np.sqrt(np.maximum(0, 1-(x1/ppc1)**2))
    ax.plot(x0, y0, color=C['MUTE'], lw=2, ls='--')
    ax.plot(x1, y1, color=C['MC'], lw=2.5)
    x_arrow0, x_arrow1 = 5.4, 6.35
    y_arrow0 = ppc0*np.sqrt(1-(x_arrow0/ppc0)**2)
    y_arrow1 = ppc1*np.sqrt(1-(x_arrow1/ppc1)**2)
    ax.annotate('', xy=(x_arrow1, y_arrow1), xytext=(x_arrow0, y_arrow0),
                arrowprops=dict(arrowstyle='-|>', color=C['ALERT'], lw=2))
    growth_label_y = (y_arrow0+y_arrow1)/2
    label_at(ax, (x_arrow0+x_arrow1)/2, growth_label_y, 'Growth', C['ALERT'], dx=-38, dy=0)
    ppc_label_y = ppc1*np.sqrt(1-(9.8/ppc1)**2)
    label_at(ax, (x_arrow0+x_arrow1)/2, ppc_label_y, 'PPC$_0$', C['MUTE'], dx=-10, dy=10)
    label_at(ax, 9.8, ppc_label_y, 'PPC$_1$', C['MC'], dx=10, dy=10)
    setup_axes(ax, 'Consumer Goods', 'Capital Goods', (0, ppc1), (0, ppc1))
    save(fig, 'u1_ppc_growth.png')

def u1_dim_mu():
    fig, ax = plt.subplots(figsize=(7.2, 5.0))
    qmax, mumax = 10, 8
    q = np.linspace(1, qmax, 300)
    mu = 7.2 / np.sqrt(q)
    ax.plot(q, mu, color=C['S'], lw=2.5)
    for qi in [1, 2.8, 4.6, 6.4, 8.2, 10]:
        pt(ax, qi, 7.2/np.sqrt(qi), C['S'], None)
    label_at(ax, qmax, 7.2/np.sqrt(qmax), 'MU', C['S'], dx=12, dy=14)
    setup_axes(ax, 'Quantity', 'Marginal Utility', (0, qmax), (0, mumax))
    save(fig, 'u1_dim_mu.png')

def u1_budget_ic():
    """Budget line + indifference curve + tangency (optimal consumption bundle)."""
    fig, ax = plt.subplots(figsize=(7.4, 5.8))
    Px, Py, I = 2.0, 1.5, 12.0
    x_max = I / Px   # 6.0
    y_max = I / Py   # 8.0
    x = np.linspace(0.01, x_max, 200)
    y_budget = (I - Px * x) / Py
    ax.plot(x, y_budget, color=C['D'], lw=2.5, label='Budget')
    x_star, y_star = 3.0, 4.0
    U_star = x_star * y_star          # 12
    U_hi   = U_star * 1.6             # 19.2
    U_lo   = U_star * 0.5             # 6.0
    # Left endpoints aligned on horizontal baseline y=y_max; right endpoints at x=x_max
    x_ic_star = np.linspace(U_star / y_max, x_max, 200)
    x_ic_hi   = np.linspace(U_hi   / y_max, x_max, 200)
    x_ic_lo   = np.linspace(U_lo   / y_max, x_max, 200)
    ax.plot(x_ic_hi,   U_hi   / x_ic_hi,   color=C['MC'], lw=1.3, ls='--', alpha=0.6)
    ax.plot(x_ic_star, U_star / x_ic_star, color=C['MC'], lw=2.5)
    ax.plot(x_ic_lo,   U_lo   / x_ic_lo,   color=C['MC'], lw=1.3, ls='--', alpha=0.6)
    pt(ax, x_star, y_star, C['ALERT'], 'Optimal bundle', 0.35, 0.4, fontsize=10)
    dashed_v(ax, x_star, 0, y_star, C['DASH'])
    ax.plot([0, x_star], [y_star, y_star], ls='--', color=C['DASH'], lw=1, zorder=2)
    q_label(ax, x_star, 'X*')
    ax.text(-0.4, y_star, 'Y*', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    # Labels at right endpoints of each curve (x = x_max)
    label_at(ax, x_max, U_hi   / x_max, 'IC$_{higher}$', C['MC'], dx=8, dy=0,  ha='left', fontsize=9)
    label_at(ax, x_max, U_star / x_max, 'IC*',           C['MC'], dx=8, dy=0,  ha='left')
    label_at(ax, x_max, U_lo   / x_max, 'IC$_{lower}$',  C['MC'], dx=8, dy=-4, ha='left', fontsize=9)
    label_at(ax, x_max, 0.0,              'Budget Line',   C['D'],  dx=8, dy=4,  ha='left')
    setup_axes(ax, 'Good X', 'Good Y', (0, 6.2), (0, 9))
    save(fig, 'u1_budget_ic.png')

# ═══════════════════════════════════════════════════════════════
# UNIT 2 — Supply and Demand
# ═══════════════════════════════════════════════════════════════
def u2_demand_move():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 100)
    d0 = 10 - x; d1 = 12.5 - x
    ax.plot(x, d0, color=C['D'], lw=2.5)
    ax.plot(x, d1, color=C['D'], lw=2.5, ls='--')
    label_curve_end(ax, 9.8, 10-9.8, 'D$_0$', C['D'], dx=12, dy=2, ha='left', va='center')
    label_curve_end(ax, 9.8, 12.5-9.8, 'D$_1$', C['D'], dx=12, dy=2, ha='left', va='center')
    ax.annotate('', xy=(5.8, 4.2), xytext=(3.8, 6.2),
                arrowprops=dict(arrowstyle='-|>', color=C['S'], lw=2))
    label_at(ax, 5.8, 4.2, 'Movement', C['S'], dx=-42, dy=-24, fontsize=10)
    x_shift0, x_shift1 = 5.6, 5.6
    ax.annotate('', xy=(x_shift1, 12.5-x_shift1), xytext=(x_shift0, 10-x_shift0),
                arrowprops=dict(arrowstyle='-|>', color=C['MC'], lw=2))
    label_at(ax, x_shift1, 12.5-x_shift1, 'Shift', C['MC'], dx=14, dy=12, fontsize=10)
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,13))
    save(fig, 'u2_demand_move.png')

def u2_supply_move():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 100)
    s0 = 1 + x; s1 = -1.5 + x
    ax.plot(x, s0, color=C['S'], lw=2.5)
    ax.plot(x, s1, color=C['S'], lw=2.5, ls='--')
    label_curve_end(ax, 10, s0[-1], 'S$_0$', C['S'], dy=12)
    label_curve_end(ax, 10, s1[-1], 'S$_1$', C['S'], dy=12)
    ax.annotate('', xy=(3.0, 4.0), xytext=(4.7, 5.7),
                arrowprops=dict(arrowstyle='-|>', color=C['D'], lw=2))
    label_at(ax, 3.0, 4.0, 'Movement', C['D'], dx=-18, dy=16, fontsize=10, ha='right')
    ax.annotate('', xy=(5.8, -1.5+5.8), xytext=(5.8, 1+5.8),
                arrowprops=dict(arrowstyle='-|>', color=C['MC'], lw=2))
    label_at(ax, 5.8, -1.5+5.8, 'Shift', C['MC'], dx=16, dy=-8, fontsize=10)
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,12))
    save(fig, 'u2_supply_move.png')

def u2_equilibrium():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 200)
    d = 10 - x; s = 1 + x
    ax.plot(x, d, color=C['D'], lw=2.5); ax.plot(x, s, color=C['S'], lw=2.5)
    label_curve_end(ax, 10, d[190], 'D', C['D'])
    label_curve_end(ax, 10, s[190], 'S', C['S'], dy=12)
    xe, ye = 4.5, 5.5
    pt(ax, xe, ye, C['MC'], None)
    label_at(ax, xe, ye, 'E (P$_e$, Q$_e$)', C['MC'], dx=18, dy=0, ha='left', va='center')
    dashed_v(ax, xe, 0, ye); dashed_h(ax, ye, 0, xe)
    q_label(ax, xe, 'Q$_e$')
    ax.text(-0.5, ye, 'P$_e$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    ph = 7.5
    ax.plot([0,10*0.92],[ph,ph], ls='--', color=C['TAX'], lw=1)
    ax.text(-0.5, ph, 'P$_{high}$', ha='right', va='center', color=C['TAX'], fontsize=LABEL_FONTSIZE, fontweight='bold')
    h_bracket(ax, 10-ph, ph-1, ph+0.45, 'Surplus', C['TAX'], dy=8)
    pl = 3.5
    ax.plot([0,10*0.92],[pl,pl], ls='--', color=C['D'], lw=1)
    ax.text(-0.5, pl, 'P$_{low}$', ha='right', va='center', color=C['D'], fontsize=LABEL_FONTSIZE, fontweight='bold')
    h_bracket(ax, pl-1, 10-pl, pl-0.45, 'Shortage', C['D'], dy=-22)
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u2_equilibrium.png')

def u2_demand_increase():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 200)
    d0 = 10 - x; d1 = 12.5 - x; s = 1 + x
    ax.plot(x, d0, color=C['D'], lw=2); ax.plot(x, d1, color=C['D'], lw=2.5)
    ax.plot(x, s, color=C['S'], lw=2.5)
    label_curve_end(ax, 10, d0[190], 'D$_0$', C['D'], fontsize=10)
    label_curve_end(ax, 10, d1[-1], 'D$_1$', C['D'], dy=-10)
    label_curve_end(ax, 10, s[190], 'S', C['S'], fontsize=10, dy=12)
    pt(ax, 4.5, 5.5, C['MUTE'], 'E$_0$', 0, 0.4, ha='center')
    pt(ax, 5.75, 6.75, C['MUTE'], 'E$_1$', 0, 0.4, ha='center')
    dashed_v(ax, 4.5, 0, 5.5, C['MUTE']); dashed_v(ax, 5.75, 0, 6.75, C['MUTE'])
    dashed_h(ax, 5.5, 0, 4.5, C['MUTE']); dashed_h(ax, 6.75, 0, 5.75, C['MUTE'])
    ax.text(-0.5, 5.5, 'P$_0$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    ax.text(-0.5, 6.75, 'P$_1$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, 4.5, 'Q$_0$')
    q_label(ax, 5.75, 'Q$_1$', C['MUTE'])
    ax.annotate('', xy=(5.75, 6.75), xytext=(4.5, 5.5),
                arrowprops=dict(arrowstyle='-|>', color=C['MUTE'], lw=2))
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,13.5))
    save(fig, 'u2_demand_increase.png')

def u2_supply_decrease():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 200)
    d = 10 - x; s0 = 1 + x; s1 = 3 + x
    ax.plot(x, d, color=C['D'], lw=2.5)
    ax.plot(x, s0, color=C['S'], lw=2); ax.plot(x, s1, color=C['S'], lw=2.5)
    label_curve_end(ax, 10, d[190], 'D', C['D'])
    label_curve_end(ax, 10, s0[190], 'S$_0$', C['S'], fontsize=10, dy=12)
    label_curve_end(ax, 10, s1[190], 'S$_1$', C['S'], dy=12)
    pt(ax, 4.5, 5.5, C['MUTE'], 'E$_0$', 0, 0.4, ha='center')
    pt(ax, 3.5, 6.5, C['MUTE'], 'E$_1$', 0, 0.4, ha='center')
    dashed_v(ax, 4.5, 0, 5.5, C['MUTE']); dashed_v(ax, 3.5, 0, 6.5, C['MUTE'])
    dashed_h(ax, 5.5, 0, 4.5, C['MUTE']); dashed_h(ax, 6.5, 0, 3.5, C['MUTE'])
    ax.text(-0.5, 5.5, 'P$_0$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    ax.text(-0.5, 6.5, 'P$_1$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, 4.5, 'Q$_0$')
    q_label(ax, 3.5, 'Q$_1$', C['MUTE'])
    ax.annotate('', xy=(3.5, 6.5), xytext=(4.5, 5.5),
                arrowprops=dict(arrowstyle='-|>', color=C['MUTE'], lw=2))
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u2_supply_decrease.png')

def u2_elasticity_five():
    fig, axes = plt.subplots(2, 3, figsize=(10, 6.5))
    titles = ['Perfectly Inelastic\nPED = 0', 'Relatively Inelastic\nPED < 1',
              'Unit Elastic\nPED = 1', 'Relatively Elastic\nPED > 1',
              'Perfectly Elastic\nPED = ∞', 'Total Revenue Test']
    x = np.linspace(0, 5, 100)
    curves = [
        ('v', None), ('iso', 0.5), ('iso', 1.0),
        ('iso', 2.0), ('h', None), ('text', None)
    ]
    for ax, title, (ctype, elasticity) in zip(axes.flat, titles, curves):
        ax.set_xlim(0,5); ax.set_ylim(0,5)
        for sp in ax.spines.values(): sp.set_visible(False)
        ax.set_xticks([]); ax.set_yticks([])
        ax.annotate('', xy=(5,0), xytext=(0,0), arrowprops=dict(arrowstyle='-|>',color=C['AXIS'],lw=1.2))
        ax.annotate('', xy=(0,5), xytext=(0,0), arrowprops=dict(arrowstyle='-|>',color=C['AXIS'],lw=1.2))
        if ctype == 'v': ax.plot([2.5,2.5],[0.3,4.7], color=C['D'], lw=3)
        elif ctype == 'iso':
            p_min = 0.8 if elasticity <= 1 else 1.85
            p = np.linspace(p_min, 4.6, 160)
            quantity = 2.5 * (2.5 / p) ** elasticity
            ax.plot(quantity, p, color=C['D'], lw=3)
        elif ctype == 'h': ax.plot([0.3,4.7],[3,3], color=C['D'], lw=3)
        elif ctype == 'text':
            ax.text(2.5, 4.2, 'TR Test', ha='center', fontsize=11, fontweight='bold', color=C['S'])
            ax.text(2.5, 3.3, 'Price and TR move together: Inelastic', ha='center', fontsize=9, color=C['TEXT'])
            ax.text(2.5, 2.6, 'Price and TR move opposite: Elastic', ha='center', fontsize=9, color=C['TEXT'])
            ax.text(2.5, 1.9, 'TR unchanged: Unit Elastic', ha='center', fontsize=9, color=C['TEXT'])
            ax.plot([1,4],[1.3,1.3], color='#BFDBFE', lw=0.8)
            ax.text(2.5, 0.9, 'Slope ≠ Elasticity', ha='center', fontsize=LABEL_FONTSIZE, color=C['MUTE'])
        ax.set_title(title, fontsize=LABEL_FONTSIZE, fontweight='bold', color=C['TEXT'], pad=4)
    fig.tight_layout(pad=1.0)
    save(fig, 'u2_elasticity_five.png')

def u2_price_ceiling():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 200)
    d = 10 - x; s = 1 + x
    ax.plot(x, d, color=C['D'], lw=2.5); ax.plot(x, s, color=C['S'], lw=2.5)
    label_curve_end(ax, 10, d[190], 'D', C['D'])
    label_curve_end(ax, 10, s[190], 'S', C['S'], dy=12)
    xe, ye = 4.5, 5.5
    pt(ax, xe, ye, C['MUTE'], 'E', 0, 0.4, ha='center')
    dashed_v(ax, xe, 0, ye, C['DASH'])
    dashed_h(ax, ye, 0, xe, C['DASH'])
    q_label(ax, xe, 'Q$_e$')
    ax.text(-0.5, ye, 'P$_e$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    pc = 3.5
    ax.plot([0, 10], [pc, pc], ls='--', color=C['D'], lw=1)
    ax.text(-0.5, pc, 'P$_c$', ha='right', va='center', color=C['D'], fontsize=10, fontweight='bold')
    xs = pc - 1; xd = 10 - pc
    h_bracket(ax, xs, xd, pc + 0.45, 'Shortage', C['D'], dy=8)
    dashed_v(ax, xs, 0, pc, C['D']); dashed_v(ax, xd, 0, pc, C['D'])
    q_label(ax, xs, 'Q$_s$', C['D']); q_label(ax, xd, 'Q$_d$', C['D'])
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u2_price_ceiling.png')

def u2_price_floor():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 200)
    d = 10 - x; s = 1 + x
    ax.plot(x, d, color=C['D'], lw=2.5); ax.plot(x, s, color=C['S'], lw=2.5)
    label_curve_end(ax, 10, d[190], 'D', C['D'])
    label_curve_end(ax, 10, s[190], 'S', C['S'], dy=12)
    xe, ye = 4.5, 5.5
    pt(ax, xe, ye, C['MUTE'], 'E', 0, 0.4, ha='center')
    dashed_v(ax, xe, 0, ye, C['DASH'])
    dashed_h(ax, ye, 0, xe, C['DASH'])
    q_label(ax, xe, 'Q$_e$')
    ax.text(-0.5, ye, 'P$_e$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    pf = 7.5
    ax.plot([0, 10], [pf, pf], ls='--', color=C['TAX'], lw=1)
    ax.text(-0.5, pf, 'P$_f$', ha='right', va='center', color=C['TAX'], fontsize=10, fontweight='bold')
    xd = 10 - pf; xs = pf - 1
    h_bracket(ax, xd, xs, pf + 0.45, 'Surplus', C['TAX'], dy=8)
    dashed_v(ax, xd, 0, pf, C['TAX']); dashed_v(ax, xs, 0, pf, C['TAX'])
    q_label(ax, xd, 'Q$_d$', C['TAX']); q_label(ax, xs, 'Q$_s$', C['TAX'])
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u2_price_floor.png')

def u2_tax_incidence():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 200)
    d = 10 - x; s = 1 + x; s_tax = 3 + x
    ax.plot(x, d, color=C['D'], lw=2.5)
    ax.plot(x, s, color=C['S'], lw=2.5)
    ax.plot(x, s_tax, color=C['S'], lw=2, ls='--')
    label_curve_end(ax, 10, d[190], 'D', C['D'], dy=0)
    label_curve_end(ax, 10, s[190], 'S$_0$', C['S'], dy=12)
    label_curve_end(ax, 10, s_tax[190], 'S + Tax', C['S'], fontsize=10, dy=10)
    e0_q, e0_p = 4.5, 5.5
    pt(ax, e0_q, e0_p, C['MUTE'], 'E$_0$', 0, 0.4, ha='center')
    dashed_v(ax, e0_q, 0, e0_p, C['DASH'])
    q_label(ax, e0_q, 'Q$_e$')
    pc = 6.5; pp = 4.5; qt = 3.5
    dashed_v(ax, qt, 0, pc, C['DASH'])
    price_label(ax, pc, 'P$_c$', C['D'], 0, qt)
    price_label(ax, pp, 'P$_p$', C['S'], 0, qt)
    price_label(ax, e0_p, 'P$_e$', C['MUTE'], 0, e0_q)
    pt(ax, qt, pc, C['D'], 'E$_1$', 0, 0.4, ha='center')
    pt(ax, qt, pp, C['S'], None)
    shade_poly(ax, [(qt, pc), (qt, pp), (e0_q, e0_p)], C['DWL'])
    ax.text((qt + e0_q)/2 - 0.15, e0_p, 'DWL',
            ha='center', va='center', fontsize=9, color=C['DWL_TEXT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.72))
    arrow_bg(ax, qt-0.45, pp, qt-0.45, pc)
    ax.annotate('', xy=(qt-0.45, pc), xytext=(qt-0.45, pp),
                arrowprops=dict(arrowstyle='<|-|>', color=C['TAX'], lw=1.5), zorder=4)
    label_at(ax, qt-0.8, (pc+pp)/2, 'Tax', C['TAX'], dx=0, dy=0, fontsize=LABEL_FONTSIZE, ha='right', va='center')
    q_label(ax, qt, 'Q$_t$')
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u2_tax_incidence.png')

def u2_subsidy():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 200)
    d = 10 - x; s = 1 + x; s_sub = -1 + x
    ax.plot(x, d, color=C['D'], lw=2.5)
    ax.plot(x, s, color=C['S'], lw=2.5)
    ax.plot(x, s_sub, color=C['S'], lw=2, ls='--')
    label_curve_end(ax, 10, d[190], 'D', C['D'], dy=4)
    label_curve_end(ax, 10, s[190], 'S$_0$', C['S'], dy=10)
    label_curve_end(ax, 10, s_sub[190], 'S + Sub', C['S'], fontsize=10, dy=10)
    e0_q, e0_p = 4.5, 5.5
    q1 = 5.5
    pc = 4.5
    pp = 6.5
    pt(ax, e0_q, e0_p, C['MUTE'], 'E$_0$', 0, 0.4, ha='center')
    dashed_v(ax, e0_q, 0, e0_p, C['DASH'])
    q_label(ax, e0_q, 'Q$_e$')
    pt(ax, q1, pc, C['D'], 'E$_1$', 0, 0.4, ha='center')
    pt(ax, q1, pp, C['S'], None)
    dashed_v(ax, q1, 0, pp, C['DASH'])
    price_label(ax, pc, 'P$_c$', C['D'], 0, q1)
    price_label(ax, pp, 'P$_p$', C['S'], 0, q1)
    price_label(ax, e0_p, 'P$_e$', C['MUTE'], 0, q1)
    q_label(ax, q1, 'Q$_1$')
    shade_poly(ax, [(e0_q, e0_p), (q1, pp), (q1, pc)], C['DWL'])
    ax.text(5.0, e0_p, 'DWL',
            ha='center', va='center', fontsize=9, color=C['DWL_TEXT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.72))
    arrow_bg(ax, q1+0.45, pc, q1+0.45, pp)
    ax.annotate('', xy=(q1+0.45, pp), xytext=(q1+0.45, pc),
                arrowprops=dict(arrowstyle='<|-|>', color=C['TAX'], lw=1.5), zorder=4)
    label_at(ax, q1+0.7, (pc+pp)/2, 'Subsidy', C['TAX'], dx=0, dy=0, fontsize=LABEL_FONTSIZE, ha='left', va='center')
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u2_subsidy.png')

def u2_cs_ps():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    x = np.linspace(0, 10, 200)
    d = 10 - x
    s = 1 + x
    qe, pe = 4.5, 5.5
    ax.plot(x, d, color=C['D'], lw=2.5)
    ax.plot(x, s, color=C['S'], lw=2.5)
    ax.plot([0, qe], [pe, pe], color=C['DASH'], lw=1.2, ls='--')
    shade_poly(ax, [(0, 10), (0, pe), (qe, pe)], C['CS'], alpha=0.78)
    shade_poly(ax, [(0, 1), (0, pe), (qe, pe)], C['PS'], alpha=0.78)
    pt(ax, qe, pe, C['MC'], 'E', 0, 0.4, ha='center', fontsize=10)
    dashed_v(ax, qe, 0, pe, C['DASH'])
    q_label(ax, qe, 'Q$_e$')
    ax.text(-0.5, pe, 'P$_e$', ha='right', va='center', fontsize=10,
            color=C['MUTE'], fontweight='bold')
    label_curve_end(ax, 10, d[-1], 'D', C['D'], dy=20)
    label_curve_end(ax, 10, s[-1], 'S', C['S'], dy=8)
    ax.text(2.0, 6.5, 'CS', ha='center', va='center', fontsize=12, color=C['CS_TEXT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.72))
    ax.text(2.0, 4.5, 'PS', ha='center', va='center', fontsize=12, color=C['PS_TEXT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.72))
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u2_cs_ps.png')

def u2_tariff():
    """Tariff in an importing country: domestic price rises to Pw+t, CS↓ PS↑ Gov Rev↑ DWL>0."""
    fig, ax = plt.subplots(figsize=(8.0, 6.0))
    x = np.linspace(0, 10, 200)
    d = 10 - x          # domestic demand
    s = 1 + x           # domestic supply
    xe, ye = 4.5, 5.5   # autarky equilibrium (no-trade)
    pw = 3.5            # world price (below autarky → importing country)
    t = 1.5             # tariff
    pt_eff = pw + t     # domestic price after tariff = 5.0
    # Quantities at Pw (free trade): Qs = Pw-1=2.5, Qd = 10-Pw=6.5, import=4
    qs_free = pw - 1
    qd_free = 10 - pw
    # Quantities at Pw+t (after tariff): Qs = 4, Qd = 5, import=1
    qs_tar = pt_eff - 1
    qd_tar = 10 - pt_eff
    # Plot curves
    ax.plot(x, d, color=C['D'], lw=2.5)
    ax.plot(x, s, color=C['S'], lw=2.5)
    label_curve_end(ax, 10, d[-1], 'D', C['D'], fontsize=10, dy=12)
    label_curve_end(ax, 10, s[-1], 'S', C['S'], fontsize=10, dy=12)
    # World price line
    ax.plot([0, 10], [pw, pw], ls='--', color=C['MUTE'], lw=1)
    ax.text(-0.5, pw, 'P$_w$', ha='right', va='center', color=C['MUTE'], fontsize=9, fontweight='bold')
    # Tariff price line
    ax.plot([0, 10], [pt_eff, pt_eff], ls='-', color=C['TAX'], lw=1.8)
    ax.text(-0.5, pt_eff, 'P$_w$ + T', ha='right', va='center', color=C['TAX'], fontsize=9, fontweight='bold')
    # Free-trade quantities (dashed)
    dashed_v(ax, qs_free, 0, pw, C['DASH'])
    dashed_v(ax, qd_free, 0, pw, C['DASH'])
    q_label(ax, qs_free, 'Q$_s^0$')
    q_label(ax, qd_free, 'Q$_d^0$')
    # Tariff quantities
    dashed_v(ax, qs_tar, 0, pt_eff, C['TAX'])
    dashed_v(ax, qd_tar, 0, pt_eff, C['TAX'])
    q_label(ax, qs_tar, 'Q$_s^t$')
    q_label(ax, qd_tar, 'Q$_d^t$')
    # Gov revenue rectangle: width = import after tariff = qd_tar - qs_tar, height = t
    shade_rect(ax, qs_tar, qd_tar, pw, pt_eff, C['TAX'], alpha=0.32)
    label_at(ax, (qs_tar+qd_tar)/2, pw + t/2, 'Gov\nRevenue', C['TAX'],
             dx=0, dy=-14, fontsize=10, ha='center')
    # DWL triangles: production distortion (between S and Pw from qs_free to qs_tar)
    shade_poly(ax, [(qs_free, pw), (qs_tar, pt_eff), (qs_tar, pw)], C['DWL'])
    # Consumption distortion (between D and Pw from qd_tar to qd_free)
    shade_poly(ax, [(qd_tar, pt_eff), (qd_free, pw), (qd_tar, pw)], C['DWL'])
    label_at(ax, (qs_free+qs_tar)/2, pw + t/2, 'DWL', C['DWL_TEXT'],
             dx=10, dy=-14, fontsize=9, ha='center')
    label_at(ax, (qd_tar+qd_free)/2, pw + t/2, 'DWL', C['DWL_TEXT'],
             dx=-10, dy=-14, fontsize=9, ha='center')
    # Bracket import quantity after tariff
    h_bracket(ax, qs_tar, qd_tar, pw - 0.45, 'Import', C['MUTE'], dy=-22)
    setup_axes(ax, 'Quantity', 'Price', (0, 11), (0, 11))
    save(fig, 'u2_tariff.png')

def u2_quota():
    """Import quota: same price effect as tariff but no gov revenue; quota rent instead."""
    fig, ax = plt.subplots(figsize=(8.0, 6.0))
    x = np.linspace(0, 10, 200)
    d = 10 - x
    s = 1 + x
    pw = 3.5
    # Quota restricts import to Q_quota = 1.5 → find price where Qd - Qs = 1.5
    # (10 - P) - (P - 1) = 1.5 → 11 - 2P = 1.5 → P = 4.75
    pq = 4.75
    qs_q = pq - 1   # 3.75
    qd_q = 10 - pq  # 5.25
    import_after = qd_q - qs_q  # 1.5
    ax.plot(x, d, color=C['D'], lw=2.5)
    ax.plot(x, s, color=C['S'], lw=2.5)
    label_curve_end(ax, 10, d[-1], 'D', C['D'], fontsize=10, dy=12)
    label_curve_end(ax, 10, s[-1], 'S', C['S'], fontsize=10, dy=12)
    # World price
    ax.plot([0, 10], [pw, pw], ls='--', color=C['MUTE'], lw=1)
    ax.text(-0.5, pw, 'P$_w$', ha='right', va='center', color=C['MUTE'], fontsize=10, fontweight='bold')
    # Quota price
    ax.plot([0, 10], [pq, pq], ls='-', color=C['MR'], lw=1.8)
    ax.text(-0.5, pq, 'P$_q$', ha='right', va='center', color=C['MR'], fontsize=9, fontweight='bold')
    # Free-trade Qs/Qd
    qs_free = pw - 1; qd_free = 10 - pw
    dashed_v(ax, qs_free, 0, pw, C['DASH'])
    dashed_v(ax, qd_free, 0, pw, C['DASH'])
    q_label(ax, qs_free, 'Q$_s^0$')
    q_label(ax, qd_free, 'Q$_d^0$')
    # Quota Qs/Qd
    dashed_v(ax, qs_q, 0, pq, C['MR'])
    dashed_v(ax, qd_q, 0, pq, C['MR'])
    q_label(ax, qs_q, 'Q$_s^q$')
    q_label(ax, qd_q, 'Q$_d^q$')
    # Quota rent rectangle: width = import_after, height = pq - pw
    shade_rect(ax, qs_q, qd_q, pw, pq, C['MR'], alpha=0.32)
    label_at(ax, (qs_q+qd_q)/2, pw + (pq-pw)/2, 'Quota\nRent', C['MR'],
             dx=0, dy=-14, fontsize=10, ha='center')
    # DWL triangles (same shape as tariff)
    shade_poly(ax, [(qs_free, pw), (qs_q, pq), (qs_q, pw)], C['DWL'])
    shade_poly(ax, [(qd_q, pq), (qd_free, pw), (qd_q, pw)], C['DWL'])
    label_at(ax, (qs_free+qs_q)/2, pw + (pq-pw)/2, 'DWL', C['DWL_TEXT'],
             dx=10, dy=-14, fontsize=9, ha='center')
    label_at(ax, (qd_q+qd_free)/2, pw + (pq-pw)/2, 'DWL', C['DWL_TEXT'],
             dx=-10, dy=-14, fontsize=9, ha='center')
    h_bracket(ax, qs_q, qd_q, pw - 0.45, 'Import', C['MUTE'], dy=-22)
    setup_axes(ax, 'Quantity', 'Price', (0, 11), (0, 11))
    save(fig, 'u2_quota.png')

# ═══════════════════════════════════════════════════════════════
# UNIT 3 — Production, Cost & Perfect Competition
# ═══════════════════════════════════════════════════════════════
def u3_tp_mp_ap():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    L = np.linspace(0.2, 8, 300)
    TP = -L**3 + 12*L**2
    MP = -3*L**2 + 24*L
    AP = -L**2 + 12*L
    ax.plot(L, TP/8, color=C['TP'], lw=2.5)
    ax.plot(L, MP, color=C['MP'], lw=2.5)
    ax.plot(L, AP, color=C['AP'], lw=2.5)
    pt(ax, 6, 36, C['MUTE'], 'MP=AP', 0.4, 0.3)
    label_curve_end(ax, 8, TP[-1]/8, 'TP', C['TP'], dx=10, dy=-8)
    label_curve_end(ax, 8, MP[-1], 'MP', C['MP'], dx=10, dy=10)
    label_curve_end(ax, 8, AP[-1], 'AP', C['AP'], dx=10, dy=18)
    setup_axes(ax, 'Labor', 'Output', (0,9), (0,55))
    save(fig, 'u3_tp_mp_ap.png')

def u3_total_cost():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    q = np.linspace(0.1, 10, 300)
    tfc_val = 50
    tvc = q**3/20 - 0.8*q**2 + 10*q
    tc = tfc_val + tvc
    ax.plot(q, np.full_like(q, tfc_val), color=C['AFC'], lw=2.5)
    ax.plot(q, tvc, color=C['AVC'], lw=2.5)
    ax.plot(q, tc, color=C['D'], lw=2.5)
    label_curve_end(ax, 10, tfc_val, 'TFC', C['AFC'])
    label_curve_end(ax, 10, tvc[-1], 'TVC', C['AVC'])
    label_curve_end(ax, 10, tc[-1], 'TC', C['D'])
    qi = 7
    arrow_bg(ax, qi, tvc[int(qi/10*299)], qi, tfc_val+tvc[int(qi/10*299)])
    ax.annotate('', xy=(qi, tfc_val+tvc[int(qi/10*299)]), xytext=(qi, tvc[int(qi/10*299)]),
                arrowprops=dict(arrowstyle='<|-|>', color=C['MUTE'], lw=1.2), zorder=4)
    ax.text(qi+0.4, tvc[int(qi/10*299)]+25, 'TFC', color=C['MUTE'], fontsize=10, fontweight='bold')
    setup_axes(ax, 'Quantity', 'Cost', (0,11.5), (0, max(tc)*1.1))
    save(fig, 'u3_total_cost.png')

def u3_unit_cost():
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    q = Q_RANGE
    # Local cost overrides: raise ATC significantly (higher TFC) and AVC slightly (higher _C)
    _TFC_loc = 20.0
    _A_loc, _B_loc, _C_loc = 0.35, -2.6, 9.0
    def AVC_loc(q): return _A_loc*q**2 + _B_loc*q + _C_loc
    def AFC_loc(q): return _TFC_loc / q
    def ATC_loc(q): return AVC_loc(q) + AFC_loc(q)
    def MC_loc(q):  return 3*_A_loc*q**2 + 2*_B_loc*q + _C_loc
    avc = AVC_loc(q); afc = AFC_loc(q); atc = ATC_loc(q); mc = MC_loc(q)
    ax.plot(q, afc, color=C['AFC'], lw=2)
    ax.plot(q, avc, color=C['AVC'], lw=2.5)
    ax.plot(q, atc, color=C['ATC'], lw=2.5)
    ax.plot(q, mc, color=C['MC'], lw=2.5)
    q_avc_min = q[np.argmin(avc)]
    q_atc_min = q[np.argmin(atc)]
    pt(ax, q_avc_min, AVC_loc(q_avc_min), C['AVC'], None)
    pt(ax, q_atc_min, ATC_loc(q_atc_min), C['ATC'], None)
    label_curve_end(ax, 9.0, MC_loc(9.0), 'MC', C['MC'], dx=10, dy=0)
    label_curve_end(ax, 9.0, ATC_loc(9.0), 'ATC', C['ATC'], dx=10, dy=18)
    label_curve_end(ax, 9.0, AVC_loc(9.0), 'AVC', C['AVC'], dx=10, dy=-18)
    label_curve_end(ax, 9.0, AFC_loc(9.0), 'AFC', C['AFC'], dx=10, dy=10)
    setup_axes(ax, 'Quantity', 'Cost', (0,10.5), (0, 50))
    save(fig, 'u3_unit_cost.png')

def u3_lratc():
    fig, ax = plt.subplots(figsize=(7.4, 5.3))
    q = np.linspace(1.0, 11.2, 400)
    lratc = 0.85 + 0.04*(q-6.1)**2
    centers = [2.4, 4.3, 6.1, 7.9, 9.8]
    for i, center in enumerate(centers, start=1):
        base = 0.85 + 0.04*(center-6.1)**2
        xx = np.linspace(center-1.7, center+1.7, 160)
        yy = base + 0.08*(center-6.1)*(xx-center) + 0.30*(xx-center)**2
        ax.plot(xx, yy, color=C['MUTE'], lw=1.35, ls='--')
        ax.text(center, base+0.85, f'SRATC$_{i}$', color=C['MUTE'], fontsize=LABEL_FONTSIZE, ha='center')
        pt(ax, center, base, C['MR'], None)
    ax.plot(q, lratc, color=C['MR'], lw=3)
    label_at(ax, 10.8, 0.85 + 0.04*(10.8-6.1)**2, 'LRATC', C['MR'], dx=18, dy=8)
    ax.text(2.4, 2.9, 'Economies\nof Scale', color=C['MC'], fontsize=LABEL_FONTSIZE, fontweight='bold', ha='center')
    ax.text(6.1, 2.9, 'Minimum LRATC\nEfficient Scale', color=C['TEXT'], fontsize=LABEL_FONTSIZE, fontweight='bold', ha='center')
    ax.text(9.6, 2.9, 'Diseconomies\nof Scale', color=C['ALERT'], fontsize=LABEL_FONTSIZE, fontweight='bold', ha='center')
    setup_axes(ax, 'Quantity', 'Cost', (0,12), (0,4.2))
    save(fig, 'u3_lratc.png')

def _pc_market(ax, price=7, title='Market', ymax=PC_YMAX):
    """Draw the market supply/demand panel for perfect competition."""
    qe = 5.0
    # Adaptive slope: gentler curves for elasticity, fitted to axis bounds
    max_m = min(price / qe, (ymax - price) / qe) * 0.9
    m = min(0.7, max_m)
    m = max(m, 0.25)
    x = np.linspace(0, 10, 200)
    d = price + m * (qe - x)
    s = price + m * (x - qe)
    d_clipped = np.where(d >= 0, d, np.nan)
    s_clipped = np.where(s >= 0, s, np.nan)
    ax.plot(x, d_clipped, color=C['D'], lw=2.2)
    ax.plot(x, s_clipped, color=C['S'], lw=2.2)
    pt(ax, qe, price, C['MC'], 'E', 0, 0.4, ha='center')
    dashed_h(ax, price, 0, 10.0, C['DASH'])
    dashed_v(ax, qe, 0, price, C['DASH'])
    q_label(ax, qe, 'Q$_M$')
    ax.text(-0.5, price, 'P$_M$', ha='right', va='center', fontsize=LABEL_FONTSIZE,
            color=C['MUTE'], fontweight='bold')
    label_curve_end(ax, 10, price + m * (qe - 10), 'D', C['D'], dy=0)
    label_curve_end(ax, 10, price + m * (10 - qe), 'S', C['S'], dy=0)
    ax.set_title(title, fontsize=11, fontweight='bold', color=C['TEXT'])
    setup_axes(ax, 'Quantity', 'Price', (0, 12), (0, ymax), add_headroom=False)

def _pc_qstar(P):
    vals = MC(Q_RANGE) - P
    idx = np.where(np.diff(np.sign(vals)) != 0)[0]
    candidates = []
    for i in idx:
        x0, x1 = Q_RANGE[i], Q_RANGE[i+1]
        y0, y1 = vals[i], vals[i+1]
        candidates.append(x0 - y0*(x1-x0)/(y1-y0))
    return max(candidates) if candidates else Q_RANGE[len(Q_RANGE)//2]

def _draw_pc_firm_chart(ax, P, title, ymax=PC_YMAX,
                         show_profit=False, show_loss=False,
                         show_shutdown=False, atc_func=None, show_qstar=True):
    """Draw a single firm cost-curve chart for perfect competition short-run analysis."""
    q = Q_RANGE
    _atc = atc_func if atc_func else ATC

    # Cost curves
    ax.plot(q, MC(q), color=C['MC'], lw=2.5)
    ax.plot(q, _atc(q), color=C['ATC'], lw=2.5)
    ax.plot(q, AVC(q), color=C['AVC'], lw=2)

    # MR = D = AR = P horizontal line (right end aligns with ATC/AVC curve endpoints at q=9)
    ax.plot([0, 9.0], [P, P], color=C['D'], lw=2.5)
    label_curve_end(ax, 9.0, P, 'MR = D = AR = P', C['D'], dx=10, dy=0)

    # Curve end labels (right side)
    label_curve_end(ax, 9.0, _atc(9.0), 'ATC', C['ATC'], dx=10, dy=14)
    label_curve_end(ax, 9.0, AVC(9.0), 'AVC', C['AVC'], dx=10, dy=-8)
    # MC label at the rightmost visible point on the curve
    mc_vis = q[MC(q) <= ymax]
    mc_lq = mc_vis[-1] if len(mc_vis) > 0 else q[-1]
    label_at(ax, mc_lq, MC(mc_lq), 'MC', C['MC'], dx=10, dy=0, ha='left')

    # Find Q* where MC = P (MR = MC rule)
    qstar = _pc_qstar(P)

    if show_qstar:
        # Vertical dashed line at Q* up to P
        dashed_v(ax, qstar, 0, P, C['DASH'])
        q_label(ax, qstar, 'Q*')

    # Mark MR = MC intersection
    pt(ax, qstar, P, C['MC'], None)

    if show_profit:
        atc_q = _atc(qstar)
        pt(ax, qstar, atc_q, C['ATC'], None)
        shade_rect(ax, 0, qstar, atc_q, P, C['PROFIT'])
        ax.text(qstar * 0.5, (P + atc_q) / 2, 'Profit', ha='center', va='center',
                fontsize=11, color=C['PROFIT'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.75))

    if show_loss:
        atc_q = _atc(qstar)
        pt(ax, qstar, P, C['D'], None)
        pt(ax, qstar, atc_q, C['ATC'], None)
        shade_rect(ax, 0, qstar, P, atc_q, C['LOSS'], alpha=0.20, zorder=0)
        ax.text(qstar * 0.5, (P + atc_q) / 2, 'Loss', ha='center', va='center',
                fontsize=11, color=C['LOSS'], fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.75))

    if show_shutdown:
        pt(ax, qstar, P, C['D'], None, 0.4, 0.5)

    ax.set_title(title, fontsize=12, fontweight='bold', color=C['TEXT'])
    return qstar

def u3_pc_profit():
    fig, (ax_m, ax) = plt.subplots(1, 2, figsize=(11.2, 5.4))
    P = 9.0
    _pc_market(ax_m, P, ymax=PC_YMAX)
    _draw_pc_firm_chart(ax, P, 'Firm', ymax=PC_YMAX, show_profit=True)
    setup_axes(ax, 'Quantity', 'Price', (0, 10.5), (0, PC_YMAX), add_headroom=False)
    save(fig, 'u3_pc_profit.png')

def u3_pc_loss():
    fig, (ax_m, ax) = plt.subplots(1, 2, figsize=(11.2, 5.4))
    P = 3.6
    local_TFC = 14.0
    def ATC_loss(q): return AVC(q) + local_TFC / q
    _pc_market(ax_m, P, ymax=18)
    _draw_pc_firm_chart(ax, P, 'Firm', ymax=18, show_loss=True, atc_func=ATC_loss)
    setup_axes(ax, 'Quantity', 'Price', (0, 10.5), (0, 18), add_headroom=False)
    save(fig, 'u3_pc_loss.png')

def u3_pc_shutdown():
    fig, (ax_m, ax) = plt.subplots(1, 2, figsize=(11.2, 5.4))
    q_min_avc = Q_RANGE[np.argmin(AVC(Q_RANGE))]
    P = AVC(q_min_avc)
    _pc_market(ax_m, P, ymax=PC_YMAX)
    _draw_pc_firm_chart(ax, P, 'Firm', ymax=PC_YMAX, show_shutdown=True)
    setup_axes(ax, 'Quantity', 'Price', (0, 10.5), (0, PC_YMAX), add_headroom=False)
    save(fig, 'u3_pc_shutdown.png')

def u3_pc_lr_equilibrium():
    fig, (ax_m, ax) = plt.subplots(1, 2, figsize=(11.2, 5.4))
    q_min = Q_RANGE[np.argmin(ATC(Q_RANGE))]
    P = ATC(q_min)
    _pc_market(ax_m, P, ymax=PC_YMAX)
    _draw_pc_firm_chart(ax, P, 'Firm', ymax=PC_YMAX, show_qstar=False)
    # Add LR equilibrium point
    pt(ax, q_min, P, C['D'], None)
    dashed_v(ax, q_min, 0, P, C['DASH'])
    q_label(ax, q_min, 'Q$_{LR}$')
    setup_axes(ax, 'Quantity', 'Price', (0,10.5), (0,PC_YMAX), add_headroom=False)
    save(fig, 'u3_pc_lr_equilibrium.png')

# ═══════════════════════════════════════════════════════════════
# UNIT 4 — Imperfect Competition
# ═══════════════════════════════════════════════════════════════
def u4_monopoly():
    fig, ax = plt.subplots(figsize=(7.8, 6.0))
    q = np.linspace(0, 10, 300)
    qc = np.linspace(1.0, 10, 280)
    d = 10 - q; mr = 10 - 2*q; mc = 1 + 0.8*q
    _TFC_m = 8.0
    def ATC_m(q): return 1 + 0.4*q + _TFC_m/q
    ax.plot(q, d, color=C['D'], lw=2.5)
    ax.plot(q, mr, color=C['MR'], lw=2.5, ls='--')
    ax.plot(q, mc, color=C['MC'], lw=2.5)
    ax.plot(qc, ATC_m(qc), color=C['ATC'], lw=2)
    label_curve_end(ax, 9.8, 1+0.8*9.8, 'MC', C['MC'], dx=12, dy=0, ha='left', va='center')
    label_curve_end(ax, 9.8, ATC_m(9.8), 'ATC', C['ATC'], dx=12, dy=0, ha='left', va='center')
    label_curve_end(ax, 9.8, 10-9.8, 'D = AR', C['D'], dx=12, dy=2, ha='left', va='center')
    label_at(ax, 5.2, 10-9.8, 'MR', C['MR'], dx=8, dy=2, ha='left', va='center')
    qm = 9/2.8; pm = 10 - qm; atc_qm = ATC_m(qm)
    # Marker at MR=MC intersection
    pt(ax, qm, 1+0.8*qm, C['MC'], None)
    pt(ax, qm, pm, C['D'], None)
    dashed_v(ax, qm, 0, pm, C['DASH'])
    dashed_h(ax, pm, 0, qm, C['DASH'])
    ax.text(-0.5, pm, 'P$_m$', ha='right', va='center', fontsize=10, color=C['D'], fontweight='bold')
    q_label(ax, qm, 'Q$_m$')
    pt(ax, qm, atc_qm, C['ATC'], None)
    shade_rect(ax, 0, qm, atc_qm, pm, C['PROFIT'])
    ax.text(qm*0.5, (pm+atc_qm)/2, 'Profit', ha='center', va='center',
            fontsize=10, color=C['PROFIT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.18', fc='white', ec='none', alpha=0.75))
    qsoc = 5
    pt(ax, qsoc, 10-qsoc, C['S'], 'Q$_{soc}$', 0, 0.4, ha='center')
    shade_poly(ax, [(qm, pm), (qsoc, 10-qsoc), (qm, 1+0.8*qm)], C['DWL'])
    # Place DWL label at the centroid of the red triangle so it sits inside the shade.
    ax.text((qm + qsoc + qm)/3, (pm + (10-qsoc) + (1+0.8*qm))/3, 'DWL',
            ha='center', va='center', fontsize=10, color=C['DWL_TEXT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.72))
    setup_axes(ax, 'Quantity', 'Price', (0,10), (0,10))
    save(fig, 'u4_monopoly.png')

def u4_price_discrim():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    q = np.linspace(0, 10, 300)
    d = 10 - q; mc = 1 + 0.8*q
    ax.plot(q, d, color=C['D'], lw=2.5)
    ax.plot(q, mc, color=C['MC'], lw=2.5)
    label_curve_end(ax, 10, d[-1], 'D = AR', C['D'], dy=16)
    label_curve_end(ax, 10, mc[-1], 'MC', C['MC'])
    qstar = 5; pstar = 5
    pt(ax, qstar, pstar, C['MC'], None)
    dashed_v(ax, qstar, 0, pstar, C['DASH'])
    dashed_h(ax, pstar, 0, qstar, C['DASH'])
    ax.text(-0.5, pstar, 'P(Q*)=MC', ha='right', va='center', fontsize=9, color=C['MUTE'], fontweight='bold')
    q_label(ax, qstar, 'Q*')
    qfill = np.linspace(0, qstar, 200)
    ax.fill_between(qfill, 1 + 0.8*qfill, 10 - qfill,
                    alpha=0.15, color=C['PROFIT'])
    ax.text(2.5, 6.0, 'PS = Total Surplus', color=C['MC'], fontsize=10, fontweight='bold', ha='center', va='center')
    ax.text(2.5, 4.0, 'DWL = 0', color=C['MC'], fontsize=10, fontweight='bold', ha='center', va='center')
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u4_price_discrim.png')

def u4_mc_short_run():
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    q = np.linspace(0, 10, 300)
    qc = np.linspace(1.0, 10, 280)
    d = 10 - q; mr = 10 - 2*q; mc = 1 + 0.8*q
    _TFC_sr = 8.0
    def ATC_sr(q): return 1 + 0.4*q + _TFC_sr/q
    ax.plot(q, d, color=C['D'], lw=2.5)
    ax.plot(q, mr, color=C['MR'], lw=2, ls='--')
    ax.plot(q, mc, color=C['MC'], lw=2.5)
    ax.plot(qc, ATC_sr(qc), color=C['ATC'], lw=2.5)
    label_curve_end(ax, 9.8, 10-9.8, 'D', C['D'], dx=12, dy=2, ha='left', va='center')
    label_at(ax, 5.2, 10-9.8, 'MR', C['MR'], dx=8, dy=2, ha='left', va='center', fontsize=10)
    label_curve_end(ax, 9.8, 1+0.8*9.8, 'MC', C['MC'], dx=12, dy=2, ha='left', va='center')
    label_curve_end(ax, 9.8, ATC_sr(9.8), 'ATC', C['ATC'], dx=12, dy=0, ha='left', va='center')
    qm = 9/2.8; pm = 10 - qm; atc_qm = ATC_sr(qm)
    # Marker at MR=MC intersection
    pt(ax, qm, 1+0.8*qm, C['MC'], None)
    pt(ax, qm, pm, C['D'], None)
    dashed_v(ax, qm, 0, pm, C['DASH'])
    dashed_h(ax, pm, 0, qm, C['DASH'])
    ax.text(-0.5, pm, 'P*', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, qm, 'Q*')
    pt(ax, qm, atc_qm, C['ATC'], None)
    shade_rect(ax, 0, qm, atc_qm, pm, C['PROFIT'])
    ax.text(qm*0.5, (pm+atc_qm)/2, 'Profit', ha='center', va='center',
            color=C['PROFIT'], fontsize=LABEL_FONTSIZE, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.16', fc='white', ec='none', alpha=0.72))
    setup_axes(ax, 'Quantity', 'Price', (0,10), (0,10))
    save(fig, 'u4_mc_short_run.png')

def u4_mc_long_run():
    """Monopolistic competition long-run: D tangent to ATC at Q_LR (zero profit).
    Uses same D, MR, MC as u4_mc_short_run; ATC is a quadratic tangent to D
    at the MR=MC vertical, with its minimum on the MC curve."""
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    q = np.linspace(0, 10, 300)
    qc = np.linspace(0.8, 10, 280)
    # Same D, MR, MC as u4_mc_short_run
    d = 10 - q; mr = 10 - 2*q; mc = 1 + 0.8*q
    # ATC: quadratic (parabola), tangent to D at (qm, pm), minimum on MC
    # Solved: a=91/450, b=-2.3, c=12.089 satisfies:
    #   ATC(qm)=pm, ATC'(qm)=-1 (slope of D), ATC(q_min)=MC(q_min)
    _a_lr = 91/450; _b_lr = -2.3; _c_lr = 12.089
    def ATC_lr(q): return _a_lr*q**2 + _b_lr*q + _c_lr
    ax.plot(q, d, color=C['D'], lw=2.5)
    # Clip MR to y >= 0 (no purple dashed line below Quantity axis)
    q_mr = np.linspace(0, 5, 100)
    ax.plot(q_mr, 10 - 2*q_mr, color=C['MR'], lw=2, ls='--')
    ax.plot(q, mc, color=C['MC'], lw=2.5)
    ax.plot(qc, ATC_lr(qc), color=C['ATC'], lw=2.5)
    # Curve end labels (same style as short_run)
    label_curve_end(ax, 9.8, 10-9.8, 'D', C['D'], dx=12, dy=2, ha='left', va='center')
    label_at(ax, 5.0, 0.2, 'MR', C['MR'], dx=8, dy=2, ha='left', va='center', fontsize=10)
    label_curve_end(ax, 9.8, 1+0.8*9.8, 'MC', C['MC'], dx=12, dy=2, ha='left', va='center')
    label_curve_end(ax, 9.8, ATC_lr(9.8), 'ATC', C['ATC'], dx=12, dy=12, ha='left', va='center')
    # MR=MC intersection → Q_LR
    qm = 9/2.8; pm = 10 - qm
    pt(ax, qm, 1+0.8*qm, C['MC'], None)
    pt(ax, qm, pm, C['D'], None)
    dashed_v(ax, qm, 0, pm, C['DASH'])
    dashed_h(ax, pm, 0, qm, C['DASH'])
    ax.text(-0.5, pm, 'P=ATC', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, qm, 'Q$_{LR}$')
    # ATC minimum (MC crosses ATC here → Q_eff)
    q_atc_min = -_b_lr/(2*_a_lr)
    atc_min_val = ATC_lr(q_atc_min)
    pt(ax, q_atc_min, atc_min_val, C['MC'], None)
    dashed_v(ax, q_atc_min, 0, atc_min_val, C['DASH'])
    q_label(ax, q_atc_min, 'Q$_{eff}$')
    # Excess Capacity arrow (Q_LR to Q_eff)
    arrow_y = -0.5
    arrow_bg(ax, qm, arrow_y, q_atc_min, arrow_y)
    ax.annotate('', xy=(q_atc_min, arrow_y), xytext=(qm, arrow_y),
                arrowprops=dict(arrowstyle='<|-|>', color=C['D'], lw=1.6),
                xycoords='data', textcoords='data', zorder=4)
    ax.annotate('Excess\nCapacity', xy=((qm+q_atc_min)/2, 0), xytext=(0, -18),
                textcoords='offset points',
                ha='center', va='top', fontsize=LABEL_FONTSIZE, color=C['D'], fontweight='bold')
    setup_axes(ax, 'Quantity', 'Price', (0,10), (0,10))
    ax.set_ylim(bottom=-3)
    save(fig, 'u4_mc_long_run.png')

def u4_game_theory():
    """2×2 payoff matrix (Prisoner's Dilemma — Pricing Game) as PNG with white background."""
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('white')
    # Matrix layout
    x0, y0 = 2.0, 1.0   # bottom-left of matrix
    cw, ch = 3.0, 2.0   # cell width/height
    # Column headers (Firm B)
    ax.text(x0 + cw/2,       y0 + 2*ch + 0.4, 'Firm B: High Price', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C['S'])
    ax.text(x0 + 1.5*cw,     y0 + 2*ch + 0.4, 'Firm B: Low Price',  ha='center', va='center',
            fontsize=10, fontweight='bold', color=C['D'])
    # Row headers (Firm A) — rotated
    ax.text(x0 - 0.5, y0 + 1.5*ch, 'Firm A: High Price', ha='center', va='center',
            fontsize=10, fontweight='bold', color=C['S'], rotation=90)
    ax.text(x0 - 0.5, y0 + 0.5*ch, 'Firm A: Low Price',  ha='center', va='center',
            fontsize=10, fontweight='bold', color=C['D'], rotation=90)
    # Cells: (col, row, fill, A_payoff, B_payoff, note, border_color)
    # row=1 → top (A high), row=0 → bottom (A low)
    cells = [
        (0, 1, '#ECFDF5', '50', '50', 'Cooperation',      None),
        (1, 1, '#FEF2F2', '20', '80', '',                 None),
        (0, 0, '#FEF2F2', '80', '20', '',                 None),
        (1, 0, '#FFFBEB', '30', '30', 'Nash Equilibrium', C['ATC']),
    ]
    for col, row, fill, a, b, note, border in cells:
        cx = x0 + col * cw
        cy = y0 + row * ch
        rect = Rectangle((cx, cy), cw, ch, facecolor=fill,
                         edgecolor=border or '#CBD5E1',
                         lw=2 if border else 1.2, zorder=1)
        ax.add_patch(rect)
        ax.text(cx + cw/2, cy + ch/2, f'{a}, {b}', ha='center', va='center',
                fontsize=16, fontweight='bold', color=C['TEXT'])
        if note:
            ncolor = C['ATC'] if 'Nash' in note else C['MUTE']
            ax.text(cx + cw/2, cy + 0.2, note, ha='center', va='center',
                    fontsize=9, fontweight='bold', color=ncolor)
    save(fig, 'u4_game_theory.png')

def u4_natural_monopoly():
    """Natural monopoly: ATC declines over the entire relevant demand range.
    Three regulatory outcomes:
      1. Unregulated monopoly: MR=MC → P_m, Q_m (profit + DWL)
      2. Fair-return (AC) pricing: P=ATC → zero economic profit, covers costs
      3. Socially optimal (MC) pricing: P=MC → allocatively efficient, firm needs subsidy
    """
    fig, ax = plt.subplots(figsize=(8.2, 6.2))
    q = np.linspace(0.01, 10, 300)
    qc = np.linspace(0.6, 10, 280)
    d = 12 - q; mr = 12 - 2*q; mc_const = 2.0
    mc = np.full_like(q, mc_const)
    atc = 14/qc + 2
    ax.plot(q, d, color=C['D'], lw=2.5)
    ax.plot(q, mr, color=C['MR'], lw=2, ls='--')
    ax.plot(q, mc, color=C['MC'], lw=2.5)
    ax.plot(qc, atc, color=C['ATC'], lw=2.5)
    label_curve_end(ax, 9.8, 12-9.8, 'D=AR', C['D'], dx=20, dy=12, ha='center')
    label_at(ax, 4.9, 12-2*4.9, 'MR', C['MR'], dx=-35, dy=12, ha='right', fontsize=10)
    label_curve_end(ax, 9.8, mc_const, 'MC', C['MC'], dx=20, dy=-20, ha='center')
    # 1. Unregulated monopoly: MR=MC → 12-2Q = 2 → Q_m = 5
    qm = 5.0; pm = 12 - qm; atc_qm = 14/qm + 2
    # Pre-compute qac for ATC label alignment
    qac = (10 + np.sqrt(44))/2
    # ATC label at the right end of the ATC curve, vertically aligned with D=AR and MC
    label_curve_end(ax, 9.8, 14/9.8 + 2, 'ATC', C['ATC'], dx=20, dy=0, ha='center')
    pt(ax, qm, pm, C['D'], None)
    pt(ax, qm, atc_qm, C['ATC'], None)
    dashed_v(ax, qm, 0, pm, C['DASH'])
    dashed_h(ax, pm, 0, qm, C['DASH'])
    ax.text(-0.5, pm, 'P$_m$', ha='right', va='center', fontsize=10, color=C['D'], fontweight='bold')
    q_label(ax, qm, 'Q$_m$')
    shade_rect(ax, 0, qm, atc_qm, pm, C['PROFIT'])
    ax.text(qm*0.5, (pm+atc_qm)/2, 'Profit', ha='center', va='center',
            color=C['PROFIT'], fontsize=9, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.14', fc='white', ec='none', alpha=0.72))
    # 2. Fair-return pricing: D=ATC → 12-Q = 14/Q + 2 → Q² - 10Q + 14 = 0
    pac = 12 - qac
    pt(ax, qac, pac, C['ATC'], None)
    label_at(ax, qac, pac, 'Fair-Return', C['ATC'], dx=10, dy=8, fontsize=9)
    dashed_v(ax, qac, 0, pac, C['DASH'])
    dashed_h(ax, pac, 0, qac, C['DASH'])
    ax.text(-0.5, pac, 'P$_{FR}$', ha='right', va='center', fontsize=10, color=C['ATC'], fontweight='bold')
    q_label(ax, qac, 'Q$_{FR}$')
    # 3. Socially optimal (MC) pricing: D=MC → Q_mc = 10
    qmc = 10.0; pmc = mc_const
    pt(ax, qmc, pmc, C['MC'], None)
    dashed_v(ax, qmc, 0, pmc, C['DASH'])
    dashed_h(ax, pmc, 0, qmc, C['DASH'])
    ax.text(-0.5, pmc, 'P$_{MC}$', ha='right', va='center', fontsize=10, color=C['MC'], fontweight='bold')
    q_label(ax, qmc, 'Q$_{MC}$')
    # DWL of unregulated monopoly: triangle between D and MC from Qm to Qmc
    shade_poly(ax, [(qm, pm), (qmc, pmc), (qm, mc_const)], C['DWL'])
    ax.text((qm+qmc+qm)/3, (pm+pmc+mc_const)/3, 'DWL',
            ha='center', va='center', fontsize=9, color=C['DWL_TEXT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.72))
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,13))
    save(fig, 'u4_natural_monopoly.png')

def ATC_alt(q): return 2 + 2/q + 0.4*q
def ATC_mc_lr(q): return 4.21 + 0.09*(q-5.8)**2
def ATC_mc_lr_deriv(q): return 0.18*(q-5.8)

# ═══════════════════════════════════════════════════════════════
# UNIT 5 — Factor Markets
# ═══════════════════════════════════════════════════════════════
def u5_pc_labor():
    fig, (ax_m, ax) = plt.subplots(1, 2, figsize=(11.2, 5.4))
    L = np.linspace(0, 10, 200)
    d_l = 12 - 1.2*L
    s_l = 1 + 0.6*L
    le = (12 - 1) / 1.8
    w = 1 + 0.6*le
    ax_m.plot(L, d_l, color=C['MRP'], lw=2.5)
    ax_m.plot(L, s_l, color=C['MFC'], lw=2.5)
    pt(ax_m, le, w, C['MC'], 'E', 0, 0.4, ha='center')
    dashed_h(ax_m, w, 0, le, C['DASH'])
    dashed_v(ax_m, le, 0, w, C['DASH'])
    q_label(ax_m, le, 'L$_M$')
    ax_m.text(-0.5, w, 'w$_e$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    label_curve_end(ax_m, 10, d_l[-1], 'D$_L$', C['MRP'], fontsize=10, dy=12)
    label_curve_end(ax_m, 10, s_l[-1], 'S$_L$', C['MFC'], fontsize=10, dy=0)
    ax_m.set_title('Labor Market', fontsize=11, fontweight='bold', color=C['TEXT'])
    setup_axes(ax_m, 'Market Labor', 'Wage', (0,11), (0,13))
    mrp = 12 - 1.2*L
    ax.plot(L, mrp, color=C['MRP'], lw=2.5)
    ax.plot([0, 10], [w, w], color=C['MFC'], lw=2.5)
    label_curve_end(ax, 10, mrp[-1], 'MRP = D$_L$', C['MRP'], fontsize=10, dy=12)
    label_curve_end(ax, 10, w, 'MFC = S$_L$ = w', C['MFC'], fontsize=10, dy=0)
    lstar = (12-w)/1.2
    pt(ax, lstar, w, C['MC'], None)
    dashed_v(ax, lstar, 0, w, C['DASH'])
    q_label(ax, lstar, 'L*')
    ax.set_title('Individual Firm', fontsize=11, fontweight='bold', color=C['TEXT'])
    setup_axes(ax, 'Firm Labor', 'Wage', (0,11), (0,13))
    save(fig, 'u5_pc_labor.png')

def u5_monopsony():
    fig, ax = plt.subplots(figsize=(7.8, 6.2))
    L = np.linspace(0, 10, 200)
    mrp = 12 - 1.2*L
    s_l = 1 + 0.5*L
    mfc = 1 + 1.0*L
    ax.plot(L, mrp, color=C['MRP'], lw=2.5)
    ax.plot(L, s_l, color=C['MFC'], lw=2.5)
    L_mfc = np.linspace(0, 10, 100)
    ax.plot(L_mfc, 1 + 1.0*L_mfc, color=C['MFCCURVE'], lw=2, ls='--')
    label_curve_end(ax, 10, mrp[-1], 'MRP = D$_L$', C['MRP'], fontsize=10, dy=8)
    label_curve_end(ax, 10, s_l[-1], 'S$_L$', C['MFC'], dy=0)
    label_at(ax, 10, 1+1.0*10, 'MFC', C['MFCCURVE'], dx=10, dy=0, ha='left', va='center')
    lm = 11/2.2; wm = 1 + 0.5*lm
    lc = 11/1.7; wc = 1 + 0.5*lc
    mrp_m = 12 - 1.2*lm
    pt(ax, lm, mrp_m, C['MFCCURVE'], None)
    pt(ax, lm, wm, C['MFC'], None)
    dashed_v(ax, lm, 0, mrp_m, C['DASH'])
    dashed_h(ax, wm, 0, lm, C['DASH'])
    ax.text(-0.5, wm, 'w$_m$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, lm, 'L$_m$')
    pt(ax, lc, wc, C['MUTE'], None)
    dashed_v(ax, lc, 0, wc, C['DASH'])
    dashed_h(ax, wc, 0, lc, C['DASH'])
    ax.text(-0.5, wc, 'w$_c$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, lc, 'L$_c$')
    setup_axes(ax, 'Labor', 'Wage', (0, 11), (0, 13))
    save(fig, 'u5_monopsony.png')

def u5_min_wage():
    fig, ax = plt.subplots(figsize=(7.2, 5.5))
    L = np.linspace(0, 10, 200)
    dl = 12 - 1.2*L; sl = 1 + 0.6*L
    ax.plot(L, dl, color=C['MRP'], lw=2.5)
    ax.plot(L, sl, color=C['MFC'], lw=2.5)
    label_curve_end(ax, 10, dl[-1], 'D$_L$', C['MRP'], dy=8)
    label_curve_end(ax, 10, sl[-1], 'S$_L$', C['MFC'])
    le = 11/1.8; we = 1+0.6*le
    pt(ax, le, we, C['MUTE'], 'E', 0, 0.4, ha='center', fontsize=10)
    dashed_v(ax, le, 0, we, C['DASH'])
    dashed_h(ax, we, 0, le, C['DASH'])
    q_label(ax, le, 'L$_e$')
    ax.text(-0.5, we, 'w$_e$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    wmin = 6
    ax.plot([0, 10], [wmin, wmin], ls='--', color=C['TAX'], lw=1)
    ax.text(-0.5, wmin, 'w$_{min}$', ha='right', va='center', fontsize=10, color=C['TAX'], fontweight='bold')
    ld = (12-wmin)/1.2; ls = (wmin-1)/0.6
    # Intersection markers at Wmin ∩ DL and Wmin ∩ SL
    pt(ax, ld, wmin, C['MRP'], None)
    pt(ax, ls, wmin, C['MFC'], None)
    h_bracket(ax, ld, ls, wmin+0.45, 'Unemployment', C['ALERT'], dy=8)
    dashed_v(ax, ld, 0, wmin, C['DASH']); dashed_v(ax, ls, 0, wmin, C['DASH'])
    q_label(ax, ld, 'L$_d$'); q_label(ax, ls, 'L$_s$')
    setup_axes(ax, 'Labor', 'Wage', (0,11), (0,13))
    save(fig, 'u5_min_wage.png')

def u5_monopsony_min_wage():
    """Reasonable minimum wage in monopsony: simultaneously ↑ wage and ↑ employment."""
    fig, ax = plt.subplots(figsize=(8.2, 6.2))
    L = np.linspace(0, 10, 200)
    mrp = 12 - 1.2*L
    s_l = 1 + 0.5*L
    mfc = 1 + 1.0*L
    ax.plot(L, mrp, color=C['MRP'], lw=2.5)
    ax.plot(L, s_l, color=C['MFC'], lw=2.5)
    ax.plot(L, mfc, color=C['MFCCURVE'], lw=2, ls='--')
    label_curve_end(ax, 10, mrp[-1], 'MRP = D$_L$', C['MRP'], fontsize=10, dy=8)
    label_curve_end(ax, 10, s_l[-1], 'S$_L$', C['MFC'], dy=0)
    label_at(ax, 10, 1+1.0*10, 'MFC', C['MFCCURVE'], dx=10, dy=10, ha='left', va='center')
    # Original monopsony: MRP = MFC → 12 - 1.2L = 1 + L → 2.2L = 11 → L_m = 5
    lm = 11/2.2; wm = 1 + 0.5*lm
    # Competitive: MRP = S_L → 12 - 1.2L = 1 + 0.5L → 1.7L = 11 → L_c = 11/1.7
    lc = 11/1.7; wc = 1 + 0.5*lc
    # Min wage between wm and wc
    wmin = 4.0
    l_star_target = (12 - wmin)/1.2
    l_supply_at_wmin = (wmin-1)/0.5
    l_actual = min(l_star_target, l_supply_at_wmin)
    # Plot min wage line (dashed, same lw as gray dashed lines)
    ax.plot([0, 10], [wmin, wmin], ls='--', color=C['TAX'], lw=1)
    label_at(ax, 10, wmin, 'w$_{min}$', C['TAX'], dx=10, dy=0, ha='left', va='center', fontsize=10)
    # New effective MFC: vertical jump from wmin back to original MFC (standard dashed)
    ax.plot([l_supply_at_wmin, l_supply_at_wmin],
            [wmin, 1 + 1.0*l_supply_at_wmin],
            color=C['DASH'], lw=1, ls='--')
    # Keep intersection marker but remove 'new MFC' label
    pt(ax, l_supply_at_wmin, wmin, C['TAX'], None)
    # Old monopsony point
    pt(ax, lm, wm, C['MFC'], None)
    dashed_v(ax, lm, 0, 12-1.2*lm, C['DASH'])
    dashed_h(ax, wm, 0, lm, C['DASH'])
    ax.text(-0.5, wm, 'w$_m$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, lm, 'L$_m$')
    # New point with min wage
    pt(ax, l_actual, wmin, C['MC'], None)
    dashed_v(ax, l_actual, 0, wmin, C['DASH'])
    q_label(ax, l_actual, 'L*')
    # Competitive reference
    pt(ax, lc, wc, C['MUTE'], None)
    dashed_v(ax, lc, 0, wc, C['DASH'])
    dashed_h(ax, wc, 0, lc, C['DASH'])
    ax.text(-0.5, wc, 'w$_c$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, lc, 'L$_c$')
    # Arrow from old to new
    ax.annotate('', xy=(l_actual, wmin), xytext=(lm, wm),
                arrowprops=dict(arrowstyle='-|>', color=C['MC'], lw=1.6))
    setup_axes(ax, 'Labor', 'Wage', (0, 11), (0, 13))
    save(fig, 'u5_monopsony_min_wage.png')

# ═══════════════════════════════════════════════════════════════
# UNIT 6 — Market Failure & Government
# ═══════════════════════════════════════════════════════════════
def u6_neg_externality():
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    q = np.linspace(0, 10, 300)
    d = 10 - q; mpc = 1 + (2/3)*q; msc = 10/3 + (2/3)*q
    ax.plot(q, d, color=C['D'], lw=2.5)
    ax.plot(q, mpc, color=C['S'], lw=2)
    ax.plot(q, msc, color=C['MSC'], lw=2.5, ls='--')
    label_curve_end(ax, 10, d[-1], 'D = MSB = MPB', C['D'], fontsize=10, dx=10, dy=8)
    label_curve_end(ax, 10, mpc[-1], 'S=MPC', C['S'], fontsize=10)
    label_curve_end(ax, 10, msc[-1], 'MSC', C['MSC'])
    # Market: D=MPC → 10-q = 1+(2/3)q → 9=(5/3)q → q_m=27/5=5.4, p_m=4.6
    # Social:  D=MSC → 10-q = 10/3+(2/3)q → 20/3=(5/3)q → q_s=4, p_s=6
    qm = 27/5; pm = 10 - qm; qs = 4; ps = 6
    pt(ax, qm, pm, C['MUTE'], None)
    pt(ax, qs, ps, C['MC'], None)
    dashed_v(ax, qm, 0, pm, C['DASH']); dashed_v(ax, qs, 0, ps, C['DASH'])
    dashed_h(ax, pm, 0, qm, C['DASH']); dashed_h(ax, ps, 0, qs, C['DASH'])
    ax.text(-0.5, pm, 'P$_m$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    ax.text(-0.5, ps, 'P$_s$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, qm, 'Q$_m$'); q_label(ax, qs, 'Q$_s$')
    qfill = np.linspace(qs, qm, 50)
    ax.fill_between(qfill, 10-qfill, 10/3+(2/3)*qfill, alpha=0.15, color=C['DWL'])
    # DWL triangle: (qs,ps),(qm,pm),(qm,msc(qm)) — centroid sits inside the shade.
    msc_qm = 10/3 + (2/3)*qm
    ax.text((qs+qm+qm)/3, (ps+pm+msc_qm)/3, 'DWL',
            ha='center', va='center', fontsize=10, color=C['DWL_TEXT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.72))
    arrow_bg(ax, qs, 1.5, qm, 1.5)
    ax.annotate('', xy=(qm, 1.5), xytext=(qs, 1.5),
                arrowprops=dict(arrowstyle='<|-|>', color=C['D'], lw=1), zorder=4)
    ax.text((qs+qm)/2, 1.0, 'Overproduction', ha='center', fontsize=LABEL_FONTSIZE, color=C['D'], fontweight='bold')
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u6_neg_externality.png')

def u6_pos_externality():
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    q = np.linspace(0, 10, 300)
    mpb = 10 - q; msb = 12 - q; msc = 1 + q
    ax.plot(q, mpb, color=C['D'], lw=2)
    ax.plot(q, msb, color=C['MSB'], lw=2.5, ls='--')
    ax.plot(q, msc, color=C['S'], lw=2.5)
    label_curve_end(ax, 10, 10-10, 'D=MPB', C['D'], fontsize=10, dx=10, dy=8)
    label_curve_end(ax, 10, msb[-1], 'MSB', C['MSB'])
    label_curve_end(ax, 10, msc[-1], 'S = MSC = MPC', C['S'], fontsize=10)
    qm = 4.5; pm = 5.5; qs = 5.5; ps = 6.5
    pt(ax, qm, pm, C['MUTE'], None)
    pt(ax, qs, ps, C['MC'], None)
    dashed_v(ax, qm, 0, pm, C['DASH']); dashed_v(ax, qs, 0, ps, C['DASH'])
    dashed_h(ax, pm, 0, qm, C['DASH']); dashed_h(ax, ps, 0, qs, C['DASH'])
    ax.text(-0.5, pm, 'P$_m$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    ax.text(-0.5, ps, 'P$_s$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    q_label(ax, qm, 'Q$_m$'); q_label(ax, qs, 'Q$_s$')
    qfill = np.linspace(qm, qs, 50)
    ax.fill_between(qfill, 12-qfill, 1+qfill, alpha=0.15, color=C['DWL'])
    # DWL triangle: (qm,5.5),(qm,7.5),(qs,6.5) — centroid sits inside the shade.
    ax.text((qm+qm+qs)/3, (5.5+7.5+6.5)/3, 'DWL',
            ha='center', va='center', fontsize=10, color=C['DWL_TEXT'], fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.15', fc='white', ec='none', alpha=0.72))
    arrow_bg(ax, qm, 1.5, qs, 1.5)
    ax.annotate('', xy=(qs, 1.5), xytext=(qm, 1.5),
                arrowprops=dict(arrowstyle='<|-|>', color=C['D'], lw=1), zorder=4)
    ax.text((qm+qs)/2, 1.0, 'Underproduction', ha='center', fontsize=LABEL_FONTSIZE, color=C['D'], fontweight='bold')
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,13))
    save(fig, 'u6_pos_externality.png')

def u6_pigouvian_tax():
    fig, ax = plt.subplots(figsize=(7.8, 5.8))
    q = np.linspace(0, 10, 300)
    d = 10 - q; mpc = 1 + (2/3)*q; msc = 10/3 + (2/3)*q
    ax.plot(q, d, color=C['D'], lw=2.5)
    ax.plot(q, mpc, color=C['S'], lw=1.5, ls='--')
    ax.plot(q, msc, color=C['MC'], lw=2.5)
    label_curve_end(ax, 10, d[-1], 'D = MSB = MPB', C['D'], fontsize=10, dy=8)
    label_curve_end(ax, 10, mpc[-1], 'MPC', C['S'], fontsize=10)
    label_at(ax, 10, msc[-1], 'MSC = MPC + Tax', C['MC'], dx=8, dy=0, fontsize=10, va='bottom')
    # Social optimum: D=MSC → q_s=4, p_s=6; MPC at q_s = 1+(2/3)*4 = 11/3
    qs = 4; ps = 6; mpc_at_qs = 1 + (2/3)*qs
    pt(ax, qs, ps, C['MC'], None)
    dashed_v(ax, qs, 0, ps, C['DASH'])
    dashed_h(ax, ps, 0, qs, C['DASH'])
    q_label(ax, qs, 'Q$_s$')
    ax.text(-0.5, ps, 'P$_s$', ha='right', va='center', fontsize=10, color=C['MUTE'], fontweight='bold')
    arrow_bg(ax, qs-0.45, mpc_at_qs, qs-0.45, ps)
    ax.annotate('', xy=(qs-0.45, ps), xytext=(qs-0.45, mpc_at_qs),
                arrowprops=dict(arrowstyle='<|-|>', color=C['TAX'], lw=1.8), zorder=4)
    ax.annotate('Tax = MEC', xy=(qs-0.45, (ps+mpc_at_qs)/2), xytext=(-8, 0),
                textcoords='offset points', ha='right', va='center',
                color=C['TAX'], fontsize=LABEL_FONTSIZE, fontweight='bold',
                bbox=dict(boxstyle='round,pad=0.14', fc='white', ec='none', alpha=0.7))
    setup_axes(ax, 'Quantity', 'Price', (0,11), (0,11))
    save(fig, 'u6_pigouvian_tax.png')

def u6_lorenz():
    fig, ax = plt.subplots(figsize=(6.8, 6.2))
    pop = np.linspace(0, 1, 200)
    inc = pop**1.85
    ax.plot([0,1],[0,0], color=C['AXIS'], lw=1.5)
    ax.plot([0,0],[0,1], color=C['AXIS'], lw=1.5)
    ax.fill_between(pop, 0, inc, alpha=0.08, color=C['S'])
    ax.fill_between(pop, inc, pop, alpha=0.12, color=C['D'])
    ax.plot([0,1],[0,1], color=C['S'], lw=2.5)
    ax.plot(pop, inc, color=C['D'], lw=3)
    ax.text(0.32, 0.5, 'Perfect\nEquality', color=C['S'], fontsize=LABEL_FONTSIZE, fontweight='bold', va='center', ha='center')
    ax.text(0.62, 0.28, 'Lorenz Curve', color=C['D'], fontsize=11, fontweight='bold')
    ax.text(0.32, 0.21, 'A', color=C['D'], fontsize=16, fontweight='bold')
    ax.text(0.55, 0.12, 'B', color=C['S'], fontsize=16, fontweight='bold')
    ax.text(0.45, 0.88, 'Gini = A/(A+B)', color=C['MR'], fontsize=10, fontweight='bold')
    for t in [0.25, 0.5, 0.75, 1.0]:
        ax.plot([t,t],[-0.02,0], color=C['AXIS'], lw=1)
        ax.text(t, -0.05, f'{int(t*100)}%', ha='center', fontsize=8, color=C['MUTE'])
        ax.plot([-0.02,0],[t,t], color=C['AXIS'], lw=1)
        ax.text(-0.05, t, f'{int(t*100)}%', ha='right', va='center', fontsize=8, color=C['MUTE'])
    ax.set_xlim(-0.18, 1.18); ax.set_ylim(-0.1, 1.12)
    ax.axis('off')
    ax.text(0.5, -0.08, 'Cumulative % of Population', ha='center', fontsize=10, color=C['TEXT'])
    ax.text(-0.16, 0.5, 'Cumulative % of Income', ha='center', va='center', fontsize=10, color=C['TEXT'], rotation=90)
    save(fig, 'u6_lorenz.png')

# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════
if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    charts = [
        ('Unit 1', [u1_ppc, u1_ppc_growth, u1_dim_mu, u1_budget_ic]),
        ('Unit 2', [u2_demand_move, u2_supply_move, u2_equilibrium, u2_demand_increase,
                    u2_supply_decrease, u2_elasticity_five, u2_price_ceiling, u2_price_floor,
                    u2_tax_incidence, u2_subsidy, u2_cs_ps, u2_tariff, u2_quota]),
        ('Unit 3', [u3_tp_mp_ap, u3_total_cost, u3_unit_cost, u3_lratc,
                    u3_pc_profit, u3_pc_loss, u3_pc_shutdown, u3_pc_lr_equilibrium]),
        ('Unit 4', [u4_monopoly, u4_price_discrim, u4_natural_monopoly,
                    u4_mc_short_run, u4_mc_long_run, u4_game_theory]),
        ('Unit 5', [u5_pc_labor, u5_monopsony, u5_min_wage, u5_monopsony_min_wage]),
        ('Unit 6', [u6_neg_externality, u6_pos_externality, u6_pigouvian_tax, u6_lorenz]),
    ]
    total = sum(len(fns) for _, fns in charts)
    print(f'Generating {total} charts...')
    for unit_name, fns in charts:
        print(f'\n[{unit_name}]')
        for fn in fns:
            fn()
    print(f'\nDone! {total} charts saved to {OUT}/')
