#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLR Interior Design Concept Document
Space: North Riyadh — Raw shell office
Concept: Al-Maktaba (Arabic-Contemporary Fusion)
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, FancyArrowPatch
from matplotlib.gridspec import GridSpec
import numpy as np
import io

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, Image, PageBreak, HRFlowable,
                                 KeepTogether)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas as pdfcanvas

# ─── PALETTE ────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor('#0D1B2A')
GOLD      = colors.HexColor('#C9A84C')
GOLD_LIGHT= colors.HexColor('#E8C97A')
SAND      = colors.HexColor('#F7F0E3')
TEAL      = colors.HexColor('#1B5E7A')
DARK_WALL = colors.HexColor('#1C2B1A')
TERRA     = colors.HexColor('#C4714B')
WALNUT    = colors.HexColor('#5C3D2E')
CREAM     = colors.HexColor('#FAF6EF')
WHITE     = colors.white
MID_GRAY  = colors.HexColor('#7F8C8D')
DARK_GRAY = colors.HexColor('#2C3E50')
SAGE      = colors.HexColor('#7A9E7E')
BRASS     = colors.HexColor('#B5860D')
WARM_WHITE= colors.HexColor('#FFF8EE')
RED_ACC   = colors.HexColor('#C0392B')

W, H = A4
OUTPUT = '/home/user/ABD-BND/CLR_Design_Concept.pdf'

# ═══════════════════════════════════════════════════════════════════════════
# MATPLOTLIB FIGURES
# ═══════════════════════════════════════════════════════════════════════════

def fig_to_image(fig, wm=165, hm=100):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return Image(buf, width=wm*mm, height=hm*mm)

# ── 1. COLOUR PALETTE ───────────────────────────────────────────────────────
def make_palette():
    palettes = [
        ('#0D1B2A', 'NAVY\nMurs accent\nMobilier dark'),
        ('#C9A84C', 'OR / LAITON\nAccents métal\nLuminaires'),
        ('#F7F0E3', 'SABLE CHAUD\nMurs principaux\nPlafond'),
        ('#5C3D2E', 'NOYER\nBoiseries\nÉtagères'),
        ('#C4714B', 'TERRA\nCoussins\nArt mural'),
        ('#7A9E7E', 'SAUGE\nPlantes\nPanneau phoniq.'),
        ('#1B5E7A', 'TEAL DEEP\nSignalétique\nAccents cool'),
        ('#FAF6EF', 'CRÈME IVOIRE\nTextiles\nArabesques'),
    ]
    fig, axes = plt.subplots(1, 8, figsize=(14, 2.8))
    fig.patch.set_facecolor('#0D1B2A')
    for ax, (col, lbl) in zip(axes, palettes):
        ax.set_facecolor(col)
        ax.set_xlim(0,1); ax.set_ylim(0,1)
        ax.axis('off')
        lines = lbl.split('\n')
        text_col = 'white' if col in ['#0D1B2A','#5C3D2E','#1B5E7A','#C4714B'] else '#0D1B2A'
        for i, ln in enumerate(lines):
            fs = 7.5 if i == 0 else 6
            fw = 'bold' if i == 0 else 'normal'
            ax.text(0.5, 0.75 - i*0.18, ln, ha='center', va='center',
                    fontsize=fs, color=text_col, fontweight=fw,
                    transform=ax.transAxes)
    plt.suptitle('PALETTE MATIÈRES & COULEURS — Centre Linguistique de Riyad',
                 color='#C9A84C', fontsize=10, fontweight='bold', y=1.04)
    plt.tight_layout(pad=0.3)
    return fig_to_image(fig, 165, 45)

# ── 2. FLOOR PLAN ────────────────────────────────────────────────────────────
def make_floorplan():
    fig, ax = plt.subplots(figsize=(11, 7))
    fig.patch.set_facecolor('#1A1A1A')
    ax.set_facecolor('#1A1A1A')
    ax.set_aspect('equal')
    ax.set_xlim(-1, 22); ax.set_ylim(-1, 14)
    ax.axis('off')

    wall_kw = dict(linewidth=3.5, edgecolor='#C9A84C', facecolor='#2A2A2A')
    door_kw = dict(linewidth=1.5, edgecolor='#C9A84C', facecolor='none', linestyle='--')

    # ── OUTER WALLS ──
    outer = patches.Rectangle((0, 0), 21, 13, **wall_kw, zorder=2)
    ax.add_patch(outer)
    inner = patches.Rectangle((0.3, 0.3), 20.4, 12.4, facecolor='#F7F0E3',
                                edgecolor='none', zorder=3)
    ax.add_patch(inner)

    # ── ZONES ──
    zones = [
        ((0.3, 7.5), (5.2, 4.9), '#E8C97A', 0.18, 'ZONE A\nRÉCEPTION\n& ACCUEIL'),
        ((0.3, 0.3), (8.5, 7.2), '#FAF6EF', 0.22, 'ZONE B\nCAFÉ\n"MAKTABA"\n40–45 m²'),
        ((5.5, 7.5), (9.0, 4.9), '#E8F4F8', 0.22, 'ZONE C\nSALLE 1\nGROUPES\n35–40 m²'),
        ((14.5, 7.5), (6.2, 5.0), '#EDF5EC', 0.22, 'ZONE D\nSALLE 2\nSEMI-PRIVÉ\n20–25 m²'),
        ((8.5, 0.3), (6.0, 7.2), '#F0EBF5', 0.22, 'ZONE E\nSALLE 3\nCOURS PART.\n25 m²'),
        ((14.5, 0.3), (6.2, 7.2), '#EEF5FA', 0.22, 'ZONE F\nADMIN &\nBURO\n20 m²'),
        ((20.7, 5.5), (0.01, 2.5), '#D4EDDA', 0.22, ''),
        ((14.5, 5.5), (0.3, 2.0), '#F7DCE3', 0.22, ''),
    ]
    zone_colors_plt = ['#E8C97A22','#FAF6EF88','#E8F4F888','#EDF5EC88',
                       '#F0EBF588','#EEF5FA88','#D4EDDA88','#F7DCE388']

    zone_defs = [
        # (x, y, w, h, fill_hex, alpha, label)
        (0.3, 7.5, 5.2, 4.9, '#FFF8DC', 0.7, 'A — RÉCEPTION\n& ACCUEIL\n18 m²'),
        (0.3, 0.3, 8.2, 7.2, '#E8F4E8', 0.5, 'B — CAFÉ\n"MAKTABA"\n40 m²'),
        (5.5, 7.5, 9.0, 4.9, '#E8EEF8', 0.5, 'C — SALLE 1\nCOURS GROUPES\n35 m²'),
        (14.5, 7.5, 6.2, 4.9, '#F5EDE8', 0.5, 'D — SALLE 2\nSEMI-PRIVÉ\n22 m²'),
        (8.5, 0.3, 6.0, 7.2, '#EDE8F5', 0.5, 'E — COURS\nPARTICULIERS\n25 m²'),
        (14.5, 0.3, 6.2, 7.2, '#E8F5F5', 0.5, 'F — ADMIN\n& BACK-OFFICE\n20 m²'),
    ]

    zone_label_colors = ['#7B5A00','#1A4A1A','#1A2A5A','#5A2A1A','#3A1A5A','#1A4A4A']
    for i, (x, y, w, h, fc, alpha, lbl) in enumerate(zone_defs):
        r = patches.Rectangle((x, y), w, h, facecolor=fc, edgecolor='#999999',
                               linewidth=0.8, alpha=alpha, zorder=4)
        ax.add_patch(r)
        cx, cy = x + w/2, y + h/2
        for j, ln in enumerate(lbl.split('\n')):
            fs = 7.5 if j == 0 else 6
            fw = 'bold' if j == 0 else 'normal'
            ax.text(cx, cy + 0.5 - j*0.7, ln, ha='center', va='center',
                    fontsize=fs, color=zone_label_colors[i], fontweight=fw, zorder=8)

    # ── INTERNAL WALLS ──
    walls_int = [
        ((5.5, 7.5), (0.25, 4.9)),   # A/B separator
        ((5.5, 0.3), (0.25, 7.2)),   # B/E separator
        ((14.5, 0.3),(0.25, 12.1)),  # E+F / right separator
        ((5.5, 7.5), (9.25, 0.25)),  # C/D bottom of upper
        ((8.5, 0.3), (0.25, 7.2)),   # B/E
    ]
    for (x,y),(w,h) in walls_int:
        r = patches.Rectangle((x,y), w, h, facecolor='#888888',
                               edgecolor='#C9A84C', linewidth=0.5, zorder=6)
        ax.add_patch(r)

    # Glass wall marker
    for x in [5.5, 14.5]:
        ax.plot([x, x], [7.5, 12.4], color='#4FC3F7', linewidth=3,
                linestyle='-', alpha=0.8, zorder=7)
    ax.text(10.0, 12.0, '— CLOISON VITRÉE —', color='#4FC3F7', fontsize=7,
            ha='center', va='center', zorder=9)

    # ── FURNITURE ICONS ──
    # Reception desk
    desk_r = patches.Rectangle((0.6, 10.0), 3.5, 1.2, facecolor='#5C3D2E',
                                edgecolor='#C9A84C', linewidth=1, zorder=8)
    ax.add_patch(desk_r)
    ax.text(2.35, 10.6, 'Accueil', ha='center', va='center',
            fontsize=5.5, color='white', fontweight='bold', zorder=9)

    # Café tables
    cafe_positions = [(1.5,4.0),(2.8,4.0),(4.2,4.0),(1.5,2.5),(2.8,2.5),(4.2,2.5),
                      (1.5,1.2),(2.8,1.2),(4.2,1.2)]
    for cx, cy in cafe_positions:
        c = Circle((cx, cy), 0.4, facecolor='#C9A84C', edgecolor='#5C3D2E',
                   linewidth=1, zorder=8, alpha=0.8)
        ax.add_patch(c)

    # Bookshelf along wall
    shelf = patches.Rectangle((0.3, 5.5), 0.6, 4.5, facecolor='#5C3D2E',
                               edgecolor='#C9A84C', linewidth=0.8, zorder=8)
    ax.add_patch(shelf)
    ax.text(0.6, 7.75, 'Books', ha='center', va='center',
            fontsize=4.5, color='#E8C97A', rotation=90, zorder=9)

    # Classroom 1 tables
    cl1_tables = [(7.0, 10.5),(8.5, 10.5),(10.0,10.5),(7.0,9.0),(8.5,9.0),(10.0,9.0),
                  (7.0, 11.8),(8.5,11.8),(10.0,11.8)]
    for cx, cy in cl1_tables:
        r = patches.Rectangle((cx-0.45, cy-0.3), 0.9, 0.6, facecolor='#DDEEFF',
                               edgecolor='#1B5E7A', linewidth=0.7, zorder=8, alpha=0.9)
        ax.add_patch(r)

    # Whiteboard Salle 1
    wb1 = patches.Rectangle((5.7, 11.8), 8.6, 0.35, facecolor='white',
                              edgecolor='#1B5E7A', linewidth=1.5, zorder=8)
    ax.add_patch(wb1)
    ax.text(10.0, 11.97, '⬛ TABLEAU INTERACTIF', ha='center', va='center',
            fontsize=5, color='#1B5E7A', zorder=9)

    # Salle 2 - round table
    ct = Circle((17.6, 10.0), 1.5, facecolor='#F5EDE8', edgecolor='#C4714B',
                linewidth=1.5, zorder=8, alpha=0.8)
    ax.add_patch(ct)
    ax.text(17.6, 10.0, 'Table\nronde', ha='center', va='center',
            fontsize=5.5, color='#5C3D2E', zorder=9)

    # Coffee bar counter
    bar = patches.Rectangle((0.3, 5.0), 4.0, 0.5, facecolor='#3D2B1A',
                              edgecolor='#C9A84C', linewidth=1, zorder=8)
    ax.add_patch(bar)
    ax.text(2.3, 5.25, '☕ COMPTOIR CAFÉ', ha='center', va='center',
            fontsize=5, color='#E8C97A', zorder=9)

    # Salle 3 - private
    r3 = patches.Rectangle((9.0, 2.0), 4.5, 3.5, facecolor='#EDE8F5',
                             edgecolor='#7A9E7E', linewidth=1, alpha=0.8, zorder=8)
    ax.add_patch(r3)
    ax.text(11.25, 3.75, 'Table\nprivée', ha='center', va='center',
            fontsize=5.5, color='#3A1A5A', zorder=9)

    # North arrow
    ax.annotate('N', xy=(20.5, 12.5), fontsize=10, color='#C9A84C',
                fontweight='bold', ha='center', zorder=10)
    ax.annotate('', xy=(20.5, 12.8), xytext=(20.5, 12.2),
                arrowprops=dict(arrowstyle='->', color='#C9A84C', lw=1.5), zorder=10)

    # LEGEND
    legend_items = [
        (mpatches.Patch(facecolor='#FFF8DC', edgecolor='#999', linewidth=0.8), 'A — Réception (18m²)'),
        (mpatches.Patch(facecolor='#E8F4E8', edgecolor='#999', linewidth=0.8), 'B — Café Maktaba (40m²)'),
        (mpatches.Patch(facecolor='#E8EEF8', edgecolor='#999', linewidth=0.8), 'C — Salle Groupes (35m²)'),
        (mpatches.Patch(facecolor='#F5EDE8', edgecolor='#999', linewidth=0.8), 'D — Semi-Privé (22m²)'),
        (mpatches.Patch(facecolor='#EDE8F5', edgecolor='#999', linewidth=0.8), 'E — Cours Particuliers (25m²)'),
        (mpatches.Patch(facecolor='#E8F5F5', edgecolor='#999', linewidth=0.8), 'F — Admin / Back-office (20m²)'),
        (plt.Line2D([0],[0], color='#4FC3F7', lw=3), 'Cloison vitrée'),
        (mpatches.Patch(facecolor='#5C3D2E', edgecolor='#C9A84C'), 'Étagères / Mobilier bois noyer'),
    ]
    handles, labels = zip(*legend_items)
    leg = ax.legend(handles, labels, loc='lower right', fontsize=6,
                    facecolor='#1A1A1A', labelcolor='white', framealpha=0.92,
                    bbox_to_anchor=(1.0, 0.0), ncol=2,
                    title='LÉGENDE', title_fontsize=7)
    leg.get_title().set_color('#C9A84C')

    ax.set_title('PLAN D\'AMÉNAGEMENT — Centre Linguistique de Riyad\n'
                 'Surface totale ~160 m² — Nord Riyad',
                 color='#C9A84C', fontsize=11, fontweight='bold', pad=12)
    plt.tight_layout()
    return fig_to_image(fig, 165, 110)

