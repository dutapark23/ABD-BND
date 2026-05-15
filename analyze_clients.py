import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    HRFlowable, KeepTogether, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ── LOAD DATA ─────────────────────────────────────────────────────────────────
df = pd.read_csv('/home/user/ABD-BND/clients_raw.csv')

# ── NORMALISE COLUMNS ─────────────────────────────────────────────────────────
def norm_status(s):
    s = str(s).strip().lower()
    if s == 'answer':     return 'Answer'
    if 'no answer' in s:  return 'No Answer'
    if 'off' in s:        return 'Phone Off'
    if s in ('nan', ''):  return 'Not Yet Called'
    return 'Not Yet Called'

def norm_dubai(s):
    s = str(s).strip().lower()
    if s in ('yes', 'yes '):           return 'In Dubai'
    if s in ('no', 'no ', 'no\xa0'):   return 'Not in Dubai'
    return 'Unknown'

df['status']       = df['Call Status'].apply(norm_status)
df['dubai_status'] = df['In Dubai'].apply(norm_dubai)

# Normalise date column — fix variants like '26.3', '7,04'
df['date'] = (df['Date of contact ']
              .astype(str)
              .str.strip()
              .str.replace(',', '.', regex=False)
              .str.replace(r'\.(\d)$', r'.0\1', regex=True))   # '26.3' → '26.03'

# ── CORE STATS ────────────────────────────────────────────────────────────────
total        = len(df)
s_counts     = df['status'].value_counts()
answered     = s_counts.get('Answer', 0)
no_ans       = s_counts.get('No Answer', 0)
phone_off    = s_counts.get('Phone Off', 0)
not_called   = s_counts.get('Not Yet Called', 0)

answered_df  = df[df['status'] == 'Answer']
d_counts     = answered_df['dubai_status'].value_counts()
in_dubai     = d_counts.get('In Dubai', 0)
not_dubai    = d_counts.get('Not in Dubai', 0)
dubai_unk    = d_counts.get('Unknown', 0)

contact_rate = round(answered / total * 100, 1)
dubai_rate   = round(in_dubai / answered * 100, 1) if answered else 0
absent_rate  = round(not_dubai / answered * 100, 1) if answered else 0

# Countries of absent clients (clean up noise)
absent_df = answered_df[answered_df['dubai_status'] == 'Not in Dubai'].copy()
country_noise = {'did not answer', 'she did not answer this', 'he did not answer this',
                 'she did not want to answer', ''}
raw_countries = absent_df['Which country based if not Dubai '].dropna()
raw_countries = raw_countries[~raw_countries.str.strip().str.lower().isin(country_noise)]
# Merge London → UK
raw_countries = raw_countries.str.strip().replace({'London': 'UK'})
countries = raw_countries.value_counts()

# Return timeline for absent clients
def classify_return(val):
    v = str(val).strip().lower()
    if v in ('nan', '', 'she did not want to answer'): return 'No Info'
    if 'not anymore' in v:                             return 'Lost / Left Dubai'
    if any(k in v for k in ['weekend','saturday','april','week ','next week','few days','just got back']): return 'Imminent (<2 wks)'
    if any(k in v for k in ['month','june','3 month','6 month']): return 'Mid-term (1–3 mo)'
    if any(k in v for k in ['september','later this year','5 month']): return 'Long-term (3+ mo)'
    return 'Uncertain / No Date'

absent_df['return_seg'] = absent_df['Return to Dubai '].apply(classify_return)
ret_seg = absent_df['return_seg'].value_counts()

# Studios
studio_col = df['Which studio they usually book '].dropna()
studio_col = studio_col[studio_col.str.strip() != '']
studio_col = studio_col[~studio_col.str.startswith('http')]
studios = studio_col.str.strip().value_counts()

# Daily call volume — ordered chronologically
date_order_raw = [
    '23.03','25.03','26.03','26.03','27.03','28.03','30.03','31.03',
    '01.04','02.04','03.04','06.04','07.04','08.04','09.04',
    '11.04','13.04','14.04','15.04','23.04','25.04',
    '04.05','05.05','06.05','07.05','08.05','11.05','12.05','13.05','14.05',
]
# Build unique ordered list
seen = set()
date_order = []
for d in date_order_raw:
    if d not in seen:
        date_order.append(d)
        seen.add(d)

daily = (df.groupby(['date','status'])
           .size()
           .unstack(fill_value=0)
           .reindex(date_order, fill_value=0))

