#!/usr/bin/env python3
"""
AL-MAKTABA · Centre Linguistique de Riyad
Interior Design Concept Boards — Présentation Partenaires
High-resolution PIL-based design boards
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import arabic_reshaper
from bidi.algorithm import get_display
from scipy.ndimage import gaussian_filter

# ── SETUP ─────────────────────────────────────────────────────────────────────
W, H   = 1654, 2339   # A4 at 200 DPI
M      = 90            # outer margin
OUT    = '/home/user/ABD-BND/CLR_Design_Boards.pdf'

# ── PALETTE ──────────────────────────────────────────────────────────────────
NAVY      = ( 13,  27,  42)
NAVY2     = ( 22,  42,  66)
NAVY3     = ( 30,  55,  85)
GOLD      = (197, 166,  92)
GOLD_L    = (228, 205, 148)
IVORY     = (248, 242, 230)
OFF_W     = (232, 226, 214)
WARM_G    = (155, 150, 142)
TERRA     = (196, 113,  75)
TERRA_L   = (218, 143, 105)
SAGE      = (104, 136, 120)
SAGE_L    = (138, 172, 156)
WALNUT    = ( 87,  58,  38)
WALNUT_L  = (120,  85,  55)
BRASS     = (176, 141,  87)
CREAM     = (242, 237, 225)
CHARCOAL  = ( 38,  42,  50)

# ── FONTS ─────────────────────────────────────────────────────────────────────
FONT_CACHE = {}

def fnt(style, size):
    key = (style, size)
    if key in FONT_CACHE:
        return FONT_CACHE[key]
    paths = {
        'bold':    ['/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'],
        'regular': ['/tmp/fonts/Montserrat.ttf',
                    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
        'light':   ['/tmp/fonts/Montserrat.ttf',
                    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'],
        'arabic':  ['/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Bold.ttf'],
        'arabic_r':['/usr/share/fonts/opentype/fonts-hosny-amiri/Amiri-Regular.ttf'],
        'italic':  ['/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf',
                    '/tmp/fonts/Montserrat.ttf'],
    }
    for p in paths.get(style, paths['regular']):
        if Path(p).exists() and Path(p).stat().st_size > 100:
            f = ImageFont.truetype(p, size)
            FONT_CACHE[key] = f
            return f
    f = ImageFont.load_default()
    FONT_CACHE[key] = f
    return f

def ar(text):
    return get_display(arabic_reshaper.reshape(text))

def tw(draw, text, font):
    bb = draw.textbbox((0, 0), text, font=font)
    return bb[2] - bb[0], bb[3] - bb[1]

def center_text(draw, y, text, font, color, canvas_w=W):
    w_, h_ = tw(draw, text, font)
    draw.text(((canvas_w - w_) // 2, y), text, font=font, fill=color)
    return h_

def rule(draw, y, x0=None, x1=None, color=GOLD, lw=2):
    if x0 is None: x0 = M
    if x1 is None: x1 = W - M
    draw.line([(x0, y), (x1, y)], fill=color, width=lw)

# ── TEXTURES ──────────────────────────────────────────────────────────────────

def tex_concrete(w, h, seed=1):
    """Polished concrete — grey with trowel marks"""
    rng = np.random.RandomState(seed)
    n = gaussian_filter(rng.normal(0, 1, (h, w)), sigma=4) * 10
    base = 148 + n
    r = np.clip(base + rng.normal(0, 1.5, (h, w)), 122, 175).astype(np.uint8)
    g = np.clip(base + rng.normal(0, 1.5, (h, w)) - 1, 120, 173).astype(np.uint8)
    b = np.clip(base + rng.normal(0, 1.5, (h, w)) - 4, 116, 169).astype(np.uint8)
    img = Image.fromarray(np.stack([r, g, b], axis=2))
    d = ImageDraw.Draw(img)
    for _ in range(h // 16):
        y0 = rng.randint(0, h)
        x0_ = rng.randint(0, w // 3)
        x1_ = x0_ + rng.randint(w // 3, w)
        gv = rng.randint(140, 162)
        d.line([(x0_, y0), (min(w-1, x1_), y0 + rng.randint(-1, 1))],
               fill=(gv, gv-1, gv-3), width=1)
    return img.filter(ImageFilter.GaussianBlur(0.6))

def tex_wood_dark(w, h, seed=2):
    """Dark walnut — rich brown grain"""
    rng = np.random.RandomState(seed)
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        t = y / h
        w1 = np.sin(t * np.pi * 42 + rng.normal(0, 0.6)) * 0.5 + 0.5
        w2 = np.sin(t * np.pi * 14 + rng.normal(0, 0.3)) * 0.35 + 0.65
        r = 70 + w1 * 32 + w2 * 14
        g = 44 + w1 * 20 + w2 * 8
        b = 25 + w1 * 11 + w2 * 4
        arr[y, :, 0] = r + rng.normal(0, 2.5, w)
        arr[y, :, 1] = g + rng.normal(0, 1.8, w)
        arr[y, :, 2] = b + rng.normal(0, 1.2, w)
    for _ in range(w // 10):
        x = rng.randint(0, w)
        drift = rng.normal(0, 0.8)
        for y in range(h):
            xc = max(0, min(w-1, int(x + drift * y / h * 30)))
            arr[y, xc:xc+rng.randint(1, 3)] *= rng.uniform(0.62, 0.78)
    return Image.fromarray(np.clip(arr, 14, 152).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.45))

def tex_marble_cream(w, h, seed=3):
    """Calacatta cream marble with grey veining"""
    rng = np.random.RandomState(seed)
    base = gaussian_filter(rng.normal(236, 5, (h, w)), sigma=4)
    r = np.clip(base + 5, 210, 253).astype(np.uint8)
    g = np.clip(base + 1, 206, 249).astype(np.uint8)
    b = np.clip(base - 8, 196, 240).astype(np.uint8)
    img = Image.fromarray(np.stack([r, g, b], axis=2))
    d = ImageDraw.Draw(img)
    for _ in range(18):
        x = rng.randint(-w // 4, w)
        y = rng.randint(-h // 3, h // 3)
        pts = [(x, y)]
        for _ in range(300):
            x += int(rng.normal(10, 5))
            y += int(rng.normal(0, 5))
            pts.append((min(w-1, max(0, x)), min(h-1, max(0, y))))
        gv = rng.randint(148, 195)
        vw = rng.choice([1, 1, 1, 2, 2, 3])
        for i in range(len(pts) - 1):
            d.line([pts[i], pts[i+1]], fill=(gv, gv-4, gv-9), width=vw)
    return img.filter(ImageFilter.GaussianBlur(1.1))

def tex_zellige(w, h, seed=4):
    """Moroccan zellige terracotta — irregular hand-fired tiles"""
    rng = np.random.RandomState(seed)
    tile = 46
    img = Image.new('RGB', (w, h), (22, 16, 12))
    d = ImageDraw.Draw(img)
    cols = [(196,113,75),(212,132,90),(180,96,62),(218,140,96),
            (174,104,68),(202,120,80),(188,108,72),(208,126,86)]
    for ty in range(0, h + tile, tile):
        for tx in range(0, w + tile, tile):
            c = cols[rng.randint(0, len(cols))]
            bv = rng.uniform(0.87, 1.11)
            c2 = tuple(max(0, min(255, int(v * bv))) for v in c)
            gap = rng.randint(3, 7)
            # Slightly irregular tile edges
            x0 = tx + gap + rng.randint(-1, 1)
            y0 = ty + gap + rng.randint(-1, 1)
            x1 = tx + tile - gap - 1 + rng.randint(-1, 1)
            y1 = ty + tile - gap - 1 + rng.randint(-1, 1)
            d.rectangle([x0, y0, x1, y1], fill=c2)
    return img.filter(ImageFilter.GaussianBlur(0.3))

def tex_brass(w, h, seed=5):
    """Brushed brass / laiton brossé"""
    rng = np.random.RandomState(seed)
    y_a = np.arange(h)
    wave = 0.5 + 0.5 * np.sin(y_a * 0.14)
    r = (158 + wave * 38).reshape(h, 1) * np.ones((1, w))
    g = (124 + wave * 28).reshape(h, 1) * np.ones((1, w))
    b = (68  + wave * 18).reshape(h, 1) * np.ones((1, w))
    step = 0
    y = 0
    while y < h:
        step = rng.randint(2, 9)
        bv = rng.uniform(0.86, 1.04)
        r[y:y+step] *= bv
        g[y:y+step] *= bv
        b[y:y+step] *= bv
        y += step
    nr = rng.normal(0, 3, (h, w))
    arr = np.stack([r + nr, g + nr * 0.7, b + nr * 0.4], axis=2)
    return Image.fromarray(np.clip(arr, 55, 228).astype(np.uint8))

def tex_navy_fabric(w, h, seed=6):
    """Deep navy bouclé / fabric"""
    rng = np.random.RandomState(seed)
    arr = np.zeros((h, w, 3), dtype=np.float32)
    step = 5
    for y in range(h):
        for xb in range(0, w, step):
            ph = ((xb // step) + (y // 3)) % 2
            v = 0.90 if ph == 0 else 0.72
            n = rng.uniform(0.94, 1.06)
            arr[y, xb:xb+step] = [14*v*n, 29*v*n, 68*v*n]
    noise = rng.normal(0, 1, (h, w, 3))
    arr += noise
    return Image.fromarray(np.clip(arr, 6, 92).astype(np.uint8))

def tex_sage_plaster(w, h, seed=7):
    """Sage green tadelakt plaster"""
    rng = np.random.RandomState(seed)
    large = gaussian_filter(rng.normal(0, 1, (h, w)), sigma=40)
    large = (large - large.min()) / (np.ptp(large) + 1e-9)
    fine  = gaussian_filter(rng.normal(0, 1, (h, w)), sigma=2)
    fine  = (fine - fine.min()) / (np.ptp(fine) + 1e-9)
    combined = large * 0.68 + fine * 0.32
    r = np.clip(98  + combined * 18 + rng.normal(0, 2, (h, w)), 72, 132)
    g = np.clip(130 + combined * 22 + rng.normal(0, 2, (h, w)), 100, 162)
    b = np.clip(114 + combined * 14 + rng.normal(0, 2, (h, w)), 88, 145)
    return Image.fromarray(
        np.stack([r.astype(np.uint8), g.astype(np.uint8), b.astype(np.uint8)], axis=2))

def tex_wood_light(w, h, seed=8):
    """Light oak — pale golden grain"""
    rng = np.random.RandomState(seed)
    arr = np.zeros((h, w, 3), dtype=np.float32)
    for y in range(h):
        t = y / h
        wave = np.sin(t * np.pi * 38 + rng.normal(0, 0.4)) * 0.38 + 0.62
        r = 188 + wave * 28
        g = 155 + wave * 20
        b = 108 + wave * 15
        arr[y, :, 0] = r + rng.normal(0, 2.5, w)
        arr[y, :, 1] = g + rng.normal(0, 1.8, w)
        arr[y, :, 2] = b + rng.normal(0, 1.2, w)
    for _ in range(w // 20):
        x = rng.randint(0, w)
        for y in range(h):
            xc = max(0, min(w-1, x + int(rng.normal(0, 2.5))))
            arr[y, xc] *= rng.uniform(0.82, 0.94)
    return Image.fromarray(np.clip(arr, 142, 232).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(0.4))

def tex_stone_beige(w, h, seed=9):
    """Beige sandstone / travertin"""
    rng = np.random.RandomState(seed)
    base = gaussian_filter(rng.normal(210, 8, (h, w)), sigma=5)
    # Horizontal strata lines
    for y in range(0, h, rng.randint(12, 35)):
        thickness = rng.randint(1, 3)
        base[y:y+thickness, :] -= rng.uniform(8, 18)
    r = np.clip(base + 18, 178, 248).astype(np.uint8)
    g = np.clip(base + 10, 170, 240).astype(np.uint8)
    b = np.clip(base - 8,  155, 225).astype(np.uint8)
    return Image.fromarray(np.stack([r, g, b], axis=2)).filter(
        ImageFilter.GaussianBlur(0.7))

# ── COMPOSITE HELPERS ─────────────────────────────────────────────────────────

def paste_rounded(canvas, src_img, x, y, w_, h_, radius=16):
    """Paste image with rounded corner mask"""
    scaled = src_img.resize((w_, h_), Image.LANCZOS)
    mask = Image.new('L', (w_, h_), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, w_-1, h_-1], radius=radius, fill=255)
    canvas.paste(scaled, (x, y), mask)

def dark_overlay(canvas, x, y, w_, h_, alpha=80):
    """Overlay a dark translucent panel"""
    ov = Image.new('RGBA', (w_, h_), (13, 27, 42, alpha))
    c_rgba = canvas.convert('RGBA')
    c_rgba.paste(ov, (x, y), ov)
    return c_rgba.convert('RGB')

def swatch_block(canvas, draw, x, y, w_, h_, tex_fn, seed, label, sublabel, radius=14):
    """Material swatch with label below"""
    tex = tex_fn(w_, h_, seed)
    paste_rounded(canvas, tex, x, y, w_, h_, radius=radius)
    draw.text((x, y + h_ + 12), label, font=fnt('bold', 17), fill=IVORY)
    draw.text((x, y + h_ + 38), sublabel, font=fnt('light', 13), fill=WARM_G)

# ── FLOOR PLAN SKETCHES ───────────────────────────────────────────────────────

def sketch_zone(draw, zone_id, x0, y0, pw, ph):
    """Simple architectural floor plan per zone"""
    lw = 2
    # Outer wall
    draw.rectangle([x0, y0, x0+pw, y0+ph], outline=IVORY, width=lw)

    if zone_id == 'A':
        # Reception desk arc
        rx, ry = x0+30, y0+30
        draw.arc([rx, ry, rx+pw-60, ry+int(ph*0.45)], start=0, end=180,
                 fill=GOLD, width=lw)
        draw.line([(rx, ry+int(ph*0.45)//2), (rx, ry+int(ph*0.45)//2)],
                  fill=GOLD, width=lw)
        # Two armchairs
        for i in range(2):
            ax = x0+int(pw*0.55) + i*int(pw*0.18)
            ay = y0 + int(ph*0.55)
            r_ = int(pw*0.08)
            draw.ellipse([ax-r_, ay-r_, ax+r_, ay+r_], fill=TERRA, outline=GOLD, width=1)
        # Plant corner
        px = x0+int(pw*0.82); py = y0+int(ph*0.18)
        pr = int(pw*0.07)
        draw.ellipse([px-pr, py-pr, px+pr, py+pr], fill=SAGE, outline=GOLD, width=1)
        # Door
        draw.line([(x0+int(pw*0.3), y0), (x0+int(pw*0.5), y0)], fill=NAVY2, width=4)
        draw.arc([x0+int(pw*0.3), y0-int(pw*0.2), x0+int(pw*0.5), y0+int(pw*0.0)],
                start=0, end=90, fill=GOLD, width=1)
        # Labels
        draw.text((x0+5, y0+5), "ACCUEIL", font=fnt('regular', 11), fill=GOLD)
        draw.text((x0+int(pw*0.55), y0+int(ph*0.78)), "LOUNGE", font=fnt('regular', 11), fill=WARM_G)

    elif zone_id == 'B':
        # Counter along left wall
        draw.rectangle([x0+8, y0+int(ph*0.08), x0+int(pw*0.22), y0+int(ph*0.92)],
                      fill=WALNUT, outline=GOLD, width=1)
        draw.text((x0+12, y0+int(ph*0.45)), "BAR", font=fnt('regular', 11), fill=GOLD)
        # Round café tables
        for (dx, dy) in [(0.5, 0.3), (0.72, 0.3), (0.5, 0.65), (0.72, 0.65)]:
            tx = x0 + int(pw*dx); ty = y0 + int(ph*dy)
            r_ = int(pw*0.09)
            draw.ellipse([tx-r_, ty-r_, tx+r_, ty+r_], fill=CHARCOAL, outline=GOLD, width=1)
            # 2 chairs each
            for ang in [0, 180]:
                import math
                ch_x = int(tx + (r_+8)*math.cos(math.radians(ang)))
                ch_y = int(ty + (r_+8)*math.sin(math.radians(ang)))
                cr = int(pw*0.04)
                draw.ellipse([ch_x-cr, ch_y-cr, ch_x+cr, ch_y+cr], fill=TERRA)
        # Bookshelf along back wall
        draw.rectangle([x0+int(pw*0.28), y0+8, x0+int(pw*0.92), y0+int(ph*0.07)],
                      fill=WALNUT, outline=GOLD, width=1)
        draw.text((x0+int(pw*0.4), y0+12), "BIBLIOTHÈQUE", font=fnt('regular', 9), fill=GOLD)

    elif zone_id == 'C':
        # SMART board front
        draw.rectangle([x0+int(pw*0.12), y0+8, x0+int(pw*0.88), y0+int(ph*0.1)],
                      fill=CHARCOAL, outline=GOLD, width=1)
        draw.text((x0+int(pw*0.32), y0+12), "SMART BOARD", font=fnt('regular', 9), fill=GOLD)
        # Tables in 2 rows × 3 cols
        tw_ = int(pw*0.22); th_ = int(ph*0.14)
        tw_gap = int(pw*0.05); th_gap = int(ph*0.1)
        start_y = y0 + int(ph*0.22)
        for row in range(2):
            for col in range(3):
                tx = x0 + int(pw*0.06) + col*(tw_+tw_gap)
                ty = start_y + row*(th_+th_gap)
                draw.rectangle([tx, ty, tx+tw_, ty+th_], fill=CHARCOAL, outline=GOLD, width=1)
                # Chair
                cy = ty + th_ + 6
                draw.rectangle([tx+int(tw_*0.2), cy, tx+int(tw_*0.8), cy+int(th_*0.35)],
                               fill=SAGE, outline=GOLD, width=1)
        # Teacher desk
        draw.rectangle([x0+int(pw*0.35), y0+int(ph*0.88), x0+int(pw*0.65), y0+int(ph*0.97)],
                      fill=WALNUT, outline=GOLD, width=1)
        draw.text((x0+int(pw*0.38), y0+int(ph*0.90)), "BUREAU", font=fnt('regular', 10), fill=GOLD)

    elif zone_id == 'D':
        # Round central table
        cx = x0 + pw//2; cy = y0 + int(ph*0.48)
        r_ = int(pw*0.22)
        draw.ellipse([cx-r_, cy-r_, cx+r_, cy+r_], fill=WALNUT, outline=GOLD, width=2)
        draw.text((cx-18, cy-8), "TABLE", font=fnt('regular', 11), fill=GOLD)
        # 4 chairs
        import math
        for ang in [0, 90, 180, 270]:
            chx = int(cx + (r_+14)*math.cos(math.radians(ang)))
            chy = int(cy + (r_+14)*math.sin(math.radians(ang)))
            cr = int(pw*0.065)
            draw.ellipse([chx-cr, chy-cr, chx+cr, chy+cr], fill=TERRA, outline=GOLD, width=1)
        # Curtains along one wall
        draw.rectangle([x0+pw-12, y0+int(ph*0.1), x0+pw, y0+int(ph*0.9)],
                      fill=IVORY, outline=GOLD, width=1)
        draw.text((x0+int(pw*0.05), y0+int(ph*0.08)), "FENÊTRE", font=fnt('regular', 9), fill=WARM_G)

    # North indicator
    na_x = x0 + pw - 18; na_y = y0 + 14
    draw.polygon([(na_x, na_y), (na_x-6, na_y+14), (na_x+6, na_y+14)], fill=GOLD)
    draw.text((na_x-4, na_y+15), "N", font=fnt('regular', 10), fill=GOLD)

# ── PAGE: COVER ───────────────────────────────────────────────────────────────

def page_cover():
    canvas = Image.new('RGB', (W, H), NAVY)
    draw = ImageDraw.Draw(canvas)

    # Subtle vignette background
    rng = np.random.RandomState(42)
    vgn = gaussian_filter(rng.normal(0, 1, (H, W)), sigma=120)
    vgn = (vgn - vgn.min()) / (np.ptp(vgn) + 1e-9)
    bg_r = np.clip(13 + vgn*14, 8, 38).astype(np.uint8)
    bg_g = np.clip(27 + vgn* 9, 18, 48).astype(np.uint8)
    bg_b = np.clip(42 + vgn*18, 30, 72).astype(np.uint8)
    canvas = Image.fromarray(np.stack([bg_r, bg_g, bg_b], axis=2))
    draw = ImageDraw.Draw(canvas)

    # ── TOP BAR ──────────────────────────────────────────────────────────────
    draw.line([(0, 0), (W, 0)], fill=GOLD, width=5)
    draw.text((M, 18), "AL-MAKTABA", font=fnt('bold', 15), fill=GOLD)
    rt = "NORD RIYAD  ·  160 m²  ·  2025"
    rtw, _ = tw(draw, rt, fnt('light', 14))
    draw.text((W - M - rtw, 20), rt, font=fnt('light', 14), fill=WARM_G)

    # ── GOLD DIAGONAL STRIPE ─────────────────────────────────────────────────
    stripe_y1 = int(H * 0.28)
    stripe_y2 = int(H * 0.32)
    pts = [(0, stripe_y1 + 40), (W, stripe_y1), (W, stripe_y2), (0, stripe_y2 + 40)]
    stripe_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(stripe_img).polygon(pts, fill=(197, 166, 92, 22))
    canvas = canvas.convert('RGBA')
    canvas.alpha_composite(stripe_img)
    canvas = canvas.convert('RGB')
    draw = ImageDraw.Draw(canvas)

    # ── ARABIC CALLIGRAPHY ────────────────────────────────────────────────────
    arabic_main = ar("المكتبة")
    ar_font = fnt('arabic', 210)
    center_text(draw, 95, arabic_main, ar_font, GOLD)

    # ── THIN RULE ────────────────────────────────────────────────────────────
    rule(draw, 410, x0=M*4, x1=W-M*4, lw=1)

    # ── MAIN TITLE ────────────────────────────────────────────────────────────
    center_text(draw, 440, "AL-MAKTABA", fnt('bold', 94), IVORY)
    center_text(draw, 562, "CENTRE LINGUISTIQUE DE RIYAD", fnt('bold', 34), GOLD)
    center_text(draw, 618, "Concept d'intérieur  ·  Présentation partenaires", fnt('light', 22), WARM_G)

    # ── RULE ─────────────────────────────────────────────────────────────────
    rule(draw, 672, x0=M*4, x1=W-M*4, lw=1)

    # ── COLOUR PALETTE DOTS ───────────────────────────────────────────────────
    pal_items = [
        (NAVY2,   "NAVY"),
        (WALNUT,  "NOYER"),
        (TERRA,   "TERRACOTTA"),
        (SAGE,    "SAUGE"),
        (GOLD,    "LAITON"),
        (CREAM,   "MARBRE"),
    ]
    dr, dg = 44, 28
    total_dw = len(pal_items) * (dr*2 + dg) - dg
    dx0 = (W - total_dw) // 2
    for i, (c, n) in enumerate(pal_items):
        cx_ = dx0 + i*(dr*2+dg) + dr
        cy_ = 740
        draw.ellipse([cx_-dr, cy_-dr, cx_+dr, cy_+dr], fill=c)
        draw.ellipse([cx_-dr, cy_-dr, cx_+dr, cy_+dr], outline=GOLD, width=1)
        tw_, _ = tw(draw, n, fnt('regular', 12))
        draw.text((cx_-tw_//2, cy_+dr+8), n, font=fnt('regular', 12), fill=WARM_G)

    # ── ZONES OVERVIEW ────────────────────────────────────────────────────────
    center_text(draw, 860, "ZONES DU PROJET", fnt('bold', 22), GOLD)
    rule(draw, 900)

    zones_info = [
        ('A', "RÉCEPTION & ACCUEIL",   "35 m²", GOLD),
        ('B', "CAFÉ MAKTABA",           "40 m²", TERRA),
        ('C', "SALLES DE COURS",        "55 m²", SAGE),
        ('D', "ESPACES SEMI-PRIVÉS",   "30 m²", BRASS),
    ]
    for i, (zid, zname, zarea, zcol) in enumerate(zones_info):
        zy = 922 + i * 105
        # Zone badge
        draw.rounded_rectangle([M, zy, M+68, zy+70], radius=7, fill=zcol)
        zid_w, _ = tw(draw, zid, fnt('bold', 36))
        draw.text((M + (68-zid_w)//2, zy+14), zid, font=fnt('bold', 36), fill=NAVY)
        draw.text((M+88, zy+10), zname, font=fnt('bold', 25), fill=IVORY)
        draw.text((M+88, zy+44), zarea, font=fnt('light', 17), fill=WARM_G)
        # Dotted separator
        dot_x = M + 410
        while dot_x < W - M - 120:
            draw.ellipse([dot_x, zy+35, dot_x+3, zy+38], fill=NAVY3)
            dot_x += 16
        areaw, _ = tw(draw, zarea, fnt('bold', 22))
        draw.text((W-M-areaw, zy+22), zarea, font=fnt('bold', 22), fill=zcol)

    rule(draw, 1345)

    # ── SPECS LINE ────────────────────────────────────────────────────────────
    specs = "Budget 280 000 SAR  ·  Livraison 10 semaines  ·  Surface 160 m²"
    center_text(draw, 1362, specs, fnt('light', 18), WARM_G)

    # ── MATERIAL STRIP AT BOTTOM ──────────────────────────────────────────────
    strip_y = H - 430
    strip_h = 360
    mat_list = [
        (tex_concrete,    "BÉTON CIRÉ"),
        (tex_wood_dark,   "NOYER MASSIF"),
        (tex_marble_cream,"MARBRE"),
        (tex_zellige,     "ZELLIGE"),
        (tex_brass,       "LAITON"),
        (tex_sage_plaster,"TADELAKT"),
    ]
    sw = W // len(mat_list)
    for i, (tfn, mname) in enumerate(mat_list):
        tx = i * sw
        t_img = tfn(sw, strip_h, seed=i+10)
        canvas.paste(t_img.resize((sw, strip_h), Image.LANCZOS), (tx, strip_y))

    # Dark overlay over material strip
    ov = Image.new('RGBA', (W, strip_h), (13, 27, 42, 148))
    c_rgba = canvas.convert('RGBA')
    c_rgba.paste(ov, (0, strip_y), ov)
    canvas = c_rgba.convert('RGB')
    draw = ImageDraw.Draw(canvas)

    # Material labels
    for i, (tfn, mname) in enumerate(mat_list):
        cx_ = i * sw + sw // 2
        mw, _ = tw(draw, mname, fnt('bold', 14))
        draw.text((cx_ - mw//2, strip_y + strip_h//2 - 10), mname,
                  font=fnt('bold', 14), fill=IVORY)
        # Small gold underline
        rule(draw, strip_y + strip_h//2 + 16, x0=cx_-30, x1=cx_+30, color=GOLD, lw=1)

    # Gold borders on strip
    draw.line([(0, strip_y), (W, strip_y)], fill=GOLD, width=3)
    draw.line([(0, strip_y+strip_h), (W, strip_y+strip_h)], fill=GOLD, width=3)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    footer = "AL-MAKTABA  ·  Centre Linguistique  ·  Nord Riyad"
    fw, _ = tw(draw, footer, fnt('light', 14))
    draw.text(((W-fw)//2, H-55), footer, font=fnt('light', 14), fill=WARM_G)
    pn = "01 / 05"
    pnw, _ = tw(draw, pn, fnt('regular', 14))
    draw.text((W-M-pnw, H-55), pn, font=fnt('regular', 14), fill=WARM_G)

    return canvas

# ── PAGE: ZONE ────────────────────────────────────────────────────────────────

def page_zone(pnum, zone_id, zone_name, zone_area, zone_col,
              hero_fn, hero_label, hero_sub,
              swatches,           # list of (tex_fn, seed, label, sublabel)
              palette,            # list of (color, name)
              concept_lines,      # list of str (concept description)
              elements,           # list of str (bullet points)
              arabic_phrase, arabic_trans):

    canvas = Image.new('RGB', (W, H), NAVY)

    # Subtle noise background
    rng = np.random.RandomState(pnum * 13)
    vgn = gaussian_filter(rng.normal(0, 1, (H, W)), sigma=110)
    vgn = (vgn - vgn.min()) / (np.ptp(vgn) + 1e-9)
    bg_r = np.clip(13 + vgn*10, 8, 35).astype(np.uint8)
    bg_g = np.clip(27 + vgn* 7, 18, 46).astype(np.uint8)
    bg_b = np.clip(42 + vgn*15, 28, 68).astype(np.uint8)
    canvas = Image.fromarray(np.stack([bg_r, bg_g, bg_b], axis=2))
    draw = ImageDraw.Draw(canvas)

    # ── TOP GOLD BORDER ───────────────────────────────────────────────────────
    draw.line([(0, 0), (W, 0)], fill=GOLD, width=5)
    # Zone colour sidebar
    draw.rectangle([0, 5, 7, 220], fill=zone_col)

    # ── HEADER ────────────────────────────────────────────────────────────────
    # Zone badge
    draw.rounded_rectangle([M, 22, M+76, 22+82], radius=7, fill=zone_col)
    zidw, _ = tw(draw, zone_id, fnt('bold', 42))
    draw.text((M+(76-zidw)//2, 36), zone_id, font=fnt('bold', 42), fill=NAVY)
    # Zone name
    draw.text((M+96, 24), zone_name, font=fnt('bold', 50), fill=IVORY)
    # Area + project (right)
    prt = "AL-MAKTABA · RIYAD"
    prtw, _ = tw(draw, prt, fnt('light', 16))
    draw.text((W-M-prtw, 26), prt, font=fnt('light', 16), fill=GOLD)
    draw.text((W-M-prtw, 56), zone_area, font=fnt('regular', 15), fill=WARM_G)
    # Page number
    pgn = f"0{pnum} / 05"
    pgnw, _ = tw(draw, pgn, fnt('regular', 14))
    draw.text((W-M-pgnw, 85), pgn, font=fnt('regular', 14), fill=WARM_G)

    rule(draw, 128, lw=1)

    # ── HERO TEXTURE ──────────────────────────────────────────────────────────
    hero_h = 440
    hero_w = W - 2*M
    hero_tex = hero_fn(hero_w, hero_h, seed=pnum*5)
    paste_rounded(canvas, hero_tex, M, 148, hero_w, hero_h, radius=18)

    # Top-fade overlay for label legibility
    fade = Image.new('RGBA', (hero_w, 70), (0,0,0,0))
    fd = ImageDraw.Draw(fade)
    for row in range(70):
        a = int(90*(1-row/70))
        fd.line([(0,row),(hero_w,row)], fill=(13,27,42,a))
    c_rgba = canvas.convert('RGBA')
    c_rgba.paste(fade, (M, 148), fade)
    canvas = c_rgba.convert('RGB')
    draw = ImageDraw.Draw(canvas)

    # Bottom label on hero
    hlabw, _ = tw(draw, hero_label.upper(), fnt('bold', 18))
    draw.text((M+20, 148+hero_h-52), hero_label.upper(), font=fnt('bold', 18), fill=IVORY)
    draw.text((M+20, 148+hero_h-26), hero_sub, font=fnt('light', 13), fill=GOLD)

    # ── 3 SWATCHES ROW ────────────────────────────────────────────────────────
    sw_y  = 148 + hero_h + 24
    sw_h  = 210
    sw_gap = 22
    sw_w  = (W - 2*M - 2*sw_gap) // 3

    for i, (tfn, seed, lbl, sub) in enumerate(swatches[:3]):
        sx = M + i*(sw_w+sw_gap)
        swatch_block(canvas, draw, sx, sw_y, sw_w, sw_h, tfn, seed, lbl, sub, radius=12)

    draw = ImageDraw.Draw(canvas)  # refresh after pasting

    # ── LEFT COLUMN: PALETTE + CONCEPT ───────────────────────────────────────
    col_y = sw_y + sw_h + 70
    rule(draw, col_y - 18, x1=W//2 - 20)

    draw.text((M, col_y), "PALETTE", font=fnt('bold', 18), fill=GOLD)
    dr2 = 32; dg2 = 20
    for i, (c, n) in enumerate(palette):
        cx_ = M + i*(dr2*2+dg2) + dr2
        cy_ = col_y + 60
        draw.ellipse([cx_-dr2, cy_-dr2, cx_+dr2, cy_+dr2], fill=c)
        draw.ellipse([cx_-dr2, cy_-dr2, cx_+dr2, cy_+dr2], outline=GOLD, width=1)
        nw, _ = tw(draw, n, fnt('regular', 11))
        draw.text((cx_-nw//2, cy_+dr2+6), n, font=fnt('regular', 11), fill=WARM_G)

    # Concept text
    conc_y = col_y + 145
    draw.text((M, conc_y), "CONCEPT", font=fnt('bold', 18), fill=GOLD)
    rule(draw, conc_y + 28, x1=W//2-20, lw=1)
    for i, line in enumerate(concept_lines[:6]):
        draw.text((M, conc_y + 44 + i*32), line, font=fnt('light', 17), fill=IVORY)

    # Elements list
    elem_y = conc_y + 44 + len(concept_lines[:6])*32 + 28
    draw.text((M, elem_y), "ÉLÉMENTS CLÉS", font=fnt('bold', 18), fill=GOLD)
    rule(draw, elem_y+28, x1=W//2-20, lw=1)
    for i, elem in enumerate(elements[:7]):
        ey = elem_y + 44 + i*34
        draw.ellipse([M, ey+7, M+8, ey+15], fill=GOLD)
        draw.text((M+18, ey), elem, font=fnt('light', 17), fill=IVORY)

    # ── RIGHT COLUMN: FLOOR PLAN ──────────────────────────────────────────────
    plan_x = W//2 + 10
    plan_y = col_y
    plan_w = W - plan_x - M
    plan_h = H - 280 - col_y

    draw.text((plan_x, plan_y), "PLAN DE ZONE", font=fnt('bold', 18), fill=GOLD)
    rule(draw, plan_y+28, x0=plan_x, lw=1)

    # Plan card
    card_y = plan_y + 42
    card_h = plan_h - 42
    draw.rounded_rectangle([plan_x, card_y, plan_x+plan_w, card_y+card_h],
                           radius=12, fill=NAVY2, outline=GOLD, width=1)

    # Floor plan sketch inside card
    sketch_zone(draw, zone_id, plan_x+28, card_y+28, plan_w-56, card_h-56)

    # Zone area label
    arew, _ = tw(draw, zone_area, fnt('bold', 16))
    draw.text((plan_x+plan_w-arew-12, card_y+card_h-30), zone_area,
              font=fnt('bold', 16), fill=GOLD)

    # ── ARABIC CALLIGRAPHY BAND ───────────────────────────────────────────────
    calli_y = H - 240
    draw.rectangle([0, calli_y, W, calli_y+148], fill=NAVY2)
    draw.line([(0, calli_y), (W, calli_y)], fill=GOLD, width=2)
    draw.line([(0, calli_y+148), (W, calli_y+148)], fill=GOLD, width=2)

    ar_text = ar(arabic_phrase)
    ar_font = fnt('arabic', 64)
    ar_w, ar_h2 = tw(draw, ar_text, ar_font)
    draw.text(((W-ar_w)//2, calli_y+18), ar_text, font=ar_font, fill=GOLD)

    trans_w, _ = tw(draw, arabic_trans, fnt('italic', 16))
    draw.text(((W-trans_w)//2, calli_y+102), arabic_trans, font=fnt('italic', 16), fill=WARM_G)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    draw.line([(0, H-68), (W, H-68)], fill=GOLD, width=3)
    footer = f"AL-MAKTABA  ·  ZONE {zone_id}  ·  {zone_name}  ·  {zone_area}  ·  NORD RIYAD"
    ftw, _ = tw(draw, footer, fnt('light', 14))
    draw.text(((W-ftw)//2, H-50), footer, font=fnt('light', 14), fill=WARM_G)

    return canvas

# ── GENERATE ALL PAGES ────────────────────────────────────────────────────────

print("Generating cover...", end=' ', flush=True)
cover = page_cover()
print("✓")

print("Generating Zone A — Réception...", end=' ', flush=True)
zone_a = page_zone(
    pnum=2, zone_id='A',
    zone_name="RÉCEPTION",
    zone_area="35 m²",
    zone_col=GOLD,
    hero_fn=tex_marble_cream,
    hero_label="Marbre Calacatta",
    hero_sub="Sol & comptoir  ·  Finition polie",
    swatches=[
        (tex_wood_dark,  20, "Noyer Massif",    "Bureau d'accueil — incurvé"),
        (tex_brass,      21, "Laiton Brossé",   "Incrustations & quincaillerie"),
        (tex_sage_plaster,22,"Tadelakt Sauge",  "Mur d'accent — panneau arrière"),
    ],
    palette=[
        (CREAM,  "MARBRE"), (WALNUT, "NOYER"), (BRASS, "LAITON"),
        (SAGE,   "SAUGE"), (NAVY2,  "NAVY"),
    ],
    concept_lines=[
        "Une entrée au caractère affirmé,",
        "entre raffinement arabesque et",
        "hospitalité contemporaine.",
        "Le marbre Calacatta habille le sol",
        "et le comptoir en arc de cercle",
        "en noyer massif avec laiton.",
    ],
    elements=[
        "Comptoir incurvé noyer & marbre",
        "Panneau calligraphie rétroéclairé",
        "Olivier naturel en pot laiton",
        "Lanterne suspendue grand format",
        "Sol marbre Calacatta 60×60",
        "Assises lounge en velours ivoire",
        "Signalétique bilingue AR / FR",
    ],
    arabic_phrase="أهلاً وسهلاً — مرحباً بكم",
    arabic_trans="«  Bienvenue — Soyez les bienvenus  »",
)
print("✓")

print("Generating Zone B — Café Maktaba...", end=' ', flush=True)
zone_b = page_zone(
    pnum=3, zone_id='B',
    zone_name="CAFÉ MAKTABA",
    zone_area="40 m²",
    zone_col=TERRA,
    hero_fn=tex_zellige,
    hero_label="Zellige Terracotta",
    hero_sub="Mur principal  ·  Carreaux émaillés fait-main",
    swatches=[
        (tex_wood_dark,   30, "Noyer Foncé",      "Rayonnages bibliothèque sol/plafond"),
        (tex_marble_cream,31, "Marbre Blanc",      "Comptoir espresso — plan de travail"),
        (tex_brass,       32, "Laiton Antique",    "Luminaires suspendus & robinetterie"),
    ],
    palette=[
        (TERRA,  "TERRACOTTA"), (WALNUT, "NOYER"), (CREAM, "MARBRE"),
        (BRASS,  "LAITON"), (CHARCOAL,"ANTHRACITE"),
    ],
    concept_lines=[
        "Un café-librairie à l'atmosphère",
        "chaleureuse, inspiré des riad",
        "marocains et des maktabas",
        "traditionnelles. Zellige, noyer",
        "et laiton créent un intérieur",
        "à la fois intime et stimulant.",
    ],
    elements=[
        "Bibliothèques du sol au plafond",
        "Zellige terracotta fait-main",
        "Machine espresso La Marzocco",
        "Comptoir marbre blanc & bois",
        "Lanternes laiton suspendues",
        "Tables basses en chêne foncé",
        "Coussins majlis au sol",
    ],
    arabic_phrase="مكتبة القهوة — مساحة للقراءة والحوار",
    arabic_trans="«  La bibliothèque du café — espace lecture et dialogue  »",
)
print("✓")

print("Generating Zone C — Salle de Cours...", end=' ', flush=True)
zone_c = page_zone(
    pnum=4, zone_id='C',
    zone_name="SALLE DE COURS",
    zone_area="55 m²",
    zone_col=SAGE,
    hero_fn=tex_sage_plaster,
    hero_label="Tadelakt Sauge",
    hero_sub="Panneaux acoustiques  ·  Finition enduit perforé",
    swatches=[
        (tex_wood_light,  40, "Chêne Clair",       "Parquet flottant — structure tables"),
        (tex_concrete,    41, "Béton Ciré",         "Allège & sol couloir central"),
        (tex_navy_fabric, 42, "Tissu Navy",         "Sièges ergonomiques rembourrés"),
    ],
    palette=[
        (SAGE,   "SAUGE"), (WALNUT, "CHÊNE"), (NAVY2, "NAVY"),
        (IVORY,  "IVOIRE"), (GOLD,  "LAITON"),
    ],
    concept_lines=[
        "Un espace pédagogique modulable,",
        "pensé pour la concentration et",
        "l'interactivité. Les panneaux",
        "acoustiques en tadelakt sauge",
        "absorbent le son tout en créant",
        "une identité visuelle forte.",
    ],
    elements=[
        "SMART Board 86\" Samsung Flip",
        "Tables modulables en U ou rangées",
        "Panneaux acoustiques perforés sauge",
        "Cloison en mashrabiya (lattice bois)",
        "Pendants linéaires LED 4000K",
        "Prises USB intégrées aux tables",
        "Projecteur 4K de secours",
    ],
    arabic_phrase="تعلّم اللغة — انفتاح على الثقافة",
    arabic_trans="«  Apprendre la langue — s'ouvrir à la culture  »",
)
print("✓")

print("Generating Zone D — Semi-Privé...", end=' ', flush=True)
zone_d = page_zone(
    pnum=5, zone_id='D',
    zone_name="SEMI-PRIVÉ",
    zone_area="30 m²",
    zone_col=BRASS,
    hero_fn=tex_navy_fabric,
    hero_label="Tissu Navy / Bouclé",
    hero_sub="Mur d'accent  ·  Motif géométrique doré",
    swatches=[
        (tex_wood_dark,   50, "Noyer Massif",       "Table ronde centrale — 120 cm Ø"),
        (tex_zellige,     51, "Zellige Terracotta",  "Détails accent — niche et étagères"),
        (tex_stone_beige, 52, "Pierre de Riyad",    "Sol dalle calcaire 80×80"),
    ],
    palette=[
        (NAVY2,  "NAVY"), (GOLD,   "OR"), (TERRA, "TERRACOTTA"),
        (WALNUT, "NOYER"), (IVORY, "IVOIRE"),
    ],
    concept_lines=[
        "Un salon de réunion intime pour",
        "sessions privées, tutorats ou",
        "rencontres corporate. Navy profond,",
        "géométries dorées et calligraphie",
        "Amiri créent une atmosphère de",
        "prestige à la saoudienne.",
    ],
    elements=[
        "Table ronde noyer Ø 120 cm",
        "4 fauteuils terracotta rivets laiton",
        "Mur navy + motif géométrique doré",
        "Calligraphie Amiri encadrée",
        "Lanterne hexagonale laiton grand Ø",
        "Rideaux lin ivoire sol au plafond",
        "Éclairage tamisé variateur",
    ],
    arabic_phrase="مجلس الحوار — فضاء للتفكير والإبداع",
    arabic_trans="«  Le salon du dialogue — espace de réflexion et de création  »",
)
print("✓")

# ── SAVE OUTPUT ───────────────────────────────────────────────────────────────
pages = [cover, zone_a, zone_b, zone_c, zone_d]

print("\nSaving individual PNGs...", end=' ', flush=True)
names = ['Cover', 'Reception', 'Cafe', 'Classroom', 'SemiPrive']
for name, img in zip(names, pages):
    img.save(f'/home/user/ABD-BND/board_{name}.png', quality=95)
print("✓")

print("Saving PDF...", end=' ', flush=True)
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import io

with PdfPages(OUT) as pdf:
    for img in pages:
        fig = plt.figure(figsize=(8.27, 11.69), dpi=200)
        fig.patch.set_facecolor('#0D1B2A')
        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        import matplotlib.image as mpimg
        arr = mpimg.imread(buf)
        ax.imshow(arr, aspect='auto', extent=[0, 1, 0, 1], origin='upper')
        pdf.savefig(fig, bbox_inches='tight', dpi=200)
        plt.close(fig)
print(f"✓\n\nDone → {OUT}")