# ── 3. MATERIALS BOARD ───────────────────────────────────────────────────────
def make_materials():
    fig, axes = plt.subplots(2, 5, figsize=(13, 5))
    fig.patch.set_facecolor('#0D1B2A')

    materials = [
        # (bg_color, pattern_type, title, subtitle)
        ('#F7F0E3', 'arabesque', 'STUC SABLÉ\nMurs principaux', 'Teinte sable chaud\nFinition mate'),
        ('#1C2522', 'wood', 'NOYER AMÉRICAIN\nBoiseries & Étagères', 'Teinte foncée vernie\nEpaisseur 18mm'),
        ('#C9A84C', 'metal', 'LAITON BROSSÉ\nQuincailleries & Accents', 'Poignées, bordures\nLuminaires'),
        ('#E8E0D0', 'marble', 'MARBRE CREMA MARFIL\nComptoir café & Tables', 'Calcaire espagnol\nFinition poncée'),
        ('#FAF6EF', 'fabric', 'LIN IVOIRE\nRideaux & Coussins', 'Tissus naturels\n80% lin / 20% coton'),
        ('#C4714B', 'terracotta', 'ZELLIGE TERRACOTTA\nMur accent café', 'Artisanat marocain\n15×15cm hand-made'),
        ('#7A9E7E', 'acoustic', 'PANNEAU PHONIQUE\nSalles de cours', 'Tissu sauge tendu\nLaine minérale 5cm'),
        ('#3D2B1A', 'leather', 'CUIR VIEILLI COGNAC\nAssises lounge', 'Full grain naturel\nPatine artisanale'),
        ('#E8E8E8', 'concrete', 'BÉTON CIRÉ\nSol café & réception', 'Teinte gris perle\nVernis mat protection'),
        ('#2C1A0E', 'rattan', 'ROTIN / OSIER\nAccessoires déco', 'Suspensions & plateaux\nLumiIère tamisée'),
    ]

    for i, (ax, (bg, ptype, title, sub)) in enumerate(zip(axes.flat, materials)):
        ax.set_facecolor(bg)
        ax.set_xlim(0,10); ax.set_ylim(0,10)
        ax.axis('off')

        # Draw pattern
        if ptype == 'arabesque':
            for x in np.arange(0, 10, 1.5):
                for y in np.arange(0, 10, 1.5):
                    c = Circle((x, y), 0.5, facecolor='none',
                                edgecolor='#C9A84C', linewidth=0.4, alpha=0.4)
                    ax.add_patch(c)
        elif ptype == 'wood':
            for y in np.arange(0.5, 10, 1.2):
                ax.plot([0,10],[y,y+0.3], color='#2A1A10', alpha=0.3, lw=0.8)
                ax.plot([0,10],[y+0.4,y+0.5], color='#3D2B1A', alpha=0.2, lw=0.5)
        elif ptype == 'metal':
            for x in np.arange(0,10,0.8):
                ax.plot([x,x],[0,10], color='#E8C97A', alpha=0.15, lw=0.5)
        elif ptype == 'marble':
            for _ in range(8):
                x0 = np.random.uniform(0,10)
                ax.plot([x0, x0+np.random.uniform(-3,3)],
                        [np.random.uniform(0,10), np.random.uniform(0,10)],
                        color='#B0A090', alpha=0.25, lw=0.8)
        elif ptype == 'terracotta':
            for x in np.arange(0,10,1.5):
                for y in np.arange(0,10,1.5):
                    r = patches.Rectangle((x+0.05,y+0.05), 1.4, 1.4,
                                          facecolor=bg, edgecolor='#8B4513',
                                          linewidth=0.8)
                    ax.add_patch(r)
        elif ptype == 'acoustic':
            for x in np.arange(0,10,0.6):
                for y in np.arange(0,10,0.6):
                    c = Circle((x,y), 0.12, facecolor='#5A7A5A', alpha=0.5)
                    ax.add_patch(c)
        elif ptype == 'rattan':
            for x in np.arange(0,10,1.0):
                ax.plot([x,x],[0,10], color='#4A2A10', alpha=0.25, lw=0.8)
            for y in np.arange(0,10,1.0):
                ax.plot([0,10],[y,y], color='#4A2A10', alpha=0.25, lw=0.8)

        text_col = 'white' if bg in ['#1C2522','#2C1A0E','#3D2B1A','#7A9E7E'] else '#1A1A1A'
        lines_t = title.split('\n')
        lines_s = sub.split('\n')
        ax.text(5, 7.2, lines_t[0], ha='center', va='center', fontsize=6.5,
                color=text_col, fontweight='bold')
        if len(lines_t) > 1:
            ax.text(5, 5.8, lines_t[1], ha='center', va='center', fontsize=5.5, color=text_col)
        for j, sl in enumerate(lines_s):
            ax.text(5, 4.2 - j*1.2, sl, ha='center', va='center',
                    fontsize=5, color=text_col, alpha=0.8, style='italic')

        # Chip number
        c_num = Circle((0.8, 9.2), 0.6, facecolor='#C9A84C', zorder=5)
        ax.add_patch(c_num)
        ax.text(0.8, 9.2, str(i+1), ha='center', va='center',
                fontsize=6, color='#0D1B2A', fontweight='bold', zorder=6)

    fig.suptitle('PLANCHE MATIÈRES — Sélection premium pour le Centre Linguistique de Riyad',
                 color='#C9A84C', fontsize=11, fontweight='bold', y=1.02)
    plt.tight_layout(pad=0.8)
    np.random.seed(42)
    return fig_to_image(fig, 165, 100)