# Notes quality sample (non-null, short enough to show)
notes_sample = (df[df['Notes'].notna() & (df['Notes'].str.len() < 80)]
                [['Client name','Notes']]
                .head(6))

# ── COLOUR PALETTE ────────────────────────────────────────────────────────────
C_DARK   = '#1a1a2e'
C_MID    = '#16213e'
C_ACCENT = '#e94560'
C_GOLD   = '#f5a623'
C_GREEN  = '#27ae60'
C_BLUE   = '#2980b9'
C_GREY   = '#7f8c8d'
C_LIGHT  = '#ecf0f1'

def fig_to_img(fig, dpi=150):
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight',
                facecolor=fig.get_facecolor())
    buf.seek(0)
    return buf

# ════════════════════════════════════════════════════════════════════════════
# CHART 1 — Call Status Donut
# ════════════════════════════════════════════════════════════════════════════
fig1, ax1 = plt.subplots(figsize=(5, 4.2), facecolor=C_DARK)
ax1.set_facecolor(C_DARK)
vals1 = [answered, no_ans, phone_off, not_called]
lbls1 = ['Answered','No Answer','Phone Off','Not Yet Called']
clrs1 = [C_GREEN, C_ACCENT, C_GOLD, C_GREY]
wedges, _, autotexts = ax1.pie(
    vals1, colors=clrs1, autopct='%1.1f%%', startangle=140,
    pctdistance=0.72, wedgeprops=dict(width=0.52, edgecolor=C_DARK, linewidth=2))
for t in autotexts:
    t.set_color('white'); t.set_fontsize(9); t.set_fontweight('bold')
ax1.legend(wedges, [f'{l} ({v})' for l,v in zip(lbls1, vals1)],
           loc='lower center', bbox_to_anchor=(0.5, -0.14),
           ncol=2, fontsize=8, frameon=False, labelcolor='white')
ax1.set_title('Call Status Breakdown', color='white', fontsize=12,
              fontweight='bold', pad=8)
buf1 = fig_to_img(fig1); plt.close(fig1)

# ════════════════════════════════════════════════════════════════════════════
# CHART 2 — Dubai Status Donut (answered only)
# ════════════════════════════════════════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(5, 4.2), facecolor=C_DARK)
ax2.set_facecolor(C_DARK)
vals2 = [in_dubai, not_dubai, dubai_unk]
lbls2 = ['In Dubai','Currently Absent','Unknown']
clrs2 = [C_BLUE, C_ACCENT, C_GREY]
wedges2, _, auto2 = ax2.pie(
    vals2, colors=clrs2, autopct='%1.1f%%', startangle=90,
    pctdistance=0.72, wedgeprops=dict(width=0.52, edgecolor=C_DARK, linewidth=2))
for t in auto2:
    t.set_color('white'); t.set_fontsize(9); t.set_fontweight('bold')
ax2.legend(wedges2, [f'{l} ({v})' for l,v in zip(lbls2, vals2)],
           loc='lower center', bbox_to_anchor=(0.5, -0.14),
           ncol=2, fontsize=8, frameon=False, labelcolor='white')
ax2.set_title('Client Location (Answered Only)', color='white', fontsize=12,
              fontweight='bold', pad=8)
buf2 = fig_to_img(fig2); plt.close(fig2)

# ════════════════════════════════════════════════════════════════════════════
# CHART 3 — Countries of absent clients
# ════════════════════════════════════════════════════════════════════════════
top_c = countries.head(12)
fig3, ax3 = plt.subplots(figsize=(7, 4), facecolor=C_DARK)
ax3.set_facecolor(C_DARK)
bars3 = ax3.barh(top_c.index[::-1], top_c.values[::-1],
                 color=C_ACCENT, edgecolor=C_DARK, height=0.6)
for bar, val in zip(bars3, top_c.values[::-1]):
    ax3.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
             str(val), va='center', color='white', fontsize=9, fontweight='bold')
ax3.set_xlabel('Clients', color=C_LIGHT, fontsize=9)
ax3.set_title('Where Are Absent Clients Based?', color='white',
              fontsize=12, fontweight='bold')
ax3.tick_params(colors=C_LIGHT, labelsize=9)
ax3.xaxis.set_major_locator(mticker.MaxNLocator(integer=True))
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
ax3.spines['bottom'].set_color(C_GREY)
ax3.spines['left'].set_color(C_GREY)
ax3.set_xlim(0, top_c.values.max() * 1.30)
buf3 = fig_to_img(fig3); plt.close(fig3)

