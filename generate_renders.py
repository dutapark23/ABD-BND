#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLR — Interior Room Renders
High-quality perspective visualizations of each zone
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Arc, Polygon
import matplotlib.patheffects as pe
import matplotlib.font_manager as fm
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
from scipy.ndimage import gaussian_filter
import warnings
warnings.filterwarnings('ignore')

fm.fontManager.addfont('/tmp/fonts/Montserrat.ttf')
fm.fontManager.addfont('/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Regular.ttf')

import arabic_reshaper
from bidi.algorithm import get_display
def ar(t): return get_display(arabic_reshaper.reshape(t))

FONT = 'Montserrat'
AMIRI = 'Amiri'

OUTPUT_PDF = '/home/user/ABD-BND/CLR_Room_Renders.pdf'

W, H = 16, 9   # landscape widescreen per render

# ── colour helpers ────────────────────────────────────────────────────────────
NAVY   = '#0D1B2A'
GOLD   = '#C9A84C'
SAND   = '#F5EFE4'
WALNUT = '#3D2314'
TERRA  = '#B5622F'
SAGE   = '#6B8F71'
IVORY  = '#FAF6EF'
TEAL   = '#1B5E7A'
CREAM  = '#F0E9DC'
WHITE  = '#FFFFFF'
DARK   = '#1A1A1A'
WARM_LIGHT = '#FFE090'
BRASS  = '#B8902A'

def gradient_rect(ax, x, y, w, h, color_top, color_bot, steps=80):
    """Draw a vertical gradient rectangle."""
    t_arr = np.array(matplotlib.colors.to_rgb(color_top))
    b_arr = np.array(matplotlib.colors.to_rgb(color_bot))
    for i in range(steps):
        t = i / steps
        col = tuple((1-t)*t_arr + t*b_arr)
        r = patches.Rectangle((x, y + h*(1-t-1/steps)), w, h/steps,
                                facecolor=col, edgecolor='none', zorder=1)
        ax.add_patch(r)

def glow(ax, cx, cy, radius, color, alpha_center=0.6, steps=20, zorder=5):
    """Radial glow effect."""
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = alpha_center * (1 - i/steps)**0.5
        c = Circle((cx, cy), r, facecolor=color, edgecolor='none', alpha=a, zorder=zorder)
        ax.add_patch(c)

def add_label_bar(fig, zone, name, surface, desc):
    """Bottom info bar for each render."""
    ax = fig.add_axes([0, 0, 1, 0.075])
    ax.set_facecolor(NAVY)
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis('off')
    # Gold top line
    ax.axhline(0.92, color=GOLD, lw=2)
    # Zone badge
    r = patches.FancyBboxPatch((0.02, 0.1), 0.06, 0.78,
                                boxstyle='round,pad=0.02',
                                facecolor=GOLD, edgecolor='none')
    ax.add_patch(r)
    ax.text(0.05, 0.5, zone, fontsize=18, color=NAVY, fontweight='bold',
            ha='center', va='center', fontfamily=FONT)
    # Name
    ax.text(0.10, 0.68, name, fontsize=13, color=WHITE, fontweight='bold',
            va='center', fontfamily=FONT)
    ax.text(0.10, 0.28, desc, fontsize=9, color='#8A9BB0',
            va='center', fontfamily=FONT)
    # Surface
    ax.text(0.82, 0.5, surface, fontsize=16, color=GOLD, fontweight='bold',
            va='center', ha='center', fontfamily=FONT)
    ax.text(0.92, 0.5, '· CONCEPT AL-MAKTABA', fontsize=8, color='#8A9BB0',
            va='center', fontfamily=FONT)

