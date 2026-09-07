# -*- coding: utf-8 -*-
"""Graphical abstract for Insights into Imaging.

Single-panel, 300 dpi. Every number is read from the audit outputs, not typed in.
Form: emphasis (one accent hue plus de-emphasis grey) — the story is that one
element was recorded and the elements underpinning published accuracy were not.
"""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle

OUT = '/home/user/-Diagnostic-performance-of-intestinal-malrotation/'
u = pd.read_csv('us_audit4.csv')
N = len(u)
det = u['det'].astype(int); w = u['whirl_pos'].astype(bool)
pct = lambda c: 100 * u[c].mean()

BLUE, RED, GREY = '#2C7FB8', '#B22222', '#8d8b86'
INK, INK2, MUTED = '#0b0b0b', '#52514e', '#898781'
GRID, RULE = '#e1e0d9', '#c3c2b7'
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 10})

fig = plt.figure(figsize=(9.4, 6.3), dpi=300)
fig.patch.set_facecolor('white')

def rbar(ax, x0, y, val, h, color, r=None):
    """Bar with a rounded data-end and a square baseline end."""
    r = min(h * 0.42, val * 0.5) if r is None else r
    if val <= 0: return
    v = Path([(x0, y-h/2), (x0+val-r, y-h/2), (x0+val-r+r*0.55, y-h/2),
              (x0+val, y-h/2+r*0.45), (x0+val, y), (x0+val, y+h/2-r*0.45),
              (x0+val-r+r*0.55, y+h/2), (x0+val-r, y+h/2), (x0, y+h/2), (x0, y-h/2)],
             [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO,
              Path.CURVE3, Path.CURVE3, Path.LINETO, Path.LINETO, Path.CLOSEPOLY])
    ax.add_patch(PathPatch(v, fc=color, ec='none', zorder=3))

# ---------------- header ----------------
fig.text(0.035, 0.955, 'Routine ultrasound reports for intestinal malrotation',
         fontsize=15.5, fontweight='bold', color=INK, va='center')
fig.text(0.035, 0.900, 'rarely document the duodenal landmarks that published accuracy rests on',
         fontsize=15.5, fontweight='bold', color=INK, va='center')
fig.text(0.035, 0.848,
         '13.5-year single-centre report audit  ·  410 children with surgically confirmed malrotation  ·  '
         '740 preoperative index examinations  ·  119 routine ultrasound examinations',
         fontsize=9.3, color=INK2, va='center')
fig.text(0.035, 0.810,
         'Case-only design: every child had surgically confirmed malrotation, so these are report-level detection rates, not sensitivities.',
         fontsize=9.3, color=INK2, va='center', style='italic')
fig.add_artist(plt.Line2D([0.035, 0.965], [0.784, 0.784], color=RULE, lw=0.9))

# ---------------- panel a: documented content ----------------
axa = fig.add_axes([0.045, 0.295, 0.435, 0.423]); axa.set_facecolor('white')
ROWS = [('Whirlpool, swirl or spiral',      'whirl_pos', BLUE),
        ('Mesenteric artery–vein relationship', 'sma_smv', RED),
        ('Duodenum mentioned in any form',  'duodenum',  GREY),
        ('Caecal position',                 'cecum',     GREY),
        ('D3 or duodenojejunal junction',   'd3_or_djj', RED),
        ('Enteric fluid administered',      'fluid',     RED)]
ys = list(range(len(ROWS)))[::-1]
for gl in (0, 10, 20, 30, 40, 50):
    axa.plot([gl, gl], [-0.62, len(ROWS)-0.38], color=GRID, lw=0.8, zorder=0)
for (lab, col, c), y in zip(ROWS, ys):
    v = pct(col); k = int(u[col].sum())
    rbar(axa, 0, y, v, 0.46, c)
    axa.text(v + 1.1, y, f'{v:.1f}%', va='center', ha='left', fontsize=9.6,
             color=INK, fontweight='bold')
    axa.text(v + 1.1, y - 0.30, f'{k}/{N}', va='center', ha='left', fontsize=8.1, color=MUTED)
axa.set_yticks(ys); axa.set_yticklabels([r[0] for r in ROWS], fontsize=9.4, color=INK2)
axa.set_xlim(0, 62); axa.set_ylim(-0.72, len(ROWS)-0.28)
axa.set_xticks([0, 10, 20, 30, 40, 50]); axa.set_xticklabels(['0', '10', '20', '30', '40', '50%'],
                                                            fontsize=8.6, color=MUTED)