# ════════════════════════════════════════════════════════════════════════════
# CHART 4 — Daily call activity
# ════════════════════════════════════════════════════════════════════════════
date_labels = {
    '23.03':'Mar 23','25.03':'Mar 25','26.03':'Mar 26','27.03':'Mar 27',
    '28.03':'Mar 28','30.03':'Mar 30','31.03':'Mar 31','01.04':'Apr 1',
    '02.04':'Apr 2','03.04':'Apr 3','06.04':'Apr 6','07.04':'Apr 7',
    '08.04':'Apr 8','09.04':'Apr 9','11.04':'Apr 11','13.04':'Apr 13',
    '14.04':'Apr 14','15.04':'Apr 15','23.04':'Apr 23','25.04':'Apr 25',
    '04.05':'May 4','05.05':'May 5','06.05':'May 6','07.05':'May 7',
    '08.05':'May 8','11.05':'May 11','12.05':'May 12','13.05':'May 13','14.05':'May 14',
}

fig4, ax4 = plt.subplots(figsize=(12, 4), facecolor=C_DARK)
ax4.set_facecolor(C_DARK)
x = np.arange(len(daily.index))
w = 0.25
for i, (col, clr) in enumerate(zip(['Answer','No Answer','Phone Off'],
                                    [C_GREEN, C_ACCENT, C_GOLD])):
    if col in daily.columns:
        ax4.bar(x + i*w, daily[col], w, label=col, color=clr, alpha=0.88)
ax4.set_xticks(x + w)
tick_labels = [date_labels.get(d, d) for d in daily.index]
ax4.set_xticklabels(tick_labels, rotation=45, ha='right', color=C_LIGHT, fontsize=7)
ax4.set_ylabel('# Contacts', color=C_LIGHT, fontsize=9)
ax4.set_title('Daily Outreach Activity  (Mar 23 – May 14, 2025)',
              color='white', fontsize=12, fontweight='bold')
ax4.tick_params(colors=C_LIGHT)
ax4.legend(frameon=False, labelcolor='white', fontsize=8)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
ax4.spines['bottom'].set_color(C_GREY)
ax4.spines['left'].set_color(C_GREY)
buf4 = fig_to_img(fig4); plt.close(fig4)

# ════════════════════════════════════════════════════════════════════════════
# CHART 5 — Return timeline segmentation
# ════════════════════════════════════════════════════════════════════════════
seg_order  = ['Imminent (<2 wks)','Mid-term (1–3 mo)','Long-term (3+ mo)',
              'Uncertain / No Date','No Info','Lost / Left Dubai']
seg_colors = {'Imminent (<2 wks)': C_GREEN,  'Mid-term (1–3 mo)': C_GOLD,
              'Long-term (3+ mo)': C_ACCENT, 'Uncertain / No Date': C_GREY,
              'No Info': '#8e44ad',           'Lost / Left Dubai': '#c0392b'}

ret_plot = ret_seg.reindex(seg_order, fill_value=0)
fig5, ax5 = plt.subplots(figsize=(7, 3.8), facecolor=C_DARK)
ax5.set_facecolor(C_DARK)
bars5 = ax5.bar(seg_order, ret_plot.values,
                color=[seg_colors[s] for s in seg_order],
                edgecolor=C_DARK, width=0.6)
for bar, val in zip(bars5, ret_plot.values):
    if val > 0:
        ax5.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(val), ha='center', color='white', fontsize=10,
                 fontweight='bold')
ax5.set_xticks(range(len(seg_order)))
ax5.set_xticklabels(seg_order, rotation=18, ha='right', color=C_LIGHT, fontsize=8)
ax5.set_ylabel('Clients', color=C_LIGHT, fontsize=9)
ax5.set_title('Absent Clients — Return Timeline Segmentation',
              color='white', fontsize=12, fontweight='bold')
ax5.tick_params(colors=C_LIGHT)
ax5.spines['top'].set_visible(False)
ax5.spines['right'].set_visible(False)
ax5.spines['bottom'].set_color(C_GREY)
ax5.spines['left'].set_color(C_GREY)
buf5 = fig_to_img(fig5); plt.close(fig5)

# ════════════════════════════════════════════════════════════════════════════
# BUILD PDF
# ════════════════════════════════════════════════════════════════════════════
pdf_path = '/home/user/ABD-BND/Dubai_Podcast_Studio_Marketing_Report.pdf'

PW, PH = A4
LM = RM = 1.8*cm
W  = PW - LM - RM   # ~558 pts

doc = SimpleDocTemplate(pdf_path, pagesize=A4,
                        leftMargin=LM, rightMargin=RM,
                        topMargin=1.8*cm, bottomMargin=1.8*cm)
