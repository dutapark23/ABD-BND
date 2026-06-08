#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, cm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, Image, PageBreak, HRFlowable,
                                 KeepTogether)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import Flowable
import os
import io

# ─── PALETTE ────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor('#0D1B2A')
GOLD      = colors.HexColor('#C9A84C')
GOLD_LIGHT= colors.HexColor('#E8C97A')
SAND      = colors.HexColor('#F7F3EC')
TEAL      = colors.HexColor('#1B6CA8')
TEAL_LIGHT= colors.HexColor('#4A9CC7')
DARK_GRAY = colors.HexColor('#2C3E50')
MID_GRAY  = colors.HexColor('#7F8C8D')
LIGHT_GRAY= colors.HexColor('#ECF0F1')
WHITE     = colors.white
RED_ACCENT= colors.HexColor('#C0392B')
GREEN_ACC = colors.HexColor('#27AE60')

W, H = A4  # 595.27 x 841.89 pts

OUTPUT = '/home/user/ABD-BND/Riyadh_Language_Center_Strategy.pdf'

# ─── CHART HELPERS ──────────────────────────────────────────────────────────
def save_fig(fig, width_mm=160, height_mm=90):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=180, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    plt.close(fig)
    return Image(buf, width=width_mm*mm, height=height_mm*mm)

def chart_revenue():
    months = ['M1','M2','M3','M4','M5','M6','M7','M8','M9','M10','M11','M12']
    corporate = [48,55,72,96,110,130,145,155,160,165,170,175]
    individuel= [24,28,34,42,52,62,72,82,88,92,96,100]
    kids      = [15,18,22,28,34,40,48,58,65,70,75,80]
    cafe      = [12,14,16,20,22,25,28,30,32,34,35,36]
    online    = [0, 2, 4, 6, 8,10,13,16,18,20,22,25]
    merch     = [0, 0, 2, 3, 4, 5, 6, 8, 8,10,10,12]

    fig, ax = plt.subplots(figsize=(9,4.8))
    fig.patch.set_facecolor('#0D1B2A')
    ax.set_facecolor('#0D1B2A')

    x = np.arange(12)
    bar_w = 0.13
    bars = [
        (corporate, '#C9A84C', 'Corporate B2B'),
        (individuel,'#1B6CA8', 'Adultes individuels'),
        (kids,      '#4A9CC7', 'Enfants expatriés'),
        (cafe,      '#E8C97A', 'Coffee Shop'),
        (online,    '#27AE60', 'Cours en ligne'),
        (merch,     '#7F8C8D', 'Merchandising'),
    ]
    for i,(data,col,lbl) in enumerate(bars):
        ax.bar(x + i*bar_w - 2.5*bar_w, data, bar_w, color=col, label=lbl, alpha=0.92)

    ax.set_xticks(x)
    ax.set_xticklabels(months, color='white', fontsize=8)
    ax.set_ylabel('SAR (000)', color='#C9A84C', fontsize=9)
    ax.tick_params(colors='white', labelsize=8)
    ax.spines['bottom'].set_color('#C9A84C')
    ax.spines['left'].set_color('#C9A84C')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.yaxis.label.set_color('#C9A84C')
    ax.legend(loc='upper left', fontsize=7, facecolor='#1B2838',
              labelcolor='white', framealpha=0.8, ncol=3)
    ax.set_title('Revenus mensuels par flux — Année 1 (SAR 000)', color='#C9A84C',
                 fontsize=10, pad=8, fontweight='bold')
    fig.tight_layout(pad=1.2)
    return save_fig(fig, 165, 95)

def chart_pie_revenue():
    labels = ['Corporate B2B', 'Adultes indiv.', 'Enfants expats',
              'Coffee Shop', 'Cours en ligne', 'Merchandising']
    sizes  = [175, 100, 80, 36, 25, 12]
    colors_pie = ['#C9A84C','#1B6CA8','#4A9CC7','#E8C97A','#27AE60','#7F8C8D']
    explode= (0.05,0,0,0,0,0)

    fig, ax = plt.subplots(figsize=(5,4))
    fig.patch.set_facecolor('#0D1B2A')
    ax.set_facecolor('#0D1B2A')
    wedges, texts, autotexts = ax.pie(sizes, labels=None, autopct='%1.1f%%',
                                       colors=colors_pie, explode=explode,
                                       startangle=140,
                                       textprops={'color':'white','fontsize':8},
                                       pctdistance=0.78)
    for at in autotexts:
        at.set_color('white')
        at.set_fontsize(7)
    ax.legend(wedges, labels, loc='lower center', fontsize=7,
              facecolor='#1B2838', labelcolor='white', framealpha=0.8,
              bbox_to_anchor=(0.5,-0.18), ncol=2)
    ax.set_title('Répartition M12', color='#C9A84C', fontsize=10,
                 fontweight='bold', pad=6)
    fig.tight_layout(pad=0.5)
    return save_fig(fig, 80, 80)

def chart_breakeven():
    months = list(range(1,13))
    costs  = [95]*12
    rev    = [99,115,132,157,176,202,225,249,263,271,278,285]
    cumcost= list(np.cumsum([95]*12))
    cumrev = list(np.cumsum(rev))

    fig, (ax1,ax2) = plt.subplots(1,2, figsize=(9,4))
    fig.patch.set_facecolor('#0D1B2A')
    for ax in (ax1,ax2):
        ax.set_facecolor('#0D1B2A')
        ax.spines['bottom'].set_color('#C9A84C')
        ax.spines['left'].set_color('#C9A84C')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.tick_params(colors='white', labelsize=8)

    ax1.plot(months, costs, '--', color='#C0392B', linewidth=2, label='Coûts fixes')
    ax1.plot(months, rev,   '-',  color='#27AE60', linewidth=2, label='Revenus')
    ax1.fill_between(months, costs, rev, where=[r>=c for r,c in zip(rev,costs)],
                     alpha=0.2, color='#27AE60')
    ax1.set_title('Mensuel (SAR 000)', color='#C9A84C', fontsize=9, fontweight='bold')
    ax1.legend(fontsize=7, facecolor='#1B2838', labelcolor='white', framealpha=0.8)
    ax1.set_xlabel('Mois', color='#C9A84C', fontsize=8)

    ax2.plot(months, cumcost, '--', color='#C0392B', linewidth=2, label='Coûts cumulés')
    ax2.plot(months, cumrev,  '-',  color='#27AE60', linewidth=2, label='Revenus cumulés')
    ax2.fill_between(months, cumcost, cumrev,
                     where=[r>=c for r,c in zip(cumrev,cumcost)],
                     alpha=0.2, color='#27AE60')
    ax2.set_title('Cumulatif (SAR 000)', color='#C9A84C', fontsize=9, fontweight='bold')
    ax2.legend(fontsize=7, facecolor='#1B2838', labelcolor='white', framealpha=0.8)
    ax2.set_xlabel('Mois', color='#C9A84C', fontsize=8)
    fig.suptitle('Analyse seuil de rentabilité', color='#C9A84C',
                 fontsize=10, fontweight='bold', y=1.02)
    fig.tight_layout(pad=1.2)
    return save_fig(fig, 165, 90)

def chart_market_size():
    categories = ['Expatriés\nRiyadh', 'Employés\nCorporate', 'Enfants\nExpats',
                  'Saoudiens\nL. étrangères']
    sizes = [1200000, 450000, 85000, 320000]
    target= [15000,   8000,   2500,   5000]
    colors_b = ['#1B6CA8','#C9A84C','#4A9CC7','#27AE60']

    fig, ax = plt.subplots(figsize=(8,4))
    fig.patch.set_facecolor('#0D1B2A')
    ax.set_facecolor('#0D1B2A')
    x = np.arange(len(categories))
    b1 = ax.bar(x-0.2, [s/1000 for s in sizes], 0.35, color=colors_b, alpha=0.5, label='Marché total (000)')
    b2 = ax.bar(x+0.2, [t/100 for t in target], 0.35, color=colors_b, alpha=0.95, label='Cible Y1 (×10)')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, color='white', fontsize=8)
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('#C9A84C')
    ax.spines['left'].set_color('#C9A84C')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_title('Taille de marché vs cible Année 1', color='#C9A84C',
                 fontsize=10, fontweight='bold', pad=8)
    ax.legend(fontsize=7, facecolor='#1B2838', labelcolor='white', framealpha=0.8)
    fig.tight_layout(pad=1.2)
    return save_fig(fig, 155, 85)