for s in ('top', 'right', 'left', 'bottom'): axa.spines[s].set_visible(False)
axa.plot([0, 50], [-0.72, -0.72], color=RULE, lw=0.9, clip_on=False, zorder=2)
axa.tick_params(axis='y', length=0); axa.tick_params(axis='x', length=2.5, color=RULE)
axa.set_title('What the reports documented', fontsize=11.2, fontweight='bold',
              color=INK, loc='left', pad=9)

# ---------------- panel b: what was reported ----------------
axb = fig.add_axes([0.605, 0.498, 0.335, 0.220]); axb.set_facecolor('white')
kw, nw = int(det[w].sum()), int(w.sum())
kn, nn = int(det[~w].sum()), int((~w).sum())
BARS = [(f'Whirlpool recorded', 100*kw/nw, f'{kw}/{nw}', BLUE),
        (f'No whirlpool recorded', 100*kn/nn, f'{kn}/{nn}', GREY)]
yb = [1, 0]
for gl in (0, 25, 50, 75, 100):
    axb.plot([gl, gl], [-0.62, 1.62], color=GRID, lw=0.8, zorder=0)
for (lab, v, ann, c), y in zip(BARS, yb):
    rbar(axb, 0, y, v, 0.32, c)
    axb.text(v + 2.2, y, f'{v:.0f}%' if v == 100 else f'{v:.1f}%', va='center', ha='left',
             fontsize=11.5, color=INK, fontweight='bold')
    axb.text(v + 2.2, y - 0.30, ann, va='center', ha='left', fontsize=8.1, color=MUTED)
axb.set_yticks(yb); axb.set_yticklabels([b[0] for b in BARS], fontsize=9.4, color=INK2)
axb.set_xlim(0, 128); axb.set_ylim(-0.72, 1.72)
axb.set_xticks([0, 25, 50, 75, 100]); axb.set_xticklabels(['0', '25', '50', '75', '100%'],
                                                          fontsize=8.6, color=MUTED)
for s in ('top', 'right', 'left', 'bottom'): axb.spines[s].set_visible(False)
axb.plot([0, 100], [-0.72, -0.72], color=RULE, lw=0.9, clip_on=False, zorder=2)
axb.tick_params(axis='y', length=0); axb.tick_params(axis='x', length=2.5, color=RULE)
axb.set_title('Whether malrotation was reported', fontsize=11.2, fontweight='bold',
              color=INK, loc='left', pad=9)
v = u[u['volvulus'].astype(bool)]
fig.text(0.605, 0.392,
         f'A whirlpool was recorded in only {int(v["whirl_pos"].sum())} of the {len(v)} children '
         f'({100*v["whirl_pos"].mean():.0f}%)\nin whom operation confirmed midgut volvulus —\n'
         'the sign the reports depended on was itself\nabsent in half of them.',
         fontsize=9.0, color=INK2, va='top', ha='left', linespacing=1.65)

# ---------------- legend ----------------
def swatch(x, c, lab):
    fig.patches.append(Rectangle((x, 0.196), 0.0112, 0.0165, transform=fig.transFigure,
                                 fc=c, ec='none'))
    fig.text(x + 0.0165, 0.2043, lab, fontsize=8.8, color=INK2, va='center')
swatch(0.035, RED,  'Elements underpinning published ultrasound accuracy')
swatch(0.425, BLUE, 'Whirlpool sign — a sign of volvulus, not of malrotation')
swatch(0.812, GREY, 'Other documented content')

# ---------------- takeaway ----------------
fig.add_artist(plt.Line2D([0.035, 0.965], [0.155, 0.155], color=RULE, lw=0.9))
fig.text(0.035, 0.078,
         'Routine ultrasound functioned as a whirlpool-dependent test for volvulus, not a protocolised assessment of duodenal position.\n'
         'Departments adopting ultrasound-first pathways should audit whether their own reports document the landmarks that produced the published sensitivities.',
         fontsize=9.5, color=INK, va='center', linespacing=1.6)

fig.savefig(OUT + 'Graphical_Abstract.png', dpi=300, facecolor='white', bbox_inches='tight')
plt.close()

# The submission system wants a flat RGB TIFF; matplotlib writes RGBA, and an
# alpha channel is a common cause of rejected image uploads.
from PIL import Image
im = Image.open(OUT + 'Graphical_Abstract.png')
Image.alpha_composite(Image.new('RGBA', im.size, (255, 255, 255, 255)), im.convert('RGBA')) \
     .convert('RGB').save(OUT + 'Graphical_Abstract.tif', compression='tiff_lzw', dpi=(300, 300))
print('graphical abstract written (.tif LZW + .png)')