styles = getSampleStyleSheet()

# ── PDF COLOR SCHEME (white background → all text must be dark) ───────────────
PDF_BLACK  = '#1a1a2e'   # near-black for body text
PDF_RED    = '#c0392b'   # strong red for headers
PDF_SUBRED = '#e94560'   # lighter red for sub-headers & emphasis
PDF_GOLD   = '#d4850a'   # darker gold (readable on white)
PDF_GREY   = '#555555'   # mid-grey for meta / footer
PDF_LGREY  = '#95a5a6'   # light grey for dividers
PDF_TBLHDR = '#1a1a2e'   # table header bg (dark navy, white text)
PDF_TBLROW = '#f4f6f7'   # table row bg (very light grey, dark text)

def S(name, parent='Normal', **kw):
    return ParagraphStyle(name, parent=styles[parent], **kw)

S_title  = S('T1', fontSize=20, textColor=colors.HexColor(PDF_RED),
             spaceAfter=4, fontName='Helvetica-Bold', alignment=TA_CENTER)
S_sub    = S('T2', fontSize=10, textColor=colors.HexColor(PDF_GOLD),
             spaceAfter=2, fontName='Helvetica-Bold', alignment=TA_CENTER)
S_meta   = S('TM', fontSize=8,  textColor=colors.HexColor(PDF_GREY),
             spaceAfter=10, alignment=TA_CENTER)
S_h2     = S('H2', fontSize=12, textColor=colors.HexColor(PDF_RED),
             spaceBefore=8, spaceAfter=4, fontName='Helvetica-Bold')
S_h3     = S('H3', fontSize=9,  textColor=colors.HexColor(PDF_SUBRED),
             spaceBefore=5, spaceAfter=3, fontName='Helvetica-Bold')
S_body   = S('BD', fontSize=9,  textColor=colors.HexColor(PDF_BLACK),
             spaceAfter=5, leading=14)
S_bullet = S('BU', fontSize=9,  textColor=colors.HexColor(PDF_BLACK),
             spaceAfter=4, leading=14, leftIndent=12)
# KPI cards: dark navy background → white text is fine inside the table cells
S_kpi_v  = S('KV', fontSize=22, textColor=colors.white,
             alignment=TA_CENTER, fontName='Helvetica-Bold', leading=26)
S_kpi_s  = S('KS', fontSize=12, textColor=colors.HexColor('#f5a623'),
             alignment=TA_CENTER, fontName='Helvetica-Bold', leading=14)
S_kpi_l  = S('KL', fontSize=7,  textColor=colors.HexColor('#bdc3c7'),
             alignment=TA_CENTER, leading=10)
S_foot   = S('FT', fontSize=7.5, textColor=colors.HexColor(PDF_GREY),
             alignment=TA_CENTER)

def divider(thick=1, before=8, after=4):
    return HRFlowable(width=W, thickness=thick,
                      color=colors.HexColor(PDF_LGREY),
                      spaceBefore=before, spaceAfter=after)

def sec_hdr(text):
    return KeepTogether([divider(), Paragraph(text, S_h2)])