# ─── COVER PAGE CANVAS ──────────────────────────────────────────────────────
def draw_cover(c):
    """Draw the entire cover page on a canvas object."""
    # Deep navy background
    c.setFillColor(NAVY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Gold top stripe
    c.setFillColor(GOLD)
    p = c.beginPath()
    p.moveTo(0, H); p.lineTo(W, H); p.lineTo(W, H-100); p.lineTo(0, H-65); p.close()
    c.drawPath(p, fill=1, stroke=0)
    # Gold bottom stripe
    p2 = c.beginPath()
    p2.moveTo(0, 0); p2.lineTo(W, 0); p2.lineTo(W, 90); p2.lineTo(0, 55); p2.close()
    c.drawPath(p2, fill=1, stroke=0)
    # Subtle concentric circles (top-right decoration)
    c.setStrokeColor(colors.HexColor('#1A2E45'))
    c.setLineWidth(0.8)
    for r in [50, 100, 160, 220, 290]:
        c.circle(W - 30, H - 20, r, stroke=1, fill=0)
    # Left accent bars
    c.setFillColor(GOLD)
    c.rect(32, 80, 3.5, H-150, fill=1, stroke=0)
    c.setFillColor(GOLD_LIGHT)
    c.rect(40, 90, 1, H-170, fill=1, stroke=0)

    # Arabic + French title bar
    bar_y = H - 170
    c.setFillColor(colors.HexColor('#0F2233'))
    c.rect(55, bar_y, W-110, 36, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.2)
    c.line(55, bar_y+36, W-55, bar_y+36)
    c.line(55, bar_y, W-55, bar_y)
    c.setFont('Helvetica-Bold', 12)
    c.setFillColor(GOLD)
    c.drawString(65, bar_y+12, 'CENTRE LINGUISTIQUE')
    c.drawRightString(W-65, bar_y+12, 'مركز اللغات')

    # Main title
    c.setFont('Helvetica-Bold', 46)
    c.setFillColor(WHITE)
    c.drawString(58, bar_y-70, 'DE RIYAD')
    c.setFont('Helvetica', 17)
    c.setFillColor(GOLD_LIGHT)
    c.drawString(60, bar_y-98, 'Dialecte Saoudien & Langues du Monde')

    # Subtitle line
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.6)
    c.line(60, bar_y-110, W-60, bar_y-110)

    # Tag chips
    chip_y = bar_y - 148
    chips = [('BUSINESS PLAN', TEAL, 118), ('STRATÉGIE 2025–2028', GOLD, 140), ('CONFIDENTIEL', RED_ACCENT, 100)]
    cx = 60
    for label, col, w in chips:
        c.setFillColor(col)
        c.roundRect(cx, chip_y, w, 18, 4, fill=1, stroke=0)
        c.setFillColor(WHITE)
        c.setFont('Helvetica-Bold', 7.5)
        c.drawCentredString(cx + w/2, chip_y + 5.5, label)
        cx += w + 8

    # Description text block
    desc_y = chip_y - 30
    c.setFont('Helvetica', 9)
    c.setFillColor(colors.HexColor('#A0B4C8'))
    desc = ("Document stratégique & plan d'affaires pour la création, le lancement "
            "et la mise à l'échelle d'un centre linguistique premium au nord de Riyad, "
            "Arabie Saoudite.")
    # Simple word-wrap
    words = desc.split()
    line, lines = '', []
    for w_word in words:
        test = (line + ' ' + w_word).strip()
        if c.stringWidth(test, 'Helvetica', 9) < W - 140:
            line = test
        else:
            lines.append(line)
            line = w_word
    if line: lines.append(line)
    for i, ln in enumerate(lines):
        c.drawString(60, desc_y - i*13, ln)

    # Meta info bar
    meta_y = 105
    c.setFillColor(colors.HexColor('#0F2233'))
    c.rect(55, meta_y, W-110, 42, fill=1, stroke=0)
    c.setStrokeColor(GOLD)
    c.setLineWidth(1.5)
    c.line(55, meta_y+42, W-55, meta_y+42)
    meta_items = [('Préparé par', 'Équipe Stratégique'), ('Date', 'Juin 2025'),
                  ('Version', 'v1.0'), ('Marché', 'Riyad — KSA')]
    col_w = (W-110)/4
    for i, (lbl, val) in enumerate(meta_items):
        mx = 65 + i*col_w
        c.setFont('Helvetica', 7)
        c.setFillColor(MID_GRAY)
        c.drawString(mx, meta_y+28, lbl)
        c.setFont('Helvetica-Bold', 9)
        c.setFillColor(WHITE)
        c.drawString(mx, meta_y+12, val)
        if i < 3:
            c.setStrokeColor(colors.HexColor('#1A2E3A'))
            c.setLineWidth(0.5)
            c.line(mx + col_w - 5, meta_y+5, mx + col_w - 5, meta_y+37)

# ─── HEADER / FOOTER via onFirstPage / onLaterPages ─────────────────────────
def on_later_pages(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, H-30, W, 30, fill=1, stroke=0)
    canvas_obj.setFillColor(GOLD)
    canvas_obj.rect(0, H-33, W, 3, fill=1, stroke=0)
    canvas_obj.setFont('Helvetica-Bold', 8)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.drawString(20, H-20, 'CENTRE LINGUISTIQUE DE RIYAD')
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(GOLD_LIGHT)
    canvas_obj.drawRightString(W-20, H-20, 'STRATÉGIE & BUSINESS PLAN — CONFIDENTIEL')
    canvas_obj.setFillColor(NAVY)
    canvas_obj.rect(0, 0, W, 20, fill=1, stroke=0)
    canvas_obj.setFillColor(GOLD)
    canvas_obj.rect(0, 20, W, 1.5, fill=1, stroke=0)
    canvas_obj.setFont('Helvetica', 7)
    canvas_obj.setFillColor(GOLD_LIGHT)
    canvas_obj.drawString(20, 6, '© 2025 Centre Linguistique de Riyad — Document confidentiel')
    canvas_obj.drawRightString(W-20, 6, f'Page {doc.page}')
    canvas_obj.restoreState()

def on_first_page(canvas_obj, doc):
    canvas_obj.saveState()
    draw_cover(canvas_obj)
    canvas_obj.restoreState()

# ─── STYLES ─────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    S = {}

    S['cover_title'] = ParagraphStyle('cover_title',
        fontName='Helvetica-Bold', fontSize=32, leading=40,
        textColor=WHITE, alignment=TA_LEFT, spaceAfter=6)

    S['cover_sub'] = ParagraphStyle('cover_sub',
        fontName='Helvetica', fontSize=15, leading=22,
        textColor=GOLD_LIGHT, alignment=TA_LEFT, spaceAfter=4)

    S['cover_tag'] = ParagraphStyle('cover_tag',
        fontName='Helvetica-Bold', fontSize=10,
        textColor=GOLD, alignment=TA_LEFT, spaceAfter=2)

    S['h1'] = ParagraphStyle('h1',
        fontName='Helvetica-Bold', fontSize=18, leading=24,
        textColor=GOLD, spaceBefore=18, spaceAfter=8,
        borderPad=4)

    S['h2'] = ParagraphStyle('h2',
        fontName='Helvetica-Bold', fontSize=13, leading=18,
        textColor=NAVY, spaceBefore=12, spaceAfter=6,
        backColor=LIGHT_GRAY, leftIndent=0,
        borderPad=(4,4,4,8))

    S['h3'] = ParagraphStyle('h3',
        fontName='Helvetica-Bold', fontSize=11, leading=15,
        textColor=TEAL, spaceBefore=8, spaceAfter=4)

    S['body'] = ParagraphStyle('body',
        fontName='Helvetica', fontSize=9.5, leading=15,
        textColor=DARK_GRAY, alignment=TA_JUSTIFY,
        spaceAfter=5, leftIndent=0)

    S['body_small'] = ParagraphStyle('body_small',
        fontName='Helvetica', fontSize=8.5, leading=13,
        textColor=DARK_GRAY, alignment=TA_JUSTIFY, spaceAfter=4)

    S['bullet'] = ParagraphStyle('bullet',
        fontName='Helvetica', fontSize=9.5, leading=15,
        textColor=DARK_GRAY, leftIndent=18, firstLineIndent=-12,
        spaceAfter=3)

    S['callout'] = ParagraphStyle('callout',
        fontName='Helvetica-Bold', fontSize=10, leading=15,
        textColor=WHITE, backColor=TEAL, alignment=TA_CENTER,
        borderPad=8, spaceAfter=8, spaceBefore=8)

    S['kpi_val'] = ParagraphStyle('kpi_val',
        fontName='Helvetica-Bold', fontSize=20, leading=24,
        textColor=GOLD, alignment=TA_CENTER)

    S['kpi_lbl'] = ParagraphStyle('kpi_lbl',
        fontName='Helvetica', fontSize=7.5, leading=11,
        textColor=DARK_GRAY, alignment=TA_CENTER)

    S['section_num'] = ParagraphStyle('section_num',
        fontName='Helvetica-Bold', fontSize=42, leading=48,
        textColor=colors.HexColor('#E8EAED'), alignment=TA_RIGHT)

    S['toc_item'] = ParagraphStyle('toc_item',
        fontName='Helvetica', fontSize=10, leading=16,
        textColor=DARK_GRAY, leftIndent=20, spaceAfter=2)

    S['toc_head'] = ParagraphStyle('toc_head',
        fontName='Helvetica-Bold', fontSize=10, leading=16,
        textColor=NAVY, leftIndent=0, spaceAfter=2)

    S['footer_note'] = ParagraphStyle('footer_note',
        fontName='Helvetica-Oblique', fontSize=7.5, leading=11,
        textColor=MID_GRAY, alignment=TA_CENTER, spaceAfter=4)

    S['table_header'] = ParagraphStyle('table_header',
        fontName='Helvetica-Bold', fontSize=8.5,
        textColor=WHITE, alignment=TA_CENTER)

    S['table_cell'] = ParagraphStyle('table_cell',
        fontName='Helvetica', fontSize=8.5, leading=12,
        textColor=DARK_GRAY, alignment=TA_LEFT)

    S['highlight_box'] = ParagraphStyle('highlight_box',
        fontName='Helvetica', fontSize=9, leading=14,
        textColor=NAVY, backColor=colors.HexColor('#FEF9EC'),
        borderPad=8, leftIndent=10, spaceAfter=6)

    return S

# ─── TABLE HELPER ────────────────────────────────────────────────────────────
def styled_table(data, col_widths, S, zebra=True, header=True):
    style_cmds = [
        ('BACKGROUND', (0,0), (-1,0), NAVY),
        ('TEXTCOLOR',  (0,0), (-1,0), WHITE),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,0), 8.5),
        ('ALIGN',      (0,0), (-1,0), 'CENTER'),
        ('VALIGN',     (0,0), (-1,-1),'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0), (-1,-1), 7),
        ('RIGHTPADDING',(0,0),(-1,-1), 7),
        ('GRID',       (0,0), (-1,-1), 0.4, colors.HexColor('#D0D5DB')),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[WHITE, colors.HexColor('#F4F7FA')]),
        ('LINEBELOW',  (0,0), (-1,0),  1.5, GOLD),
    ]
    table = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    table.setStyle(TableStyle(style_cmds))
    return table