# ── 4. ZONE DETAILS ──────────────────────────────────────────────────────────
def make_zone_diagram(zone_name, color_main, color_accent, elements, note):
    fig, ax = plt.subplots(figsize=(9.5, 3.5))
    fig.patch.set_facecolor('#0D1B2A')
    ax.set_facecolor(color_main)
    ax.set_xlim(0,10); ax.set_ylim(0,4); ax.axis('off')

    # Zone label
    ax.text(0.2, 3.7, zone_name, ha='left', va='top', fontsize=13,
            color=color_accent, fontweight='bold')
    ax.plot([0,10],[3.35,3.35], color=color_accent, lw=1.5, alpha=0.6)

    # Elements as chips in 2 columns
    mid = len(elements)//2
    left_items  = elements[:mid + len(elements)%2]
    right_items = elements[mid + len(elements)%2:]
    for j, item in enumerate(left_items):
        y_pos = 3.05 - j*0.52
        r = FancyBboxPatch((0.15, y_pos-0.18), 4.2, 0.38,
                           boxstyle='round,pad=0.05',
                           facecolor=color_accent, alpha=0.15,
                           edgecolor=color_accent, linewidth=0.6)
        ax.add_patch(r)
        ax.text(0.5, y_pos+0.02, '▸', fontsize=7, color=color_accent, va='center')
        ax.text(0.85, y_pos+0.02, item, fontsize=6.5, color='#1A1A1A',
                va='center', fontweight='normal')
    for j, item in enumerate(right_items):
        y_pos = 3.05 - j*0.52
        r = FancyBboxPatch((4.85, y_pos-0.18), 4.2, 0.38,
                           boxstyle='round,pad=0.05',
                           facecolor=color_accent, alpha=0.15,
                           edgecolor=color_accent, linewidth=0.6)
        ax.add_patch(r)
        ax.text(5.2, y_pos+0.02, '▸', fontsize=7, color=color_accent, va='center')
        ax.text(5.55, y_pos+0.02, item, fontsize=6.5, color='#1A1A1A',
                va='center', fontweight='normal')

    # Note box
    if note:
        ax.text(0.2, 0.2, f'💡  {note}', ha='left', va='bottom', fontsize=6,
                color='#3A3A3A', style='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor=color_accent,
                          alpha=0.12, edgecolor=color_accent, lw=0.8))

    plt.tight_layout(pad=0.4)
    return fig_to_image(fig, 165, 62)

# ── 5. BUDGET CHART ──────────────────────────────────────────────────────────
def make_budget_chart():
    categories = ['Sol béton\nciré', 'Étagères &\njoinery noyer', 'Comptoir café\n(marbre+bois)',
                  'Luminaires\n(laiton)', 'Mobilier\nclasses', 'Mobilier\ncafé lounge',
                  'Réception\ndésk custom', 'Calligraphie\n& art mural', 'Plantes &\nvégétaux',
                  'Signalétique\n& branding', 'Rideaux\n& textiles', 'Divers\n& imprévus']
    amounts  = [28000, 45000, 35000, 22000, 30000, 38000, 18000, 12000, 8000, 15000, 10000, 19000]
    bar_cols = ['#7A9E7E','#5C3D2E','#E8E0D0','#C9A84C','#1B5E7A','#C4714B',
                '#0D1B2A','#C4714B','#7A9E7E','#C9A84C','#FAF6EF','#7F8C8D']

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.5))
    fig.patch.set_facecolor('#0D1B2A')

    # Bar chart
    ax1.set_facecolor('#0D1B2A')
    bars = ax1.barh(categories, amounts, color=bar_cols, alpha=0.88, height=0.65)
    ax1.set_xlabel('SAR', color='#C9A84C', fontsize=8)
    ax1.tick_params(colors='white', labelsize=7)
    ax1.spines['bottom'].set_color('#C9A84C')
    ax1.spines['left'].set_color('#C9A84C')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.xaxis.label.set_color('#C9A84C')
    for bar, val in zip(bars, amounts):
        ax1.text(val + 400, bar.get_y() + bar.get_height()/2,
                 f'{val:,}', va='center', fontsize=6.5, color='white')
    ax1.set_title('Budget aménagement par poste (SAR)', color='#C9A84C',
                  fontsize=9, fontweight='bold', pad=8)

    # Pie chart
    ax2.set_facecolor('#0D1B2A')
    groups = ['Menuiserie & Surfaces', 'Mobilier', 'Lumière & Accents', 'Déco & Art', 'Divers']
    grp_vals = [73000, 86000, 22000, 20000, 29000]
    grp_cols = ['#5C3D2E','#1B5E7A','#C9A84C','#C4714B','#7F8C8D']
    wedges, texts, autotexts = ax2.pie(grp_vals, labels=None, colors=grp_cols,
                                        autopct='%1.1f%%', startangle=120,
                                        textprops={'color':'white','fontsize':8},
                                        pctdistance=0.75, explode=[0.03]*5)
    for at in autotexts: at.set_fontsize(7); at.set_color('white')
    ax2.legend(wedges, groups, loc='lower center', fontsize=7,
               facecolor='#1A2838', labelcolor='white', framealpha=0.8,
               bbox_to_anchor=(0.5,-0.2), ncol=2)
    ax2.set_title(f'Répartition globale\nTotal: 280 000 SAR',
                  color='#C9A84C', fontsize=9, fontweight='bold', pad=8)

    plt.tight_layout(pad=1.5)
    return fig_to_image(fig, 165, 88)

# ── 6. LIGHTING CONCEPT ───────────────────────────────────────────────────────
def make_lighting():
    fig, ax = plt.subplots(figsize=(11, 3.5))
    fig.patch.set_facecolor('#0D1B2A')
    ax.set_facecolor('#08111E')
    ax.set_xlim(0,11); ax.set_ylim(0,4); ax.axis('off')

    zones_light = [
        (1.0, 'RÉCEPTION\n& ENTRÉE', ['Cove LED chaud\n2700K continue',
         'Spot encastré\nLED orientable', 'Enseigne rétroéclairée\nOr/blanc'],
         '#E8C97A'),
        (3.6, 'CAFÉ\n"MAKTABA"', ['Suspensions laiton\nMarocaines H:80cm',
         'Cove LED ambiante\n2700K dimmable', 'Spots accent\nSur étagères'],
         '#C9A84C'),
        (6.2, 'SALLES DE\nCOURS', ['LED linéaire\n4000K neutre', 'Spots tableau\ninteractif 5000K',
         'Cove secondaire\n3000K détente'],
         '#4FC3F7'),
        (8.8, 'ADMIN &\nBACK-OFFICE', ['Dalle LED\n4000K uniforme', 'Bureau individuel\nLED articulé',
         'Fenêtre naturelle\nPrio. lumière jour'],
         '#7A9E7E'),
    ]

    for x0, zone, lamps, col in zones_light:
        ax.text(x0+1.1, 3.7, zone, ha='center', va='top', fontsize=8,
                color=col, fontweight='bold')
        ax.plot([x0, x0+2.2],[3.4,3.4], color=col, lw=1.5, alpha=0.7)
        for j, lamp in enumerate(lamps):
            # Light bulb icon
            c = Circle((x0 + 0.3, 3.0 - j*1.1), 0.2, facecolor=col,
                        alpha=0.85, zorder=5)
            ax.add_patch(c)
            # Glow effect
            c2 = Circle((x0 + 0.3, 3.0 - j*1.1), 0.38, facecolor=col,
                         alpha=0.12, zorder=4)
            ax.add_patch(c2)
            for ln_i, ln in enumerate(lamp.split('\n')):
                ax.text(x0 + 0.7, 3.03 - j*1.1 - ln_i*0.22, ln, va='center',
                        fontsize=6, color='white', alpha=0.9)

    ax.text(5.5, 0.15, '⚡  Toutes zones pilotées par système DALI — gradation 0-100% — scénarios programmables',
            ha='center', fontsize=6.5, color='#C9A84C', style='italic')

    ax.set_title('CONCEPT ÉCLAIRAGE — Architecture lumineuse par zone',
                 color='#C9A84C', fontsize=10, fontweight='bold', pad=8)
    plt.tight_layout(pad=0.5)
    return fig_to_image(fig, 165, 72)