def base_ts():
    """Dark header row, light alternating body rows, dark text."""
    return TableStyle([
        ('BACKGROUND',    (0,0),(-1, 0), colors.HexColor(PDF_TBLHDR)),
        ('BACKGROUND',    (0,1),(-1,-1), colors.HexColor(PDF_TBLROW)),
        ('TEXTCOLOR',     (0,0),(-1, 0), colors.white),
        ('TEXTCOLOR',     (0,1),(-1,-1), colors.HexColor(PDF_BLACK)),
        ('FONTNAME',      (0,0),(-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',      (0,0),(-1,-1), 8),
        ('BOX',           (0,0),(-1,-1), 0.8, colors.HexColor(PDF_LGREY)),
        ('INNERGRID',     (0,0),(-1,-1), 0.4, colors.HexColor(PDF_LGREY)),
        ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING',    (0,0),(-1,-1), 5),
        ('BOTTOMPADDING', (0,0),(-1,-1), 5),
        ('LEFTPADDING',   (0,0),(-1,-1), 5),
        ('RIGHTPADDING',  (0,0),(-1,-1), 5),
        ('WORDWRAP',      (0,0),(-1,-1), 1),
    ])

story = []

# ── PAGE 1: COVER + KPIs + EXEC SUMMARY ──────────────────────────────────────
story.append(Spacer(1, 1.2*cm))
story.append(Paragraph('DUBAI PODCAST STUDIO  |  YALLAPOD', S_title))
story.append(Paragraph('Client Database — Marketing Intelligence Report', S_sub))
story.append(Paragraph('Reporting Period: March 23 – May 14, 2025  |  Generated: May 15, 2025', S_meta))
story.append(HRFlowable(width=W, thickness=2, color=colors.HexColor(PDF_RED), spaceAfter=12))

# KPI cards — 3 rows: big number / pct / label
kpi_data = [
    [Paragraph(str(total),             S_kpi_v),
     Paragraph(str(answered),          S_kpi_v),
     Paragraph(str(in_dubai),          S_kpi_v),
     Paragraph(str(not_dubai),         S_kpi_v)],
    [Paragraph('—',                    S_kpi_s),
     Paragraph(f'{contact_rate}%',     S_kpi_s),
     Paragraph(f'{dubai_rate}%',       S_kpi_s),
     Paragraph(f'{absent_rate}%',      S_kpi_s)],
    [Paragraph('Total Records',        S_kpi_l),
     Paragraph('Answered',             S_kpi_l),
     Paragraph('Confirmed In Dubai',   S_kpi_l),
     Paragraph('Currently Absent',     S_kpi_l)],
]
kpi_t = Table(kpi_data, colWidths=[W/4]*4, rowHeights=[34, 18, 16])
kpi_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0),(-1,-1), colors.HexColor(PDF_TBLHDR)),
    ('BOX',           (0,0),(-1,-1), 1,   colors.HexColor(PDF_RED)),
    ('INNERGRID',     (0,0),(-1,-1), 0.5, colors.HexColor('#2c3e50')),
    ('ALIGN',         (0,0),(-1,-1), 'CENTER'),
    ('VALIGN',        (0,0),(-1,-1), 'MIDDLE'),
    ('TOPPADDING',    (0,0),(-1,-1), 3),
    ('BOTTOMPADDING', (0,0),(-1,-1), 3),
]))
story.append(kpi_t)
story.append(Spacer(1, 0.4*cm))

story.append(Paragraph('EXECUTIVE SUMMARY', S_h2))
story.append(Paragraph(
    f'Between <b>March 23 and May 14, 2025</b>, the studio outreach team contacted '
    f'<b>{total} clients</b> from the YallaPod database to assess how the <b>regional conflict</b> '
    f'and the approaching <b>summer season</b> are impacting client presence and booking intent in Dubai. '
    f'Of the <b>{answered} clients reached ({contact_rate}%)</b>, the vast majority — '
    f'<b>{in_dubai} ({dubai_rate}%)</b> — confirmed they are currently in Dubai, a reassuring signal. '
    f'However, <b>{not_dubai} confirmed they are abroad</b>, and <b>{phone_off} phones were off</b> — '
    f'a combined signal that the summer exodus has already begun. '
    f'This report translates those findings into a concrete June–August marketing strategy and '
    f'budget allocation.', S_body))
story.append(PageBreak())

# ── PAGE 2: SECTIONS 1 + 2 ────────────────────────────────────────────────────
story.append(sec_hdr('1. OUTREACH PERFORMANCE'))

IMG_W2 = W * 0.46
IMG_H2 = IMG_W2 * 0.80
story.append(KeepTogether([
    Table([[Image(buf1, width=IMG_W2, height=IMG_H2),
            Image(buf2, width=IMG_W2, height=IMG_H2)]],
          colWidths=[W*0.5, W*0.5], rowHeights=[IMG_H2+6]),
    Spacer(1, 0.15*cm),
    Paragraph('Key Findings:', S_h3),
    Paragraph(
        f'• <b>{answered} clients answered ({contact_rate}%)</b> out of {total} total records — '
        f'strong for a cold-recall campaign.', S_bullet),
    Paragraph(
        f'• <b>{phone_off} phones were off ({round(phone_off/total*100,1)}%)</b> — '
        f'likely clients who have temporarily or permanently left the region.', S_bullet),
    Paragraph(
        f'• <b>{no_ans} no-answers ({round(no_ans/total*100,1)}%)</b> — '
        f'recoverable via WhatsApp/SMS follow-up.', S_bullet),
    Paragraph(
        f'• <b>{not_called} records not yet contacted ({round(not_called/total*100,1)}%)</b> — '
        f'a significant pool that should be prioritised in the next outreach wave.', S_bullet),
    Paragraph(
        f'• Of those reached: <b>{dubai_rate}% in Dubai</b>, <b>{absent_rate}% currently abroad</b>.', S_bullet),
]))