# ══════════════════════════════════════════════════════════════════════════════
# RENDER 1 — RÉCEPTION & ACCUEIL
# ══════════════════════════════════════════════════════════════════════════════
def render_reception():
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(SAND)

    ax = fig.add_axes([0, 0.075, 1, 0.925])
    ax.set_xlim(0, 160); ax.set_ylim(0, 90)
    ax.axis('off')
    ax.set_facecolor(SAND)

    # ── FLOOR ──────────────────────────────────────────────────────────────
    # Polished concrete floor — béton ciré gris perle
    gradient_rect(ax, 0, 0, 160, 28, '#C8C4BE', '#DEDAD4')
    # Floor reflection/shine
    for lx in np.linspace(5, 155, 14):
        ax.plot([lx, lx+6], [0, 28], color='white', lw=0.4, alpha=0.18)

    # ── BACK WALL — stuc sable chaud ─────────────────────────────────────
    gradient_rect(ax, 0, 28, 160, 62, '#ECE4D6', '#F5EFE6')

    # ── CEILING — dark wood coffered ──────────────────────────────────────
    gradient_rect(ax, 0, 80, 160, 10, '#1A0E06', '#2C1A0E')
    # Wood grain lines on ceiling
    for cy in np.linspace(80.5, 89, 14):
        ax.plot([0, 160], [cy, cy], color='#3D2010', lw=0.4, alpha=0.35)
    # Coffered beam lines
    for bx in np.linspace(0, 160, 7):
        ax.add_patch(patches.Rectangle((bx-1, 80), 2, 10,
                     facecolor='#120A04', edgecolor='none'))

    # ── LED COVE LIGHT STRIP ───────────────────────────────────────────────
    # Warm glow wash on ceiling-wall junction
    for step in range(30, 0, -1):
        alpha = 0.022 * step
        h_glow = step * 0.25
        ax.add_patch(patches.Rectangle((0, 80-h_glow), 160, h_glow,
                     facecolor=WARM_LIGHT, edgecolor='none', alpha=alpha, zorder=2))

    # ── LEFT ACCENT WALL (partial) ────────────────────────────────────────
    gradient_rect(ax, 0, 28, 22, 52, '#2A1A0E', WALNUT)
    # Vertical wood slats
    for sx in np.linspace(2, 20, 12):
        ax.add_patch(patches.Rectangle((sx, 28), 1.0, 52,
                     facecolor='#4A2818', edgecolor='#1A0A04', linewidth=0.3))

    # ── CALLIGRAPHY WALL PANEL (center-right) ────────────────────────────
    # Recessed panel on main wall
    ax.add_patch(patches.FancyBboxPatch((70, 42), 72, 34,
                 boxstyle='round,pad=0.5',
                 facecolor='#EDE5D4', edgecolor='#D4C4A8', linewidth=1.5))
    # Shadow beneath panel
    ax.add_patch(patches.FancyBboxPatch((70.5, 41), 72, 2,
                 boxstyle='round,pad=0.2',
                 facecolor='#B8A888', edgecolor='none', alpha=0.3))

    # Brass calligraphy — laser-cut letters simulation
    ax.text(106, 67, ar('مركز اللغات'), fontsize=26, color=BRASS,
            ha='center', va='center', fontfamily=AMIRI, fontweight='bold',
            alpha=0.95, zorder=10)
    ax.text(106, 55, 'CENTRE LINGUISTIQUE DE RIYAD', fontsize=9,
            color='#8A7A5A', ha='center', va='center', fontfamily=FONT,
            fontweight='bold', alpha=0.8, zorder=10)
    # Gold frame on panel
    for lw, alpha in [(2.5, 0.6), (0.8, 0.9)]:
        ax.add_patch(patches.FancyBboxPatch((72, 43), 68, 32,
                     boxstyle='round,pad=0.3',
                     facecolor='none', edgecolor=GOLD, linewidth=lw, alpha=alpha))

    # ── RECEPTION DESK ────────────────────────────────────────────────────
    # Desk body — curved walnut
    desk_pts = np.array([[28, 18],[90, 18],[90, 28],[28, 28],[28,18]])
    # Perspective foreshortening
    desk_front = np.array([[24,10],[96,10],[96,18],[24,18]])
    ax.fill(desk_front[:,0], desk_front[:,1],
            facecolor='#3D2010', edgecolor='#5A3020', linewidth=1.5, zorder=8)
    # Desk face — walnut paneling
    ax.add_patch(patches.Rectangle((24, 18), 72, 10,
                 facecolor='#4A2818', edgecolor='#2A1008', linewidth=1.5, zorder=8))
    # Brass inset strips on desk face
    for bstrip in np.linspace(28, 88, 6):
        ax.add_patch(patches.Rectangle((bstrip-0.4, 19), 0.8, 8,
                     facecolor=BRASS, edgecolor='none', alpha=0.7, zorder=9))
    # Marble desk top
    ax.add_patch(patches.Rectangle((23, 28), 74, 2.5,
                 facecolor='#E8E0D0', edgecolor='#C9A84C', linewidth=1.5, zorder=9))
    # Marble veining
    for vx in [35, 55, 70, 85]:
        ax.plot([vx, vx+8], [28, 30.5], color='#B0A090', lw=0.5, alpha=0.4, zorder=10)
    # Desk top items
    ax.add_patch(patches.Rectangle((68, 29), 8, 0.8,
                 facecolor='#1A1A2E', edgecolor=GOLD, linewidth=0.5, zorder=11))  # tablet
    ax.text(72, 29.4, 'CLR', fontsize=3.5, color=GOLD, ha='center', zorder=12, fontfamily=FONT)
    # Small vase on desk
    ax.add_patch(patches.FancyBboxPatch((33, 29), 3, 2.5,
                 boxstyle='round,pad=0.3', facecolor=BRASS, edgecolor='#8A6A1A', zorder=11))
    # Flower in vase
    for fa in range(6):
        angle = fa * 60
        fx = 34.5 + 1.2*np.cos(np.radians(angle))
        fy = 32.5 + 0.7*np.sin(np.radians(angle))
        ax.add_patch(Circle((fx, fy), 0.5, facecolor='#E8D4A0', edgecolor='none',
                             alpha=0.8, zorder=12))

    # ── RECEPTION PERSON SILHOUETTE ───────────────────────────────────────
    # Standing figure behind desk
    ax.add_patch(Circle((58, 34), 3.5, facecolor='#D4C0A0', edgecolor='none', zorder=10))  # head
    ax.add_patch(patches.Rectangle((54, 22), 8, 12,
                 facecolor='#F0EAE0', edgecolor='none', zorder=9))  # body (white shirt)

    # ── OLIVE TREE ────────────────────────────────────────────────────────
    # Laiton pot
    ax.add_patch(patches.FancyBboxPatch((135, 8), 12, 14,
                 boxstyle='round,pad=0.5',
                 facecolor='#B8902A', edgecolor='#8A6A1A', linewidth=1.5, zorder=7))
    # Sheen on pot
    ax.add_patch(patches.Rectangle((136, 9), 2, 12,
                 facecolor='#E8C050', edgecolor='none', alpha=0.25, zorder=8))
    # Tree trunk
    ax.plot([141, 141], [22, 55], color='#5A3020', lw=3, zorder=7)
    ax.plot([141, 137], [40, 52], color='#5A3020', lw=1.5, zorder=7)
    ax.plot([141, 146], [38, 50], color='#5A3020', lw=1.5, zorder=7)
    ax.plot([141, 135], [48, 62], color='#5A3020', lw=1.5, zorder=7)
    ax.plot([141, 148], [50, 65], color='#5A3020', lw=1.5, zorder=7)
    # Foliage clusters
    foliage_pts = [(141,60,14),(137,54,10),(146,52,10),(134,64,12),(149,65,11),(141,72,9)]
    for fx, fy, fr in foliage_pts:
        ax.add_patch(Circle((fx, fy), fr, facecolor='#3A5A2A', edgecolor='none',
                             alpha=0.7, zorder=8))
        ax.add_patch(Circle((fx-2, fy+2), fr*0.5, facecolor='#4A7A3A', edgecolor='none',
                             alpha=0.5, zorder=9))

    # ── CEILING PENDANT LIGHT ──────────────────────────────────────────────
    # Thin cord
    ax.plot([80, 80], [80, 68], color='#888', lw=0.8, zorder=10)
    # Hexagonal lantern
    hex_angles = np.linspace(0, 2*np.pi, 7)
    hex_x = 80 + 4*np.cos(hex_angles)
    hex_y = 64 + 6*np.sin(hex_angles)
    ax.fill(hex_x, hex_y, facecolor=BRASS, edgecolor='#8A6A1A', linewidth=1.5, zorder=10)
    # Light glow below lantern
    glow(ax, 80, 62, 12, WARM_LIGHT, alpha_center=0.35, steps=20, zorder=6)
    ax.add_patch(Circle((80, 64), 2, facecolor='#FFF0A0', edgecolor='none',
                         alpha=0.95, zorder=11))

    # ── WALL SCONCES ──────────────────────────────────────────────────────
    for scx in [28, 128]:
        ax.add_patch(patches.Rectangle((scx-2, 58), 4, 6,
                     facecolor=BRASS, edgecolor='none', zorder=8, alpha=0.9))
        glow(ax, scx, 64, 8, WARM_LIGHT, alpha_center=0.2, steps=15, zorder=5)

    # ── FLOOR REFLECTION ──────────────────────────────────────────────────
    # Subtle desk reflection on concrete
    for rx in range(24, 97, 2):
        ax.add_patch(patches.Rectangle((rx, 0), 1.5, 10,
                     facecolor='#4A2818', edgecolor='none', alpha=0.04, zorder=3))

    # ── DECORATIVE ELEMENTS ───────────────────────────────────────────────
    # Wall art left side
    ax.add_patch(patches.FancyBboxPatch((2, 45), 15, 22,
                 boxstyle='round,pad=0.3',
                 facecolor='#2A1A0A', edgecolor=BRASS, linewidth=1, zorder=7))
    ax.text(9.5, 56, ar('لغة'), fontsize=18, color=GOLD, ha='center',
            va='center', fontfamily=AMIRI, zorder=8)

    # Geometric diamond motif on wall (right of panel)
    for di in range(5):
        dx = 148 + di*3
        dy = 55
        s = 3
        pts = np.array([[dx,dy+s],[dx+s,dy],[dx,dy-s],[dx-s,dy]])
        ax.add_patch(patches.Polygon(pts, facecolor='none', edgecolor=GOLD,
                                     linewidth=0.6, alpha=0.4, zorder=7))

    # ── BASEBOARD ─────────────────────────────────────────────────────────
    ax.add_patch(patches.Rectangle((0, 28), 160, 1.5,
                 facecolor='#D4C8B8', edgecolor='none', zorder=7))

    add_label_bar(fig, 'A', 'RÉCEPTION & ACCUEIL',
                  '18 m²',
                  'Desk noyer + laiton brossé · Calligraphie murale dorée · Béton ciré · Olivier en cache-pot laiton')
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# RENDER 2 — CAFÉ MAKTABA
# ══════════════════════════════════════════════════════════════════════════════
def render_cafe():
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor('#1C0E08')

    ax = fig.add_axes([0, 0.075, 1, 0.925])
    ax.set_xlim(0, 160); ax.set_ylim(0, 90)
    ax.axis('off')

    # ── FLOOR — herringbone pattern ───────────────────────────────────────
    gradient_rect(ax, 0, 0, 160, 25, '#3A2418', '#2A1A10')
    # Herringbone tiles suggestion
    for tx in range(0, 160, 8):
        for ty in range(0, 25, 4):
            angle = 45 if (tx//8 + ty//4) % 2 == 0 else -45
            # simplified: alternating slant lines
            col = '#4A2E1A' if (tx//8 + ty//4) % 2 == 0 else '#3A2210'
            ax.add_patch(patches.Rectangle((tx, ty), 7.5, 3.5,
                         facecolor=col, edgecolor='#2A1408', linewidth=0.3, alpha=0.8))

    # ── BACK WALL — bookshelves ───────────────────────────────────────────
    gradient_rect(ax, 0, 25, 90, 65, '#2C1608', '#1C0E04')
    # Shelf structure — vertical dividers
    for sdx in np.linspace(5, 88, 8):
        ax.add_patch(patches.Rectangle((sdx-0.8, 25), 1.6, 65,
                     facecolor='#4A2818', edgecolor='#3A1808', linewidth=0.5, zorder=4))
    # Horizontal shelves
    shelf_ys = [28, 36, 44, 52, 60, 68, 76, 84]
    for sy in shelf_ys:
        ax.add_patch(patches.Rectangle((5, sy), 82, 1.8,
                     facecolor='#5A3020', edgecolor='#3A1808', linewidth=0.6, zorder=5))

    # Books on shelves
    book_colors = ['#C0392B','#1B5E7A',GOLD,'#2D5016','#8B4513','#4A0080',
                   '#B5622F','#1A3A5A','#8B0000','#2A6020','#5A2D82','#C4714B',
                   TEAL, WALNUT, SAGE, '#6B3A1A']
    np.random.seed(42)
    for sy in shelf_ys[:-1]:
        bx = 6.0
        while bx < 87:
            bw = np.random.uniform(1.5, 3.5)
            bh = np.random.uniform(5, 8)
            bcol = book_colors[np.random.randint(len(book_colors))]
            ax.add_patch(patches.Rectangle((bx, sy+1.8), bw, bh,
                         facecolor=bcol, edgecolor='#1A1A1A',
                         linewidth=0.3, alpha=0.9, zorder=6))
            # Spine texture
            ax.add_patch(patches.Rectangle((bx+0.1, sy+2), 0.2, bh-0.5,
                         facecolor='white', edgecolor='none', alpha=0.08, zorder=7))
            bx += bw + 0.3

    # Decorative objects on shelves
    obj_positions = [(14, 60), (38, 52), (62, 68), (28, 76), (72, 44)]
    for ox, oy in obj_positions:
        # Vase
        ax.add_patch(patches.FancyBboxPatch((ox-1.5, oy+1.8), 3, 5,
                     boxstyle='round,pad=0.2',
                     facecolor=BRASS, edgecolor='#8A6A1A', linewidth=0.8, zorder=8))

    # ── RIGHT WALL — zellige terracotta ───────────────────────────────────
    # Zellige section (right portion of back wall)
    ax.add_patch(patches.Rectangle((90, 25), 35, 55,
                 facecolor='#B5622F', edgecolor='none', zorder=3))
    # Individual zellige tiles
    for tz_x in np.arange(91, 124, 4.5):
        for tz_y in np.arange(26, 78, 5.5):
            col = '#C4714B' if (int(tz_x/4.5)+int(tz_y/5.5))%2==0 else '#A85225'
            ax.add_patch(patches.Rectangle((tz_x, tz_y), 4, 5,
                         facecolor=col, edgecolor='#8B3A1A', linewidth=0.6, zorder=4))
            # Tile highlight
            ax.add_patch(patches.Rectangle((tz_x+0.3, tz_y+0.3), 1, 1,
                         facecolor='white', edgecolor='none', alpha=0.08, zorder=5))
    ax.text(107.5, 50, ar('قهوة'), fontsize=28, color='#3A1808', ha='center',
            va='center', fontfamily=AMIRI, alpha=0.3, zorder=6)

    # ── PLAIN WALL SEGMENT (right side) ───────────────────────────────────
    gradient_rect(ax, 125, 25, 35, 65, '#E8DDD0', '#F0E8DC')

    # ── CEILING ───────────────────────────────────────────────────────────
    gradient_rect(ax, 0, 82, 160, 8, '#1A0A04', '#2A1408')
    for bx in np.linspace(0, 160, 7):
        ax.add_patch(patches.Rectangle((bx-1, 82), 2, 8,
                     facecolor='#0E0604', edgecolor='none'))
    # Coffered pattern
    for cx_c in np.linspace(8, 152, 6):
        ax.add_patch(patches.Rectangle((cx_c-4, 82.5), 8, 7,
                     facecolor='none', edgecolor='#3A1808', linewidth=0.6))

    # LED cove warm glow
    for gs in range(25, 0, -1):
        ax.add_patch(patches.Rectangle((0, 82 - gs*0.18), 160, 0.19,
                     facecolor=WARM_LIGHT, edgecolor='none',
                     alpha=0.018*gs, zorder=2))

    # ── MARBLE COFFEE COUNTER ─────────────────────────────────────────────
    # Counter body
    ax.add_patch(patches.Rectangle((100, 5), 55, 15,
                 facecolor='#2A1208', edgecolor='#4A2010', linewidth=1.5, zorder=8))
    # Panel detailing
    for pnx in np.linspace(102, 152, 6):
        ax.add_patch(patches.Rectangle((pnx, 6), 8, 13,
                     facecolor='none', edgecolor='#4A2010', linewidth=0.6, zorder=9))
    # Marble countertop
    ax.add_patch(patches.Rectangle((98, 20), 59, 4,
                 facecolor='#E8E0D0', edgecolor=GOLD, linewidth=1.5, zorder=9))
    # Marble veins
    for mv in range(8):
        x0 = np.random.uniform(100, 155)
        ax.plot([x0, x0+np.random.uniform(-8,8)],
                [20, 24], color='#B0A080', lw=0.5, alpha=0.5, zorder=10)

    # Espresso machine
    ax.add_patch(patches.FancyBboxPatch((115, 21), 14, 10,
                 boxstyle='round,pad=0.3',
                 facecolor='#C0C0C0', edgecolor='#888', linewidth=1, zorder=11))
    ax.add_patch(Circle((122, 26), 3, facecolor='#888', edgecolor='#666', zorder=12))
    ax.add_patch(Circle((122, 26), 2, facecolor='#555', edgecolor='none', zorder=13))
    # Coffee cups on counter
    for cx_cup in [107, 110, 137, 140, 143]:
        ax.add_patch(patches.FancyBboxPatch((cx_cup-1.2, 21.2), 2.4, 2,
                     boxstyle='round,pad=0.1',
                     facecolor='white', edgecolor='#CCCCCC', linewidth=0.5, zorder=11))

    # ── PENDANT LANTERNS ──────────────────────────────────────────────────
    lantern_positions = [28, 55, 80]
    for lx_l in lantern_positions:
        # Cord
        ax.plot([lx_l, lx_l], [82, 70], color='#666', lw=0.8, zorder=10)
        # Lantern body — hexagonal
        hex_a = np.linspace(0, 2*np.pi, 7)
        hx = lx_l + 5*np.cos(hex_a)
        hy = 65 + 7*np.sin(hex_a)
        ax.fill(hx, hy, facecolor=BRASS, edgecolor='#8A6A1A', linewidth=1.5, zorder=11)
        # Lattice on lantern
        for lat in range(6):
            ang = lat*60
            lax = lx_l + 3.5*np.cos(np.radians(ang))
            lay = 65 + 4.5*np.sin(np.radians(ang))
            ax.plot([lx_l, lax], [65, lay], color='#8A6A1A', lw=0.8, alpha=0.5, zorder=12)
        # Inner light
        ax.add_patch(Circle((lx_l, 65), 2.5, facecolor='#FFF0A0',
                             edgecolor='none', alpha=0.95, zorder=12))
        # Glow below
        glow(ax, lx_l, 62, 18, WARM_LIGHT, alpha_center=0.4, steps=25, zorder=5)
        # Light pool on floor/tables
        glow(ax, lx_l, 10, 10, WARM_LIGHT, alpha_center=0.15, steps=15, zorder=3)

    # ── CAFÉ TABLES ───────────────────────────────────────────────────────
    tables = [(28, 9, 7), (55, 9, 7), (28, 18, 5), (55, 18, 5)]
    for tx_t, ty_t, tr in tables:
        # Table shadow
        ax.add_patch(Circle((tx_t+1, ty_t-0.5), tr, facecolor='#1A0A04',
                             edgecolor='none', alpha=0.4, zorder=6))
        # Table
        ax.add_patch(Circle((tx_t, ty_t), tr, facecolor=BRASS,
                             edgecolor='#8A6A1A', linewidth=1.5, zorder=7))
        ax.add_patch(Circle((tx_t, ty_t), tr-1, facecolor='#C9A84C',
                             edgecolor='none', alpha=0.5, zorder=8))
        # Table items
        ax.add_patch(Circle((tx_t-1, ty_t), 1.2, facecolor='white',
                             edgecolor='#DDD', linewidth=0.5, zorder=9))  # cup

    # ── CHAIRS / STOOLS ───────────────────────────────────────────────────
    chair_pos = [(20,8),(36,8),(20,18),(36,18),(47,9),(63,9),(47,18),(63,18)]
    for cpx, cpy in chair_pos:
        ax.add_patch(patches.FancyBboxPatch((cpx-2, cpy-2.5), 4, 3,
                     boxstyle='round,pad=0.4',
                     facecolor='#8B4513', edgecolor='#6A3010', linewidth=0.8, zorder=6))

    # ── MAJLIS CORNER (low seating) ───────────────────────────────────────
    # Low bench / floor cushions near left wall
    for cs in range(4):
        ax.add_patch(patches.FancyBboxPatch((2, 4+cs*5), 6, 4,
                     boxstyle='round,pad=0.5',
                     facecolor=['#C4714B','#1B5E7A',GOLD,'#6B8F71'][cs],
                     edgecolor='none', alpha=0.85, zorder=7))

    add_label_bar(fig, 'B', 'CAFÉ "MAKTABA" — المكتبة',
                  '40 m²',
                  'Étagères noyer floor-to-ceiling · Comptoir marbre · Lanternes laiton · Zellige terracotta · Majlis coussins')
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# RENDER 3 — SALLE DE COURS GROUPES
# ══════════════════════════════════════════════════════════════════════════════
def render_classroom():
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor('#EEF4F8')

    ax = fig.add_axes([0, 0.075, 1, 0.925])
    ax.set_xlim(0, 160); ax.set_ylim(0, 90)
    ax.axis('off')

    # ── FLOOR — light grey wood ───────────────────────────────────────────
    gradient_rect(ax, 0, 0, 160, 25, '#D8D0C8', '#E4DED8')
    # Wood plank lines
    for ply in np.linspace(0, 25, 20):
        ax.plot([0, 160], [ply, ply], color='#C8C0B8', lw=0.3, alpha=0.6)
    for plx in np.linspace(0, 160, 22):
        ax.plot([plx, plx], [0, 25], color='#C8C0B8', lw=0.2, alpha=0.4)

    # ── BACK WALL — acoustic panel + SMART board ──────────────────────────
    gradient_rect(ax, 0, 25, 160, 65, '#EAF0F4', '#F0F5F8')

    # Acoustic panel (sage) behind whiteboard
    ax.add_patch(patches.Rectangle((20, 60), 120, 22,
                 facecolor='#8FAF94', edgecolor='none', zorder=3))
    # Acoustic perforations
    for px in np.arange(22, 138, 3):
        for py in np.arange(62, 81, 3):
            ax.add_patch(Circle((px, py), 0.4, facecolor='#6B8F71',
                                edgecolor='none', alpha=0.5, zorder=4))

    # ── SMART BOARD ───────────────────────────────────────────────────────
    # Board frame
    ax.add_patch(patches.FancyBboxPatch((25, 62), 110, 18,
                 boxstyle='round,pad=0.5',
                 facecolor='#1A1A2E', edgecolor='#333360', linewidth=2, zorder=8))
    # Screen content — language lesson
    ax.add_patch(patches.Rectangle((27, 63.5), 106, 15,
                 facecolor='#0A0A20', edgecolor='none', zorder=9))
    # Screen content
    ax.text(80, 74, 'كيف حالك؟', fontsize=20, color='#4FC3F7',
            ha='center', va='center', fontfamily=AMIRI, zorder=10)
    ax.text(80, 70, 'Comment allez-vous ?', fontsize=11, color='#90CAF9',
            ha='center', va='center', fontfamily=FONT, zorder=10)
    ax.text(80, 66, 'How are you?  /  ¿Cómo estás?', fontsize=9, color='#64B5F6',
            ha='center', va='center', fontfamily=FONT, zorder=10)
    # CLR logo small on board
    ax.text(120, 63, 'CLR', fontsize=6, color=GOLD, ha='right',
            va='bottom', fontfamily=FONT, zorder=10, alpha=0.6)
    # Board stand / mount
    ax.add_patch(patches.Rectangle((77, 60), 6, 2.5,
                 facecolor='#333', edgecolor='none', zorder=8))

    # ── GLASS PARTITION WALL (right side) ────────────────────────────────
    # Glass wall with mashrabiya film
    ax.add_patch(patches.Rectangle((148, 25), 12, 65,
                 facecolor='#B8D4E0', edgecolor='#90B8CC', linewidth=1.5,
                 alpha=0.35, zorder=3))
    # Mashrabiya geometric pattern on glass
    for mx in np.arange(149, 158, 3.5):
        for my in np.arange(27, 88, 3.5):
            # Star/diamond pattern
            s = 1.2
            pts = np.array([[mx,my+s],[mx+s,my],[mx,my-s],[mx-s,my]])
            ax.add_patch(patches.Polygon(pts, facecolor='none',
                                          edgecolor=TEAL, linewidth=0.6, alpha=0.6, zorder=5))
            # Inner square
            s2 = 0.6
            pts2 = np.array([[mx,my+s2],[mx+s2,my],[mx,my-s2],[mx-s2,my]])
            ax.add_patch(patches.Polygon(pts2, facecolor=TEAL,
                                          edgecolor='none', alpha=0.1, zorder=5))

    # ── CEILING ───────────────────────────────────────────────────────────
    gradient_rect(ax, 0, 82, 160, 8, '#2A1A10', '#1C1008')
    for bx in np.linspace(0, 160, 7):
        ax.add_patch(patches.Rectangle((bx-1, 82), 2, 8,
                     facecolor='#140C06', edgecolor='none'))
    # LED cove glow
    for gs in range(22, 0, -1):
        ax.add_patch(patches.Rectangle((0, 82-gs*0.2), 160, 0.2,
                     facecolor='#D4F0FF', edgecolor='none',
                     alpha=0.015*gs, zorder=2))

    # ── LINEAR LED PENDANT ────────────────────────────────────────────────
    for led_x in [40, 80, 120]:
        ax.plot([led_x-15, led_x+15], [78, 78], color='#E8F4FF', lw=3, alpha=0.9, zorder=10)
        # Glow
        for lg in range(15, 0, -1):
            ax.add_patch(patches.Rectangle((led_x-15, 78-lg*0.3), 30, 0.3,
                         facecolor='#D4F0FF', edgecolor='none',
                         alpha=0.04*lg, zorder=9))
        # Suspension wires
        for wx in [led_x-15, led_x, led_x+15]:
            ax.plot([wx, wx], [78, 82], color='#888', lw=0.5, zorder=10)

    # ── CLASSROOM TABLES (U-shape arrangement) ────────────────────────────
    # Table rows — light wood / white
    table_positions = [
        # (x, y, w, h) — from student perspective
        (15, 8, 18, 5),   (42, 8, 18, 5),   (69, 8, 18, 5),
        (96, 8, 18, 5),   (123, 8, 18, 5),
        (15, 16, 18, 5),  (42, 16, 18, 5),  (69, 16, 18, 5),
        (96, 16, 18, 5),  (123, 16, 18, 5),
    ]
    for tx, ty, tw, th in table_positions:
        # Shadow
        ax.add_patch(patches.Rectangle((tx+1, ty-0.5), tw, th,
                     facecolor='#C0B8B0', edgecolor='none', alpha=0.3, zorder=5))
        # Table surface
        ax.add_patch(patches.FancyBboxPatch((tx, ty), tw, th,
                     boxstyle='round,pad=0.3',
                     facecolor='#F0ECE4', edgecolor='#D8D0C4', linewidth=1, zorder=6))
        # Wood edge strip
        ax.add_patch(patches.Rectangle((tx, ty), tw, 0.8,
                     facecolor='#C9A84C', edgecolor='none', alpha=0.4, zorder=7))
        # Items on table
        ax.add_patch(patches.Rectangle((tx+2, ty+1.5), 6, 2,
                     facecolor='#F8F4EE', edgecolor='#E0D8CC', linewidth=0.4, zorder=8))  # notebook
        ax.add_patch(Circle((tx+14, ty+2.5), 1.2, facecolor='white',
                             edgecolor='#DDD', linewidth=0.4, zorder=8))  # cup

    # Chairs (teal/sage upholstery)
    chair_colors = [TEAL, SAGE, '#B5622F', TEAL, SAGE]
    for row_y in [6, 14]:
        for ci, cx in enumerate([16, 43, 70, 97, 124]):
            ax.add_patch(patches.FancyBboxPatch((cx+2, row_y-3), 14, 3.5,
                         boxstyle='round,pad=0.3',
                         facecolor=chair_colors[ci % len(chair_colors)],
                         edgecolor='none', alpha=0.8, zorder=5))

    # ── SIDE WALL — resource shelf ────────────────────────────────────────
    ax.add_patch(patches.Rectangle((0, 30), 12, 50,
                 facecolor='#3D2314', edgecolor='#2A1408', linewidth=1, zorder=4))
    for shy in np.linspace(32, 78, 7):
        ax.add_patch(patches.Rectangle((1, shy), 10, 0.8,
                     facecolor='#5A3020', edgecolor='none', zorder=5))
    # Reference books
    for bk_y in [34, 42, 50, 58, 66, 74]:
        for bk_x in np.linspace(1.5, 10, 5):
            bcol = book_colors[np.random.randint(len(book_colors))]
            ax.add_patch(patches.Rectangle((bk_x, bk_y), 1.5, 7,
                         facecolor=bcol, edgecolor='none', alpha=0.85, zorder=6))

    # World clock on wall
    ax.add_patch(patches.Rectangle((6, 82), 14, 0.8,
                 facecolor='#F8F4EE', edgecolor='#E0D8CC', linewidth=0.5, zorder=6))

    add_label_bar(fig, 'C', 'SALLE DE COURS — GROUPES',
                  '35 m²',
                  'SMART Board 86" · Tables modulables · Film mashrabiya · Panneaux phoniques sauge · LED 4000K dimmable')
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# RENDER 4 — SALON SEMI-PRIVÉ
# ══════════════════════════════════════════════════════════════════════════════
def render_semiprive():
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor('#2A1A1A')

    ax = fig.add_axes([0, 0.075, 1, 0.925])
    ax.set_xlim(0, 160); ax.set_ylim(0, 90)
    ax.axis('off')

    # ── FLOOR — dark herringbone ──────────────────────────────────────────
    gradient_rect(ax, 0, 0, 160, 26, '#2A1A0E', '#1C1008')
    # Herringbone dark wood
    for hx in range(0, 160, 12):
        for hy in range(0, 26, 8):
            col = '#2E1C10' if (hx//12+hy//8)%2==0 else '#241408'
            ax.add_patch(patches.Rectangle((hx, hy), 11, 7.5,
                         facecolor=col, edgecolor='#180E06', linewidth=0.4, alpha=0.9))

    # ── NAVY ACCENT WALL (full back wall) ────────────────────────────────
    gradient_rect(ax, 0, 26, 160, 64, '#0A1520', '#0D1B2A')

    # Geometric gold pattern on wall
    for gi in np.linspace(5, 155, 16):
        for gj in np.linspace(30, 85, 10):
            s = 2.5
            pts = np.array([[gi,gj+s],[gi+s,gj],[gi,gj-s],[gi-s,gj]])
            ax.add_patch(patches.Polygon(pts, facecolor='none',
                                          edgecolor=GOLD, linewidth=0.3,
                                          alpha=0.08, zorder=2))

    # ── CALLIGRAPHY ARTWORK (center panel) ───────────────────────────────
    # Gold frame
    for lw, alpha in [(3, 0.5), (1, 0.9), (0.4, 0.6)]:
        ax.add_patch(patches.FancyBboxPatch((40, 52), 80, 30,
                     boxstyle='round,pad=0.5',
                     facecolor='none', edgecolor=GOLD, linewidth=lw, alpha=alpha, zorder=4))
    # Dark inner panel
    ax.add_patch(patches.Rectangle((42, 53), 76, 28,
                 facecolor='#060E18', edgecolor='none', zorder=4))
    # Calligraphy
    ax.text(80, 70, ar('الحياة رحلة'), fontsize=32, color=GOLD,
            ha='center', va='center', fontfamily=AMIRI, zorder=6)
    ax.text(80, 60, 'La vie est un voyage', fontsize=10, color='#8A9BB0',
            ha='center', va='center', fontfamily=FONT, style='italic', zorder=6)
    # Frame corner ornaments
    for cx_o, cy_o in [(40,52),(120,52),(40,82),(120,82)]:
        ax.add_patch(Circle((cx_o, cy_o), 2.5, facecolor=GOLD,
                             edgecolor='none', alpha=0.7, zorder=5))

    # ── CEILING ───────────────────────────────────────────────────────────
    gradient_rect(ax, 0, 82, 160, 8, '#2A1A0A', '#1A0E06')
    for bx in np.linspace(0, 160, 7):
        ax.add_patch(patches.Rectangle((bx-1.2, 82), 2.4, 8,
                     facecolor='#120A04', edgecolor='none'))
    # Warm glow from cove
    for gs in range(20, 0, -1):
        ax.add_patch(patches.Rectangle((0, 82-gs*0.22), 160, 0.23,
                     facecolor=WARM_LIGHT, edgecolor='none',
                     alpha=0.025*gs, zorder=2))

    # ── STATEMENT PENDANT LIGHT ───────────────────────────────────────────
    # Main cable
    ax.plot([80, 80], [82, 68], color='#888', lw=1, zorder=10)
    # Grand lantern
    hex_a = np.linspace(0, 2*np.pi, 7)
    outer_r = 8
    hx_o = 80 + outer_r*np.cos(hex_a)
    hy_o = 60 + outer_r*1.3*np.sin(hex_a)
    ax.fill(hx_o, hy_o, facecolor=BRASS, edgecolor='#8A6A1A', linewidth=2, zorder=11)
    # Inner hexagon
    inner_r = 5
    hx_i = 80 + inner_r*np.cos(hex_a)
    hy_i = 60 + inner_r*1.1*np.sin(hex_a)
    ax.fill(hx_i, hy_i, facecolor='#FFF0A0', edgecolor='none', alpha=0.95, zorder=12)
    # Lattice spokes
    for ang in range(0, 360, 60):
        lx_s = 80 + 6*np.cos(np.radians(ang))
        ly_s = 60 + 7*np.sin(np.radians(ang))
        ax.plot([80, lx_s], [60, ly_s], color='#8A6A1A', lw=1.2, alpha=0.6, zorder=12)
    # Glow effect
    glow(ax, 80, 58, 30, WARM_LIGHT, alpha_center=0.5, steps=30, zorder=5)
    glow(ax, 80, 20, 25, WARM_LIGHT, alpha_center=0.15, steps=20, zorder=3)

    # ── ROUND WALNUT TABLE ────────────────────────────────────────────────
    # Table shadow
    ax.add_patch(Circle((82, 13), 23, facecolor='#0A0604', edgecolor='none', alpha=0.6, zorder=6))
    # Table
    ax.add_patch(Circle((80, 14), 22, facecolor='#3D2010', edgecolor='#5A3020', linewidth=2, zorder=7))
    # Table grain
    for tg in range(8):
        angle = tg*22.5
        tx_g = 80 + 10*np.cos(np.radians(angle))
        ty_g = 14 + 8*np.sin(np.radians(angle))
        ax.plot([80, tx_g], [14, ty_g], color='#5A3020', lw=0.4, alpha=0.4, zorder=8)
    # Table surface sheen
    ax.add_patch(Circle((74, 18), 5, facecolor='white', edgecolor='none', alpha=0.06, zorder=9))
    # Table edge
    ax.add_patch(Circle((80, 14), 22, facecolor='none', edgecolor=GOLD, linewidth=1.5, zorder=9))
    # Items on table
    # Notebooks
    ax.add_patch(patches.FancyBboxPatch((66, 12), 9, 5,
                 boxstyle='round,pad=0.2',
                 facecolor='#F8F4EE', edgecolor='#E0D8CC', linewidth=0.5, zorder=10))
    ax.add_patch(patches.FancyBboxPatch((85, 10), 9, 5,
                 boxstyle='round,pad=0.2',
                 facecolor='#F0EBDC', edgecolor='#E0D8CC', linewidth=0.5, zorder=10))
    # Cups
    for cup_pos in [(72, 20), (90, 19)]:
        ax.add_patch(patches.FancyBboxPatch((cup_pos[0]-1.2, cup_pos[1]-1.2), 2.4, 2.4,
                     boxstyle='round,pad=0.2',
                     facecolor='white', edgecolor='#CCC', linewidth=0.5, zorder=10))
    # Flower centerpiece
    for petal in range(8):
        pa = petal*45
        px = 80 + 2.5*np.cos(np.radians(pa))
        py = 14 + 2*np.sin(np.radians(pa))
        ax.add_patch(Circle((px, py), 1.5, facecolor='#E8D4A0',
                             edgecolor='none', alpha=0.8, zorder=11))
    ax.add_patch(Circle((80, 14), 1.5, facecolor='#F5C842',
                         edgecolor='none', zorder=12))

    # ── UPHOLSTERED CHAIRS ────────────────────────────────────────────────
    chair_angles = [0, 90, 180, 270]
    chair_col = '#C4714B'  # terracotta
    for ca in chair_angles:
        dist = 25
        chx = 80 + dist*np.cos(np.radians(ca))
        chy = 14 + dist*0.65*np.sin(np.radians(ca))
        # Chair seat
        ax.add_patch(patches.FancyBboxPatch((chx-6, chy-4), 12, 8,
                     boxstyle='round,pad=0.8',
                     facecolor=chair_col, edgecolor='#8B4513', linewidth=1, zorder=7))
        # Chair back
        back_x = chx + 5*np.cos(np.radians(ca))
        back_y = chy + 5*0.65*np.sin(np.radians(ca))
        ax.add_patch(patches.FancyBboxPatch((back_x-5, back_y-3), 10, 7,
                     boxstyle='round,pad=0.8',
                     facecolor='#A85225', edgecolor='#7A3A1A', linewidth=1, zorder=7))
        # Gold stud detail
        for stud_ang in range(0, 360, 45):
            sx = chx + 5.5*np.cos(np.radians(stud_ang))
            sy = chy + 3.8*np.sin(np.radians(stud_ang))
            ax.add_patch(Circle((sx, sy), 0.4, facecolor=BRASS,
                                 edgecolor='none', zorder=8))

    # ── SIDE WALLS ────────────────────────────────────────────────────────
    # Left wall — wood panel
    gradient_rect(ax, 0, 26, 20, 64, '#3A2010', '#2A1808')
    for spx in np.linspace(2, 18, 8):
        ax.add_patch(patches.Rectangle((spx-0.6, 28), 1.2, 52,
                     facecolor='#4A2818', edgecolor='#2A1008', linewidth=0.3))

    # Right wall — bookcase
    gradient_rect(ax, 140, 26, 20, 64, '#2A1408', '#1C0E04')
    for bsy in np.linspace(30, 80, 8):
        ax.add_patch(patches.Rectangle((141, bsy), 18, 0.6,
                     facecolor='#4A2818', edgecolor='none'))
    for bk_y2 in [32, 40, 48, 56, 64, 72]:
        for bk_x2 in np.linspace(141.5, 158, 6):
            col2 = book_colors[np.random.randint(len(book_colors))]
            ax.add_patch(patches.Rectangle((bk_x2, bk_y2), 2.2, 7,
                         facecolor=col2, edgecolor='none', alpha=0.85, zorder=5))

    # ── DRAPES / CURTAINS ─────────────────────────────────────────────────
    # Lin ivory curtains left
    for fold in np.linspace(0, 18, 6):
        ax.add_patch(patches.Rectangle((fold, 26), 2.5, 56,
                     facecolor='#FAF6EF', edgecolor='none', alpha=0.7, zorder=3))
        ax.add_patch(patches.Rectangle((fold+1, 26), 0.5, 56,
                     facecolor='#E8E0D0', edgecolor='none', alpha=0.4, zorder=3))

    # Curtain rod
    ax.add_patch(patches.Rectangle((0, 81), 20, 1, facecolor=BRASS,
                                   edgecolor='none', zorder=5))

    add_label_bar(fig, 'D', 'SALON SEMI-PRIVÉ',
                  '22 m²',
                  'Table ronde noyer · Fauteuils cuir terracotta · Mur navy + calligraphie · Suspension laiton grand format')
    return fig

# ══════════════════════════════════════════════════════════════════════════════
# RENDER 5 — OVERVIEW COMPOSITE (all 4 zones as mosaic)
# ══════════════════════════════════════════════════════════════════════════════
def render_overview():
    """2×2 grid showing all zones at a glance."""
    fig = plt.figure(figsize=(W, H))
    fig.patch.set_facecolor(NAVY)

    # Title bar
    ax_title = fig.add_axes([0, 0.91, 1, 0.09])
    ax_title.set_facecolor(NAVY); ax_title.axis('off')
    ax_title.set_xlim(0,1); ax_title.set_ylim(0,1)
    ax_title.axhline(0.08, color=GOLD, lw=2.5)
    ax_title.text(0.5, 0.58, 'AL-MAKTABA — CENTRE LINGUISTIQUE DE RIYAD — CONCEPT VISUEL D\'ENSEMBLE',
                  fontsize=12, color=GOLD, fontweight='bold', ha='center', va='center',
                  fontfamily=FONT)
    _MID_OVERVIEW = '#8A9BB0'
    ax_title.text(0.5, 0.18, 'Nord Riyad  ·  160 m²  ·  6 zones  ·  Budget 280 000 SAR  ·  Livraison 10 semaines',
                  fontsize=8, color=_MID_OVERVIEW, ha='center', va='center', fontfamily=FONT)

    grid_positions = [
        (0.01, 0.455, 0.485, 0.445, 'A', 'RÉCEPTION'),
        (0.505, 0.455, 0.485, 0.445, 'B', 'CAFÉ MAKTABA'),
        (0.01, 0.01, 0.485, 0.435, 'C', 'SALLE DE COURS'),
        (0.505, 0.01, 0.485, 0.435, 'D', 'SEMI-PRIVÉ'),
    ]

    render_fns = [render_reception, render_cafe, render_classroom, render_semiprive]
    zone_labels = ['A — RÉCEPTION', 'B — CAFÉ MAKTABA', 'C — SALLE COURS', 'D — SEMI-PRIVÉ']
    zone_cols = [GOLD, '#C4714B', TEAL, '#9B7BC4']

    for (lft, bot, w, h, zid, zname), rfn, zcol in zip(grid_positions, render_fns, zone_cols):
        # Create the sub-render
        sub_fig = rfn()
        buf = __import__('io').BytesIO()
        sub_fig.savefig(buf, format='png', dpi=100, bbox_inches='tight',
                        facecolor=sub_fig.get_facecolor())
        buf.seek(0)
        plt.close(sub_fig)

        import matplotlib.image as mpimg
        img = mpimg.imread(buf)

        ax_sub = fig.add_axes([lft, bot, w, h])
        ax_sub.imshow(img, aspect='auto')
        ax_sub.axis('off')

        # Zone badge overlay
        badge = plt.Rectangle((0.02, 0.88), 0.15, 0.1,
                               transform=ax_sub.transAxes,
                               facecolor=zcol, edgecolor='none', zorder=10)
        ax_sub.add_patch(badge)
        ax_sub.text(0.095, 0.93, f'{zid}  {zname}', transform=ax_sub.transAxes,
                    fontsize=6.5, color=NAVY if zcol==GOLD else 'white',
                    fontweight='bold', ha='center', va='center',
                    fontfamily=FONT, zorder=11)

        # Gold border
        for spine in ax_sub.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor(GOLD)
            spine.set_linewidth(1.5)

    return fig

# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
book_colors = ['#C0392B','#1B5E7A',GOLD,'#2D5016','#8B4513','#4A0080',
               '#B5622F','#1A3A5A','#8B0000','#2A6020','#5A2D82','#C4714B',
               TEAL, WALNUT, SAGE, '#6B3A1A']

np.random.seed(42)

renders = [
    ('Reception', render_reception),
    ('Cafe', render_cafe),
    ('Classroom', render_classroom),
    ('SemiPrive', render_semiprive),
    ('Overview', render_overview),
]

# Save individual PNGs + combined PDF
with PdfPages(OUTPUT_PDF) as pdf:
    for name, fn in renders:
        print(f'Rendering {name}...', end=' ', flush=True)
        fig = fn()
        fig.savefig(f'/home/user/ABD-BND/render_{name}.png',
                    dpi=180, bbox_inches='tight',
                    facecolor=fig.get_facecolor())
        pdf.savefig(fig, dpi=150, bbox_inches='tight',
                    facecolor=fig.get_facecolor())
        plt.close(fig)
        print('✓')

print(f'\nDone. PDF: {OUTPUT_PDF}')