# ── 7. PINTEREST MOOD BOARD ───────────────────────────────────────────────────
def make_moodboard():
    fig = plt.figure(figsize=(13, 6.5))
    fig.patch.set_facecolor('#0D1B2A')

    # Create a 3x4 grid of mood rectangles
    mood_items = [
        # (x, y, w, h, bg_color, label, icon)
        (0.01, 0.55, 0.24, 0.43, '#F5EDE0', 'Calligraphie arabe\nencadrée — entrée', '✦'),
        (0.26, 0.55, 0.24, 0.43, '#2C1A10', 'Étagères noyer\nfloor-to-ceiling', '📚'),
        (0.51, 0.55, 0.24, 0.43, '#8B5E3C', 'Assises lounge\ncuir cognac', '🪑'),
        (0.76, 0.55, 0.23, 0.43, '#C4714B', 'Zellige terracotta\nmur accent café', '🔶'),
        (0.01, 0.10, 0.16, 0.43, '#E8D5A3', 'Luminaire laiton\narabian lantern', '🪔'),
        (0.18, 0.10, 0.22, 0.43, '#1C2A1E', 'Mur végétal\nentrée & café', '🌿'),
        (0.41, 0.10, 0.22, 0.43, '#E8EEF8', 'Salle cours —\nmobilier scandi', '📐'),
        (0.64, 0.10, 0.17, 0.43, '#3D2010', 'Comptoir café\nmarbre + bois', '☕'),
        (0.82, 0.10, 0.17, 0.43, '#D4C5A9', 'Mashrabiya vinyl\nvitre dépoli', '🔷'),
    ]

    for x, y, w, h, bg, lbl, icon in mood_items:
        ax = fig.add_axes([x, y, w, h])
        ax.set_facecolor(bg)
        ax.set_xlim(0,1); ax.set_ylim(0,1)
        ax.axis('off')
        # Pattern overlay
        if bg.startswith('#2') or bg.startswith('#1') or bg.startswith('#3'):
            text_col = '#E8C97A'
        else:
            text_col = '#1A1A1A'
        ax.text(0.5, 0.65, icon, ha='center', va='center', fontsize=20,
                color=text_col)
        for j, ln in enumerate(lbl.split('\n')):
            ax.text(0.5, 0.35 - j*0.18, ln, ha='center', va='center',
                    fontsize=7, color=text_col, fontweight='bold' if j==0 else 'normal')
        # Gold border
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('#C9A84C')
            spine.set_linewidth(1)

    # Title
    title_ax = fig.add_axes([0.0, 0.94, 1.0, 0.06])
    title_ax.set_facecolor('#0D1B2A')
    title_ax.axis('off')
    title_ax.text(0.5, 0.5, 'MOOD BOARD — CONCEPT "AL-MAKTABA" — Arabesques Contemporaines',
                  ha='center', va='center', fontsize=12, color='#C9A84C',
                  fontweight='bold')

    return fig_to_image(fig, 165, 105)

# ═══════════════════════════════════════════════════════════════════════════
# PDF STYLES
# ═══════════════════════════════════════════════════════════════════════════
def styles():
    S = {}
    S['h1'] = ParagraphStyle('h1', fontName='Helvetica-Bold', fontSize=18, leading=24,
        textColor=GOLD, spaceBefore=16, spaceAfter=8)
    S['h2'] = ParagraphStyle('h2', fontName='Helvetica-Bold', fontSize=12, leading=17,
        textColor=colors.HexColor('#0D1B2A'), spaceBefore=10, spaceAfter=5,
        backColor=colors.HexColor('#F0EBDF'), borderPad=(5,5,5,10))
    S['h3'] = ParagraphStyle('h3', fontName='Helvetica-Bold', fontSize=10, leading=14,
        textColor=TEAL, spaceBefore=7, spaceAfter=4)
    S['body'] = ParagraphStyle('body', fontName='Helvetica', fontSize=9.5, leading=15,
        textColor=DARK_GRAY, alignment=TA_JUSTIFY, spaceAfter=5)
    S['bullet'] = ParagraphStyle('bullet', fontName='Helvetica', fontSize=9, leading=14,
        textColor=DARK_GRAY, leftIndent=16, firstLineIndent=-10, spaceAfter=3)
    S['caption'] = ParagraphStyle('caption', fontName='Helvetica-Oblique', fontSize=7.5,
        leading=11, textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=6)
    S['callout'] = ParagraphStyle('callout', fontName='Helvetica-Bold', fontSize=9.5,
        leading=14, textColor=WHITE, backColor=TEAL, alignment=TA_CENTER,
        borderPad=8, spaceAfter=8, spaceBefore=8)
    S['quote'] = ParagraphStyle('quote', fontName='Helvetica-Oblique', fontSize=11,
        leading=17, textColor=colors.HexColor('#5C3D2E'), alignment=TA_CENTER,
        spaceBefore=10, spaceAfter=10, borderPad=8)
    S['footer_note'] = ParagraphStyle('footer_note', fontName='Helvetica-Oblique',
        fontSize=7.5, textColor=MID_GRAY, alignment=TA_CENTER)
    S['table_header'] = ParagraphStyle('table_header', fontName='Helvetica-Bold',
        fontSize=8.5, textColor=WHITE, alignment=TA_CENTER)
    S['table_cell'] = ParagraphStyle('table_cell', fontName='Helvetica', fontSize=8.5,
        leading=12, textColor=DARK_GRAY, alignment=TA_LEFT)
    return S

def styled_table(data, col_widths):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), NAVY),
        ('TEXTCOLOR',  (0,0),(-1,0), WHITE),
        ('FONTNAME',   (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0),(-1,0), 8.5),
        ('ALIGN',      (0,0),(-1,0), 'CENTER'),
        ('VALIGN',     (0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1), 7),
        ('RIGHTPADDING',(0,0),(-1,-1), 7),
        ('GRID',       (0,0),(-1,-1), 0.4, colors.HexColor('#D0D5DB')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, colors.HexColor('#FAF5EE')]),
        ('LINEBELOW',  (0,0),(-1,0),  2, GOLD),
    ]))
    return t

def section_bar(num, title):
    t = Table([[
        Paragraph(f'0{num}', ParagraphStyle('sn', fontName='Helvetica-Bold',
            fontSize=44, textColor=colors.HexColor('#1A2E45'), alignment=TA_RIGHT)),
        Paragraph(title, ParagraphStyle('st', fontName='Helvetica-Bold',
            fontSize=19, textColor=GOLD, alignment=TA_LEFT, leading=24))
    ]], colWidths=[80, W-160])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), NAVY),
        ('VALIGN',    (0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING',(0,0),(-1,-1), 12),
        ('BOTTOMPADDING',(0,0),(-1,-1),12),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
        ('RIGHTPADDING',(0,0),(-1,-1), 10),
        ('LINEBELOW', (0,0),(-1,-1), 3, GOLD),
    ]))
    return t

def info_box(title, content, S, bg='#FFF8EE', border_col=GOLD):
    t = Table([[
        Paragraph(f'<b>{title}</b>',
                  ParagraphStyle('ib_t', fontName='Helvetica-Bold', fontSize=9.5,
                                 textColor=border_col)),
    ],[
        Paragraph(content,
                  ParagraphStyle('ib_c', fontName='Helvetica', fontSize=9, leading=14,
                                 textColor=DARK_GRAY, alignment=TA_JUSTIFY)),
    ]], colWidths=[W-80])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1), colors.HexColor(bg) if isinstance(bg,str) else bg),
        ('LEFTPADDING',(0,0),(-1,-1), 12),
        ('RIGHTPADDING',(0,0),(-1,-1), 12),
        ('TOPPADDING', (0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LINEAFTER',  (0,0),(0,-1), 3, border_col),
        ('SPAN',       (0,0),(-1,0)),
        ('SPAN',       (0,1),(-1,1)),
    ]))
    return t