story.append(Spacer(1, 0.35*cm))
story.append(sec_hdr('2. GEOGRAPHIC DISPERSION OF ABSENT CLIENTS'))

IMG_W3 = W * 0.88
IMG_H3 = IMG_W3 * 0.46
story.append(KeepTogether([
    Spacer(1, 0.1*cm),
    Image(buf3, width=IMG_W3, height=IMG_H3),
    Spacer(1, 0.15*cm),
    Paragraph('Key Findings:', S_h3),
    Paragraph(
        '• <b>UK is the #1 destination</b> for absent clients — strong British expat segment '
        'travelling home for summer.', S_bullet),
    Paragraph(
        '• <b>France is #2</b> — significant Francophone clientele (France + potential North African diaspora).', S_bullet),
    Paragraph(
        '• <b>Abu Dhabi and Bahrain</b> indicate regional displacement — these clients can return to '
        'Dubai quickly and are the easiest to re-activate.', S_bullet),
    Paragraph(
        '• <b>Germany, Spain, Russia, Egypt, Bali, Singapore, Morocco, Panama, Texas</b> all '
        'represented — a genuinely global client base.', S_bullet),
]))
story.append(PageBreak())

# ── PAGE 3: SECTIONS 3 + 4 ────────────────────────────────────────────────────
story.append(sec_hdr('3. OUTREACH VOLUME OVER TIME'))

IMG_W4 = W
IMG_H4 = IMG_W4 * 0.31
story.append(KeepTogether([
    Spacer(1, 0.1*cm),
    Image(buf4, width=IMG_W4, height=IMG_H4),
    Spacer(1, 0.15*cm),
    Paragraph('Key Findings:', S_h3),
    Paragraph(
        '• <b>March 25</b> was the single highest-volume day (110 contacts) — the campaign launched '
        'aggressively right after the regional conflict escalation.', S_bullet),
    Paragraph(
        '• <b>April 14</b> was the second-largest day (68 contacts) — a systematic full-database sweep.', S_bullet),
    Paragraph(
        '• <b>Late April and May show declining volume</b> — the reachable pool is being exhausted. '
        'A fresh outreach wave on the untouched pool is now the priority.', S_bullet),
    Paragraph(
        '• <b>206 records (22%) have never been contacted</b> — these should be the next outreach batch.', S_bullet),
]))

story.append(Spacer(1, 0.4*cm))
story.append(sec_hdr('4. ABSENT CLIENT RETURN TIMELINE SEGMENTATION'))

IMG_W5 = W * 0.90
IMG_H5 = IMG_W5 * 0.42
imm_n  = ret_seg.get('Imminent (<2 wks)', 0)
mid_n  = ret_seg.get('Mid-term (1–3 mo)', 0)
lng_n  = ret_seg.get('Long-term (3+ mo)', 0)
unc_n  = ret_seg.get('Uncertain / No Date', 0)
noi_n  = ret_seg.get('No Info', 0)
lst_n  = ret_seg.get('Lost / Left Dubai', 0)

story.append(KeepTogether([
    Spacer(1, 0.1*cm),
    Image(buf5, width=IMG_W5, height=IMG_H5),
    Spacer(1, 0.15*cm),
    Paragraph('Key Findings:', S_h3),
    Paragraph(
        f'• <b>{imm_n} imminent returnees (&lt;2 weeks)</b> — contact NOW with a booking offer; '
        f'highest conversion potential.', S_bullet),
    Paragraph(
        f'• <b>{mid_n} mid-term (1–3 months)</b> — target with June/July advance-booking campaigns.', S_bullet),
    Paragraph(
        f'• <b>{lng_n} long-term (3+ months)</b> — low summer priority; nurture with email/content '
        f'for an autumn re-engagement campaign.', S_bullet),
    Paragraph(
        f'• <b>{unc_n} gave no certain date</b> — re-ping in 30 days; situation may have changed.', S_bullet),
    Paragraph(
        f'• <b>{lst_n} confirmed they are no longer Dubai-based</b> — archive or target with '
        f'remote/virtual recording services.', S_bullet),
]))
story.append(PageBreak())

# ── PAGE 4: SECTIONS 5, 6, 7, 8 ───────────────────────────────────────────────
story.append(sec_hdr('5. COMPETITOR STUDIO MENTIONS'))

S_tbl_body = S('TB', fontSize=8.5, textColor=colors.HexColor(PDF_BLACK), leading=13)
studio_rows = [[Paragraph('<b>Studio Named by Clients</b>', S_body),
                Paragraph('<b>Mentions</b>', S_body)]]