def kpi_table(items, S):
    """items = list of (value, label, color_hex)"""
    ncols = len(items)
    cw = (W - 80) / ncols
    cells_top = []
    cells_bot = []
    for val, lbl, col in items:
        cells_top.append(Paragraph(val, ParagraphStyle('kv',
            fontName='Helvetica-Bold', fontSize=18, leading=22,
            textColor=colors.HexColor(col), alignment=TA_CENTER)))
        cells_bot.append(Paragraph(lbl, ParagraphStyle('kl',
            fontName='Helvetica', fontSize=7.5, leading=11,
            textColor=WHITE, alignment=TA_CENTER)))
    t = Table([cells_top, cells_bot], colWidths=[cw]*ncols)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), NAVY),
        ('TOPPADDING', (0,0), (-1,0), 12),
        ('BOTTOMPADDING',(0,1),(-1,1),12),
        ('LEFTPADDING', (0,0),(-1,-1), 4),
        ('RIGHTPADDING',(0,0),(-1,-1), 4),
        ('LINEBELOW',   (0,0),(-1,0), 0.5, colors.HexColor('#1A3050')),
        ('BOX',         (0,0),(-1,-1), 1, GOLD),
        ('LINEAFTER',   (0,0),(-2,-1), 0.5, colors.HexColor('#1A3050')),
    ]))
    return t

def section_divider(number, title, S):
    """Full-width dark section header with big number"""
    bg_table = Table([[
        Paragraph(f'0{number}', ParagraphStyle('sn', fontName='Helvetica-Bold',
            fontSize=48, textColor=colors.HexColor('#1A2E45'), alignment=TA_RIGHT)),
        Paragraph(title, ParagraphStyle('st', fontName='Helvetica-Bold',
            fontSize=20, textColor=GOLD, alignment=TA_LEFT, leading=26))
    ]], colWidths=[80, W-120])
    bg_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), NAVY),
        ('VALIGN',     (0,0),(-1,-1),'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 14),
        ('BOTTOMPADDING',(0,0),(-1,-1),14),
        ('LEFTPADDING', (0,0),(-1,-1), 10),
        ('RIGHTPADDING',(0,0),(-1,-1), 10),
        ('LINEBELOW',  (0,0),(-1,-1), 3, GOLD),
    ]))
    return bg_table

def bullet_item(text, S, icon='▸'):
    return Paragraph(f'<b>{icon}</b>  {text}', S['bullet'])

def info_box(title, content, S, bg='#EBF4FD', border=TEAL):
    data = [[Paragraph(f'<b>{title}</b>', ParagraphStyle('ib_t',
                fontName='Helvetica-Bold', fontSize=9.5, textColor=border)),
             ''],
            [Paragraph(content, ParagraphStyle('ib_c', fontName='Helvetica',
                fontSize=9, leading=14, textColor=DARK_GRAY, alignment=TA_JUSTIFY)),
             '']]
    t = Table(data, colWidths=[W-80, 0])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), colors.HexColor(bg)),
        ('LEFTPADDING', (0,0),(-1,-1), 12),
        ('RIGHTPADDING',(0,0),(-1,-1), 12),
        ('TOPPADDING',  (0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('LINEAFTER',   (0,0),(0,-1), 3, border),
        ('SPAN',        (0,0),(-1,0)),
        ('SPAN',        (0,1),(-1,1)),
    ]))
    return t