# ═══════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════
def draw_cover(c):
    # Background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Top gold stripe
    c.setFillColor(GOLD)
    p = c.beginPath()
    p.moveTo(0,H); p.lineTo(W,H); p.lineTo(W,H-90); p.lineTo(0,H-55); p.close()
    c.drawPath(p, fill=1, stroke=0)
    # Bottom gold stripe
    p2 = c.beginPath()
    p2.moveTo(0,0); p2.lineTo(W,0); p2.lineTo(W,80); p2.lineTo(0,45); p2.close()
    c.drawPath(p2, fill=1, stroke=0)
    # Geometric circles top right
    c.setStrokeColor(colors.HexColor('#1A2E45'))
    c.setLineWidth(0.8)
    for r in [40, 90, 150, 220, 300]:
        c.circle(W-20, H-10, r, stroke=1, fill=0)
    # Arabesque pattern area (right side)
    c.setFillColor(colors.HexColor('#0F2233'))
    c.rect(W*0.55, 90, W*0.45, H-170, fill=1, stroke=0)
    # Grid overlay on right
    c.setStrokeColor(colors.HexColor('#1A3050'))
    c.setLineWidth(0.4)
    for x in np.arange(W*0.55, W, 20):
        c.line(x, 90, x, H-80)
    for y in np.arange(90, H-80, 20):
        c.line(W*0.55, y, W, y)
    # Diamond pattern on right panel
    c.setFillColor(GOLD)
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    for x in np.arange(W*0.58, W-10, 22):
        for y in np.arange(105, H-90, 22):
            c.setFillColor(colors.HexColor('#C9A84C22'))
            size = 8
            pts = [(x, y+size),(x+size,y),(x,y-size),(x-size,y)]
            path = c.beginPath()
            path.moveTo(*pts[0])
            for pt in pts[1:]: path.lineTo(*pt)
            path.close()
            c.drawPath(path, fill=1, stroke=0)
    # Left accent
    c.setFillColor(GOLD)
    c.rect(32, 60, 4, H-130, fill=1, stroke=0)
    c.setFillColor(GOLD_LIGHT)
    c.rect(40, 70, 1, H-150, fill=1, stroke=0)
    # Arabic text (right panel)
    c.setFont('Helvetica-Bold', 22)
    c.setFillColor(GOLD)
    c.drawCentredString(W*0.775, H-140, 'مركز اللغات')
    c.setFont('Helvetica', 11)
    c.setFillColor(colors.HexColor('#C9A84C88'))
    c.drawCentredString(W*0.775, H-165, 'الرياض — المملكة العربية السعودية')
    # Design icons
    icons_y = H - 280
    for i, icon in enumerate(['✦', '◆', '◈', '◇']):
        c.setFont('Helvetica', 14)
        c.setFillColor(colors.HexColor('#C9A84C66'))
        c.drawCentredString(W*0.65 + i*30, icons_y, icon)
    # Main title block
    c.setFont('Helvetica-Bold', 9)
    c.setFillColor(GOLD_LIGHT)
    c.drawString(58, H-148, 'CONCEPT DESIGN')
    c.setFont('Helvetica-Bold', 38)
    c.setFillColor(WHITE)
    c.drawString(55, H-195, 'AL-MAKTABA')
    c.setFont('Helvetica', 16)
    c.setFillColor(GOLD_LIGHT)
    c.drawString(57, H-222, 'المكتبة — The Living Library')
    c.setFont('Helvetica', 10)
    c.setFillColor(colors.HexColor('#A0B4C8'))
    c.drawString(57, H-242, 'Concept d\'aménagement intérieur pour le Centre Linguistique de Riyad')
    # Divider
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(55, H-255, W*0.5, H-255)
    # Tags
    chip_data = [('ARABESQUE CONTEMPORAIN', TEAL), ('PREMIUM', GOLD), ('LIFESTYLE', TERRA)]
    cx = 57
    for lbl, col in chip_data:
        cw = len(lbl)*6.5 + 16
        c.setFillColor(col)
        c.roundRect(cx, H-282, cw, 16, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 7)
        c.drawCentredString(cx + cw/2, H-274, lbl)
        cx += cw + 6
    # Description
    desc_y = H - 310
    c.setFont('Helvetica', 8.5)
    c.setFillColor(colors.HexColor('#8AAAB8'))
    desc_lines = [
        "Un centre linguistique ancré dans la culture arabe contemporaine,",
        "où chaque espace raconte une histoire — du café Maktaba",
        "aux salles de cours inspirées des riads traditionnels."
    ]
    for i, ln in enumerate(desc_lines):
        c.drawString(57, desc_y - i*13, ln)
    # Space analysis box
    box_y = H-405
    c.setFillColor(colors.HexColor('#0F2233'))
    c.roundRect(52, box_y, W*0.46, 80, 6, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.roundRect(52, box_y, W*0.46, 80, 6, fill=0, stroke=1)
    c.setFont('Helvetica-Bold', 8.5)
    c.setFillColor(GOLD)
    c.drawString(62, box_y+62, '🏢  ESPACE ANALYSÉ — SHELL RAW STATE')
    c.setFont('Helvetica', 8)
    c.setFillColor(WHITE)
    analysis = [
        '⬥  Superficie : ~160 m² — Nord Riyad',
        '⬥  État : Shell vide, prêt à aménager',
        '⬥  Atouts : LED cove intégrée, parquet vinyle, cloisons vitrées',
        '⬥  Plafond : Coffre bois foncé avec lumière chaude — Premium',
        '⬥  Cuisine/office existante — à transformer en café back-of-house',
    ]
    for i, ln in enumerate(analysis):
        c.drawString(62, box_y+47 - i*11, ln)
    # Bottom meta
    c.setFillColor(colors.HexColor('#0F2233'))
    c.rect(50, 65, W-100, 35, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(50, 100, W-50, 100)
    meta = [('Designer', 'Studio CLR — Senior Interior'), ('Style', 'Arabesque Contemporain'),
            ('Budget', '280 000 SAR (estimation)'), ('Livraison', '8–10 semaines')]
    cw2 = (W-100)/4
    for i, (lbl, val) in enumerate(meta):
        mx = 58 + i*cw2
        c.setFont('Helvetica', 6.5); c.setFillColor(MID_GRAY)
        c.drawString(mx, 90, lbl)
        c.setFont('Helvetica-Bold', 8); c.setFillColor(WHITE)
        c.drawString(mx, 75, val)

def on_first(c, doc):
    c.saveState()
    draw_cover(c)
    c.restoreState()

def on_later(c, doc):
    c.saveState()
    c.setFillColor(NAVY); c.rect(0, H-28, W, 28, fill=1, stroke=0)
    c.setFillColor(GOLD);  c.rect(0, H-31, W, 3, fill=1, stroke=0)
    c.setFont('Helvetica-Bold', 8); c.setFillColor(WHITE)
    c.drawString(20, H-19, 'CONCEPT DESIGN — AL-MAKTABA / Centre Linguistique de Riyad')
    c.setFont('Helvetica', 7); c.setFillColor(GOLD_LIGHT)
    c.drawRightString(W-20, H-19, 'CONFIDENTIEL — Studio CLR Design')
    c.setFillColor(NAVY); c.rect(0, 0, W, 18, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(0, 18, W, 1.2, fill=1, stroke=0)
    c.setFont('Helvetica', 7); c.setFillColor(GOLD_LIGHT)
    c.drawString(20, 5, '© 2025 — Tous droits réservés — Document de conception exclusif')
    c.drawRightString(W-20, 5, f'Page {doc.page}')
    c.restoreState()

# ═══════════════════════════════════════════════════════════════════════════
# BUILD STORY
# ═══════════════════════════════════════════════════════════════════════════
def build_story():
    S = styles()
    story = []

    def p(t):  return Paragraph(t, S['body'])
    def ps(t): return Paragraph(t, S['caption'])
    def h2(t): return Paragraph(t, S['h2'])
    def h3(t): return Paragraph(t, S['h3'])
    def sp(n=8): return Spacer(1, n)
    def hr(): return HRFlowable(width='100%', thickness=0.5,
                                color=colors.HexColor('#D0D5DB'), spaceAfter=6)

    # Cover = first page only
    story.append(PageBreak())

    # ─── SECTION 01 : ANALYSE ───────────────────────────────────────────────
    story.append(section_bar(1, 'ANALYSE DE L\'ESPACE EXISTANT'))
    story.append(sp(14))

    story.append(p(
        'L\'espace soumis à redesign est un plateau commercial brut de <b>~160 m²</b> '
        'situé au nord de Riyad. Il est actuellement dans un état "shell" : '
        'entièrement vide, sans mobilier ni décoration. Cependant, l\'architecture '
        'existante recèle d\'atouts considerables qui servent de base au concept "Al-Maktaba".'
    ))
    story.append(sp(8))

    analysis_data = [
        [Paragraph('Élément architectural', S['table_header']),
         Paragraph('État actuel', S['table_header']),
         Paragraph('Potentiel / Action CLR', S['table_header']),
         Paragraph('Priorité', S['table_header'])],
        ['Sol vinyle marbre gris', 'Très bon état — finition premium', 'Conserver tel quel + béton ciré réception', '✅ Conserver'],
        ['Plafond coffre bois foncé + LED cove', 'Intégré — lumière chaude ambiance', 'Atout majeur — amplifier avec spots', '✅ Conserver'],
        ['Cloisons vitrées (strip frosted)', 'Existantes — 2 séparations', 'Film vinyle mashrabiya sur vitre', '🔧 Améliorer'],
        ['Porte accordéon bois foncé', 'Existante — qualité correcte', 'Remplacer poignée laiton + peinture', '🔧 Améliorer'],
        ['Grande salle principale ouverte', 'Vide — 40+ m²', '→ Café Maktaba + réception', '🏗️ Transformer'],
        ['Salle avec cloison vitrée', 'Vide — 35 m²', '→ Salle cours groupes (8-12 pers.)', '🏗️ Transformer'],
        ['Chambre/pièce fermée', 'Vide — 20 m²', '→ Cours particuliers / semi-privé', '🏗️ Transformer'],
        ['Cuisine/office', 'Meubles gris bois — évier existant', '→ Back-of-house café espresso', '🔧 Améliorer'],
        ['Éclairage général spots', 'Spots encastrés existants', 'Compléter avec luminaires design', '🔧 Compléter'],
        ['Murs blancs lisses', 'Bon état partout', 'Peinture sable chaud + 1 mur accent navy', '🎨 Rénover'],
    ]
    for i in range(1, len(analysis_data)):
        analysis_data[i] = [Paragraph(str(c), S['table_cell']) for c in analysis_data[i]]
    story.append(styled_table(analysis_data, [115, 105, 130, 80]))
    story.append(sp(10))

    story.append(info_box(
        '🌟  Verdict : Un shell de très haute qualité',
        'Le plateau dispose déjà d\'équipements que la plupart des projets d\'aménagement '
        'doivent créer from scratch : cove lighting intégré, parquet premium, cloisons vitrées '
        'et une séparation naturelle des zones. L\'investissement ira principalement '
        'vers le mobilier, la décoration et l\'identité de marque — pas vers le génie civil.',
        S, bg='#EAFAF0', border_col=SAGE
    ))
    story.append(PageBreak())

    # ─── SECTION 02 : CONCEPT ───────────────────────────────────────────────
    story.append(section_bar(2, 'CONCEPT DESIGN — "AL-MAKTABA"'))
    story.append(sp(14))

    story.append(Paragraph(
        '"Al-Maktaba" — المكتبة — n\'est pas qu\'une bibliothèque.\n'
        'C\'est un lieu vivant où les langues se respirent, '
        'où la culture arabe contemporaine dialogue avec le monde.',
        S['quote']
    ))
    story.append(sp(8))

    story.append(p(
        'Le concept architectural s\'inspire de trois références fusionnées en un style unique : '
        '<b>(1) le riad marocain</b> — espace intérieur de sérénité avec végétaux et eau, '
        '<b>(2) le Wabi-Sabi japonais</b> — beauté de l\'imparfait, matières naturelles, lumière tamisée, '
        '<b>(3) le concept store londonien</b> — mise en scène commerciale, fluidité des zones, '
        'identité forte. Le résultat est un espace <b>instagrammable par conception</b>, '
        'premium sans ostentation, ancré dans la culture locale mais résolument contemporain.'
    ))
    story.append(sp(10))

    story.append(make_moodboard())
    story.append(ps('Références mood board — Concept "Al-Maktaba" — Arabesques Contemporaines'))
    story.append(sp(12))

    story.append(h2('2.1 — Palette de couleurs & matières'))
    story.append(sp(6))
    story.append(make_palette())
    story.append(ps('Palette officielle CLR — 8 tons coordonnés — matières naturelles premium'))
    story.append(PageBreak())

    # ─── SECTION 03 : PLAN ──────────────────────────────────────────────────
    story.append(section_bar(3, 'PLAN D\'AMÉNAGEMENT — ZONES & FONCTIONS'))
    story.append(sp(14))

    story.append(p(
        'L\'espace de 160 m² est découpé en <b>6 zones fonctionnelles distinctes</b>, '
        'chacune avec une identité visuelle propre tout en appartenant à un ensemble cohérent. '
        'La circulation est fluide et pensée pour guider naturellement un visiteur de l\'entrée '
        'vers le café, puis vers les espaces pédagogiques.'
    ))
    story.append(sp(8))

    story.append(make_floorplan())
    story.append(ps('Plan d\'aménagement schématique — CLR Nord Riyad — ~160 m² — Concept Al-Maktaba'))
    story.append(sp(12))

    # Zone summary table
    zones_summary = [
        [Paragraph(h, S['table_header']) for h in ['Zone', 'Nom', 'Surface', 'Fonction principale', 'Ambiance cible']],
        ['A', 'Réception & Accueil', '18 m²', 'Accueil, attente, branding', 'Wow factor — 1er impact'],
        ['B', 'Café "Maktaba"', '40 m²', 'Café, librairie, lounge, merch', 'Chaleureux, instagrammable'],
        ['C', 'Salle Cours 1', '35 m²', 'Groupes 8-12 personnes', 'Concentré, inspirant'],
        ['D', 'Salle Cours 2', '22 m²', 'Semi-privé 2-4 personnes', 'Intimiste, premium'],
        ['E', 'Cours Particuliers', '25 m²', 'Tutorat, diplomates, exécutifs', 'Luxueux, confidentiel'],
        ['F', 'Admin & Back-office', '20 m²', 'Gestion, studio digital', 'Fonctionnel, discret'],
    ]
    for i in range(1, len(zones_summary)):
        zones_summary[i] = [Paragraph(str(c), S['table_cell']) for c in zones_summary[i]]
    story.append(styled_table(zones_summary, [25, 90, 45, 130, 120]))
    story.append(PageBreak())

    # ─── SECTION 04 : ZONES DÉTAIL ──────────────────────────────────────────
    story.append(section_bar(4, 'DESIGN PAR ZONE — SPÉCIFICATIONS'))
    story.append(sp(14))

    # ZONE A
    story.append(h2('ZONE A — Réception & Accueil'))
    story.append(make_zone_diagram(
        'ZONE A — RÉCEPTION & ACCUEIL (18 m²)', '#FFF8EE', '#C9A84C',
        [
            'Desk accueil courbe en noyer + façade laiton brossé',
            'Mur principal : stuc sable + calligraphie laiton découpé',
            'Enseigne rétroéclairée : "مركز اللغات" — lettre par lettre',
            'Sol : béton ciré gris perle (différent des salles)',
            'Végétal : olivier ou ficus en pot terre cuite',
            'Assise attente : 2 poufs cuir cognac',
            'Plante grasse XXL dans cache-pot laiton',
            'Panneau tactile/tablette : planning cours & prix',
        ],
        'Premier point de contact client — doit générer confiance et prestige en moins de 5 secondes.'
    ))
    story.append(ps('Zone A — Réception : concept desk noyer + laiton + calligraphie murale'))
    story.append(sp(8))

    # ZONE B
    story.append(h2('ZONE B — Café "Maktaba" (المكتبة)'))
    story.append(make_zone_diagram(
        'ZONE B — CAFÉ "MAKTABA" (40 m²)', '#F5F0E8', '#5C3D2E',
        [
            'Comptoir café : 2m × 0.6m — marbre Crema Marfil + bois noyer',
            'Machine espresso La Marzocco + broyeur Mahlkönig',
            'Étagères books floor-to-ceiling : 3m haute × 4m large — noyer',
            'Tables rondes café ⌀70cm — pieds laiton + plateau bois',
            'Assises mixtes : chaises bistro Thonet + banquettes tissu',
            'Coin majlis : coussins sol bas — style arabe contemporain',
            'Mur accent : zellige terracotta 15×15cm (artisanat marocain)',
            'Suspensions : lanternes laiton oriental H:80cm au-dessus comptoir',
            'Vitrine merch et livres intégrée à l\'étagère',
            'Menu bilingue arabe/français sur ardoise murale',
        ],
        'Le café est le cœur visible du centre — générateur de trafic quotidien et d\'image de marque organique.'
    ))
    story.append(ps('Zone B — Café Maktaba : comptoir marbre, étagères, lanternes laiton, zellige terracotta'))
    story.append(sp(8))

    # ZONE C
    story.append(h2('ZONE C — Salle de cours groupes (35 m²)'))
    story.append(make_zone_diagram(
        'ZONE C — SALLE COURS GROUPES (35 m²)', '#EEF4F8', '#1B5E7A',
        [
            'Tables modulables 6 unités (groupables en îlots ou rangées)',
            'Chaises empilables assise tissu sauge — 12 unités',
            'Tableau interactif 86" SMART Board — mur principal',
            'Cloison vitrée : film vinyle motif mashrabiya géométrique',
            'Panneau phonique mur arrière : tissu sauge, motif pointillé',
            'Étagère murale ressources pédagogiques (dictionnaires, cartes)',
            'LED linéaire 4000K suspendues — dimmable',
            'Plante suspendue ou mur végétal partiel',
            'Porte-manteau design arabe en laiton et bois',
            'Horloge murale avec "heure mondiale" — 6 villes',
        ],
        'Cloison vitrée existante = atout majeur. Film mashrabiya transforme la partition en œuvre d\'art tout en préservant visibilité.'
    ))
    story.append(ps('Zone C — Salle groupes : mobilier modulable, tableau interactif, film mashrabiya sur verre'))
    story.append(sp(8))

    # ZONE D
    story.append(h2('ZONE D — Salle semi-privé (22 m²)'))
    story.append(make_zone_diagram(
        'ZONE D — SALLE SEMI-PRIVÉ (22 m²)', '#F5EDE8', '#C4714B',
        [
            'Table ovale 180×90cm en noyer massif — 4-6 personnes',
            'Fauteuils capitonnés tissu terracotta/or',
            'Mur accent : peinture deep navy + artwork calligraphie encadrée',
            'Pendule laiton brossé — touche luxury',
            'Écran 55" mural pour cours et présentations',
            'Bibliothèque basse intégrée (livres, ressources)',
            'Éclairage : suspension unique laiton au-dessus table',
            'Rideaux lin ivoire sur rails discrets',
        ],
        'Espace premium justifiant tarif ×1.8 vs cours groupes. Clients cibles : familles, collègues, petits groupes VIP.'
    ))
    story.append(ps('Zone D — Semi-privé : table noyer, fauteuils terra, mur navy, suspension laiton'))
    story.append(sp(8))

    # ZONE E
    story.append(h2('ZONE E — Cours particuliers / Exécutifs (25 m²)'))
    story.append(make_zone_diagram(
        'ZONE E — COURS PARTICULIERS & DIPLOMATES (25 m²)', '#EDE8F5', '#7A9E7E',
        [
            'Bureau face-à-face : 2 fauteuils cuir + table basse 90×60',
            'Ambiance "bureau d\'architecte" : épuré, discret, luxe silencieux',
            'Mur tapisserie texturée lin naturel — acoustique naturelle',
            'Bibliothèque sur-mesure angles et recoins',
            'Écran tablette pivot 27" pour cours particuliers',
            'Plantes vertes soignées (ficus lyrata en pot laiton)',
            'Éclairage : lampe sur pied arc en laiton — Lumière douce',
            'Coffre-fort discret : stockage matériels confidentiels',
        ],
        'Espace le plus exclusif. Prix ×2.5 vs groupe. Clients : diplomates, DG, exécutifs Aramco/NEOM.'
    ))
    story.append(ps('Zone E — Cours particuliers : salon d\'architecte, cuir, ficus, laiton, discrétion absolue'))
    story.append(PageBreak())

    # ─── SECTION 05 : MATIÈRES ──────────────────────────────────────────────
    story.append(section_bar(5, 'PLANCHE MATIÈRES & SPÉCIFICATIONS'))
    story.append(sp(14))

    story.append(make_materials())
    story.append(ps('Sélection de 10 matières premium pour l\'ensemble du centre — sourcing local et international'))
    story.append(sp(12))

    matieres_data = [
        [Paragraph(h, S['table_header']) for h in
         ['#', 'Matière', 'Application', 'Fournisseur suggéré', 'Budget unitaire']],
        ['1', 'Stuc sablé sable chaud', 'Murs principaux toutes zones', 'Peinture Jordan / local KSA', '~8 000 SAR'],
        ['2', 'Noyer américain verni foncé', 'Boiseries, étagères, desk', 'Menuisier Riyad sur-mesure', '~45 000 SAR'],
        ['3', 'Laiton brossé', 'Quincaillerie, luminaires, accents', 'IKEA + artisans + importation', '~22 000 SAR'],
        ['4', 'Marbre Crema Marfil', 'Comptoir café, table D', 'Marbrerie Riyad', '~18 000 SAR'],
        ['5', 'Lin ivoire naturel', 'Rideaux, coussins, revêtements', 'Fabric Souq Riyad', '~8 000 SAR'],
        ['6', 'Zellige terracotta', 'Mur accent café (2m²)', 'Import Maroc / Leroy Merlin KSA', '~7 000 SAR'],
        ['7', 'Panneau phonique sauge', 'Murs salles de cours', 'Fournisseur acoustique Riyad', '~12 000 SAR'],
        ['8', 'Cuir pleine fleur cognac', 'Assises Zone E, poufs réception', 'Importateur cuir', '~15 000 SAR'],
        ['9', 'Béton ciré gris perle', 'Sol réception (Zone A)', 'Applicateur béton ciré', '~9 000 SAR'],
        ['10','Rotin/osier naturel', 'Suspensions, corbeilles déco', 'Artisans + Souq', '~4 000 SAR'],
    ]
    for i in range(1, len(matieres_data)):
        matieres_data[i] = [Paragraph(str(c), S['table_cell']) for c in matieres_data[i]]
    story.append(styled_table(matieres_data, [18, 100, 120, 115, 77]))
    story.append(PageBreak())

    # ─── SECTION 06 : ÉCLAIRAGE ─────────────────────────────────────────────
    story.append(section_bar(6, 'CONCEPT ÉCLAIRAGE'))
    story.append(sp(14))

    story.append(p(
        'L\'architecture lumineuse est l\'un des leviers les plus puissants du design. '
        'L\'espace dispose déjà d\'une <b>cove lighting LED intégrée au plafond coffre</b> — '
        'un atout exceptionnel. Le concept complète ce socle avec une stratégie '
        '<b>DALI (Digital Addressable Lighting Interface)</b> permettant de programmer '
        'des scénarios lumineux par zone, par heure et par usage. '
        '"Café morning" (lumière chaude 2700K), "Cours focus" (lumière neutre 4000K), '
        '"Soirée culturelle" (lumière tamisée dramatique) — chaque moment a sa signature.'
    ))
    story.append(sp(8))

    story.append(make_lighting())
    story.append(ps('Architecture lumineuse par zone — système DALI — gradation programmable'))
    story.append(sp(10))

    light_spec = [
        [Paragraph(h, S['table_header']) for h in
         ['Zone', 'Type luminaire', 'Kelvin', 'Marque suggérée', 'Budget']],
        ['A — Réception', 'Enseigne rétroéclairée + spots', '3000K', 'Philips Hue + custom', '8 000 SAR'],
        ['B — Café', '3 lanternes laiton Ø40cm + cove', '2700K warm', 'Artisans + importation', '14 000 SAR'],
        ['C — Salle 1', 'LED linéaire suspendue + spots tableau', '4000K neutre', 'TRILUX / Zumtobel', '9 000 SAR'],
        ['D — Salle 2', 'Suspension unique laiton + cove', '3000K', 'Louis Poulsen (budget)', '6 000 SAR'],
        ['E — Cours part.', 'Lampe arc laiton + spots accent', '2700K', 'Flos (alternatif local)', '7 000 SAR'],
        ['F — Admin', 'Dalle LED standard + bureau', '4000K', 'Philips / Osram', '4 000 SAR'],
        [Paragraph('<b>TOTAL ÉCLAIRAGE</b>', S['table_cell']),
         Paragraph('—', S['table_cell']),
         Paragraph('—', S['table_cell']),
         Paragraph('Contrôle DALI central inclus', S['table_cell']),
         Paragraph('<b>48 000 SAR</b>', S['table_cell'])],
    ]
    story.append(styled_table(light_spec, [80, 130, 65, 120, 75]))
    story.append(PageBreak())

    # ─── SECTION 07 : BUDGET ────────────────────────────────────────────────
    story.append(section_bar(7, 'BUDGET AMÉNAGEMENT DÉTAILLÉ'))
    story.append(sp(14))

    story.append(p(
        'Le budget d\'aménagement total est estimé à <b>280 000 SAR (~75 000 USD)</b> '
        'pour une finition premium complète. Ce chiffre tient compte des atouts existants '
        '(sol, cove lighting, cloisons) qui réduisent significativement les coûts structurels. '
        'L\'investissement est principalement orienté vers la menuiserie sur-mesure, '
        'le mobilier et les éléments de marque différenciants.'
    ))
    story.append(sp(8))

    story.append(make_budget_chart())
    story.append(ps('Répartition du budget aménagement intérieur — 280 000 SAR total — Estimation juin 2025'))
    story.append(sp(10))

    budget_detail = [
        [Paragraph(h, S['table_header']) for h in
         ['Poste', 'Description', 'SAR', 'USD', 'Délai']],
        ['Sol béton ciré (Zone A)', 'Application béton ciré 18m², ponçage, vernis', '28 000', '7 467', 'Semaine 1-2'],
        ['Menuiserie noyer', 'Étagères, desk accueil, bar café, boiseries', '45 000', '12 000', 'Semaine 2-5'],
        ['Comptoir café marbre', 'Plan travail marbre 2m + habillage bois', '35 000', '9 333', 'Semaine 3-5'],
        ['Luminaires (toutes zones)', 'Lanternes, suspensions, lampes, LED DALI', '22 000', '5 867', 'Semaine 4-6'],
        ['Mobilier salles cours', 'Tables, chaises, panneaux phoniques', '30 000', '8 000', 'Semaine 5-7'],
        ['Mobilier café lounge', 'Tables rondes, banquettes, majlis coussins', '38 000', '10 133', 'Semaine 5-7'],
        ['Réception desk custom', 'Desk courbe noyer + laiton + signalétique', '18 000', '4 800', 'Semaine 3-5'],
        ['Art & calligraphie', 'Œuvres murales, enseignes, calligraphie laiton', '12 000', '3 200', 'Semaine 6-8'],
        ['Plantes & accessoires', 'Végétaux, caches-pots laiton, déco', '8 000', '2 133', 'Semaine 8'],
        ['Signalétique & branding', 'Logo 3D, panneaux zones, QR codes', '15 000', '4 000', 'Semaine 7-8'],
        ['Textiles & rideaux', 'Rideaux lin, coussins, nappes café', '10 000', '2 667', 'Semaine 7-8'],
        ['Zellige & revêtements', 'Zellige terracotta mur café + film mashrabiya', '9 000', '2 400', 'Semaine 4-6'],
        ['Équipement café', 'Machine espresso, frigo vitrine, accessoires', '25 000', '6 667', 'Semaine 7-8'],
        ['Imprévus & ajustements', 'Réserve 10% — toujours prévoir', '25 000', '6 667', '—'],
        [Paragraph('<b>TOTAL</b>', S['table_cell']),
         Paragraph('<b>Aménagement complet & équipement café</b>', S['table_cell']),
         Paragraph('<b>280 000 SAR</b>', ParagraphStyle('tb', fontName='Helvetica-Bold',
             fontSize=9, textColor=GOLD)),
         Paragraph('<b>~74 667 USD</b>', ParagraphStyle('tb2', fontName='Helvetica-Bold',
             fontSize=9, textColor=GOLD)),
         Paragraph('<b>8–10 semaines</b>', S['table_cell'])],
    ]
    for i in range(1, len(budget_detail)-1):
        budget_detail[i] = [Paragraph(str(c), S['table_cell']) for c in budget_detail[i]]
    story.append(styled_table(budget_detail, [130, 130, 55, 55, 70]))
    story.append(PageBreak())

    # ─── SECTION 08 : IDENTITÉ VISUELLE ────────────────────────────────────
    story.append(section_bar(8, 'IDENTITÉ VISUELLE & ÉLÉMENTS DE MARQUE'))
    story.append(sp(14))

    story.append(p(
        'L\'espace physique doit être une extension tangible de la marque CLR. '
        'Chaque élément visuel renforce l\'identité et contribue à la <b>mémorabilité de l\'expérience</b>. '
        'L\'objectif est que tout visiteur qui entre dans le centre reconnaisse instantanément '
        'l\'univers "Al-Maktaba" et veuille le partager sur ses réseaux sociaux.'
    ))
    story.append(sp(10))

    branding_items = [
        ('Logo mural 3D — entrée',
         'Lettres découpées en laiton brossé "CLR" + "مركز اللغات" sur fond stuc sable. '
         'Rétroéclairage LED blanc chaud. Taille : 80cm × 30cm.',
         '3 500 SAR'),
        ('Film mashrabiya sur cloisons vitrées',
         'Motif géométrique islamique gravé sur vinyle dépoli. Posé sur vitres existantes. '
         'Double effet : intimité acoustique + œuvre d\'art structurale.',
         '4 500 SAR'),
        ('Ardoise menu café bilingue',
         'Ardoise noire 120×80cm avec texte calligraphié en arabe + français. '
         'Encadrement bois noyer. Renouvelée chaque semaine — contenu pédagogique intégré.',
         '800 SAR'),
        ('Mur de citations multilingues',
         'Corridor ou mur secondaire : 12 citations inspirantes en 12 langues, '
         'typographie soignée, impression sur alu-dibond. Signature visuelle instagrammable.',
         '5 500 SAR'),
        ('QR codes design',
         'QR codes encadrés dans des médaillons laiton — accès rapide programme, prix, '
         'WhatsApp inscription. Répartis dans tout le centre.',
         '1 200 SAR'),
        ('Uniformes staff',
         'Équipe : chemise lin ivoire + tablier noyer (café) / chemise blanche + badge laiton '
         '(enseignants). Coiffures neutres. Cohérence totale avec l\'espace.',
         '4 800 SAR'),
        ('"Coin Instagram" dédié',
         'Un angle de 1m² designé spécifiquement pour les photos : mur zellige terracotta + '
         'plante suspendue + lanterne + neon "مركز اللغات" rose-gold.',
         '6 000 SAR'),
    ]

    for title, desc, budget in branding_items:
        row = Table([[
            Paragraph(f'<b>{title}</b>', ParagraphStyle('bt',
                fontName='Helvetica-Bold', fontSize=9, textColor=TEAL)),
            Paragraph(desc, ParagraphStyle('bd', fontName='Helvetica',
                fontSize=8.5, leading=13, textColor=DARK_GRAY)),
            Paragraph(budget, ParagraphStyle('bb', fontName='Helvetica-Bold',
                fontSize=9, textColor=GOLD, alignment=TA_RIGHT)),
        ]], colWidths=[125, 235, 70])
        row.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(0,0), colors.HexColor('#EBF4FD')),
            ('BACKGROUND', (2,0),(2,0), colors.HexColor('#FEF9EC')),
            ('TOPPADDING',(0,0),(-1,-1),7),
            ('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),8),
            ('RIGHTPADDING',(0,0),(-1,-1),8),
            ('LINEBELOW',(0,0),(-1,-1),0.4, colors.HexColor('#D0D5DB')),
            ('VALIGN',(0,0),(-1,-1),'TOP'),
        ]))
        story.append(row)
        story.append(sp(2))

    story.append(PageBreak())

    # ─── SECTION 09 : PLANNING ──────────────────────────────────────────────
    story.append(section_bar(9, 'PLANNING TRAVAUX & LIVRAISON'))
    story.append(sp(14))

    story.append(p(
        'L\'aménagement complet peut être livré en <b>8 à 10 semaines</b> avec une équipe '
        'de chantier dédiée. La phase critique est la menuiserie sur-mesure (noyer) '
        'qui nécessite 4-5 semaines de fabrication. Le planning ci-dessous est optimisé '
        'pour une ouverture opérationnelle au terme de la semaine 10.'
    ))
    story.append(sp(8))

    planning_data = [
        [Paragraph(h, S['table_header']) for h in
         ['Phase', 'Semaine', 'Actions', 'Intervenant', 'Statut']],
        ['Phase 0 — Préparation', 'S-1 à S0', 'Validation concept, commandes matières,\ndévis menuisier, dépôt permis', 'Studio CLR + propriétaire', '⏳ Planifier'],
        ['Phase 1 — Gros œuvre', 'S1 à S2', 'Béton ciré Zone A, peinture sable chaud\ntous murs, ragréage si besoin', 'Entreprise peinture/béton', '🏗️ Travaux'],
        ['Phase 2 — Menuiserie', 'S2 à S5', 'Fabrication atelier : desk, étagères,\ncomptoir café, boiseries', 'Menuisier spécialisé', '🔨 Fabrication'],
        ['Phase 3 — Zellige & films', 'S4 à S6', 'Pose zellige terracotta (2m²),\nfilm mashrabiya vitrages', 'Carreleur + poseur vinyle', '🎨 Décoration'],
        ['Phase 4 — Électricité / Lumière', 'S4 à S6', 'Câblage DALI, pose luminaires,\nspot tableau interactif, néon', 'Électricien + éclairagiste', '💡 Installation'],
        ['Phase 5 — Mobilier', 'S6 à S7', 'Livraison et pose tables, chaises,\ncanapés, panneaux phoniques', 'Studio CLR + livreurs', '🪑 Livraison'],
        ['Phase 6 — Branding & Art', 'S7 à S8', 'Logo 3D entrée, calligraphies,\nQR codes, mur citations, néon', 'Artisans signalétique', '✦ Finitions'],
        ['Phase 7 — Végétaux & Déco', 'S8', 'Plantes, caches-pots, accessoires,\nlivres, merch initial', 'Studio CLR styling', '🌿 Styling'],
        ['Phase 8 — Réception', 'S9 à S10', 'Réception chantier, punch list,\nadjustements, photoshoot', 'Studio CLR + client', '📸 Livraison'],
        ['OUVERTURE', '⭐ S10', 'Soft opening — événement inauguration', 'Équipe CLR complète', '🎉 Objectif'],
    ]
    for i in range(1, len(planning_data)):
        planning_data[i] = [Paragraph(str(c), S['table_cell']) for c in planning_data[i]]
    story.append(styled_table(planning_data, [100, 55, 150, 100, 65]))
    story.append(sp(12))

    story.append(info_box(
        '📸  Photoshoot professionnel — stratégie contenu',
        'À la livraison (Semaine 9-10), un photoshoot architectural professionnel (full day) est '
        'indispensable. Budget estimé : 3 500 SAR. Livrables : 40-60 photos HD, 2-3 vidéos courtes '
        '(Reels/TikTok), drone shot de la façade. Ce contenu alimente 3 mois de publications '
        'réseaux sociaux et donne la crédibilité visuelle pour les pitches corporate.',
        S, bg='#F0F8FF', border_col=TEAL
    ))
    story.append(PageBreak())

    # ─── SECTION 10 : SYNTHÈSE ──────────────────────────────────────────────
    story.append(section_bar(10, 'SYNTHÈSE DESIGN & PROCHAINES ÉTAPES'))
    story.append(sp(14))

    story.append(p(
        'Le concept "Al-Maktaba" transforme un plateau brut de 160 m² en un espace '
        'culturel premium qui rayonnera bien au-delà de ses murs. Par sa cohérence '
        'visuelle, sa fonctionnalité optimisée et ses zones Instagrammables par conception, '
        'il deviendra <b>le centre de référence linguistique et culturel de Riyad</b>.'
    ))
    story.append(sp(10))

    # Final comparison table
    story.append(h2('Avant / Après — Comparaison par zone'))
    avant_apres = [
        [Paragraph(h, S['table_header']) for h in ['Zone', 'AVANT (état actuel)', 'APRÈS (concept Al-Maktaba)', 'Impact']],
        ['A — Entrée', 'Porte bois sombre, espace vide', 'Desk noyer, calligraphie laiton, béton ciré, olive tree', 'Wow factor immédiat'],
        ['B — Grand espace', 'Plateau vide 40m²', 'Café Maktaba : comptoir marbre, étagères 3m, lanternes, zellige', 'Générateur de revenu J1'],
        ['C — Salle vitrée', 'Vide avec cloison frosted', 'Salle cours : mobilier scandi, mashrabiya film, whiteboard', 'Capacité 10-12 élèves'],
        ['D — Salle fermée', 'Pièce vide, porte bois', 'Semi-privé premium : table noyer, fauteuils terra, artwork', 'Revenue ×1.8'],
        ['E — 2ème salle', 'Vide', 'Salon particuliers : cuir, ficus, lampe arc, bibliothèque', 'Revenue ×2.5'],
        ['Cuisine', 'Meubles gris basiques, évier', 'Back-of-house café : machine espresso, réfrigération', 'Opérationnel Maktaba'],
    ]
    for i in range(1, len(avant_apres)):
        avant_apres[i] = [Paragraph(str(c), S['table_cell']) for c in avant_apres[i]]
    story.append(styled_table(avant_apres, [65, 130, 160, 85]))
    story.append(sp(12))

    story.append(info_box(
        '⚡  3 décisions immédiates à prendre',
        '1. VALIDER le concept et autoriser Studio CLR à lancer les devis détaillés auprès '
        'des artisans et menuisiers (délai : 48h). '
        '2. COMMANDER le zellige terracotta et les luminaires laiton (délais de livraison 3-4 semaines). '
        '3. CONFIRMER la machine espresso et le fournisseur café (La Marzocco ou Bezzera) '
        'pour un démarrage café synchrone avec l\'ouverture du centre.',
        S, bg='#EAFAF0', border_col=SAGE
    ))
    story.append(sp(10))

    story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=8))
    story.append(Paragraph(
        '"Un espace bien conçu ne se limite pas à être beau — il travaille pour vous 24h/24 '
        'en attirant, retenant et fidélisant chaque visiteur."',
        S['quote']
    ))
    story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=8))
    story.append(Paragraph(
        '© 2025 Studio CLR Design — Concept exclusif — Centre Linguistique de Riyad',
        S['footer_note']
    ))

    return story

# ═══════════════════════════════════════════════════════════════════════════
# BUILD PDF
# ═══════════════════════════════════════════════════════════════════════════
def build():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=38*mm, rightMargin=38*mm,
        topMargin=36*mm, bottomMargin=26*mm,
        title='AL-MAKTABA — Concept Design — Centre Linguistique de Riyad',
        author='Studio CLR Design',
        subject='Interior Design Concept — Confidentiel',
    )
    story = build_story()
    doc.build(story, onFirstPage=on_first, onLaterPages=on_later)
    print(f'PDF généré : {OUTPUT}')

if __name__ == '__main__':
    import numpy as np
    np.random.seed(42)
    build()