for s, c in studios.items():
    studio_rows.append([Paragraph(str(s).title(), S_tbl_body), Paragraph(str(c), S_tbl_body)])
st_t = Table(studio_rows, colWidths=[W*0.74, W*0.22])
st_t.setStyle(base_ts())
story.append(KeepTogether([
    st_t,
    Spacer(1, 0.15*cm),
    Paragraph(
        'Five competitor studios were explicitly named by clients: <b>Dimension, Metro Podcast '
        'Studio, Podster, Procast Studio, and Upod</b>. These studios are top-of-mind for your '
        'clients — understanding their pricing, equipment, and positioning is essential for '
        'retaining and winning back bookings.', S_body),
]))

story.append(Spacer(1, 0.3*cm))
story.append(sec_hdr('6. RISK ASSESSMENT — WAR IMPACT + SUMMER EFFECT'))

risk_data = [
    ['Risk Factor', 'Severity', 'Evidence', 'Recommended Action'],
    ['Regional conflict / client displacement', 'MEDIUM',
     f'{phone_off} phones off ({round(phone_off/total*100,1)}%)',
     'Retain Dubai clients with loyalty offers; avoid over-investing in permanently departed'],
    ['Summer seasonal decline', 'HIGH',
     f'{not_dubai} clients confirmed outside Dubai',
     "Shift budget to retention + 'coming back' campaigns targeting UK & France"],
    ['Large untouched contact pool', 'MEDIUM',
     f'{not_called} records not yet called',
     'Prioritise next outreach wave on this untouched segment immediately'],
    ['Competitor studio awareness', 'LOW–MED',
     '5 studios named by clients',
     'Benchmark vs. Dimension, Podster, Metro, Procast, Upod'],
    ['Long-term absent clients', 'LOW',
     f'{lng_n} returning in 3+ months',
     'Autumn re-engagement sequence; launch email nurture in Aug'],
]
risk_t = Table(risk_data, colWidths=[W*0.24, W*0.11, W*0.24, W*0.37])
ts_r = base_ts()
ts_r.add('BACKGROUND', (1,2),(1,2), colors.HexColor('#c0392b'))   # HIGH  — red bg
ts_r.add('BACKGROUND', (1,1),(1,1), colors.HexColor('#e67e22'))   # MEDIUM — orange
ts_r.add('BACKGROUND', (1,3),(1,3), colors.HexColor('#e67e22'))   # MEDIUM
ts_r.add('BACKGROUND', (1,4),(1,4), colors.HexColor('#16a085'))   # LOW-MED — teal
ts_r.add('BACKGROUND', (1,5),(1,5), colors.HexColor('#2980b9'))   # LOW — blue
ts_r.add('TEXTCOLOR',  (1,1),(1,-1), colors.white)
ts_r.add('FONTNAME',   (1,1),(1,-1), 'Helvetica-Bold')
ts_r.add('ALIGN',      (1,0),(1,-1), 'CENTER')
risk_t.setStyle(ts_r)
story.append(KeepTogether([risk_t]))
story.append(PageBreak())

# ── PAGE 5: SECTIONS 7 + 8 ────────────────────────────────────────────────────
story.append(sec_hdr('7. MARKETING STRATEGY & BUDGET — JUNE 2025'))
story.append(Paragraph('PRIORITY CAMPAIGNS', S_h3))

rec_data = [
    ['#', 'Campaign / Action', 'Target Segment', 'Priority', 'Channel'],
    ['1', "'Welcome Back' offer — booking discount\nor free add-on for returning clients",
     f'Imminent returnees\n({imm_n} clients)', '★★★★★', 'WhatsApp\n/ Call'],
    ['2', 'In-Dubai retention — monthly loyalty pack\nor multi-session discount',
     f'Confirmed in Dubai\n({in_dubai} clients)', '★★★★☆', 'Email\n+ Instagram'],
    ['3', 'WhatsApp blast to untouched pool\n+ no-answer list with studio tour video',
     f'Not yet called + unreached\n({not_called + no_ans} contacts)', '★★★★☆', 'WhatsApp'],
    ['4', "Geo-targeted ads — 'Coming back to Dubai?\nBook your recording session'",
     'UK, France, Germany\nexpat communities', '★★★☆☆', 'Meta Ads'],
    ['5', 'Competitor differentiation content\n(why YallaPod vs. Dimension / Podster)',
     'All active + returning clients', '★★★☆☆', 'Instagram\n/ YouTube'],
    ['6', 'Autumn nurture email sequence\n(6-week drip campaign)',
     f'Long-term absent + uncertain\n({lng_n + unc_n} clients)', '★★☆☆☆', 'Email'],
]
cws = [W*0.04, W*0.30, W*0.23, W*0.11, W*0.26]
rec_t = Table(rec_data, colWidths=cws)
ts_rec = base_ts()
ts_rec.add('ALIGN', (0,0),(0,-1), 'CENTER')
ts_rec.add('ALIGN', (3,0),(3,-1), 'CENTER')
rec_t.setStyle(ts_rec)
story.append(KeepTogether([rec_t]))

