#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLR — DESIGN CONCEPT "AL-MAKTABA"
100% matplotlib PdfPages — zero ReportLab — pixel-perfect control
Studio-quality interior design presentation document
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge, Arc
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.patheffects as pe
import matplotlib.font_manager as fm
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ── Register fonts ──────────────────────────────────────────────────────────
try:
    fm.fontManager.addfont('/tmp/fonts/Montserrat.ttf')
    FONT_TITLE = 'Montserrat'
except:
    FONT_TITLE = 'DejaVu Sans'

try:
    fm.fontManager.addfont('/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Regular.ttf')
    fm.fontManager.addfont('/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Bold.ttf')
    FONT_ARABIC = 'Amiri'
except:
    FONT_ARABIC = 'DejaVu Sans'

FONT_BODY = 'DejaVu Sans'

# ── Arabic text helper ───────────────────────────────────────────────────────
import arabic_reshaper
from bidi.algorithm import get_display

def ar(text):
    """Reshape + bidi-reorder Arabic text for correct matplotlib rendering."""
    return get_display(arabic_reshaper.reshape(text))

OUTPUT = '/home/user/ABD-BND/CLR_Design_Concept_v2.pdf'

# ── COLOUR SYSTEM ─────────────────────────────────────────────────────────────
NAVY    = '#0D1B2A'
NAVY2   = '#1A2E40'
GOLD    = '#C9A84C'
GOLD_LT = '#E8C97A'
SAND    = '#F5EFE4'
WALNUT  = '#3D2314'
TERRA   = '#B5622F'
SAGE    = '#6B8F71'
IVORY   = '#FAF6EF'
MID     = '#8A9BB0'
DARK    = '#2C3E50'
WHITE   = '#FFFFFF'
TEAL    = '#1B5E7A'
TEAL_LT = '#2D8FA3'
CREAM   = '#F0E9DC'
CHARCOAL= '#2A2A2A'
ROSE    = '#C49A8A'

# ── PAGE SETUP ─────────────────────────────────────────────────────────────────
W_IN, H_IN = 8.27, 11.69   # A4
DPI = 180

def new_page(facecolor=WHITE):
    fig = plt.figure(figsize=(W_IN, H_IN), dpi=DPI)
    fig.patch.set_facecolor(facecolor)
    return fig

def ax_at(fig, left, bottom, width, height, facecolor='none'):
    ax = fig.add_axes([left, bottom, width, height])
    ax.set_facecolor(facecolor)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    return ax

def txt(ax, x, y, s, size=10, color=CHARCOAL, weight='normal',
        ha='left', va='baseline', style='normal', alpha=1.0, font=None):
    if font is None: font = FONT_BODY
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight,
            ha=ha, va=va, fontstyle=style, alpha=alpha,
            fontfamily=font, transform=ax.transAxes)

def hline(ax, y, x0=0, x1=1, color=GOLD, lw=0.8, alpha=1.0):
    ax.axhline(y=y, xmin=x0, xmax=x1, color=color, linewidth=lw, alpha=alpha)

def vline(ax, x, y0=0, y1=1, color=GOLD, lw=0.8, alpha=1.0):
    ax.axvline(x=x, ymin=y0, ymax=y1, color=color, linewidth=lw, alpha=alpha)

def rect(ax, x, y, w, h, color=NAVY, alpha=1.0, zorder=1):
    r = patches.FancyBboxPatch((x, y), w, h, boxstyle='square,pad=0',
                                facecolor=color, edgecolor='none', alpha=alpha, zorder=zorder)
    ax.add_patch(r)

def border_rect(ax, x, y, w, h, edgecolor=GOLD, lw=0.8, facecolor='none'):
    r = patches.Rectangle((x, y), w, h, facecolor=facecolor,
                           edgecolor=edgecolor, linewidth=lw)
    ax.add_patch(r)

def chip(ax, x, y, label, bg=GOLD, fg=WHITE, size=6.5, pad_x=0.012, pad_y=0.008):
    tw = len(label) * size * 0.009
    r = patches.FancyBboxPatch((x, y-pad_y), tw+pad_x*2, size*0.022+pad_y*2,
                                boxstyle='round,pad=0.002',
                                facecolor=bg, edgecolor='none', zorder=10)
    ax.add_patch(r)
    ax.text(x+pad_x+tw/2, y+size*0.008, label, fontsize=size, color=fg,
            fontweight='bold', ha='center', va='center',
            fontfamily=FONT_TITLE, transform=ax.transAxes, zorder=11)

def arabesque_bg(ax, n=8, color=GOLD, alpha=0.06):
    """Subtle geometric pattern"""
    for i in range(n):
        for j in range(n):
            x = i/n + 0.5/n
            y = j/n + 0.5/n
            # Diamond shapes
            size = 0.04
            pts = np.array([[x, y+size],[x+size,y],[x,y-size],[x-size,y],[x,y+size]])
            ax.plot(pts[:,0], pts[:,1], color=color, lw=0.4, alpha=alpha,
                    transform=ax.transAxes)
            # Inner diamond
            s2 = size*0.5
            pts2 = np.array([[x,y+s2],[x+s2,y],[x,y-s2],[x-s2,y],[x,y+s2]])
            ax.plot(pts2[:,0], pts2[:,1], color=color, lw=0.3, alpha=alpha*0.7,
                    transform=ax.transAxes)

def page_header(fig, title, subtitle=None):
    """Standard page header for inner pages"""
    ax = ax_at(fig, 0, 0.94, 1, 0.06, facecolor=NAVY)
    txt(ax, 0.06, 0.55, 'CENTRE LINGUISTIQUE DE RIYAD  ·  CONCEPT AL-MAKTABA',
        size=6.5, color=GOLD, weight='bold', font=FONT_TITLE)
    txt(ax, 0.94, 0.55, 'STUDIO CLR  ·  CONFIDENTIEL  ·  JUIN 2025',
        size=6.5, color=MID, ha='right', font=FONT_TITLE)

def page_footer(fig, page_num, section=''):
    ax = ax_at(fig, 0, 0, 1, 0.038, facecolor=NAVY)
    # Gold top line
    hline(ax, 0.85, color=GOLD, lw=1.5)
    txt(ax, 0.06, 0.3, section.upper(), size=6, color=MID, font=FONT_TITLE)
    txt(ax, 0.94, 0.3, str(page_num), size=6.5, color=GOLD, ha='right',
        weight='bold', font=FONT_TITLE)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 1: COVER