# ─── DOCUMENT CONTENT ────────────────────────────────────────────────────────
def build_story(S):
    story = []
    M = 40*mm  # left/right margin (set in doc)

    def h1(t): return Paragraph(t, S['h1'])
    def h2(t): return Paragraph(t, S['h2'])
    def h3(t): return Paragraph(t, S['h3'])
    def p(t):  return Paragraph(t, S['body'])
    def ps(t): return Paragraph(t, S['body_small'])
    def sp(n=6): return Spacer(1, n)
    def hr(): return HRFlowable(width='100%', thickness=0.5,
                                color=colors.HexColor('#D0D5DB'), spaceAfter=6)

    # ══════════════════════════════════════════════════════════════════════════
    # COVER PAGE — drawn entirely via on_first_page canvas callback
    # ══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # TABLE DES MATIÈRES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(sp(10))
    story.append(Paragraph('TABLE DES MATIÈRES', ParagraphStyle('toc_title',
        fontName='Helvetica-Bold', fontSize=22, textColor=NAVY, spaceAfter=16)))
    story.append(HRFlowable(width='100%', thickness=2.5, color=GOLD, spaceAfter=14))

    toc_entries = [
        ('01', 'Résumé Exécutif', '3'),
        ('02', 'Contexte & Opportunité de Marché', '4'),
        ('03', 'Analyse des Marchés Cibles', '5'),
        ('04', 'Offre de Services & Positionnement', '6'),
        ('05', 'Stratégie de Revenus & Flux Additionnels', '7'),
        ('06', 'Stratégie Immobilière — Nord Riyad', '8'),
        ('07', 'Projections Financières & Seuil de Rentabilité', '9'),
        ('08', 'Stratégie Marketing & Acquisition', '11'),
        ('09', 'Feuille de Route Opérationnelle', '12'),
        ('10', 'Plan de Scalabilité & Vision Long Terme', '13'),
        ('11', 'Analyse des Risques & Mitigation', '14'),
        ('12', 'Synthèse & Prochaines Étapes', '15'),
    ]

    for num, title, page in toc_entries:
        row = Table([[
            Paragraph(f'<b>{num}</b>', ParagraphStyle('tn',
                fontName='Helvetica-Bold', fontSize=11,
                textColor=GOLD, alignment=TA_CENTER)),
            Paragraph(title, ParagraphStyle('tt', fontName='Helvetica',
                fontSize=10, textColor=DARK_GRAY)),
            Paragraph(page, ParagraphStyle('tp', fontName='Helvetica-Bold',
                fontSize=9, textColor=TEAL, alignment=TA_RIGHT)),
        ]], colWidths=[30, W-130, 40])
        row.setStyle(TableStyle([
            ('VALIGN', (0,0),(-1,-1),'MIDDLE'),
            ('TOPPADDING',(0,0),(-1,-1),5),
            ('BOTTOMPADDING',(0,0),(-1,-1),5),
            ('LEFTPADDING',(1,0),(1,0),8),
            ('LINEBELOW',(0,0),(-1,-1),0.3, colors.HexColor('#D8DCE0')),
        ]))
        story.append(row)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 01 — RÉSUMÉ EXÉCUTIF
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(1, 'RÉSUMÉ EXÉCUTIF', S))
    story.append(sp(14))

    story.append(p(
        'Le Centre Linguistique de Riyad (CLR) est un projet entrepreneurial à forte valeur ajoutée, '
        'conçu pour répondre à un besoin réel et non encore pleinement adressé dans la capitale saoudienne : '
        'l\'enseignement du <b>dialecte saoudien (الدارجة السعودية)</b> à une population d\'expatriés en forte '
        'croissance, et à l\'inverse, l\'enseignement de langues étrangères de prestige aux Saoudiens. '
        'Dans le cadre de la <b>Vision 2030</b>, Riyad attire chaque année des dizaines de milliers de nouveaux '
        'cadres et familles expatriés — créant une demande structurelle en compétences linguistiques et culturelles.'
    ))
    story.append(sp(8))

    kpis = [
        ('~325 000', 'SAR\nInvestissement initial', '#C9A84C'),
        ('M3', 'Seuil de\nrentabilité', '#1B6CA8'),
        ('401 000', 'SAR/mois\nRevenu M12 (proj.)', '#27AE60'),
        ('4,8×', 'ROI\nAnnée 1', '#C9A84C'),
        ('6', 'Flux de\nrevenus', '#4A9CC7'),
    ]
    story.append(kpi_table(kpis, S))
    story.append(sp(14))

    story.append(info_box(
        '💡 Proposition de valeur centrale',
        'Aucun opérateur à Riyad ne propose une offre complète combinant (1) enseignement du dialecte saoudien '
        'en immersion culturelle, (2) programmes B2B sur mesure pour les grands groupes, (3) enseignement '
        'bidirectionnel (langues étrangères pour Saoudiens) et (4) un espace lifestyle café-librairie '
        'qui génère du flux quotidien. CLR occupe ce segment vierge avec une proposition premium.',
        S, bg='#EBF4FD', border=TEAL
    ))
    story.append(sp(8))

    summary_cols = [
        ['Phase 1 : Lancement\n(M1–M3)', 'Ouverture, B2B rapide,\n30–50 étudiants'],
        ['Phase 2 : Croissance\n(M4–M6)', 'Scaling, 80+ étudiants,\ncafé opérationnel'],
        ['Phase 3 : Consolidation\n(M7–M12)', '150+ étudiants, 10+\ncontrats corporate'],
        ['Phase 4 : Expansion\n(M13–M36)', '2e centre, franchises,\nplatforme digitale'],
    ]
    sum_data = [[Paragraph(a, ParagraphStyle('ph', fontName='Helvetica-Bold',
                    fontSize=8.5, textColor=WHITE, alignment=TA_CENTER)),
                 Paragraph(b, ParagraphStyle('pb', fontName='Helvetica', fontSize=8,
                    textColor=colors.HexColor('#B0C4D8'), alignment=TA_CENTER))]
                for a,b in summary_cols]
    sum_t = Table([sum_data[0:2], sum_data[2:4]], colWidths=[(W-80)/2]*2)
    sum_t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), NAVY),
        ('BACKGROUND', (0,0),(0,0), TEAL),
        ('BACKGROUND', (1,0),(1,0), colors.HexColor('#145080')),
        ('BACKGROUND', (0,1),(0,1), colors.HexColor('#0F3D5C')),
        ('BACKGROUND', (1,1),(1,1), colors.HexColor('#0A2840')),
        ('TOPPADDING', (0,0),(-1,-1), 10),
        ('BOTTOMPADDING',(0,0),(-1,-1),10),
        ('LEFTPADDING', (0,0),(-1,-1),10),
        ('RIGHTPADDING',(0,0),(-1,-1),10),
        ('GRID', (0,0),(-1,-1), 1, GOLD),
    ]))
    story.append(sum_t)
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 02 — CONTEXTE & OPPORTUNITÉ
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(2, 'CONTEXTE & OPPORTUNITÉ DE MARCHÉ', S))
    story.append(sp(14))

    story.append(h2('2.1 — L\'Arabie Saoudite en transformation accélérée'))
    story.append(p(
        'La Vision 2030 du Royaume d\'Arabie Saoudite a déclenché une transformation économique et sociale '
        'sans précédent. Riyad, capitale et moteur de cette transformation, concentre la majorité des '
        'investissements, des méga-projets et des recrutements internationaux. Le nombre d\'expatriés '
        'dans la région de Riyad dépasse <b>1,2 million de personnes</b>, représentant environ 37% '
        'de la population totale de l\'agglomération.'
    ))
    story.append(sp(6))

    story.append(chart_market_size())
    story.append(ps('Sources : GASTAT 2024, Ministry of Human Resources KSA, estimations CLR'))
    story.append(sp(10))

    story.append(h2('2.2 — Pourquoi le dialecte saoudien et non l\'arabe classique ?'))
    story.append(p(
        'L\'arabe académique (MSA — Modern Standard Arabic) est enseigné dans de nombreuses institutions. '
        'Or, dans la vie professionnelle et sociale au Royaume, c\'est exclusivement <b>l\'arabe dialectal '
        'saoudien (الدارجة / Darija Najdi)</b> qui est utilisé. Un expatrié maîtrisant le MSA reste '
        'fondamentalement incompris dans 80% des situations quotidiennes. Ce gap crée une frustration '
        'réelle chez les professionnels et un besoin non comblé par l\'offre existante.'
    ))
    story.append(sp(6))

    story.append(info_box(
        '🎯 Le gap de marché identifié',
        'Sur les 23 centres de langues répertoriés à Riyad (British Council, KAUST Language Center, '
        'instituts privés), AUCUN ne propose un curriculum centré sur le dialecte saoudien avec '
        'immersion culturelle, roleplay situationnel et contenu adapté au monde corporate. '
        'C\'est exactement ce vide que CLR vient combler.',
        S, bg='#FEF9EC', border=GOLD
    ))
    story.append(sp(10))

    story.append(h2('2.3 — Tendances de marché favorables'))
    trends = [
        ('Croissance des expatriés', '+18% par an à Riyad (2022-2025), portée par NEOM, Vision 2030 et les méga-projets'),
        ('Arabisation des postes', 'Quotas de Saudisation (Nitaqat) créent un besoin de communication cross-culturelle'),
        ('Familles accompagnatrices', 'Les contrats d\'expatriation incluent de plus en plus les familles — enfants scolarisés'),
        ('Soft power linguistique', 'Les Saoudiens aisés plébiscitent le français et l\'italien comme marqueurs de distinction'),
        ('Numérisation de l\'éducation', 'Marché de l\'EdTech KSA estimé à 2,5 Mds USD d\'ici 2027'),
    ]
    for title, desc in trends:
        row = Table([[
            Paragraph(f'<b>{title}</b>', ParagraphStyle('trt',
                fontName='Helvetica-Bold', fontSize=9, textColor=TEAL)),
            Paragraph(desc, ParagraphStyle('trd', fontName='Helvetica',
                fontSize=9, leading=13, textColor=DARK_GRAY)),
        ]], colWidths=[130, W-210])
        row.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(0,0), colors.HexColor('#EBF4FD')),
            ('TOPPADDING',(0,0),(-1,-1),6),
            ('BOTTOMPADDING',(0,0),(-1,-1),6),
            ('LEFTPADDING',(0,0),(-1,-1),8),
            ('RIGHTPADDING',(0,0),(-1,-1),8),
            ('LINEBELOW',(0,0),(-1,-1),0.3, colors.HexColor('#C8D8E8')),
        ]))
        story.append(row)
        story.append(sp(2))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 03 — MARCHÉS CIBLES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(3, 'ANALYSE DES MARCHÉS CIBLES', S))
    story.append(sp(14))

    story.append(h2('3.1 — Segment Primaire : Corporates & Professionnels Expatriés'))
    story.append(p(
        'Ce segment est <b>le moteur de revenus le plus rapide et le plus prévisible</b>. '
        'Les grandes entreprises implantées à Riyad (Total, Aramco, McKinsey, HSBC, L\'Oréal, '
        'Airbus, Renault, Hyundai, Samsung, etc.) ont des obligations croissantes en termes '
        'd\'intégration culturelle de leurs employés étrangers. Les RH de ces groupes ont des '
        'budgets formation annuels dédiés et la capacité de signer des contrats pluriannuels.'
    ))
    story.append(sp(8))

    corp_data = [
        [Paragraph('Critère', S['table_header']),
         Paragraph('Grande entreprise (CAC40/Fortune500)', S['table_header']),
         Paragraph('ETI / Entreprise Mid-Market', S['table_header'])],
        [Paragraph('Nombre cible Riyad', S['table_cell']),
         Paragraph('~120 entreprises identifiées', S['table_cell']),
         Paragraph('~400 entreprises', S['table_cell'])],
        [Paragraph('Employés étrangers/entreprise', S['table_cell']),
         Paragraph('20 à 200', S['table_cell']),
         Paragraph('5 à 30', S['table_cell'])],
        [Paragraph('Budget formation/employé/an', S['table_cell']),
         Paragraph('8 000 – 25 000 SAR', S['table_cell']),
         Paragraph('3 000 – 8 000 SAR', S['table_cell'])],
        [Paragraph('Mode contractuel', S['table_cell']),
         Paragraph('Contrat annuel B2B, facturation mensuelle', S['table_cell']),
         Paragraph('Packages trimestriels', S['table_cell'])],
        [Paragraph('Décisionnaire', S['table_cell']),
         Paragraph('DRH / L&D Manager', S['table_cell']),
         Paragraph('PDG / Directeur Admin.', S['table_cell'])],
        [Paragraph('Priorité CLR', S['table_cell']),
         Paragraph('<b>⭐⭐⭐ Priorité 1 — quick wins</b>', S['table_cell']),
         Paragraph('⭐⭐ Priorité 2', S['table_cell'])],
    ]
    story.append(styled_table(corp_data, [120, (W-200)/2, (W-200)/2], S))
    story.append(sp(12))

    story.append(h2('3.2 — Segment Secondaire : Enfants Expatriés'))
    story.append(p(
        'Les familles d\'expatriés scolarisent leurs enfants dans les écoles internationales de Riyad '
        '(BISRI, Lycée Français de Riyad, American International School, etc.). Ces enfants ont besoin '
        'd\'une intégration linguistique et culturelle pour interagir avec leurs pairs saoudiens, '
        'naviguer dans la ville, et enrichir leur parcours. Les parents sont prêts à investir significativement '
        'dans des cours hebdomadaires de qualité. Tarification 20-30% supérieure au marché adulte.'
    ))
    story.append(sp(8))

    story.append(h2('3.3 — Segment Tertiaire : Saoudiens apprenant une langue étrangère'))
    story.append(p(
        'Ce segment représente la <b>vision long terme et l\'axe de croissance le plus puissant</b>. '
        'Les Saoudiens de classe aisée et upper-middle investissent massivement dans l\'éducation de '
        'prestige. Le français et l\'italien sont perçus comme des langues de culture, de luxe et de '
        'distinction sociale. Le russe, le japonais, l\'espagnol représentent des niches émergentes. '
        'L\'anglais, bien que déjà largement présent, peut être proposé avec une valeur ajoutée '
        '(accent British RP, Business English C1/C2, préparation IELTS/Cambridge).'
    ))
    story.append(sp(8))

    lang_data = [
        [Paragraph('Langue', S['table_header']),
         Paragraph('Demande estimée', S['table_header']),
         Paragraph('Prix marché mensuel', S['table_header']),
         Paragraph('Positionnement CLR', S['table_header']),
         Paragraph('Priorité', S['table_header'])],
        ['Français', 'Très haute (prestige, affaires)', '1 200 – 2 000 SAR', 'Alliance Française absent à Riyad', '⭐⭐⭐'],
        ['Italien', 'Haute (luxe, gastronomie)', '1 500 – 2 500 SAR', 'Offre quasi inexistante', '⭐⭐⭐'],
        ['Anglais Business', 'Très haute', '900 – 1 800 SAR', 'Premium / certifications', '⭐⭐'],
        ['Russe', 'Moyenne-haute (tourisme, affaires)', '1 800 – 3 000 SAR', 'Exotique = premium', '⭐⭐'],
        ['Espagnol', 'Moyenne', '1 000 – 1 600 SAR', 'Diversification Y2', '⭐'],
        ['Japonais', 'Émergente (Anime, technologie)', '2 000 – 3 500 SAR', 'Niche rentable', '⭐⭐'],
        ['Mandarin', 'Croissante (relations KSA-Chine)', '1 500 – 2 800 SAR', 'Vision 2030 pertinent', '⭐⭐'],
    ]
    for i in range(1, len(lang_data)):
        lang_data[i] = [Paragraph(str(c), S['table_cell']) for c in lang_data[i]]
    story.append(styled_table(lang_data, [70, 115, 100, 130, 60], S))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 04 — OFFRE DE SERVICES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(4, 'OFFRE DE SERVICES & POSITIONNEMENT', S))
    story.append(sp(14))

    story.append(h2('4.1 — Curriculum Dialecte Saoudien — Méthodologie Immersive'))
    story.append(p(
        'La méthode pédagogique CLR se distingue radicalement des approches académiques classiques. '
        'Elle s\'articule autour de <b>6 niveaux progressifs</b> (A1 à C1 selon le CECRL adapté), '
        'chacun comprenant 40 heures de cours en présentiel, renforcées par des modules digitaux '
        'accessibles 24h/24.'
    ))
    story.append(sp(8))

    modules = [
        ('Niveau Survie (A1)', '40h', 'Salutations, chiffres, marchés, transports, restaurant. Phonologie du Najdi.'),
        ('Niveau Social (A2)', '40h', 'Interactions sociales, famille, travail. Formules de politesse saoudiennes.'),
        ('Niveau Professionnel (B1)', '60h', 'Vocabulaire corporate, réunions, négociations. Roleplay en entreprise.'),
        ('Niveau Intégration (B2)', '60h', 'Nuances culturelles, humour, idiomes. Situations complexes.'),
        ('Niveau Avancé (C1)', '80h', 'Communication spontanée, dialectes régionaux, médias saoudiens.'),
        ('Corporate Intensif', '20h', 'Module sur-mesure 2 semaines pour nouveaux arrivants. Résultats immédiats.'),
    ]
    for lvl, hrs, desc in modules:
        row = Table([[
            Paragraph(f'<b>{lvl}</b>', ParagraphStyle('lv', fontName='Helvetica-Bold',
                fontSize=9, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(f'<b>{hrs}</b>', ParagraphStyle('lh', fontName='Helvetica-Bold',
                fontSize=11, textColor=GOLD, alignment=TA_CENTER)),
            Paragraph(desc, ParagraphStyle('ld', fontName='Helvetica', fontSize=9,
                leading=13, textColor=DARK_GRAY)),
        ]], colWidths=[120, 45, W-245])
        row.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(0,0), NAVY),
            ('BACKGROUND', (1,0),(1,0), colors.HexColor('#0F2233')),
            ('BACKGROUND', (2,0),(2,0), colors.HexColor('#F4F7FA')),
            ('TOPPADDING',(0,0),(-1,-1),7),
            ('BOTTOMPADDING',(0,0),(-1,-1),7),
            ('LEFTPADDING',(0,0),(-1,-1),8),
            ('RIGHTPADDING',(0,0),(-1,-1),8),
            ('LINEBELOW',(0,0),(-1,-1),0.5, colors.HexColor('#D0D5DB')),
        ]))
        story.append(row)
        story.append(sp(2))

    story.append(sp(10))
    story.append(h2('4.2 — Offre Langues Étrangères pour Saoudiens'))
    story.append(p(
        'Les programmes destinés aux Saoudiens s\'appuient sur une pédagogie culturelle différenciante : '
        'chaque langue est enseignée avec son contexte culturel, gastronomique et artistique. '
        'Les cours de français incluent des modules sur la culture française, la gastronomie, '
        'le cinéma. Les cours d\'italien sur le design, la mode et la cuisine. Ce positionnement '
        '"lifestyle & culture" justifie un premium pricing et fidélise les étudiants.'
    ))
    story.append(sp(8))

    story.append(h2('4.3 — Formats proposés'))
    formats = [
        ('Cours en groupe (6-10 pers.)', 'Format standard, économies d\'échelle, dynamique sociale positive'),
        ('Semi-privé (2-4 pers.)', 'Pour familles ou collègues. +40% vs groupe'),
        ('Cours particuliers', 'Exécutifs, diplomates. Tarification premium ×2,5'),
        ('Corporate in-house', 'Enseignant CLR en entreprise. Logistique simplifiée pour le client'),
        ('Intensif résidentiel', 'Stage 5 jours tout inclus. Offre différenciante unique à Riyad'),
        ('Cours en ligne (Live)', 'Zoom ou plateforme CLR. Cible les villes secondaires KSA'),
    ]
    fmt_data = [[Paragraph(fmt, S['table_header']),
                  Paragraph(desc, S['table_header'])] for fmt, desc in formats]
    fmt_data[0] = [Paragraph('Format', S['table_header']),
                    Paragraph('Description & avantage', S['table_header'])]
    fmt_data2 = [[Paragraph(fmt, S['table_cell']),
                   Paragraph(desc, S['table_cell'])] for fmt, desc in formats]
    story.append(styled_table([fmt_data[0]]+fmt_data2, [160, W-220], S))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 05 — STRATÉGIE DE REVENUS
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(5, 'STRATÉGIE DE REVENUS & FLUX ADDITIONNELS', S))
    story.append(sp(14))

    story.append(h2('5.1 — Vue d\'ensemble des 6 flux de revenus'))
    story.append(p(
        'La stratégie financière CLR repose sur la <b>diversification dès le jour 1</b>. '
        'Aucun flux unique ne représente plus de 45% du chiffre d\'affaires à maturité, '
        'ce qui protège le modèle contre la volatilité saisonnière et les risques concentrés.'
    ))
    story.append(sp(10))

    rev_data = [
        [Paragraph('Flux', S['table_header']),
         Paragraph('Mécanisme', S['table_header']),
         Paragraph('Tarification (SAR)', S['table_header']),
         Paragraph('Revenu M3', S['table_header']),
         Paragraph('Revenu M12', S['table_header']),
         Paragraph('Marge', S['table_header'])],
        ['1 — Corporate B2B', 'Contrats annuels\nentreprises', '800–1 500/emp./mois', '48 000', '175 000', '72%'],
        ['2 — Adultes individuels', 'Abonnements\nmensuels', '1 200–1 800/mois', '24 000', '100 000', '68%'],
        ['3 — Enfants expatriés', 'Cours hebdomadaires\n+ parascolaire', '1 500–2 200/mois', '15 000', '80 000', '65%'],
        ['4 — Coffee Shop & Café', 'Espace café intégré\nlibrairie arabe', 'Ticket moy. 22 SAR', '12 000', '36 000', '58%'],
        ['5 — Cours en ligne', 'Plateforme propriétaire\n+ YouTube Premium', '350–800/module', '0', '25 000', '82%'],
        ['6 — Merchandising', 'Livres, flashcards,\nt-shirts, mugs', 'Panier moy. 85 SAR', '0', '12 000', '55%'],
    ]
    for i in range(1, len(rev_data)):
        rev_data[i] = [Paragraph(str(c), S['table_cell']) for c in rev_data[i]]
    story.append(styled_table(rev_data, [95, 95, 90, 55, 55, 45], S))
    story.append(sp(12))

    # Revenue chart
    story.append(chart_revenue())
    story.append(ps('Projections basées sur les hypothèses de croissance conservative (ramp-up 6 mois). Valeurs en SAR 000.'))
    story.append(sp(10))

    story.append(h2('5.2 — Le Coffee Shop : Bien plus qu\'un flux secondaire'))
    story.append(p(
        'L\'espace café n\'est pas un simple service de confort. C\'est un <b>outil d\'acquisition, '
        'de rétention et de rayonnement de marque</b>. Positionné comme "café culturel linguistique", '
        'il accueille des étudiants, des professionnels étrangers, et des Saoudiens curieux. '
        'Les menus sont bilingues (arabe dialectal / langue du mois). Des "table talks" hebdomadaires '
        '(conversation exchange) y sont organisés. Des livres et ressources linguistiques y sont vendus. '
        'Le café génère en moyenne 150-200 tickets/jour à maturité (22 SAR ticket moyen), '
        'soit 3 300–4 400 SAR/jour, <b>~100 000 SAR/mois</b> à plein régime (M18+).'
    ))
    story.append(sp(8))

    story.append(info_box(
        '☕ Concept café : "Maktaba" — La Bibliothèque Café',
        '"Maktaba" (المكتبة = bibliothèque en arabe) est un espace hybride café-librairie-salon '
        'culturel de 40-50m². Décor arabesque contemporain, musique lounge, étagères remplies de livres '
        'en 12 langues. Partenariat avec un torréfacteur local (Al-Yamamah Coffee ou Bunn). '
        'Événements mensuels : soirées cinéma, dîners linguistiques, ateliers calligraphie. '
        'Instagram-friendly par design : génère de l\'acquisition organique gratuite.',
        S, bg='#FEF9EC', border=GOLD
    ))
    story.append(sp(10))

    story.append(h2('5.3 — Merchandising & Produits dérivés'))
    merch_items = [
        ('Flashcards dialecte saoudien (A1-B2)', '45–85 SAR', 'Fort potentiel export & en ligne'),
        ('Guide de survie : "Parler Saoudien en 30 jours"', '120 SAR', 'Livre + audio QR codes'),
        ('T-shirts & tote bags calligraphie', '65–150 SAR', 'Viralité sociale'),
        ('Mugs & cahiers brandés CLR', '35–80 SAR', 'Rétention & fidélité'),
        ('Coffret cadeau "Kit Expatrié"', '350–500 SAR', 'Idéal RH entreprises'),
        ('Abonnement podcast premium CLR', '99 SAR/mois', 'Revenu récurrent passif'),
    ]
    merch_data = [[Paragraph('Article', S['table_header']),
                    Paragraph('Prix', S['table_header']),
                    Paragraph('Intérêt stratégique', S['table_header'])]]
    for item, price, note in merch_items:
        merch_data.append([Paragraph(item, S['table_cell']),
                            Paragraph(price, S['table_cell']),
                            Paragraph(note, S['table_cell'])])
    story.append(styled_table(merch_data, [175, 70, 185], S))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 06 — STRATÉGIE IMMOBILIÈRE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(6, 'STRATÉGIE IMMOBILIÈRE — NORD RIYAD', S))
    story.append(sp(14))

    story.append(p(
        'L\'implantation géographique est un facteur critique de succès. Le nord de Riyad '
        'concentre la majorité de la population expatriée aisée, les ambassades, les grandes entreprises '
        'internationales et les écoles internationales. Les quartiers cibles principaux sont : '
        '<b>Al-Malqa, Al-Nakheel, Al-Olaya Nord, Hittin, Al-Rahmaniyah et Sulaymaniyah</b>.'
    ))
    story.append(sp(10))

    story.append(h2('6.1 — Données de marché immobilier (sources : Aqar.fm, Juin 2025)'))

    immo_data = [
        [Paragraph('Quartier', S['table_header']),
         Paragraph('Surface', S['table_header']),
         Paragraph('Loyer annuel (SAR)', S['table_header']),
         Paragraph('Loyer mensuel (SAR)', S['table_header']),
         Paragraph('SAR/m²/an', S['table_header']),
         Paragraph('Note stratégique', S['table_header'])],
        ['Al-Nakheel', '1 000 m²', '1 800 000', '150 000', '1 800', 'Premium — trop grand pour phase 1'],
        ['Al-Malqa (Imam Saud Rd)', '239 m²', '430 000', '35 833', '1 800', '⭐ Idéal phase 2'],
        ['Al-Aridh (King Abdelaziz)', '55 m²', '60 500', '5 042', '1 100', 'Trop petit — sous-espace seulement'],
        ['Qurtubah', '120 m²', '150 000', '12 500', '1 250', 'Acceptable phase 1'],
        ['Ishbilia', '80 m²', '68 000', '5 667', '850', 'Économique — zone moins premium'],
        ['Al-Rawdah (meublé)', '20 m²', '44 400', '3 700', '2 220', 'Bureau satellite / coworking'],
        ['<b>Cible CLR Phase 1</b>', '<b>150–200 m²</b>', '<b>~180 000–240 000</b>', '<b>15 000–20 000</b>', '<b>~1 100–1 300</b>', '<b>⭐⭐⭐ Zone nord premium</b>'],
    ]
    for i in range(1, len(immo_data)-1):
        immo_data[i] = [Paragraph(str(c), S['table_cell']) for c in immo_data[i]]
    immo_data[-1] = [Paragraph(str(c), ParagraphStyle('tbold',
        fontName='Helvetica-Bold', fontSize=8.5, textColor=NAVY,
        backColor=colors.HexColor('#FEF9EC'))) for c in immo_data[-1]]
    story.append(styled_table(immo_data, [80, 55, 80, 75, 60, 120], S))
    story.append(sp(10))

    story.append(h2('6.2 — Configuration optimale pour le Centre Linguistique de Riyad'))
    story.append(p(
        'Sur la base des prix de marché et de la configuration nécessaire, CLR Phase 1 vise un espace '
        'de <b>150 à 200 m²</b> dans les quartiers Al-Malqa, Hittin ou Al-Nakheel, pour un loyer annuel '
        'estimé entre <b>180 000 et 240 000 SAR</b> (15 000–20 000 SAR/mois). '
        'Cet espace sera agencé selon le plan suivant :'
    ))
    story.append(sp(8))

    layout_data = [
        [Paragraph('Espace', S['table_header']),
         Paragraph('Surface', S['table_header']),
         Paragraph('Fonction', S['table_header']),
         Paragraph('Priorité', S['table_header'])],
        ['Salle principale (convertible)', '45 m²', 'Cours groupes 8-12 pers. / événements', 'Indispensable'],
        ['Salle 2 (semi-privé)', '25 m²', 'Cours 2-4 pers. / cours particuliers', 'Indispensable'],
        ['Espace café "Maktaba"', '40 m²', 'Café, librairie, espace lounge', 'Fortement recommandé'],
        ['Accueil & administration', '20 m²', 'Réception, back-office', 'Indispensable'],
        ['Espace digital / E-learning', '15 m²', 'Studio enregistrement, iPads', 'Phase 2'],
        ['Sanitaires & rangement', '15 m²', 'WC, cuisine, stock merch', 'Indispensable'],
        ['<b>TOTAL</b>', '<b>160 m²</b>', 'Configuration complète opérationnelle', ''],
    ]
    for i in range(1, len(layout_data)-1):
        layout_data[i] = [Paragraph(str(c), S['table_cell']) for c in layout_data[i]]
    layout_data[-1] = [Paragraph(str(c), ParagraphStyle('lbold',
        fontName='Helvetica-Bold', fontSize=9, textColor=NAVY)) for c in layout_data[-1]]
    story.append(styled_table(layout_data, [145, 55, 170, 90], S))
    story.append(sp(10))

    story.append(info_box(
        '📍 Recommandation géographique prioritaire',
        'Première priorité : Al-Malqa (شارع الأمير سلطان / Imam Saud Bin Faisal Road) — '
        'accès direct depuis les quartiers résidentiels expats, proximité Mall of Arabia, '
        'visibilité maximale. Deuxième option : Hittin ou Al-Nakheel pour la densité corporate. '
        'Budget loyer phase 1 retenu : 200 000 SAR/an (16 667 SAR/mois).',
        S, bg='#EBF4FD', border=TEAL
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 07 — PROJECTIONS FINANCIÈRES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(7, 'PROJECTIONS FINANCIÈRES & SEUIL DE RENTABILITÉ', S))
    story.append(sp(14))

    story.append(h2('7.1 — Investissement initial & frais de démarrage'))

    invest_data = [
        [Paragraph('Poste de dépense', S['table_header']),
         Paragraph('Montant (SAR)', S['table_header']),
         Paragraph('Montant (USD)', S['table_header']),
         Paragraph('Notes', S['table_header'])],
        ['Dépôt loyer (3 mois)', '50 000', '13 333', 'Remboursable fin de bail'],
        ['Aménagement & rénovation', '80 000', '21 333', 'Design, cloisons, peinture'],
        ['Mobilier salles de classe', '35 000', '9 333', 'Tables modulables, chaises'],
        ['Équipement café "Maktaba"', '28 000', '7 467', 'Machine espresso, comptoir, vitrine'],
        ['Technologie (tableaux interactifs, iPad, logiciels)', '30 000', '8 000', 'LMS, CRM, caisse'],
        ['Signalétique & branding (intérieur/extérieur)', '15 000', '4 000', 'Logo, panneaux, vitrine'],
        ['Stock initial (livres, merch)', '12 000', '3 200', 'Premier assortiment'],
        ['Marketing & communication (lancement)', '25 000', '6 667', 'Réseaux sociaux, événement inauguration'],
        ['Licences & frais juridiques', '18 000', '4 800', 'Commercial registration, Municipality'],
        ['Fonds de roulement (3 mois)', '45 000', '12 000', 'Trésorerie de sécurité'],
        ['Imprévus (10%)', '33 800', '9 013', 'Buffer recommandé'],
        [Paragraph('<b>TOTAL</b>', S['table_cell']),
         Paragraph('<b>371 800 SAR</b>', ParagraphStyle('tb', fontName='Helvetica-Bold',
             fontSize=9, textColor=GREEN_ACC)),
         Paragraph('<b>~99 150 USD</b>', ParagraphStyle('tb2', fontName='Helvetica-Bold',
             fontSize=9, textColor=GREEN_ACC)),
         Paragraph('<b>Taux 1 USD = 3.75 SAR</b>', S['table_cell'])],
    ]
    for i in range(1, len(invest_data)-1):
        invest_data[i] = [Paragraph(str(c), S['table_cell']) for c in invest_data[i]]
    story.append(styled_table(invest_data, [170, 75, 75, 140], S))
    story.append(sp(12))

    story.append(h2('7.2 — Structure des coûts d\'exploitation mensuels'))

    opex_data = [
        [Paragraph('Charge', S['table_header']),
         Paragraph('SAR/mois', S['table_header']),
         Paragraph('% du total', S['table_header']),
         Paragraph('Nature', S['table_header'])],
        ['Loyer (160 m², Al-Malqa)', '16 667', '17,2%', 'Fixe'],
        ['Salaires (4 enseignants + 2 admin + 1 barista)', '46 000', '47,5%', 'Semi-variable'],
        ['Marketing digital & publicité', '8 000', '8,3%', 'Variable'],
        ['Approvisionnement café', '8 500', '8,8%', 'Variable'],
        ['Services (internet, téléphone, abonnements)', '3 500', '3,6%', 'Fixe'],
        ['Electricité & eau (clim intensive)', '4 500', '4,6%', 'Semi-fixe'],
        ['Entretien & nettoyage', '2 000', '2,1%', 'Fixe'],
        ['Assurances & licences (mensuel)', '1 500', '1,5%', 'Fixe'],
        ['Frais divers & imprévus', '6 000', '6,2%', 'Variable'],
        [Paragraph('<b>TOTAL OPEX</b>', S['table_cell']),
         Paragraph('<b>96 667 SAR</b>', ParagraphStyle('ob', fontName='Helvetica-Bold',
             fontSize=9, textColor=RED_ACCENT)),
         Paragraph('<b>100%</b>', ParagraphStyle('ob2', fontName='Helvetica-Bold',
             fontSize=9, textColor=RED_ACCENT)),
         Paragraph('<b>~25 778 USD/mois</b>', S['table_cell'])],
    ]
    for i in range(1, len(opex_data)-1):
        opex_data[i] = [Paragraph(str(c), S['table_cell']) for c in opex_data[i]]
    story.append(styled_table(opex_data, [175, 75, 70, 140], S))
    story.append(sp(12))

    story.append(chart_breakeven())
    story.append(ps('Le seuil de rentabilité mensuel est atteint au Mois 3. Le cumul des investissements est récupéré au Mois 8.'))
    story.append(sp(10))

    story.append(h2('7.3 — Projections de revenus sur 12 mois (SAR)'))

    proj_data = [
        [Paragraph(h, S['table_header']) for h in
         ['Flux', 'M1', 'M2', 'M3', 'M4', 'M6', 'M9', 'M12', 'Total A1']],
        ['Corporate B2B', '48K', '55K', '72K', '96K', '130K', '155K', '175K', '1 434K'],
        ['Adultes individuels', '24K', '28K', '34K', '42K', '62K', '82K', '100K', '756K'],
        ['Enfants expatriés', '15K', '18K', '22K', '28K', '40K', '58K', '80K', '508K'],
        ['Coffee Shop', '12K', '14K', '16K', '20K', '25K', '30K', '36K', '265K'],
        ['En ligne', '0', '2K', '4K', '6K', '10K', '16K', '25K', '103K'],
        ['Merch', '0', '0', '2K', '3K', '5K', '8K', '12K', '58K'],
        [Paragraph('<b>TOTAL</b>', S['table_cell']),
         Paragraph('<b>99K</b>', ParagraphStyle('pb', fontName='Helvetica-Bold',
             fontSize=8.5, textColor=GREEN_ACC)),
         Paragraph('<b>117K</b>', ParagraphStyle('pb', fontName='Helvetica-Bold',
             fontSize=8.5, textColor=GREEN_ACC)),
         Paragraph('<b>150K</b>', ParagraphStyle('pb', fontName='Helvetica-Bold',
             fontSize=8.5, textColor=GREEN_ACC)),
         Paragraph('<b>195K</b>', ParagraphStyle('pb', fontName='Helvetica-Bold',
             fontSize=8.5, textColor=GREEN_ACC)),
         Paragraph('<b>272K</b>', ParagraphStyle('pb', fontName='Helvetica-Bold',
             fontSize=8.5, textColor=GREEN_ACC)),
         Paragraph('<b>349K</b>', ParagraphStyle('pb', fontName='Helvetica-Bold',
             fontSize=8.5, textColor=GREEN_ACC)),
         Paragraph('<b>428K</b>', ParagraphStyle('pb', fontName='Helvetica-Bold',
             fontSize=8.5, textColor=GREEN_ACC)),
         Paragraph('<b>3 124K</b>', ParagraphStyle('pb', fontName='Helvetica-Bold',
             fontSize=8.5, textColor=GOLD))],
    ]
    for i in range(1, len(proj_data)-1):
        proj_data[i] = [Paragraph(str(c), S['table_cell']) for c in proj_data[i]]

    story.append(styled_table(proj_data, [80,40,40,40,40,40,40,40,65], S))
    story.append(sp(6))
    story.append(ps('Toutes les valeurs en SAR. K = ×1 000. Projections basées sur le scénario de croissance conservateur.'))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 08 — STRATÉGIE MARKETING
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(8, 'STRATÉGIE MARKETING & ACQUISITION', S))
    story.append(sp(14))

    story.append(h2('8.1 — Positionnement de marque'))
    story.append(p(
        'CLR se positionne comme le <b>centre de référence pour l\'intégration linguistique et culturelle '
        'à Riyad</b>. Ni trop académique (ne pas effrayer les non-scolaires), ni trop informel '
        '(justifier le premium pricing). Le naming "Centre Linguistique de Riyad" avec le '
        'sous-titre en arabe "مركز اللغات" ancre immédiatement la légitimité locale. '
        'La ligne éditoriale : <b>"Parlez la langue de vos voisins, ouvrez-vous leur culture."</b>'
    ))
    story.append(sp(8))

    story.append(h2('8.2 — Stratégie d\'acquisition pré-ouverture (M-3 à M0)'))
    story.append(p(
        'La génération de revenus dès le Jour 1 repose sur une phase de <b>pré-vente agressive</b> '
        'dans les 3 mois précédant l\'ouverture. L\'objectif est d\'avoir 15–20 contrats corporate '
        'signés et 40–60 inscrits individuels avant même d\'ouvrir les portes.'
    ))
    story.append(sp(6))

    acq_channels = [
        ('LinkedIn B2B outreach', 'Ciblage précis : HR Directors, L&D Managers, General Managers de sociétés '
         'étrangères à Riyad. Script de prospection personnalisé en 3 langues (FR/EN/AR). '
         'Objectif : 5 rendez-vous/semaine, taux de conversion cible 30%.'),
        ('Ambassades & Chambres de Commerce', 'Partenariats officiels avec les chambres de commerce française, '
         'italienne, britannique à Riyad. Ces organisations cherchent des services à recommander à leurs membres.'),
        ('Écoles internationales', 'Distribution de flyers dans les 8 principales écoles internationales. '
         'Présence aux portes ouvertes. Offre early-bird -20% pour les familles inscrites avant ouverture.'),
        ('Expat Facebook Groups & Riyad Guide', 'Riyad Expats, Riyad Mamas, Riyadh Women\'s Group : '
         'communautés très actives. Publications authentiques, témoignages. Budget boosts : 1 500 SAR/semaine.'),
        ('Instagram & TikTok Arabic', 'Contenu court format : "Mot du jour en dialecte saoudien", '
         '"Fail culturel d\'expatrié", "Saudi expression explained". Croissance organique + sponsorisé.'),
        ('Soft opening & événement de lancement', 'Soirée d\'inauguration invite-only pour 80 personnes : '
         'DRH des grandes entreprises, journalistes, influenceurs expats. Budget : 12 000 SAR.'),
    ]
    for ch, desc in acq_channels:
        story.append(bullet_item(f'<b>{ch} :</b> {desc}', S))
        story.append(sp(2))

    story.append(sp(8))
    story.append(h2('8.3 — Fidélisation & Programme de recommandation'))
    fidelity = [
        'Système de points "Duroos" (دروس = leçons) : 1 SAR dépensé = 1 point, échangeable contre des cours',
        'Programme parrainage : chaque recommandation active = 1 mois de cours offert au parrain',
        'Abonnement annuel avec remise : paiement annuel = -15% vs mensuel',
        'Accès prioritaire aux événements culturels exclusifs pour les abonnés premium',
        'Newsletter mensuelle "La Gazette de Riyad" : culture, lifestyle, vocabulaire, bons plans',
    ]
    for f in fidelity:
        story.append(bullet_item(f, S))
    story.append(sp(8))

    story.append(h2('8.4 — Stratégie digitale & contenu'))
    story.append(p(
        'Le contenu digital est le levier de croissance le moins cher et le plus durable. '
        'CLR publiera systématiquement en 3 canaux : <b>Instagram</b> (visual, lifestyle), '
        '<b>LinkedIn</b> (corporate, B2B), <b>YouTube/TikTok</b> (pédagogique, viral). '
        'L\'objectif est d\'atteindre 10 000 abonnés Instagram en 6 mois en publiant 5 posts/semaine '
        'et 2 Reels/semaine. Un compte Snapchat en arabe cible spécifiquement le public saoudien '
        '(Snapchat est le réseau social n°1 au KSA).'
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 09 — FEUILLE DE ROUTE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(9, 'FEUILLE DE ROUTE OPÉRATIONNELLE', S))
    story.append(sp(14))

    roadmap_phases = [
        ('Phase 0 — Préparation\n(M-6 à M-1)', '#0D1B2A', GOLD, [
            'Création de la société (LLC saoudienne — "شركة ذات مسؤولية محدودة")',
            'Obtention des licences : Ministry of Education + Municipality de Riyad',
            'Identification et signature du bail (Al-Malqa / Hittin)',
            'Recrutement : 2 enseignants dialecte saoudien natifs + 1 responsable pédagogique',
            'Développement du curriculum A1–B2 (dialecte saoudien)',
            'Création identité visuelle, site web, réseaux sociaux',
            'Campagne de pré-vente : 20 contrats corporate signés objectif',
            'Aménagement et installation du centre',
        ]),
        ('Phase 1 — Lancement\n(M1 à M3)', '#0F2A3D', TEAL_LIGHT, [
            'Ouverture officielle avec événement de lancement (80 invités premium)',
            'Démarrage des cours : 3 groupes dialecte saoudien + 1 groupe français',
            'Ouverture du café Maktaba (menu limité, montée en puissance)',
            'Activation des contrats corporate pré-signés',
            'KPI semaine 1 : 50+ inscrits, 3+ contrats B2B actifs',
            'Lancement contenu Instagram/TikTok : objectif 1 000 abonnés M1',
            'Premier atelier "Soirée culturelle arabe" (événement payant 50 SAR)',
        ]),
        ('Phase 2 — Croissance\n(M4 à M6)', '#0D2B1A', GREEN_ACC, [
            'Recrutement 2 enseignants supplémentaires (italien + russe)',
            'Lancement programme enfants expatriés (partenariat écoles)',
            'Mise en ligne de la plateforme e-learning CLR (MVP)',
            'Atteindre 10 contrats corporate actifs',
            'Lancement ligne de merchandising complète',
            'Premier "stage intensif dialecte saoudien" 5 jours',
            'Partenariat avec au moins 1 ambassade ou chambre de commerce',
        ]),
        ('Phase 3 — Consolidation\n(M7 à M12)', '#1A1A0D', GOLD, [
            'Optimisation des marges : révision tarifs +5-10%',
            'Développement cours en ligne asynchrones (self-paced)',
            'Exploration espace supplémentaire ou déménagement vers 250 m²',
            'Signature de contrats corporate pluriannuels (3 ans)',
            'Première étude de marché pour ouverture centre 2 (Djeddah ou Al-Khobar)',
            'Objectif : 150+ étudiants actifs, CA mensuel > 350 000 SAR',
            'Dépôt de marque CLR / préparation modèle de franchise',
        ]),
    ]

    for phase_title, bg_col, accent, tasks in roadmap_phases:
        # Phase header
        header = Table([[
            Paragraph(phase_title, ParagraphStyle('ph_t', fontName='Helvetica-Bold',
                fontSize=11, textColor=accent, leading=16)),
        ]], colWidths=[W-80])
        header.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), colors.HexColor(bg_col) if isinstance(bg_col, str) else bg_col),
            ('TOPPADDING',(0,0),(-1,-1), 8),
            ('BOTTOMPADDING',(0,0),(-1,-1),8),
            ('LEFTPADDING',(0,0),(-1,-1), 14),
            ('LINEAFTER',(0,0),(0,-1), 4, accent),
        ]))
        story.append(header)
        for task in tasks:
            story.append(bullet_item(task, S, icon='◆'))
        story.append(sp(6))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 10 — SCALABILITÉ
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(10, 'PLAN DE SCALABILITÉ & VISION LONG TERME', S))
    story.append(sp(14))

    story.append(p(
        'Le centre de Riyad est le <b>prototype validé</b> d\'un modèle reproductible. '
        'Une fois la rentabilité et les process établis (M12), plusieurs vecteurs de croissance '
        'permettent de multiplier le chiffre d\'affaires sans multiplier proportionnellement '
        'les coûts fixes.'
    ))
    story.append(sp(10))

    scale_data = [
        [Paragraph('Vecteur de croissance', S['table_header']),
         Paragraph('Timeline', S['table_header']),
         Paragraph('CA additionnel estimé', S['table_header']),
         Paragraph('Investissement requis', S['table_header'])],
        ['2ème centre Riyad (quartier différent)', 'M18–M24', '+350 000 SAR/mois', '250 000 SAR'],
        ['Expansion Djeddah (2ème ville KSA)', 'M24–M30', '+400 000 SAR/mois', '300 000 SAR'],
        ['Plateforme e-learning nationale', 'M12–M18', '+100 000 SAR/mois', '120 000 SAR'],
        ['Modèle de franchise (5 unités)', 'M36–M48', '+200 000 SAR/mois (royalties)', '50 000 SAR (setup)'],
        ['Contrats gouvernementaux (Aramco, SABIC)', 'M12–M24', '+500 000 SAR/trimestre', 'Effort commercial'],
        ['Application mobile CLR Premium', 'M18–M24', '+50 000 SAR/mois', '200 000 SAR'],
        ['Certifications officielles partenaires', 'M24+', 'Différenciation & pricing +30%', 'Partenariats'],
    ]
    for i in range(1, len(scale_data)):
        scale_data[i] = [Paragraph(str(c), S['table_cell']) for c in scale_data[i]]
    story.append(styled_table(scale_data, [145, 65, 110, 110], S))
    story.append(sp(10))

    story.append(info_box(
        '🚀 Vision 2028 : Le groupe CLR',
        'À horizon 3 ans, le groupe CLR ambitionne : 5 centres opérationnels au KSA, '
        '1 plateforme digitale avec 50 000 utilisateurs actifs, un catalogue de 15 langues, '
        '200+ contrats corporate actifs, un chiffre d\'affaires consolidé de 1,5–2 M SAR/mois '
        '(~5–6,5 M USD/an). Le modèle de franchise ouvre la voie à une croissance sans '
        'consommation proportionnelle de capital.',
        S, bg='#EBF4FD', border=TEAL
    ))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 11 — RISQUES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(11, 'ANALYSE DES RISQUES & MITIGATION', S))
    story.append(sp(14))

    risks = [
        ('Risque réglementaire', 'ÉLEVÉ', 'MOYEN',
         'Changement politique sur les visas expats, restriction sur l\'enseignement des langues',
         'Veille réglementaire permanente, relations ambassades, flexibilité modèle vers saoudiens'),
        ('Concurrence', 'MOYEN', 'FAIBLE',
         'Entrée d\'un acteur international (British Council, Alliance Française)',
         'First-mover advantage + spécificité dialecte saoudien inimitable, fidélisation B2B long terme'),
        ('Recrutement enseignants', 'ÉLEVÉ', 'MOYEN',
         'Difficulté à trouver des natifs qualifiés pour le dialecte saoudien',
         'Base de données préemptive, partenariat universités saoudiennes, contrats long terme + avantages'),
        ('Saisonnalité', 'MOYEN', 'FAIBLE',
         'Baisse de fréquentation été (Ramadan, vacances scolaires)',
         'Décaler les stages intensifs en été, offres spéciales, prépaiement annuel'),
        ('Dépendance B2B', 'MOYEN', 'MOYEN',
         'Perte d\'un gros client = impact fort en phase 1',
         'Diversification dès M3, max 30% CA sur 1 client, contrats 12+ mois'),
        ('Trésorerie initiale', 'ÉLEVÉ', 'ÉLEVÉ',
         'Délai entre investissement et premiers revenus stables',
         'Fonds de roulement 3 mois, pré-vente agressive, négociation loyer M1-M3 gratuit'),
    ]

    risk_data = [
        [Paragraph(h, S['table_header']) for h in
         ['Risque', 'Impact', 'Probabilité', 'Description', 'Mitigation']]
    ]
    for risk, impact, proba, desc, mit in risks:
        impact_color = '#C0392B' if impact == 'ÉLEVÉ' else '#E67E22' if impact == 'MOYEN' else '#27AE60'
        proba_color  = '#C0392B' if proba  == 'ÉLEVÉ' else '#E67E22' if proba  == 'MOYEN' else '#27AE60'
        risk_data.append([
            Paragraph(risk, S['table_cell']),
            Paragraph(f'<b>{impact}</b>', ParagraphStyle('rc', fontName='Helvetica-Bold',
                fontSize=8, textColor=colors.HexColor(impact_color), alignment=TA_CENTER)),
            Paragraph(f'<b>{proba}</b>', ParagraphStyle('rc2', fontName='Helvetica-Bold',
                fontSize=8, textColor=colors.HexColor(proba_color), alignment=TA_CENTER)),
            Paragraph(desc, S['table_cell']),
            Paragraph(mit, S['table_cell']),
        ])
    story.append(styled_table(risk_data, [80, 45, 60, 130, 145], S))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # SECTION 12 — SYNTHÈSE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(section_divider(12, 'SYNTHÈSE & PROCHAINES ÉTAPES', S))
    story.append(sp(14))

    story.append(info_box(
        '✅ Pourquoi ce projet réussira',
        '1. GAP DE MARCHÉ RÉEL : aucun opérateur ne couvre le dialecte saoudien en contexte B2B. '
        '2. TIMING PARFAIT : Vision 2030 génère un flux constant de nouveaux expatriés qualifiés. '
        '3. MODÈLE RÉSILIENT : 6 flux de revenus, seuil de rentabilité dès M3. '
        '4. SCALABLE : modèle reproductible vers d\'autres villes + franchise + digital. '
        '5. DIFFÉRENCIATION FORTE : café culturel + expérience lifestyle = rétention et bouche-à-oreille.',
        S, bg='#EAFAF0', border=GREEN_ACC
    ))
    story.append(sp(10))

    story.append(h2('Actions immédiates — Les 30 premiers jours'))
    actions_30 = [
        ('J1–J7', 'Enregistrement société + ouverture compte bancaire professionnel KSA'),
        ('J1–J14', 'Sélection et visite des 5 espaces commerciaux identifiés (Al-Malqa, Hittin)'),
        ('J7–J21', 'Recrutement responsable pédagogique + 2 enseignants natifs dialecte saoudien'),
        ('J14–J30', 'Signature du bail + démarrage travaux d\'aménagement'),
        ('J1–J30', 'Création LinkedIn, Instagram, Snapchat + 20 posts programmés'),
        ('J7–J30', 'Prospection B2B : 50 entreprises contactées, 10 RDV obtenus'),
        ('J14–J30', 'Présentation aux chambres de commerce française et italienne à Riyad'),
        ('J30', 'Premier atelier public gratuit "Découverte du dialecte saoudien" (lead gen)'),
    ]
    act_data = [[Paragraph(h, S['table_header']) for h in ['Délai', 'Action prioritaire']]]
    for delay, action in actions_30:
        act_data.append([
            Paragraph(delay, ParagraphStyle('ad', fontName='Helvetica-Bold',
                fontSize=9, textColor=TEAL, alignment=TA_CENTER)),
            Paragraph(action, S['table_cell']),
        ])
    story.append(styled_table(act_data, [65, W-125], S))
    story.append(sp(12))

    # Final KPI summary
    final_kpis = [
        ('99 000', 'SAR\nRevenu Mois 1', '#27AE60'),
        ('M3', 'Break-even\nopérationnel', '#C9A84C'),
        ('3,1 M', 'SAR\nCA total Année 1', '#27AE60'),
        ('4,8×', 'ROI\nAnnée 1', '#C9A84C'),
        ('~99 K', 'USD\nInvestissement', '#1B6CA8'),
        ('2028', 'Vision\n5 centres KSA', '#4A9CC7'),
    ]
    story.append(kpi_table(final_kpis, S))
    story.append(sp(14))

    story.append(Paragraph(
        'Ce document a été préparé sur la base d\'une analyse approfondie du marché de Riyad, '
        'des données immobilières réelles (Aqar.fm, Juin 2025), des tendances sectorielles '
        'et d\'une expérience de plus de 20 ans en développement commercial senior. '
        'Les projections financières sont basées sur un scénario conservateur. '
        'Les hypothèses de marché sont vérifiables et les risques identifiés sont maîtrisables.',
        S['footer_note']
    ))
    story.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceAfter=8))
    story.append(Paragraph(
        '© 2025 Centre Linguistique de Riyad — Tous droits réservés — Document confidentiel et propriétaire',
        S['footer_note']
    ))

    return story

# ─── BUILD PDF ───────────────────────────────────────────────────────────────
def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=40*mm,
        rightMargin=40*mm,
        topMargin=38*mm,
        bottomMargin=28*mm,
        title='Centre Linguistique de Riyad — Business Plan 2025',
        author='Équipe Stratégique Senior',
        subject='Stratégie & Business Plan — Confidentiel',
    )

    S = build_styles()
    story = build_story(S)

    doc.build(story,
              onFirstPage=on_first_page,
              onLaterPages=on_later_pages)
    print(f'PDF généré : {OUTPUT}')

if __name__ == '__main__':
    build_pdf()