story.append(Spacer(1, 0.35*cm))
story.append(Paragraph('MONTHLY BUDGET ALLOCATION (% of Total Marketing Budget)', S_h3))

budget_data = [
    ['Channel / Campaign', '%', 'Rationale'],
    ['Direct WhatsApp outreach — returnees + untouched pool', '30%',
     'Highest ROI; personal touch; very low cost per contact'],
    ['Meta Ads — UK, France, Germany geo-targeting', '22%',
     'Catch expats before they return; build anticipation'],
    ['Loyalty & retention offers for in-Dubai clients', '18%',
     'Prevent churn of confirmed active clients during summer'],
    ['Instagram Reels + organic content\n(competitor differentiation)', '15%',
     'Brand awareness; position vs. Dimension, Podster, Metro'],
    ['Email nurture — mid/long-term absent clients', '10%',
     'Low cost; keeps YallaPod top of mind for autumn return'],
    ['Content production — studio tour, testimonials', '5%',
     'One-off asset; high reuse across all channels'],
]
bud_t = Table(budget_data, colWidths=[W*0.43, W*0.08, W*0.44])
ts_b = base_ts()
ts_b.add('ALIGN',    (1,0),(1,-1), 'CENTER')
ts_b.add('FONTNAME', (1,1),(1,-1), 'Helvetica-Bold')
ts_b.add('TEXTCOLOR',(1,1),(1,-1), colors.HexColor(PDF_RED))
bud_t.setStyle(ts_b)
story.append(KeepTogether([bud_t]))

story.append(Spacer(1, 0.35*cm))
story.append(sec_hdr('8. IMMEDIATE ACTION CHECKLIST'))

actions = [
    ('TODAY',       'Export all imminent returnees — assign for personal WhatsApp/call follow-up with booking offer'),
    ('TODAY',       f'Begin outreach on the {not_called} untouched records — this is an immediate revenue opportunity'),
    ('THIS WEEK',   "Create 'Coming back to Dubai?' campaign — 10%+ booking discount or free studio add-on"),
    ('THIS WEEK',   'Launch Meta Ads targeting UK, France, Germany — UAE podcast / content creator audience'),
    ('THIS WEEK',   'Audit competitor pricing: Dimension, Podster, Metro Podcast Studio, Procast, Upod'),
    ('NEXT WEEK',   'Send loyalty offer to all confirmed in-Dubai clients (WhatsApp + Email)'),
    ('NEXT WEEK',   'Build 6-email nurture sequence for mid/long-term absent clients — schedule for July delivery'),
    ('END OF JUNE', 'Full database re-outreach — client situations will have shifted significantly'),
]
checklist = []
for timing, task in actions:
    checklist.append(Paragraph(f'<b>[{timing}]</b>  {task}', S_bullet))
story.append(KeepTogether(checklist))

# ── FOOTER ────────────────────────────────────────────────────────────────────
story.append(Spacer(1, 0.6*cm))
story.append(HRFlowable(width=W, thickness=1, color=colors.HexColor(PDF_RED), spaceAfter=4))
story.append(Paragraph(
    'YallaPod — Dubai Podcast Studio  |  Client Intelligence Report  |  Confidential  |  May 2025',
    S_foot))

# ── BUILD ─────────────────────────────────────────────────────────────────────
doc.build(story)
print(f'PDF saved → {pdf_path}')
print(f'Total records : {total}')
print(f'Answered      : {answered}  ({contact_rate}%)')
print(f'No Answer     : {no_ans}')
print(f'Phone Off     : {phone_off}')
print(f'Not Called    : {not_called}')
print(f'In Dubai      : {in_dubai}  ({dubai_rate}%)')
print(f'Absent        : {not_dubai}  ({absent_rate}%)')
print(f'Countries     : {countries.to_dict()}')
print(f'Return segs   : {ret_seg.to_dict()}')