# ═══════════════════════════════════════════════════════════════════════════════
def page_cover():
    fig = new_page(facecolor=NAVY)

    # ── Full background ──
    ax_bg = ax_at(fig, 0, 0, 1, 1, facecolor=NAVY)
    arabesque_bg(ax_bg, n=10, alpha=0.045)

    # ── Right panel – dark ──
    ax_right = ax_at(fig, 0.56, 0.08, 0.44, 0.84, facecolor='#0A1520')
    # Geometric grid
    for i in np.linspace(0, 1, 16):
        ax_right.axhline(i, color=GOLD, lw=0.15, alpha=0.3)
        ax_right.axvline(i, color=GOLD, lw=0.15, alpha=0.3)
    # Diamond pattern
    np.random.seed(7)
    for _ in range(40):
        x, y = np.random.uniform(0.05, 0.95), np.random.uniform(0.05, 0.95)
        s = np.random.uniform(0.025, 0.065)
        pts = np.array([[x,y+s],[x+s,y],[x,y-s],[x-s,y],[x,y+s]])
        ax_right.plot(pts[:,0], pts[:,1], color=GOLD, lw=0.5, alpha=0.18)
    # Arabic text in right panel
    ax_right.text(0.5, 0.72, ar('مركز اللغات'), fontsize=28, color=GOLD, fontfamily=FONT_ARABIC,
                  ha='center', va='center', alpha=0.9,
                  transform=ax_right.transAxes)
    ax_right.text(0.5, 0.58, ar('الرياض'), fontsize=18, color=GOLD_LT, fontfamily=FONT_ARABIC,
                  ha='center', va='center', alpha=0.6,
                  transform=ax_right.transAxes)
    # Horizontal divider
    ax_right.axhline(0.5, xmin=0.1, xmax=0.9, color=GOLD, lw=0.6, alpha=0.4)
    # Key specs
    specs = [('SURFACE', '160 m²'), ('CONCEPT', 'AL-MAKTABA'),
             ('STYLE', 'ARABESQUE CONTEMP.'), ('BUDGET', '280 000 SAR')]
    for i, (k, v) in enumerate(specs):
        y_pos = 0.38 - i * 0.08
        ax_right.text(0.15, y_pos, k, fontsize=6.5, color=MID,
                      fontfamily=FONT_TITLE, transform=ax_right.transAxes)
        ax_right.text(0.15, y_pos - 0.033, v, fontsize=8.5, color=WHITE,
                      fontweight='bold', fontfamily=FONT_TITLE,
                      transform=ax_right.transAxes)

    # ── Left panel – main content ──
    ax_left = ax_at(fig, 0.06, 0.08, 0.46, 0.84)

    # Gold accent bar
    r = patches.Rectangle((0, 0), 0.025, 1, facecolor=GOLD, edgecolor='none')
    ax_left.add_patch(r)
    r2 = patches.Rectangle((0.038, 0), 0.006, 1, facecolor=GOLD_LT, edgecolor='none', alpha=0.4)
    ax_left.add_patch(r2)

    # Tag
    txt(ax_left, 0.08, 0.935, 'CONCEPT D\'AMÉNAGEMENT INTÉRIEUR',
        size=7, color=GOLD, weight='bold', font=FONT_TITLE)

    # Main title
    ax_left.text(0.08, 0.82, 'AL-', fontsize=62, color=WHITE,
                 fontweight='bold', va='top', fontfamily=FONT_TITLE,
                 transform=ax_left.transAxes, linespacing=0.85)
    ax_left.text(0.08, 0.70, 'MAKTABA', fontsize=42, color=WHITE,
                 fontweight='light', va='top', fontfamily=FONT_TITLE,
                 transform=ax_left.transAxes)

    # Subtitle Arabic
    txt(ax_left, 0.08, 0.625, 'المكتبة — The Living Library',
        size=11, color=GOLD_LT, style='italic', font=FONT_BODY)

    # Divider
    hline(ax_left, 0.59, x0=0.05, x1=0.95, color=GOLD, lw=0.8)

    # Description
    lines_desc = [
        'Un centre linguistique ancré dans la culture arabe',
        'contemporaine — espace de vie, d\'apprentissage',
        'et de partage au cœur de Riyad.'
    ]
    for i, line in enumerate(lines_desc):
        txt(ax_left, 0.08, 0.555 - i*0.04, line,
            size=9, color=MID, font=FONT_BODY)

    # Chips
    chips_data = [('NORD RIYAD', TEAL), ('PREMIUM', GOLD), ('LIFESTYLE', TERRA)]
    cx = 0.08
    for label, bg in chips_data:
        w_chip = len(label) * 0.012 + 0.04
        r = patches.FancyBboxPatch((cx, 0.415), w_chip, 0.034,
                                    boxstyle='round,pad=0.003',
                                    facecolor=bg, edgecolor='none')
        ax_left.add_patch(r)
        ax_left.text(cx + w_chip/2, 0.432, label, fontsize=6.5, color=WHITE,
                     fontweight='bold', ha='center', va='center',
                     fontfamily=FONT_TITLE, transform=ax_left.transAxes)
        cx += w_chip + 0.025

    # Space analysis box
    border_rect(ax_left, 0.08, 0.22, 0.88, 0.165, edgecolor=GOLD_LT, lw=0.6)
    txt(ax_left, 0.14, 0.365, 'ESPACE ANALYSÉ — SHELL EXISTANT',
        size=6.5, color=GOLD_LT, weight='bold', font=FONT_TITLE)
    space_facts = [
        '→  Sol vinyle marbre gris — état premium — à conserver',
        '→  Plafond coffre bois foncé + LED cove intégrée — atout majeur',
        '→  Cloisons vitrées frosted — parfaites pour les classes',
        '→  Cuisine existante — convertible en back-of-house café',
        '→  État shell brut — aucun génie civil lourd requis',
    ]
    for i, fact in enumerate(space_facts):
        txt(ax_left, 0.14, 0.338 - i*0.028, fact,
            size=7.5, color=WHITE, alpha=0.85, font=FONT_BODY)

    # Bottom meta
    meta_items = [('DESIGNER', 'Studio CLR'), ('DATE', 'Juin 2025'),
                  ('VERSION', 'v2.0'), ('STATUT', 'Confidentiel')]
    hline(ax_left, 0.175, x0=0.05, x1=0.95, color=GOLD, lw=0.4, alpha=0.5)
    for i, (k, v) in enumerate(meta_items):
        x_pos = 0.08 + i*0.225
        txt(ax_left, x_pos, 0.135, k, size=6, color=MID, font=FONT_TITLE)
        txt(ax_left, x_pos, 0.095, v, size=8, color=WHITE,
            weight='bold', font=FONT_TITLE)

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 2: ANALYSE DE L'ESPACE
# ═══════════════════════════════════════════════════════════════════════════════
def page_analysis():
    fig = new_page(facecolor=IVORY)
    page_header(fig, 'Analyse de l\'espace')
    page_footer(fig, 2, 'Analyse de l\'espace existant')

    # ── Left Navy column ──────────────────────────────────────────────────────
    ax_col = ax_at(fig, 0, 0.038, 0.32, 0.902, facecolor=NAVY)
    txt(ax_col, 0.13, 0.955, '01', size=38, color=GOLD_LT, weight='bold',
        font=FONT_TITLE, va='top', alpha=0.35)
    txt(ax_col, 0.13, 0.91, 'ANALYSE', size=13, color=WHITE,
        weight='bold', font=FONT_TITLE, va='top')
    txt(ax_col, 0.13, 0.875, 'DE L\'ESPACE', size=13, color=GOLD,
        weight='bold', font=FONT_TITLE, va='top')
    hline(ax_col, 0.86, x0=0.1, x1=0.9, color=GOLD, lw=0.6)

    # Stats
    stats = [('160', 'm²  Surface totale'),('6', 'Zones fonctionnelles'),
             ('3', 'Salles pédagogiques'),('1', 'Café "Maktaba"'),
             ('10', 'Sem. de travaux')]
    for i, (val, label) in enumerate(stats):
        y = 0.81 - i * 0.095
        ax_col.text(0.13, y, val, fontsize=24, color=GOLD, fontweight='bold',
                    fontfamily=FONT_TITLE, transform=ax_col.transAxes)
        txt(ax_col, 0.13, y - 0.035, label, size=7.5, color=MID, font=FONT_BODY)
        hline(ax_col, y - 0.055, x0=0.1, x1=0.9, color='#1A3050', lw=0.4)

    # Bottom quote
    hline(ax_col, 0.28, x0=0.1, x1=0.9, color=GOLD, lw=0.4)
    quote = ['"Un shell d\'exception —', 'la structure fait', 'déjà le travail."']
    for i, line in enumerate(quote):
        txt(ax_col, 0.13, 0.25 - i*0.04, line,
            size=8.5, color=GOLD_LT, style='italic', font=FONT_BODY)

    # ── Right content area ────────────────────────────────────────────────────
    content_l = 0.36
    content_w = 0.58

    # Section title
    ax_title = ax_at(fig, content_l, 0.86, content_w, 0.075)
    txt(ax_title, 0, 0.75, 'INVENTAIRE ARCHITECTURAL', size=15, color=NAVY,
        weight='bold', font=FONT_TITLE)
    hline(ax_title, 0.25, color=GOLD, lw=2)

    # Analysis items
    items = [
        ('SOL VINYLE MARBRE GRIS', 'Très bon état, finition premium.',
         'Conserver intégralement — pas de remplacement requis.', '+ CONSERVER', SAGE),
        ('PLAFOND COFFRE BOIS + LED COVE', 'Intégré, lumière chaude 2700K.',
         'Atout majeur — amplifier avec spots design et lanternes.', '+ CONSERVER', SAGE),
        ('CLOISONS VITRÉES FROSTED', 'Deux séparations existantes.',
         'Poser film vinyle motif mashrabiya — double effet acoustique + design.', '~ AMÉLIORER', GOLD),
        ('PORTES ACCORDÉON BOIS FONCÉ', 'Qualité correcte, couleur adaptée.',
         'Remplacer poignées → laiton brossé. Option peinture deep navy.', '~ AMÉLIORER', GOLD),
        ('GRAND ESPACE OUVERT (~40m²)', 'Shell vide — murs blancs.',
         'Transformer en Café Maktaba : comptoir, étagères, lounge.', '> TRANSFORMER', TERRA),
        ('SALLE VITRÉE (~35m²)', 'Vide avec cloison existante.',
         'Salle de cours groupes 8–12 personnes + tableau interactif 86".', '> TRANSFORMER', TERRA),
        ('PIÈCE FERMÉE (~20m²)', 'Vide, porte bois foncé.',
         'Salon semi-privé premium ou cours particuliers exécutifs.', '> TRANSFORMER', TERRA),
        ('CUISINE EXISTANTE', 'Meubles gris, évier, prises.',
         'Back-of-house café : machine espresso, réfrigération, préparation.', '~ AMÉLIORER', GOLD),
    ]

    for i, (title, current, action, status, status_col) in enumerate(items):
        row_y = 0.828 - i * 0.1
        ax_row = ax_at(fig, content_l, row_y, content_w, 0.088)

        # Alternating background
        bg = '#F0EBE2' if i % 2 == 0 else IVORY
        rect(ax_row, 0, 0, 1, 1, color=bg, alpha=1)

        # Left accent bar color
        rect(ax_row, 0, 0, 0.008, 1, color=status_col)

        # Status chip
        chip_w = 0.18
        r_chip = patches.FancyBboxPatch((0.79, 0.52), chip_w, 0.36,
                                         boxstyle='round,pad=0.01',
                                         facecolor=status_col, edgecolor='none',
                                         alpha=0.15)
        ax_row.add_patch(r_chip)
        ax_row.text(0.88, 0.70, status, fontsize=5.5, color=status_col,
                    fontweight='bold', ha='center', va='center',
                    fontfamily=FONT_TITLE, transform=ax_row.transAxes)

        # Title
        txt(ax_row, 0.025, 0.82, title, size=7.5, color=NAVY,
            weight='bold', font=FONT_TITLE, va='top')
        # Current state
        txt(ax_row, 0.025, 0.56, f'État : {current}', size=7,
            color=DARK, font=FONT_BODY, va='top', alpha=0.8)
        # Action
        txt(ax_row, 0.025, 0.28, f'Action : {action}', size=7,
            color=TEAL, font=FONT_BODY, va='top', weight='bold')

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 3: CONCEPT & MOOD BOARD
# ═══════════════════════════════════════════════════════════════════════════════
def page_concept():
    fig = new_page(facecolor=CHARCOAL)
    page_header(fig, 'Concept')
    page_footer(fig, 3, 'Concept & Inspiration')

    # Full dark background with subtle pattern
    ax_bg = ax_at(fig, 0, 0, 1, 1, facecolor=CHARCOAL)
    for i in np.linspace(0, 1, 22):
        ax_bg.axhline(i, color='white', lw=0.1, alpha=0.06)

    # Section label
    ax_top = ax_at(fig, 0.05, 0.875, 0.9, 0.06)
    txt(ax_top, 0, 0.75, '02   CONCEPT & INSPIRATION', size=7,
        color=GOLD, weight='bold', font=FONT_TITLE)
    txt(ax_top, 0, 0.0, 'AL-MAKTABA  ·  Arabesques Contemporaines  ·  Wabi-Sabi  ·  Lifestyle Store',
        size=13, color=WHITE, weight='light', font=FONT_TITLE)

    # ── 6-tile mood board ──────────────────────────────────────────────────────
    tiles = [
        # (left, bottom, width, height, bg, accent, title, keywords, desc)
        (0.03, 0.49, 0.30, 0.35, WALNUT, GOLD,
         'BOISERIES & MATIÈRES', 'NOYER · LAITON · MARBRE',
         'Menuiserie sur-mesure — étagères floor-to-ceiling — comptoir marbre Crema Marfil'),

        (0.35, 0.49, 0.30, 0.35, '#3D1A0A', TERRA,
         'PALETTE ARABE', 'TERRA · OR · NAVY · SABLE',
         'Zellige terracotta 15×15 — stuc sablé chaud — accents laiton brossé'),

        (0.67, 0.49, 0.30, 0.35, '#0F2535', TEAL_LT,
         'ÉCLAIRAGE SIGNATURE', 'COVE · LANTERNE · DALI',
         'LED cove 2700K existante — lanternes laiton Ø40cm — DALI dimmable'),

        (0.03, 0.12, 0.30, 0.35, '#1C2E1C', SAGE,
         'VÉGÉTAL & BIEN-ÊTRE', 'FICUS · OLIVIER · ROTIN',
         'Plantes XXL — caches-pots laiton — mur végétal partiel — rotin naturel'),

        (0.35, 0.12, 0.30, 0.35, '#2A1A2E', '#9B7BC4',
         'CALLIGRAPHIE & ART', 'ARABIC · TYPE · GOLD',
         'Œuvres murales — enseigne laiton découpé — citations multilingues encadrées'),

        (0.67, 0.12, 0.30, 0.35, '#2A1208', ROSE,
         'CAFÉ MAKTABA', 'ESPRESSO · MARBRE · CUIR',
         'Comptoir signature — assises cuir cognac — majlis coussins — menu ardoise'),
    ]

    for left, bot, w, h, bg, accent, title, keywords, desc in tiles:
        ax_t = ax_at(fig, left, bot, w, h, facecolor=bg)

        # Subtle grid pattern inside tile
        for gi in np.linspace(0.1, 0.9, 8):
            ax_t.axhline(gi, color=accent, lw=0.15, alpha=0.2)

        # Gold border
        border_rect(ax_t, 0.01, 0.02, 0.98, 0.96, edgecolor=accent, lw=0.5)

        # Top accent line
        r = patches.Rectangle((0.01, 0.93), 0.98, 0.05, facecolor=accent, edgecolor='none', alpha=0.9)
        ax_t.add_patch(r)

        # Title on accent bar
        ax_t.text(0.5, 0.955, title, fontsize=7, color=NAVY if accent==GOLD else WHITE,
                  fontweight='bold', ha='center', va='center',
                  fontfamily=FONT_TITLE, transform=ax_t.transAxes)

        # Large decorative letter
        ax_t.text(0.08, 0.72, title[0], fontsize=52, color=accent, alpha=0.12,
                  va='top', fontfamily=FONT_TITLE, transform=ax_t.transAxes,
                  fontweight='bold')

        # Keywords
        txt(ax_t, 0.08, 0.68, keywords, size=6.5, color=accent,
            weight='bold', font=FONT_TITLE, va='top')

        # Description — wrapped manually
        words = desc.split()
        line, lines_out = '', []
        for w_word in words:
            test = line + ' ' + w_word if line else w_word
            if len(test) < 38:
                line = test
            else:
                lines_out.append(line)
                line = w_word
        if line: lines_out.append(line)

        for li, ln in enumerate(lines_out[:3]):
            txt(ax_t, 0.08, 0.48 - li*0.13, ln, size=7, color='#CCCCCC',
                font=FONT_BODY, va='top')

        # Bottom tag
        ax_t.text(0.92, 0.07, '→', fontsize=12, color=accent, ha='right',
                  va='bottom', transform=ax_t.transAxes)

    # Design philosophy statement
    ax_stmt = ax_at(fig, 0.05, 0.04, 0.9, 0.065)
    hline(ax_stmt, 0.85, color=GOLD, lw=0.5, alpha=0.5)
    ax_stmt.text(0.5, 0.35,
                 '"Chaque espace raconte une histoire — du comptoir café aux salles de cours, '
                 'tout respire la culture, l\'élégance et l\'ouverture sur le monde."',
                 fontsize=9.5, color=GOLD_LT, ha='center', va='center',
                 fontstyle='italic', fontfamily=FONT_BODY,
                 transform=ax_stmt.transAxes)

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 4: COLOUR & MATERIALS
# ═══════════════════════════════════════════════════════════════════════════════
def page_materials():
    fig = new_page(facecolor=IVORY)
    page_header(fig, 'Matières & Couleurs')
    page_footer(fig, 4, 'Palette matières & couleurs')

    # Section title
    ax_tl = ax_at(fig, 0.05, 0.875, 0.9, 0.062)
    txt(ax_tl, 0, 0.85, '03   PALETTE MATIÈRES & COULEURS', size=7,
        color=GOLD, weight='bold', font=FONT_TITLE)
    txt(ax_tl, 0, 0.08, 'Sélection de 8 matériaux premium — sourcing local & international — cohérence totale',
        size=12, color=NAVY, font=FONT_TITLE, weight='light')
    hline(ax_tl, 0.0, color=GOLD, lw=1.5)

    # ── 8 material swatches in 2×4 grid ──────────────────────────────────────
    materials = [
        # (bg, accent, pattern, number, name, application, spec1, spec2)
        (NAVY, GOLD, 'geo', '01', 'NAVY PROFOND',
         'Murs accent · Desk réception · Signalétique',
         'Couleur principale de marque', 'Hex #0D1B2A'),

        ('#C9A84C', NAVY, 'dots', '02', 'OR / LAITON',
         'Quincailleries · Accents · Luminaires · Borders',
         'Métal laiton brossé', 'Hex #C9A84C'),

        ('#F5EFE4', NAVY, 'lines', '03', 'SABLE CHAUD',
         'Murs principaux · Plafond · Fond général',
         'Stuc mat sablé', 'Hex #F5EFE4'),

        ('#3D2314', GOLD_LT, 'wood', '04', 'NOYER FONCÉ',
         'Étagères · Comptoir · Desk · Boiseries',
         'Noyer américain verni', 'Épaisseur 18 mm'),

        ('#B5622F', '#FAF6EF', 'tiles', '05', 'TERRA COTTA',
         'Zellige mur café · Coussins · Accents chauds',
         'Zellige marocain 15×15', 'Hand-made artisanal'),

        ('#6B8F71', '#FAF6EF', 'dots', '06', 'SAUGE NATUREL',
         'Panneaux phoniques · Plantes · Textiles cours',
         'Tissu sauge tendu', 'Laine minérale 50mm'),

        ('#E8E0D0', NAVY, 'marble', '07', 'MARBRE CREMA',
         'Comptoir café · Table salle D · Surfaces',
         'Crema Marfil Espagne', 'Poncé antidérapant'),

        ('#FAF6EF', TERRA, 'fabric', '08', 'LIN IVOIRE',
         'Rideaux · Coussins · Nappes café · Uniformes',
         '80% lin / 20% coton', 'Tissage naturel brut'),
    ]

    cols, rows = 4, 2
    sw = 0.21
    sh = 0.33
    gap_x, gap_y = 0.028, 0.025
    start_x = 0.04
    start_y = 0.515

    for idx, (bg, accent, pattern, num, name, appl, spec1, spec2) in enumerate(materials):
        col = idx % cols
        row = idx // cols
        lft = start_x + col*(sw + gap_x)
        bot = start_y - row*(sh + gap_y)

        ax_sw = ax_at(fig, lft, bot, sw, sh, facecolor=bg)

        # Pattern inside swatch
        if pattern == 'geo':
            for gi in np.linspace(0.1, 0.9, 7):
                for gj in np.linspace(0.1, 0.9, 7):
                    s = 0.055
                    pts = np.array([[gi,gj+s],[gi+s,gj],[gi,gj-s],[gi-s,gj],[gi,gj+s]])
                    ax_sw.plot(pts[:,0], pts[:,1], color=accent, lw=0.3, alpha=0.2)
        elif pattern == 'dots':
            for di in np.linspace(0.1, 0.9, 9):
                for dj in np.linspace(0.1, 0.9, 9):
                    c = Circle((di, dj), 0.018, facecolor=accent, alpha=0.15)
                    ax_sw.add_patch(c)
        elif pattern == 'lines':
            for li in np.linspace(0.05, 0.95, 18):
                ax_sw.axhline(li, color=NAVY, lw=0.3, alpha=0.08)
        elif pattern == 'wood':
            for wi in np.linspace(0, 1, 20):
                ax_sw.plot([0, 1],[wi, wi+0.05], color='#5A3520', lw=0.5, alpha=0.25)
        elif pattern == 'tiles':
            for ti in np.arange(0.05, 1, 0.18):
                for tj in np.arange(0.05, 1, 0.22):
                    r = patches.Rectangle((ti, tj), 0.15, 0.18, facecolor='none',
                                          edgecolor='#8B3A1A', lw=0.6, alpha=0.35)
                    ax_sw.add_patch(r)
        elif pattern == 'marble':
            np.random.seed(idx*3)
            for _ in range(10):
                x0 = np.random.uniform(0, 1)
                x1 = np.random.uniform(0, 1)
                y0 = np.random.uniform(0, 1)
                y1 = np.random.uniform(0, 1)
                ax_sw.plot([x0,x1],[y0,y1], color='#C0B090', lw=0.6, alpha=0.25)
        elif pattern == 'fabric':
            for fi in np.linspace(0.05, 0.95, 20):
                ax_sw.axhline(fi, color='#B0956A', lw=0.4, alpha=0.18)
            for fi in np.linspace(0.05, 0.95, 12):
                ax_sw.axvline(fi, color='#B0956A', lw=0.25, alpha=0.12)

        # Number badge
        c_num = Circle((0.12, 0.88), 0.1, facecolor=accent, edgecolor='none',
                        alpha=0.95, zorder=5)
        ax_sw.add_patch(c_num)
        ax_sw.text(0.12, 0.88, num, fontsize=8, color=NAVY if accent==GOLD else WHITE,
                   fontweight='bold', ha='center', va='center',
                   fontfamily=FONT_TITLE, transform=ax_sw.transAxes, zorder=6)

        # Bottom info band
        r_bot = patches.Rectangle((0, 0), 1, 0.38, facecolor='#00000055',
                                   edgecolor='none', zorder=4)
        ax_sw.add_patch(r_bot)

        # Text on dark band
        is_dark_bg = bg in [NAVY, '#3D2314', '#B5622F', '#6B8F71']
        txt_col = WHITE

        ax_sw.text(0.08, 0.335, name, fontsize=7.5, color=accent if is_dark_bg else NAVY,
                   fontweight='bold', va='top', fontfamily=FONT_TITLE,
                   transform=ax_sw.transAxes, zorder=5)
        ax_sw.text(0.08, 0.24, appl, fontsize=5.8, color='#DDDDDD',
                   va='top', fontfamily=FONT_BODY, transform=ax_sw.transAxes, zorder=5)
        ax_sw.text(0.08, 0.13, spec1, fontsize=5.5, color='#AAAAAA',
                   va='top', style='italic', fontfamily=FONT_BODY,
                   transform=ax_sw.transAxes, zorder=5)
        ax_sw.text(0.08, 0.04, spec2, fontsize=5.5, color='#888888',
                   va='top', style='italic', fontfamily=FONT_BODY,
                   transform=ax_sw.transAxes, zorder=5)

        # Gold border
        border_rect(ax_sw, 0.015, 0.01, 0.97, 0.98, edgecolor=GOLD_LT, lw=0.4)

    # Bottom note
    ax_note = ax_at(fig, 0.05, 0.058, 0.9, 0.05)
    hline(ax_note, 0.88, color=GOLD, lw=0.5, alpha=0.5)
    txt(ax_note, 0.5, 0.3,
        'Toutes les matières sont disponibles auprès de fournisseurs locaux à Riyad '
        '+ importation sélective (zellige Maroc, marbre Espagne, laiton Italie).',
        size=7.5, color=DARK, ha='center', font=FONT_BODY, va='baseline', alpha=0.8)

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 5: FLOOR PLAN
# ═══════════════════════════════════════════════════════════════════════════════
def page_floorplan():
    fig = new_page(facecolor='#F8F5F0')
    page_header(fig, 'Plan d\'aménagement')
    page_footer(fig, 5, 'Plan d\'aménagement — zones & flux')

    # Title
    ax_tl = ax_at(fig, 0.05, 0.875, 0.9, 0.062)
    txt(ax_tl, 0, 0.85, '04   PLAN D\'AMÉNAGEMENT', size=7, color=GOLD,
        weight='bold', font=FONT_TITLE)
    txt(ax_tl, 0, 0.08, '~160 m²  ·  6 zones fonctionnelles  ·  Nord Riyad',
        size=13, color=NAVY, font=FONT_TITLE, weight='light')
    hline(ax_tl, 0.0, color=GOLD, lw=1.5)

    # ── Architectural floor plan ──────────────────────────────────────────────
    ax_fp = ax_at(fig, 0.05, 0.175, 0.65, 0.69, facecolor='#FDFAF6')
    ax_fp.set_xlim(0, 22); ax_fp.set_ylim(0, 14)
    ax_fp.set_aspect('equal')
    ax_fp.axis('off')

    # Outer walls — drawn as thick rectangles
    wall_t = 0.35  # wall thickness

    def wall(ax, x, y, w, h):
        r = patches.Rectangle((x, y), w, h, facecolor='#2A2A2A', edgecolor='none')
        ax.add_patch(r)

    # Outer perimeter
    wall(ax_fp, 0, 0, 22, wall_t)        # bottom
    wall(ax_fp, 0, 14-wall_t, 22, wall_t) # top
    wall(ax_fp, 0, 0, wall_t, 14)         # left
    wall(ax_fp, 22-wall_t, 0, wall_t, 14) # right

    # Internal walls
    wall(ax_fp, 6-wall_t/2, wall_t, wall_t, 14-wall_t*2)       # A/B | C/D/E
    wall(ax_fp, 15-wall_t/2, wall_t, wall_t, 14-wall_t*2)      # B/E | F
    wall(ax_fp, wall_t, 8-wall_t/2, 6-wall_t, wall_t)          # A | café horizontal
    wall(ax_fp, 6-wall_t/2, 8-wall_t/2, 9+wall_t, wall_t)      # C | D horizontal

    # Zone fills
    zones_fp = [
        # (x, y, w, h, color, alpha, zone_id)
        (wall_t, 8, 6-wall_t*2, 6-wall_t*2, '#FFF8DC', 0.85, 'A'),  # Reception
        (wall_t, wall_t, 6-wall_t*2, 8-wall_t*1.5, '#E8F4E8', 0.85, 'B'),  # Café
        (6+wall_t/2, 8, 9-wall_t, 6-wall_t*2, '#E8EEF8', 0.85, 'C'),  # Salle 1
        (6+wall_t/2, wall_t, 9-wall_t, 8-wall_t*1.5, '#EDE8F5', 0.85, 'E'),  # Cours Priv
        (15+wall_t/2, 8, 7-wall_t*1.5, 6-wall_t*2, '#F5EDE8', 0.85, 'D'),  # Salle 2
        (15+wall_t/2, wall_t, 7-wall_t*1.5, 8-wall_t*1.5, '#E8F5F5', 0.85, 'F'),  # Admin
    ]
    for x, y, w, h, col, alpha, zid in zones_fp:
        r = patches.Rectangle((x, y), w, h, facecolor=col, edgecolor='#BBBBBB',
                               linewidth=0.5, alpha=alpha)
        ax_fp.add_patch(r)

    # Glass wall indicators
    for x_gw in [6, 15]:
        ax_fp.plot([x_gw, x_gw], [8, 14-wall_t], color='#4FC3F7',
                   lw=2.5, linestyle='-', solid_capstyle='round')
    ax_fp.text(10.5, 13.3, '— — CLOISON VITRÉE — —', color='#4FC3F7',
               fontsize=5.5, ha='center', fontfamily=FONT_TITLE, style='italic')

    # Door openings (arc)
    for dx, dy, r_arc, theta1, theta2 in [
        (1.5, 14-wall_t, 1.2, 180, 270),  # Main entrance
        (6, 9.5, 1.0, 0, 90),             # Class 1 door
        (6, 2.5, 1.0, 0, 90),             # Class E door
        (15, 9.5, 1.0, 90, 180),          # Class D door
        (15, 2.5, 1.0, 90, 180),          # Admin door
    ]:
        arc = patches.Arc((dx, dy), r_arc*2, r_arc*2,
                           angle=0, theta1=theta1, theta2=theta2,
                           color='#888888', lw=0.6, linestyle='--')
        ax_fp.add_patch(arc)

    # FURNITURE — simplified but clear
    # Desk reception
    rx, ry = 1.2, 9.5
    r_desk = patches.FancyBboxPatch((rx, ry), 3.5, 1.2, boxstyle='round,pad=0.1',
                                     facecolor=WALNUT, edgecolor=GOLD_LT, lw=0.8)
    ax_fp.add_patch(r_desk)
    ax_fp.text(rx+1.75, ry+0.6, 'ACCUEIL', fontsize=4.5, color='#E8C97A',
               ha='center', va='center', fontweight='bold', fontfamily=FONT_TITLE)

    # Bookshelf along left wall
    r_bs = patches.Rectangle((wall_t, 8.5), 0.8, 4.8, facecolor='#4A2E18',
                              edgecolor=GOLD_LT, lw=0.5)
    ax_fp.add_patch(r_bs)
    ax_fp.text(wall_t+0.4, 10.9, 'BOOKS', fontsize=3.8, color=GOLD_LT,
               ha='center', va='center', rotation=90, fontfamily=FONT_TITLE)

    # Coffee counter
    r_cc = patches.FancyBboxPatch((wall_t, 7.0), 4.5, 0.7, boxstyle='round,pad=0.05',
                                   facecolor='#2A1208', edgecolor=GOLD, lw=0.8)
    ax_fp.add_patch(r_cc)
    ax_fp.text(wall_t+2.25, 7.35, 'COMPTOIR CAFE', fontsize=4.5, color=GOLD,
               ha='center', va='center', fontfamily=FONT_TITLE)

    # Café tables
    cafe_tables = [(1.5,3.0),(2.8,3.0),(4.2,3.0),(1.5,4.5),(2.8,4.5),(4.2,4.5),
                   (1.5,5.8),(2.8,5.8),(4.2,5.8)]
    for tx, ty in cafe_tables:
        c = Circle((tx, ty), 0.52, facecolor=GOLD, edgecolor=WALNUT,
                   linewidth=0.6, alpha=0.7)
        ax_fp.add_patch(c)

    # Classroom 1 tables
    for tx in [7.5, 9.2, 11.0, 12.5]:
        for ty in [9.2, 10.6, 12.0]:
            r = patches.Rectangle((tx-0.55, ty-0.35), 1.1, 0.7,
                                   facecolor='#DDEEFF', edgecolor=TEAL,
                                   linewidth=0.5, alpha=0.8)
            ax_fp.add_patch(r)

    # Whiteboard class 1
    r_wb = patches.Rectangle((6.5, 13.4), 8, 0.3, facecolor='white',
                              edgecolor=TEAL, lw=1.2)
    ax_fp.add_patch(r_wb)
    ax_fp.text(10.5, 13.55, 'TABLEAU INTERACTIF 86"', fontsize=4.5,
               color=TEAL, ha='center', va='center', fontfamily=FONT_TITLE)

    # Salle D round table
    c_d = Circle((18.5, 10.5), 1.8, facecolor='#F5EDE8', edgecolor='#B5622F',
                  linewidth=1.2, alpha=0.8)
    ax_fp.add_patch(c_d)
    ax_fp.text(18.5, 10.5, 'TABLE\nRONDE', fontsize=4.5, color='#7A3A1A',
               ha='center', va='center', fontfamily=FONT_TITLE)

    # Zone labels
    zone_labels = [
        (3.0, 11.8, 'A', 'RÉCEPTION', '#7B5A00'),
        (3.0, 4.2, 'B', 'CAFÉ MAKTABA', '#1A4A1A'),
        (10.5, 11.8, 'C', 'SALLE COURS', '#1A2A5A'),
        (10.5, 4.2, 'E', 'COURS PART.', '#3A1A5A'),
        (18.5, 11.8, 'D', 'SEMI-PRIVÉ', '#5A2A1A'),
        (18.5, 4.2, 'F', 'ADMIN', '#1A4A4A'),
    ]
    for lx, ly, lid, lname, lcol in zone_labels:
        circle_z = Circle((lx, ly+0.5), 0.7, facecolor=lcol, alpha=0.15, edgecolor=lcol, lw=0.5)
        ax_fp.add_patch(circle_z)
        ax_fp.text(lx, ly+0.5, lid, fontsize=11, color=lcol, ha='center',
                   va='center', fontweight='bold', fontfamily=FONT_TITLE, alpha=0.9)
        ax_fp.text(lx, ly-0.35, lname, fontsize=4.2, color=lcol, ha='center',
                   va='top', fontweight='bold', fontfamily=FONT_TITLE)

    # Dimension lines
    ax_fp.annotate('', xy=(21.65, 0), xytext=(21.65, 14),
                   arrowprops=dict(arrowstyle='<->', color='#888888', lw=0.7))
    ax_fp.text(21.82, 7, '~14m', fontsize=5, color='#888888', va='center', rotation=90)
    ax_fp.annotate('', xy=(0, -0.7), xytext=(22, -0.7),
                   arrowprops=dict(arrowstyle='<->', color='#888888', lw=0.7))
    ax_fp.text(11, -1.1, '~22m', fontsize=5, color='#888888', ha='center')

    # North arrow
    ax_fp.text(21.5, 13.2, 'N', fontsize=8, color=NAVY, fontweight='bold',
               ha='center', va='center', fontfamily=FONT_TITLE)
    ax_fp.annotate('', xy=(21.5, 13.6), xytext=(21.5, 12.8),
                   arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.2))

    # ── Legend panel (right side) ─────────────────────────────────────────────
    ax_leg = ax_at(fig, 0.72, 0.175, 0.24, 0.69, facecolor=NAVY)
    rect(ax_leg, 0, 0.97, 1, 0.03, color=GOLD)
    txt(ax_leg, 0.08, 0.92, 'LÉGENDE', size=9, color=GOLD, weight='bold', font=FONT_TITLE)
    hline(ax_leg, 0.89, x0=0.05, x1=0.95, color=GOLD, lw=0.5)

    legend_zones = [
        ('#FFF8DC', 'A — Réception', '18 m²'),
        ('#E8F4E8', 'B — Café Maktaba', '40 m²'),
        ('#E8EEF8', 'C — Cours groupes', '35 m²'),
        ('#F5EDE8', 'D — Semi-privé', '22 m²'),
        ('#EDE8F5', 'E — Cours partic.', '25 m²'),
        ('#E8F5F5', 'F — Admin', '20 m²'),
    ]
    for i, (col, name, area) in enumerate(legend_zones):
        y_l = 0.83 - i*0.115
        r_swatch = patches.Rectangle((0.07, y_l), 0.12, 0.07,
                                      facecolor=col, edgecolor='#666666', lw=0.4)
        ax_leg.add_patch(r_swatch)
        txt(ax_leg, 0.24, y_l+0.04, name, size=7.5, color=WHITE, font=FONT_BODY, va='center')
        txt(ax_leg, 0.24, y_l-0.015, area, size=6.5, color=MID, font=FONT_TITLE, va='center')
        hline(ax_leg, y_l-0.025, x0=0.05, x1=0.95, color='#1A3050', lw=0.3)

    hline(ax_leg, 0.145, x0=0.05, x1=0.95, color=GOLD, lw=0.5)
    special = [('Cloison vitrée', '#4FC3F7'), ('Comptoir café', '#C9A84C'),
               ('Tableau interactif', TEAL)]
    for i, (label, col) in enumerate(special):
        y_sp = 0.105 - i * 0.048
        ax_leg.plot([0.07, 0.19], [y_sp, y_sp], color=col, lw=2.5)
        txt(ax_leg, 0.24, y_sp, label, size=7, color=WHITE, va='center', font=FONT_BODY)

    # Scale
    hline(ax_leg, 0.025, x0=0.07, x1=0.57, color=WHITE, lw=1.5, alpha=0.6)
    txt(ax_leg, 0.5, 0.04, 'Échelle ~ 1:100', size=6, color=MID,
        ha='center', font=FONT_TITLE)

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 6: ZONE A & B — RECEPTION & CAFÉ
# ═══════════════════════════════════════════════════════════════════════════════
def page_zones_ab():
    fig = new_page(facecolor=IVORY)
    page_header(fig, 'Zones A & B')
    page_footer(fig, 6, 'Zone A — Réception  ·  Zone B — Café Maktaba')

    # Page title
    ax_tl = ax_at(fig, 0.05, 0.875, 0.9, 0.062)
    txt(ax_tl, 0, 0.85, '05   ZONES A & B — RÉCEPTION & CAFÉ', size=7,
        color=GOLD, weight='bold', font=FONT_TITLE)
    txt(ax_tl, 0, 0.08, 'Entrée principale · Espace café-librairie "Maktaba"',
        size=13, color=NAVY, font=FONT_TITLE, weight='light')
    hline(ax_tl, 0.0, color=GOLD, lw=1.5)

    # ── ZONE A — top half ────────────────────────────────────────────────────
    # Zone A header bar
    ax_a_hd = ax_at(fig, 0.05, 0.805, 0.9, 0.058, facecolor=NAVY)
    rect(ax_a_hd, 0, 0, 0.008, 1, color=GOLD)
    txt(ax_a_hd, 0.025, 0.62, 'A', size=22, color=GOLD_LT, weight='bold',
        font=FONT_TITLE, alpha=0.25)
    txt(ax_a_hd, 0.025, 0.62, 'ZONE A  —  RÉCEPTION & ACCUEIL', size=11,
        color=WHITE, weight='bold', font=FONT_TITLE)
    txt(ax_a_hd, 0.92, 0.62, '18 m²', size=9, color=GOLD, ha='right',
        weight='bold', font=FONT_TITLE)

    # Zone A perspective sketch area
    ax_a_sk = ax_at(fig, 0.05, 0.585, 0.42, 0.215, facecolor='#F0EBE0')
    ax_a_sk.set_xlim(0, 10); ax_a_sk.set_ylim(0, 6)
    ax_a_sk.axis('off')
    # Simple perspective elevation of reception
    # Back wall
    r_wall = patches.Rectangle((0.5, 0.5), 9, 5, facecolor='#F5EFE4', edgecolor='#888', lw=1)
    ax_a_sk.add_patch(r_wall)
    # Ceiling cove suggestion
    r_ceil = patches.Rectangle((0.5, 4.8), 9, 0.2, facecolor='#2A1A0A', edgecolor='none')
    ax_a_sk.add_patch(r_ceil)
    # LED cove glow
    r_glow = patches.Rectangle((0.5, 4.6), 9, 0.22, facecolor='#FFE08A', edgecolor='none', alpha=0.3)
    ax_a_sk.add_patch(r_glow)
    # Reception desk (perspective)
    desk_pts = np.array([[1.5,0.5],[5.5,0.5],[5.5,2.2],[1.5,2.2]])
    ax_a_sk.fill(desk_pts[:,0], desk_pts[:,1], facecolor=WALNUT, edgecolor=GOLD, lw=1.2)
    # Desk top
    top_pts = np.array([[1.5,2.2],[5.5,2.2],[6.0,2.5],[2.0,2.5]])
    ax_a_sk.fill(top_pts[:,0], top_pts[:,1], facecolor='#E8E0D0', edgecolor='#C9A84C', lw=0.8)
    # Logo on wall
    ax_a_sk.text(7.5, 3.2, ar('مركز اللغات'), fontsize=10, color=GOLD, fontfamily=FONT_ARABIC,
                 ha='center', va='center', fontweight='bold', alpha=0.85)
    ax_a_sk.text(7.5, 2.6, 'CLR', fontsize=14, color=GOLD_LT,
                 ha='center', va='center', fontweight='bold', fontfamily=FONT_TITLE, alpha=0.6)
    # Plant
    c_plant = Circle((8.5, 1.2), 0.5, facecolor='#2A4A2A', edgecolor='none', alpha=0.8)
    ax_a_sk.add_patch(c_plant)
    ax_a_sk.text(8.5, 2.0, '', fontsize=12, ha='center', va='center')
    # Caption
    ax_a_sk.text(5, 0.1, 'Élévation frontale — Desk noyer + enseigne laiton',
                 fontsize=5, color='#666', ha='center', style='italic',
                 fontfamily=FONT_BODY)

    # Zone A specs
    ax_a_sp = ax_at(fig, 0.50, 0.585, 0.45, 0.215)
    specs_a = [
        ('DESK ACCUEIL', 'Courbe en noyer massif + façade laiton brossé\nDimensions : 180 × 80 × 110 cm H'),
        ('ENSEIGNE MURALE', 'Lettres laiton découpées rétroéclairées LED blanc\n"مركز اللغات" + "CLR" — Taille : 80 × 30 cm'),
        ('SOL', 'Béton ciré gris perle (Zone A uniquement)\nDifférence de traitement = signal spatial fort'),
        ('VÉGÉTAL', 'Olivier ou ficus lyrata Ø60cm en cache-pot laiton\n+ 2 poufs cuir cognac espace attente'),
    ]
    txt(ax_a_sp, 0, 0.97, 'ÉLÉMENTS CLÉS', size=7.5, color=NAVY, weight='bold', font=FONT_TITLE)
    hline(ax_a_sp, 0.92, color=GOLD, lw=0.6)
    for i, (label, desc) in enumerate(specs_a):
        y_s = 0.84 - i*0.22
        r_label = patches.FancyBboxPatch((0, y_s-0.02), 0.38, 0.09,
                                          boxstyle='round,pad=0.01',
                                          facecolor=NAVY, edgecolor='none')
        ax_a_sp.add_patch(r_label)
        txt(ax_a_sp, 0.02, y_s+0.03, label, size=6, color=GOLD, weight='bold',
            font=FONT_TITLE, va='center')
        for j, dline in enumerate(desc.split('\n')):
            txt(ax_a_sp, 0.02, y_s-0.06-j*0.055, dline, size=6.8, color=DARK,
                font=FONT_BODY)

    # ── ZONE B — bottom half ─────────────────────────────────────────────────
    ax_b_hd = ax_at(fig, 0.05, 0.52, 0.9, 0.058, facecolor='#1C2E1C')
    rect(ax_b_hd, 0, 0, 0.008, 1, color=TERRA)
    txt(ax_b_hd, 0.025, 0.62, 'ZONE B  —  CAFÉ "MAKTABA" — المكتبة', size=11,
        color=WHITE, weight='bold', font=FONT_TITLE)
    txt(ax_b_hd, 0.92, 0.62, '40 m²', size=9, color=TERRA, ha='right',
        weight='bold', font=FONT_TITLE)

    # Zone B sketch
    ax_b_sk = ax_at(fig, 0.05, 0.305, 0.42, 0.21, facecolor='#1A0F08')
    ax_b_sk.set_xlim(0, 10); ax_b_sk.set_ylim(0, 6)
    ax_b_sk.axis('off')
    # Back wall shelves
    r_w2 = patches.Rectangle((0, 0), 10, 6, facecolor='#1C0E06', edgecolor='none')
    ax_b_sk.add_patch(r_w2)
    # Bookshelf
    for shelf_y in np.linspace(0.5, 5.0, 7):
        r_sh = patches.Rectangle((0.3, shelf_y), 4.5, 0.55, facecolor='#3D2010',
                                  edgecolor='#5A3020', lw=0.5)
        ax_b_sk.add_patch(r_sh)
        # Books
        colors_books = [TERRA, TEAL, GOLD, '#8B4513', SAGE, '#4A0080']
        for bk_x in np.linspace(0.4, 4.6, 14):
            r_bk = patches.Rectangle((bk_x, shelf_y+0.05), 0.2, 0.48,
                                      facecolor=colors_books[int(bk_x)%6], edgecolor='none',
                                      alpha=0.85)
            ax_b_sk.add_patch(r_bk)
    # Ceiling cove
    r_ceil2 = patches.Rectangle((0, 5.5), 10, 0.5, facecolor='#1A0A02', edgecolor='none')
    ax_b_sk.add_patch(r_ceil2)
    # Warm glow
    r_cg = patches.Rectangle((0, 5.2), 10, 0.32, facecolor='#FFD060', edgecolor='none', alpha=0.15)
    ax_b_sk.add_patch(r_cg)
    # Pendant lanterns
    for lx in [6.0, 7.5, 9.0]:
        ax_b_sk.plot([lx, lx], [5.5, 4.5], color='#888', lw=0.8)
        hex_pts = np.array([[lx + 0.3*np.cos(a), 4.3 + 0.4*np.sin(a)]
                            for a in np.linspace(0, 2*np.pi, 7)])
        ax_b_sk.fill(hex_pts[:,0], hex_pts[:,1], facecolor=GOLD, edgecolor='none', alpha=0.85)
        c_inner = Circle((lx, 4.3), 0.18, facecolor='#FFE090', edgecolor='none', alpha=0.9)
        ax_b_sk.add_patch(c_inner)
        # Glow
        c_gl = Circle((lx, 4.3), 0.45, facecolor='#FFD060', edgecolor='none', alpha=0.12)
        ax_b_sk.add_patch(c_gl)
    # Counter
    ctr = patches.FancyBboxPatch((4.8, 0.2), 5.0, 1.2, boxstyle='round,pad=0.05',
                                  facecolor='#2A1208', edgecolor=GOLD, lw=1.0)
    ax_b_sk.add_patch(ctr)
    # Marble top
    mbt = patches.Rectangle((4.8, 1.2), 5.0, 0.3, facecolor='#E8E0D0', edgecolor=GOLD, lw=0.5)
    ax_b_sk.add_patch(mbt)
    ax_b_sk.text(7.3, 0.8, 'COMPTOIR', fontsize=6.5, color=GOLD_LT,
                 ha='center', va='center', fontweight='bold', fontfamily=FONT_TITLE)
    # Café tables
    for tx, ty in [(5.5, 2.8),(6.8, 2.8),(5.5, 4.2),(6.8, 4.2)]:
        c_t = Circle((tx, ty), 0.45, facecolor='#C9A84C', edgecolor=WALNUT,
                     lw=0.6, alpha=0.7)
        ax_b_sk.add_patch(c_t)
    # Zellige accent wall strip
    r_zellige = patches.Rectangle((0, 0), 0.5, 6, facecolor='#B5622F', edgecolor='none')
    ax_b_sk.add_patch(r_zellige)
    for tz_y in np.arange(0.05, 6, 0.3):
        for tz_x in np.arange(0.02, 0.48, 0.2):
            r_tile = patches.Rectangle((tz_x, tz_y), 0.16, 0.22, facecolor='none',
                                       edgecolor='#8B3A1A', lw=0.4)
            ax_b_sk.add_patch(r_tile)
    ax_b_sk.text(5, 0.08, 'Vue d\'ambiance — Café, étagères, lanternes laiton, zellige',
                 fontsize=5, color='#888', ha='center', style='italic', fontfamily=FONT_BODY)

    # Zone B specs
    ax_b_sp = ax_at(fig, 0.50, 0.305, 0.45, 0.21)
    specs_b = [
        ('ÉTAGÈRES BOOKS', 'Floor-to-ceiling noyer 3m H × 4m L\nCapacité 300+ livres + objets décoratifs'),
        ('COMPTOIR CAFÉ', 'Marbre Crema Marfil + base bois noyer\nMachine La Marzocco / Bezzera'),
        ('ÉCLAIRAGE', '3 lanternes laiton Ø40cm + LED cove 2700K\nDIMMER programmable — ambiance variable'),
        ('ZELLIGE', 'Mur accent terracotta 15×15 artisanal\nImportation Maroc — 2m² surface'),
    ]
    txt(ax_b_sp, 0, 0.97, 'ÉLÉMENTS CLÉS', size=7.5, color=NAVY, weight='bold', font=FONT_TITLE)
    hline(ax_b_sp, 0.92, color=GOLD, lw=0.6)
    for i, (label, desc) in enumerate(specs_b):
        y_s = 0.84 - i*0.22
        r_label = patches.FancyBboxPatch((0, y_s-0.02), 0.38, 0.09,
                                          boxstyle='round,pad=0.01',
                                          facecolor='#1C2E1C', edgecolor='none')
        ax_b_sp.add_patch(r_label)
        txt(ax_b_sp, 0.02, y_s+0.03, label, size=6, color=TERRA, weight='bold',
            font=FONT_TITLE, va='center')
        for j, dline in enumerate(desc.split('\n')):
            txt(ax_b_sp, 0.02, y_s-0.06-j*0.055, dline, size=6.8, color=DARK, font=FONT_BODY)

    # Cost tags at bottom
    ax_cost = ax_at(fig, 0.05, 0.21, 0.9, 0.082)
    hline(ax_cost, 0.88, color=GOLD, lw=0.5, alpha=0.5)
    txt(ax_cost, 0, 0.7, 'BUDGET ZONES A+B', size=7.5, color=NAVY,
        weight='bold', font=FONT_TITLE)
    cost_items = [('Menuiserie noyer (desk + étagères)', '42 000 SAR'),
                  ('Comptoir marbre + équipement café', '35 000 SAR'),
                  ('Luminaires (lanternes + DALI)', '18 000 SAR'),
                  ('Zellige + béton ciré + peinture', '22 000 SAR'),
                  ('Mobilier café (tables, assises)', '24 000 SAR'),
                  ('TOTAL ZONES A+B', '141 000 SAR')]
    col_w_c = 0.155
    for i, (item, cost) in enumerate(cost_items):
        is_total = i == len(cost_items)-1
        bg_c = NAVY if is_total else ('#F0EBE0' if i%2==0 else IVORY)
        r_c = patches.Rectangle((i*col_w_c + 0.01, 0.0), col_w_c-0.012, 0.75,
                                  facecolor=bg_c, edgecolor='none')
        ax_cost.add_patch(r_c)
        tc = GOLD if is_total else NAVY
        vc = WHITE if is_total else GOLD
        ax_cost.text(i*col_w_c + col_w_c/2, 0.55, item, fontsize=5.5,
                     color=tc, ha='center', va='center',
                     fontfamily=FONT_BODY, transform=ax_cost.transAxes)
        ax_cost.text(i*col_w_c + col_w_c/2, 0.22, cost, fontsize=7.5,
                     color=vc, ha='center', va='center',
                     fontweight='bold', fontfamily=FONT_TITLE,
                     transform=ax_cost.transAxes)

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 7: ZONES C, D, E
# ═══════════════════════════════════════════════════════════════════════════════
def page_zones_cde():
    fig = new_page(facecolor=IVORY)
    page_header(fig, 'Zones C, D & E')
    page_footer(fig, 7, 'Zone C — Cours groupes  ·  Zone D — Semi-privé  ·  Zone E — Particuliers')

    ax_tl = ax_at(fig, 0.05, 0.875, 0.9, 0.062)
    txt(ax_tl, 0, 0.85, '06   ZONES PÉDAGOGIQUES', size=7, color=GOLD,
        weight='bold', font=FONT_TITLE)
    txt(ax_tl, 0, 0.08, 'Salle groupes · Salon semi-privé · Espace cours particuliers',
        size=13, color=NAVY, font=FONT_TITLE, weight='light')
    hline(ax_tl, 0.0, color=GOLD, lw=1.5)

    zones_data = [
        # (zone_id, name, surface, color_hd, color_accent, left, bot_hd, items, budget)
        ('C', 'SALLE DE COURS — GROUPES', '35 m²', TEAL, TEAL_LT, 0.05,
         ['Tables modulables 6 unités — groupables en U ou rangées',
          'Chaises empilables assise tissu sauge — 12 unités',
          'Tableau interactif 86" SMART Board — mur principal',
          'Film vinyle mashrabiya sur cloison vitrée existante',
          'Panneau phonique mur arrière — tissu sauge, laine 50mm',
          'LED linéaire 4000K suspendues — dimmable DALI',
          'Horloge 6 villes + étagère ressources pédagogiques',
          'Budget : 42 000 SAR'],
         0.73),

        ('D', 'SALON SEMI-PRIVÉ', '22 m²', '#6B2D0A', TERRA, 0.05,
         ['Table ovale 180×90 cm — noyer massif — 4 à 6 personnes',
          'Fauteuils capitonnés tissu terracotta/or — 4 unités',
          'Mur accent : deep navy + artwork calligraphie arabe',
          'Suspension unique laiton brossé au-dessus de la table',
          'Écran 55" mural pour cours et présentations clients',
          'Bibliothèque basse noyer + rideaux lin ivoire',
          'Ambiance premium — tarification ×1.8 vs cours groupes',
          'Budget : 32 000 SAR'],
         0.41),

        ('E', 'COURS PARTICULIERS & EXÉCUTIFS', '25 m²', '#2E1A4A', '#9B7BC4', 0.05,
         ['Bureau conversation : 2 fauteuils cuir cognac + table basse',
          'Bibliothèque sur-mesure couvrant tout un mur',
          'Ficus lyrata XXL en cache-pot laiton Ø50cm',
          'Lampe arc laiton — lumière chaude 2700K dimmable',
          'Tablette pivot 27" pour supports de cours visuels',
          'Tapisserie lin texturée sur mur — acoustique naturelle',
          'Ambiance salon privé — tarification ×2.5 vs groupe',
          'Budget : 28 000 SAR'],
         0.09),
    ]

    for zone_id, name, surface, hd_color, accent, lft, specs, bot_y in zones_data:
        # Header
        ax_hd = ax_at(fig, lft, bot_y+0.26, 0.9, 0.048, facecolor=hd_color)
        rect(ax_hd, 0, 0, 0.007, 1, color=accent)
        txt(ax_hd, 0.022, 0.62, f'ZONE {zone_id}  —  {name}',
            size=10, color=WHITE, weight='bold', font=FONT_TITLE)
        txt(ax_hd, 0.92, 0.62, surface, size=8.5, color=accent,
            ha='right', weight='bold', font=FONT_TITLE)

        # 2 columns: specs left, visual right
        ax_sp = ax_at(fig, lft, bot_y, 0.46, 0.255)
        for i, spec in enumerate(specs[:-1]):
            y_sp = 0.92 - i * 0.128
            # Bullet
            c_bul = Circle((0.012, y_sp-0.01), 0.01, facecolor=accent, edgecolor='none')
            ax_sp.add_patch(c_bul)
            txt(ax_sp, 0.035, y_sp, spec, size=7.5, color=DARK, font=FONT_BODY, va='top')
            hline(ax_sp, y_sp-0.105, x0=0, x1=1, color='#E0D8CC', lw=0.3)

        # Budget tag
        r_bud = patches.FancyBboxPatch((0.02, 0.0), 0.45, 0.07,
                                        boxstyle='round,pad=0.01',
                                        facecolor=hd_color, edgecolor='none', alpha=0.15)
        ax_sp.add_patch(r_bud)
        txt(ax_sp, 0.04, 0.022, specs[-1], size=8, color=hd_color,
            weight='bold', font=FONT_TITLE, va='center')

        # Visual panel (simple room sketch)
        ax_vis = ax_at(fig, lft+0.49, bot_y, 0.41, 0.255, facecolor='#F5F0EA')
        ax_vis.set_xlim(0, 10); ax_vis.set_ylim(0, 6)
        ax_vis.axis('off')

        if zone_id == 'C':
            # Classroom elevation
            r_bw = patches.Rectangle((0, 0), 10, 6, facecolor='#EEF4F8', edgecolor='none')
            ax_vis.add_patch(r_bw)
            # Ceiling cove
            r_cv = patches.Rectangle((0, 5.5), 10, 0.5, facecolor='#1B5E7A', edgecolor='none')
            ax_vis.add_patch(r_cv)
            r_gl = patches.Rectangle((0, 5.2), 10, 0.32, facecolor='#90E0F0', edgecolor='none', alpha=0.2)
            ax_vis.add_patch(r_gl)
            # Whiteboard
            r_wb = patches.Rectangle((0.5, 3.5), 9, 1.8, facecolor='white', edgecolor=TEAL, lw=1.5)
            ax_vis.add_patch(r_wb)
            ax_vis.text(5, 4.4, 'TABLEAU INTERACTIF 86"', fontsize=7, color=TEAL,
                        ha='center', va='center', fontweight='bold', fontfamily=FONT_TITLE)
            # Desks
            for dx in [1.5, 4.0, 6.5]:
                for dy in [1.0, 2.2]:
                    r_d = patches.Rectangle((dx-0.7, dy-0.25), 1.4, 0.5,
                                            facecolor='#DDEEFF', edgecolor=TEAL, lw=0.5)
                    ax_vis.add_patch(r_d)
            # Glass wall with mashrabiya pattern
            for gp_y in np.linspace(0.5, 5.5, 12):
                ax_vis.plot([9.6, 10], [gp_y, gp_y], color='#4FC3F7', lw=0.5, alpha=0.5)
            r_gw = patches.Rectangle((9.6, 0), 0.4, 6, facecolor='#4FC3F7',
                                      edgecolor='none', alpha=0.12)
            ax_vis.add_patch(r_gw)
            ax_vis.text(5, 0.3, 'Élévation — Tableau interactif + mashrabiya',
                        fontsize=5, color='#888', ha='center', style='italic', fontfamily=FONT_BODY)

        elif zone_id == 'D':
            # Semi-private elevation
            r_bw = patches.Rectangle((0, 0), 10, 6, facecolor='#F5EDE8', edgecolor='none')
            ax_vis.add_patch(r_bw)
            # Navy accent wall
            r_aw = patches.Rectangle((0, 0), 3, 6, facecolor=NAVY, edgecolor='none')
            ax_vis.add_patch(r_aw)
            # Artwork calligraphy on navy wall
            ax_vis.text(1.5, 3.2, ar('الحياة') + '\n' + ar('لغة'), fontsize=18, color=GOLD,
                        ha='center', va='center', alpha=0.8)
            # Round table
            c_tb = Circle((6.5, 3.0), 1.5, facecolor='#5C3D2E', edgecolor=GOLD, lw=1.2)
            ax_vis.add_patch(c_tb)
            # Chairs around table
            for angle in [0, 90, 180, 270]:
                rad = np.radians(angle)
                cx = 6.5 + 2.2*np.cos(rad)
                cy = 3.0 + 2.0*np.sin(rad)
                c_ch = Circle((cx, cy), 0.5, facecolor=TERRA, edgecolor='none', alpha=0.8)
                ax_vis.add_patch(c_ch)
            # Pendant light
            ax_vis.plot([6.5, 6.5], [6, 4.8], color='#888', lw=0.8)
            lant = Circle((6.5, 4.5), 0.45, facecolor=GOLD, edgecolor='none', alpha=0.9)
            ax_vis.add_patch(lant)
            ax_vis.text(5, 0.3, 'Élévation — Table ronde noyer + suspension laiton',
                        fontsize=5, color='#888', ha='center', style='italic', fontfamily=FONT_BODY)

        elif zone_id == 'E':
            # Private tutoring
            r_bw = patches.Rectangle((0, 0), 10, 6, facecolor='#EDE8F5', edgecolor='none')
            ax_vis.add_patch(r_bw)
            # Bookshelf wall
            r_bsh = patches.Rectangle((0, 0), 2.5, 6, facecolor='#3D2314', edgecolor='none')
            ax_vis.add_patch(r_bsh)
            for shelf_y in np.linspace(0.3, 5.5, 8):
                r_sf = patches.Rectangle((0.1, shelf_y), 2.3, 0.04,
                                         facecolor='#5A3020', edgecolor='none')
                ax_vis.add_patch(r_sf)
                bc_list = [TERRA, TEAL, GOLD, SAGE, '#4A0080']
                for bk_x in np.linspace(0.15, 2.2, 8):
                    r_bk = patches.Rectangle((bk_x, shelf_y+0.04), 0.2, 0.45,
                                             facecolor=bc_list[int(bk_x*2)%5],
                                             edgecolor='none', alpha=0.8)
                    ax_vis.add_patch(r_bk)
            # Armchairs
            for ax_x, ax_y in [(4.0, 2.8), (7.0, 2.8)]:
                ch = patches.FancyBboxPatch((ax_x-0.8, ax_y-0.6), 1.6, 1.2,
                                            boxstyle='round,pad=0.15',
                                            facecolor='#8B4513', edgecolor='none', alpha=0.85)
                ax_vis.add_patch(ch)
            # Low table between
            r_lt = patches.FancyBboxPatch((4.8, 2.3), 1.4, 0.8,
                                           boxstyle='round,pad=0.05',
                                           facecolor='#E8E0D0', edgecolor=GOLD, lw=0.8)
            ax_vis.add_patch(r_lt)
            # Floor lamp
            ax_vis.plot([9.2, 9.2], [0.5, 4.0], color='#888', lw=1)
            ax_vis.plot([9.2, 8.2], [4.0, 4.0], color='#888', lw=1)
            c_lamp = Circle((8.2, 4.0), 0.35, facecolor=GOLD_LT, edgecolor='none', alpha=0.9)
            ax_vis.add_patch(c_lamp)
            # Ficus
            c_ficus = Circle((3.0, 1.0), 0.8, facecolor='#2A4A2A', edgecolor='none', alpha=0.8)
            ax_vis.add_patch(c_ficus)
            ax_vis.text(5, 0.3, 'Élévation — Bibliothèque, fauteuils cuir, lampe arc laiton',
                        fontsize=5, color='#888', ha='center', style='italic', fontfamily=FONT_BODY)

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 8: BUDGET & TIMELINE (clean, no overlapping)
# ═══════════════════════════════════════════════════════════════════════════════
def page_budget():
    fig = new_page(facecolor=IVORY)
    page_header(fig, 'Budget & Planning')
    page_footer(fig, 8, 'Budget aménagement  ·  Planning 10 semaines')

    ax_tl = ax_at(fig, 0.05, 0.875, 0.9, 0.062)
    txt(ax_tl, 0, 0.85, '07   BUDGET & PLANNING TRAVAUX', size=7, color=GOLD,
        weight='bold', font=FONT_TITLE)
    txt(ax_tl, 0, 0.08, 'Estimation globale 280 000 SAR  ·  Livraison 8–10 semaines',
        size=13, color=NAVY, font=FONT_TITLE, weight='light')
    hline(ax_tl, 0.0, color=GOLD, lw=1.5)

    # ── Budget bars (left) ──────────────────────────────────────────────────
    ax_bud = ax_at(fig, 0.05, 0.46, 0.52, 0.4)
    txt(ax_bud, 0, 0.97, 'DÉTAIL PAR POSTE (SAR)', size=8.5, color=NAVY,
        weight='bold', font=FONT_TITLE)
    hline(ax_bud, 0.935, color=GOLD, lw=0.8)

    budget_items = [
        ('Menuiserie noyer (étagères, desk, bar)', 47000, '#3D2314'),
        ('Mobilier café (tables, assises, majlis)', 40000, TERRA),
        ('Comptoir marbre + équipement café', 37000, '#E8E0D0'),
        ('Mobilier pédagogique (classes A,B,C)', 32000, TEAL),
        ('Sol béton ciré + finitions sols', 28000, SAGE),
        ('Luminaires toutes zones (DALI)', 24000, GOLD),
        ('Branding, calligraphie, signalétique', 18000, NAVY),
        ('Textiles, rideaux, coussins', 15000, '#B5622F'),
        ('Végétaux, déco, accessoires', 11000, '#2A4A2A'),
        ('Imprévus & ajustements', 28000, '#888888'),
    ]
    total_budget = sum(v for _, v, _ in budget_items)
    max_val = max(v for _, v, _ in budget_items)

    for i, (label, val, bar_color) in enumerate(budget_items):
        y_b = 0.88 - i * 0.088
        bar_w = (val / max_val) * 0.58
        # Background bar
        r_bg = patches.Rectangle((0, y_b-0.048), 0.62, 0.072,
                                   facecolor='#EEEBE5', edgecolor='none')
        ax_bud.add_patch(r_bg)
        # Value bar
        r_val = patches.Rectangle((0, y_b-0.048), bar_w, 0.072,
                                   facecolor=bar_color, edgecolor='none', alpha=0.85)
        ax_bud.add_patch(r_val)
        # Label
        txt(ax_bud, 0.64, y_b-0.012, label, size=7, color=DARK, font=FONT_BODY, va='center')
        # Amount
        ax_bud.text(0.30, y_b-0.008,
                    f'{val:,} SAR', fontsize=6.5, color=WHITE if bar_w > 0.15 else DARK,
                    ha='right', va='center', fontweight='bold',
                    fontfamily=FONT_TITLE, transform=ax_bud.transAxes)

    # Total line
    hline(ax_bud, 0.0, color=GOLD, lw=1.2)
    txt(ax_bud, 0, -0.06, f'TOTAL GÉNÉRAL : {total_budget:,} SAR  (~{total_budget//3750:,} USD)',
        size=9, color=NAVY, weight='bold', font=FONT_TITLE)

    # ── Budget donut (right) ─────────────────────────────────────────────────
    ax_donut = fig.add_axes([0.60, 0.505, 0.36, 0.35])
    ax_donut.set_facecolor(IVORY)
    groups = ['Menuiserie\n& Surfaces', 'Mobilier', 'Luminaires\n& Équip.', 'Déco\n& Branding', 'Imprévus']
    vals =   [84000, 92000, 63000, 29000, 28000]  # Surfaces+mob, Mobilier, Lum+equip, Déco, Imprévus
    g_cols = ['#3D2314', TEAL, GOLD, TERRA, '#888888']
    wedges, texts, autotexts = ax_donut.pie(
        vals, labels=None, colors=g_cols, autopct='%1.0f%%',
        pctdistance=0.78, startangle=90,
        wedgeprops=dict(width=0.52, edgecolor=IVORY, linewidth=2),
        textprops=dict(fontsize=7.5, color=WHITE))
    for at in autotexts:
        at.set_fontsize(6.5); at.set_color(WHITE); at.set_fontweight('bold')
    ax_donut.text(0, 0, f'{total_budget//1000}K\nSAR', ha='center', va='center',
                  fontsize=10, fontweight='bold', color=NAVY, fontfamily=FONT_TITLE)
    ax_donut.legend(wedges, groups, loc='lower center', fontsize=6.5,
                    bbox_to_anchor=(0.5, -0.22), ncol=3, frameon=False)
    ax_donut.set_title('Répartition\npar catégorie', fontsize=8,
                       color=NAVY, fontweight='bold', fontfamily=FONT_TITLE, pad=8)

    # ── Gantt / Timeline ────────────────────────────────────────────────────
    ax_gantt = ax_at(fig, 0.05, 0.065, 0.9, 0.375)
    txt(ax_gantt, 0, 0.97, 'PLANNING TRAVAUX — 10 SEMAINES', size=8.5,
        color=NAVY, weight='bold', font=FONT_TITLE)
    hline(ax_gantt, 0.93, color=GOLD, lw=0.8)

    phases = [
        ('PHASE 0 — Préparation', 0, 1, '#888888', 'Validation, commandes, devis'),
        ('PHASE 1 — Gros œuvre', 0.5, 2, SAGE, 'Béton ciré, peinture, ragréage'),
        ('PHASE 2 — Menuiserie', 1, 4.5, WALNUT, 'Fab. atelier : desk, étagères, bar'),
        ('PHASE 3 — Zellige & films', 3, 2, TERRA, 'Zellige, film mashrabiya vitrages'),
        ('PHASE 4 — Électricité', 3, 2.5, TEAL, 'Câblage DALI, spots, SMART Board'),
        ('PHASE 5 — Mobilier', 5.5, 1.5, '#4A2E80', 'Tables, chaises, canapés'),
        ('PHASE 6 — Branding', 6.5, 1.5, GOLD, 'Logo, calligraphies, QR codes, néon'),
        ('PHASE 7 — Végétaux & Déco', 7.5, 1, '#2A4A2A', 'Plantes, accessoires, styling'),
        ('PHASE 8 — Réception', 8.5, 1, NAVY, 'Punch list, photoshoot, ajustements'),
        ('* OUVERTURE', 9.5, 0.5, GOLD, 'Soft opening — événement inauguration'),
    ]

    n_phases = len(phases)
    bar_h = 0.072
    gap = 0.012
    week_w = 0.08  # width per week

    # Week headers
    for wk in range(11):
        x_wk = 0.26 + wk * week_w
        txt(ax_gantt, x_wk, 0.88, f'S{wk}', size=6, color=MID,
            ha='center', font=FONT_TITLE)
        vline(ax_gantt, x_wk, y0=0, y1=0.85, color='#E0D8CC', lw=0.3)

    txt(ax_gantt, 0.01, 0.88, 'Phase', size=6, color=MID, font=FONT_TITLE)
    hline(ax_gantt, 0.84, x0=0, x1=1, color='#D0C8BC', lw=0.5)

    for i, (name, start, duration, color, desc) in enumerate(phases):
        y_bar = 0.81 - i * (bar_h + gap)
        x_bar_start = 0.26 + start * week_w
        x_bar_end   = x_bar_start + duration * week_w

        # Row bg
        row_bg = '#F5F0EA' if i%2==0 else IVORY
        r_row = patches.Rectangle((0, y_bar), 1, bar_h,
                                    facecolor=row_bg, edgecolor='none')
        ax_gantt.add_patch(r_row)

        # Phase name
        is_last = i == len(phases)-1
        txt(ax_gantt, 0.01, y_bar+bar_h*0.5, name,
            size=6.2 if not is_last else 7, color=color if is_last else NAVY,
            weight='bold' if is_last else 'normal',
            font=FONT_TITLE, va='center')

        # Gantt bar
        r_bar = patches.FancyBboxPatch((x_bar_start+0.003, y_bar+0.01),
                                        x_bar_end-x_bar_start-0.006, bar_h*0.75,
                                        boxstyle='round,pad=0.003',
                                        facecolor=color, edgecolor='none',
                                        alpha=0.88)
        ax_gantt.add_patch(r_bar)

        # Description on bar
        mid_bar = (x_bar_start + x_bar_end)/2
        txt(ax_gantt, mid_bar, y_bar+bar_h*0.44, desc, size=5.5,
            color=NAVY if color==GOLD else WHITE, ha='center',
            font=FONT_BODY, va='center', alpha=0.95)

    # Opening star marker
    x_open = 0.26 + 9.5 * week_w
    ax_gantt.axvline(x=x_open, ymin=0, ymax=0.88, color=GOLD,
                     linewidth=1.5, linestyle='--', alpha=0.7)

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE 9: SYNTHÈSE & VISION
# ═══════════════════════════════════════════════════════════════════════════════
def page_summary():
    fig = new_page(facecolor=NAVY)
    page_header(fig, 'Synthèse')
    page_footer(fig, 9, 'Synthèse & Vision')

    # Background pattern
    ax_bg = ax_at(fig, 0, 0, 1, 1, facecolor=NAVY)
    arabesque_bg(ax_bg, n=12, alpha=0.04)

    # Right gold panel
    ax_right = ax_at(fig, 0.62, 0.038, 0.38, 0.902, facecolor='#0A1520')
    for i in np.linspace(0, 1, 18):
        ax_right.axhline(i, color=GOLD, lw=0.12, alpha=0.25)
    txt(ax_right, 0.5, 0.93, '08', size=52, color=GOLD_LT,
        weight='bold', ha='center', font=FONT_TITLE, alpha=0.18, va='top')
    txt(ax_right, 0.5, 0.85, 'SYNTHÈSE', size=14, color=WHITE,
        weight='bold', ha='center', font=FONT_TITLE, va='top')
    txt(ax_right, 0.5, 0.80, '& VISION', size=14, color=GOLD,
        weight='bold', ha='center', font=FONT_TITLE, va='top')
    hline(ax_right, 0.76, x0=0.1, x1=0.9, color=GOLD, lw=0.6)

    # Key numbers
    kpis = [
        ('160 m²', 'Surface aménagée'),
        ('6', 'Zones fonctionnelles'),
        ('280 K', 'SAR — Budget total'),
        ('10', 'Semaines livraison'),
        ('~75 K', 'USD investissement'),
        ('J+1', 'Opérationnel café'),
    ]
    for i, (val, lbl) in enumerate(kpis):
        y_kpi = 0.70 - i*0.11
        ax_right.text(0.5, y_kpi, val, fontsize=20, color=GOLD, fontweight='bold',
                      ha='center', va='center', fontfamily=FONT_TITLE,
                      transform=ax_right.transAxes)
        txt(ax_right, 0.5, y_kpi-0.045, lbl, size=7.5, color=MID,
            ha='center', font=FONT_BODY, va='center')
        hline(ax_right, y_kpi-0.065, x0=0.1, x1=0.9, color='#1A3050', lw=0.3)

    # Left content
    ax_left = ax_at(fig, 0.05, 0.038, 0.54, 0.902)
    rect(ax_left, 0, 0, 0.02, 1, color=GOLD)
    rect(ax_left, 0.03, 0, 0.005, 1, color=GOLD_LT, alpha=0.3)

    txt(ax_left, 0.06, 0.945, 'POURQUOI CE DESIGN', size=16,
        color=WHITE, weight='bold', font=FONT_TITLE, va='top')
    txt(ax_left, 0.06, 0.895, 'VA RÉUSSIR', size=16, color=GOLD,
        weight='bold', font=FONT_TITLE, va='top')
    hline(ax_left, 0.86, x0=0.04, x1=0.96, color=GOLD, lw=0.8)

    reasons = [
        ('BLANK CANVAS IDÉAL',
         'L\'espace existant offre déjà les fondations premium : cove LED intégrée, '
         'parquet vinyle marble effect, cloisons vitrées. Aucun génie civil lourd = '
         'économies substantielles réinvesties dans le mobilier et le branding.'),
        ('INSTAGRAMMABLE PAR CONCEPTION',
         'Chaque zone est designée pour générer du contenu organique : coin café '
         'avec lanternes laiton + zellige terracotta, bibliothèque floor-to-ceiling, '
         'enseigne calligraphie dorée. Le centre se markete lui-même 24h/24.'),
        ('AUTHENTICITÉ SANS KITSCH',
         'Le concept évite le piège de l\'orientalisme de pacotille. '
         'L\'arabesque est traitée de façon contemporaine : motifs mashrabiya en vinyle '
         'sur verre, zellige sélectif, calligraphie comme art — pas comme décoration.'),
        ('COHÉRENCE TOTALE',
         'De l\'enseigne à l\'uniforme du barista, de la tasse de café au manuel de cours, '
         'tout appartient au même univers "Al-Maktaba". Cette cohérence génère confiance, '
         'mémorabilité et fidélité client.'),
        ('ROI DESIGN MESURABLE',
         'Le café génère du chiffre dès J+1. Le design premium justifie des tarifs cours '
         '+30 à +50% vs concurrents. L\'espace Instagrammable = acquisition organique '
         'gratuite valorisée à 8–12K SAR/mois en équivalent pub.'),
    ]

    for i, (title, body) in enumerate(reasons):
        y_r = 0.81 - i * 0.16
        # Number
        ax_left.text(0.06, y_r, f'0{i+1}', fontsize=20, color=GOLD_LT,
                     va='top', fontfamily=FONT_TITLE, fontweight='bold', alpha=0.25,
                     transform=ax_left.transAxes)
        # Title
        txt(ax_left, 0.06, y_r, title, size=9, color=GOLD, weight='bold',
            font=FONT_TITLE, va='top')
        # Body — wrap
        words = body.split()
        line, lines_o = '', []
        for w_word in words:
            test = line + ' ' + w_word if line else w_word
            if len(test) < 62:
                line = test
            else:
                lines_o.append(line); line = w_word
        if line: lines_o.append(line)
        for j, ln in enumerate(lines_o[:3]):
            txt(ax_left, 0.06, y_r-0.04-j*0.032, ln, size=7.5,
                color=MID, font=FONT_BODY)
        hline(ax_left, y_r-0.13, x0=0.04, x1=0.96, color='#1A3050', lw=0.4)

    # Final quote
    hline(ax_left, 0.06, x0=0.04, x1=0.96, color=GOLD, lw=0.5, alpha=0.5)
    ax_left.text(0.06, 0.04,
                 '"Al-Maktaba ne sera pas seulement un centre linguistique.\n'
                 'Ce sera le lieu culturel de référence du nord de Riyad."',
                 fontsize=9, color=GOLD_LT, fontstyle='italic',
                 fontfamily=FONT_BODY, va='bottom', transform=ax_left.transAxes)

    return fig

# ═══════════════════════════════════════════════════════════════════════════════
# ASSEMBLE PDF
# ═══════════════════════════════════════════════════════════════════════════════
def build():
    print('Generating pages...')
    pages = [
        ('Cover',         page_cover),
        ('Analysis',      page_analysis),
        ('Concept',       page_concept),
        ('Materials',     page_materials),
        ('Floor Plan',    page_floorplan),
        ('Zones A & B',   page_zones_ab),
        ('Zones C,D,E',   page_zones_cde),
        ('Budget',        page_budget),
        ('Summary',       page_summary),
    ]

    with PdfPages(OUTPUT) as pdf:
        for name, fn in pages:
            print(f'  → {name}...', end=' ', flush=True)
            fig = fn()
            pdf.savefig(fig, bbox_inches='tight', dpi=DPI)
            plt.close(fig)
            print('✓')

        # PDF metadata
        d = pdf.infodict()
        d['Title'] = 'AL-MAKTABA — Concept Design — Centre Linguistique de Riyad'
        d['Author'] = 'Studio CLR Design'
        d['Subject'] = 'Interior Design Concept — Confidentiel'
        d['Keywords'] = 'Interior Design, Riyadh, Language Center, Arabic, Contemporary'

    print(f'\nPDF saved: {OUTPUT}')
    import os
    size_kb = os.path.getsize(OUTPUT) // 1024
    print(f'File size: {size_kb} KB')

if __name__ == '__main__':
    build()
