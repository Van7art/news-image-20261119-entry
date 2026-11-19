#!/usr/bin/env python3
"""Builder for news-image-20261119: three 1024x1024 variants, PIL only.

Stories (verified news of Thursday 19 November 2026):
 1 GTA VI global rollout begins, back to Vice City after 13 years
 2 Democrats nominate Hakeem Jeffries, set to become first Black Speaker
 3 Pew: Islam set to become world's largest religion by 2035
 4 US and Iran exchange fire again; Gulf states hit; US struck Qeshm 17 Nov
 5 Trump arrives in China; Trump-Xi-Putin trilateral talks in Shenzhen (APEC)
 6 Nvidia: founder Jensen Huang resigned; acting CEO Colette Kress; no more H-series chips to China
 7 Fed minutes (27-28 Oct): most officials expect further rate hikes
 8 EU proposes EUR 45bn loan for Ukraine, repaid after Russia pays reparations
 9 Cyclone Akvan intensifies over Bay of Bengal, heading for Andhra Pradesh (~20 Nov landfall)
10 NASA Voyager 1 reaches one light-day from Earth, nearly 50 years in space
11 India beat Pakistan 2-1 to win SAFF Championship final in Dhaka
12 Amazon announces $7bn renewable-energy investment in India by 2030
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (247, 241, 227)
PAPER2 = (242, 234, 214)
INK = (26, 26, 26)
RED = (176, 58, 44)
RED_D = (140, 44, 34)
NAVY = (31, 58, 95)
NAVY_D = (22, 42, 72)
GOLD = (201, 162, 39)
GREY = (96, 90, 78)
LINE = (60, 55, 45)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, width, fill=INK, leading=None):
    lh = leading or int(font.size * 1.28)
    for ln in wrap(d, text, font, width):
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def headline(d, x, y, text, font, width, fill=INK, max_lines=3, leading=None):
    lh = leading or int(font.size * 1.15)
    lines = wrap(d, text, font, width)[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += lh
    return y


def rule(d, x0, y, x1, w=2, fill=INK):
    d.line([(x0, y), (x1, y)], fill=fill, width=w)


def masthead(d, date="THURSDAY  19  NOVEMBER  2026", size=72, y0=26):
    f = F(SERIF, size)
    t = "THE DAILY GLOBE"
    tw = d.textlength(t, font=f)
    d.text(((W - tw) / 2, y0), t, font=f, fill=INK)
    y = y0 + size + 16
    rule(d, 36, y, W - 36, 3)
    y += 12
    f2 = F(SANS_B, 25)
    t2 = date
    tw = d.textlength(t2, font=f2)
    d.text(((W - tw) / 2, y), t2, font=f2, fill=RED)
    y += 36
    f3 = F(SANS, 16)
    t3 = "ONE DAY  ·  ONE PAGE  ·  THE WORLD"
    tw = d.textlength(t3, font=f3)
    d.text(((W - tw) / 2, y), t3, font=f3, fill=GREY)
    y += 26
    rule(d, 36, y, W - 36, 1)
    return y + 10


def footer_sources(d, y=990):
    f = F(SANS, 12)
    t = ("Sources: AP · Reuters · Pew Research · NASA · IMD · SAFF  |  "
         "Illustrations drawn for this page; headlines as reported on 19 November 2026.")
    tw = d.textlength(t, font=f)
    d.text(((W - tw) / 2, y), t, font=f, fill=GREY)


def num_badge(d, cx, cy, n, r=17, fill=RED):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=(255, 255, 255), width=2)
    f = F(SANS_B, 20 if r >= 17 else 16)
    t = str(n)
    tw = d.textlength(t, font=f)
    d.text((cx - tw / 2, cy - f.size / 2 - 2), t, font=f, fill=(255, 255, 255))


# ---------------------------------------------------------------- vice city scene
def vice_city_scene(d, x0, y0, x1, y1):
    """Sunset sky, sun, skyline, palms, water. All drawn shapes."""
    # sky gradient: deep orange -> pink -> pale gold
    bands = 60
    top = (214, 92, 44)
    mid = (232, 130, 84)
    bot = (248, 196, 120)
    for i in range(bands):
        t = i / (bands - 1)
        if t < 0.55:
            u = t / 0.55
            c = tuple(int(top[j] + (mid[j] - top[j]) * u) for j in range(3))
        else:
            u = (t - 0.55) / 0.45
            c = tuple(int(mid[j] + (bot[j] - mid[j]) * u) for j in range(3))
        yy0 = y0 + (y1 - y0) * i // bands
        yy1 = y0 + (y1 - y0) * (i + 1) // bands
        d.rectangle([x0, yy0, x1, yy1], fill=c)
    # sun
    cx, cy = (x0 + x1) // 2, y0 + int((y1 - y0) * 0.42)
    r = int((x1 - x0) * 0.13)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 140))
    d.ellipse([cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8], outline=(255, 214, 140), width=3)
    # skyline (dark purple silhouettes)
    horizon = y0 + int((y1 - y0) * 0.72)
    sky = (58, 32, 66)
    import random
    rnd = random.Random(1911)
    bx = x0 + 8
    while bx < x1 - 30:
        bw = rnd.randint(28, 62)
        bh = rnd.randint(int((y1 - y0) * 0.18), int((y1 - y0) * 0.48))
        by = horizon - bh
        d.rectangle([bx, by, bx + bw, horizon], fill=sky)
        # antenna on some
        if rnd.random() < 0.4:
            d.line([(bx + bw // 2, by), (bx + bw // 2, by - 18)], fill=sky, width=3)
        # lit windows
        for wy in range(by + 10, horizon - 8, 14):
            for wx in range(bx + 6, bx + bw - 6, 12):
                if rnd.random() < 0.35:
                    d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 205, 110))
        bx += bw + rnd.randint(2, 10)
    # water
    d.rectangle([x0, horizon, x1, y1], fill=(44, 62, 96))
    for i in range(14):
        yy = horizon + 6 + i * ((y1 - horizon) // 15)
        wlen = rnd.randint(30, 120)
        wx = rnd.randint(x0 + 10, x1 - 130)
        d.line([(wx, yy), (wx + wlen, yy)], fill=(255, 190, 120), width=2)
    # palm trees, left and right foreground
    for px, s in ((x0 + 34, 1.0), (x1 - 34, -1.0)):
        palm(d, px, y1 - 4, 120, s)
    d.rectangle([x0, y0, x1, y1], outline=LINE, width=2)


def palm(d, x, ybase, h, s=1.0):
    trunk = (52, 34, 44)
    # curved trunk: series of short segments
    pts = []
    for i in range(9):
        t = i / 8
        pts.append((x + s * int(26 * t * t), ybase - int(h * t)))
    d.line(pts, fill=trunk, width=9, joint="curve")
    tx, ty = pts[-1]
    # fronds
    for ang in (-70, -40, -12, 18, 48, 78):
        import math
        a = math.radians(ang)
        ex = tx + s * int(52 * math.cos(a))
        ey = ty + int(30 * math.sin(a)) - 12
        mx = tx + s * int(30 * math.cos(a))
        my = ty - 22 + int(10 * math.sin(a))
        d.line([(tx, ty), (mx, my), (ex, ey)], fill=(30, 90, 52), width=5, joint="curve")
    # coconuts
    d.ellipse([tx - 8, ty - 2, tx, ty + 6], fill=(90, 60, 30))
    d.ellipse([tx + 1, ty - 2, tx + 9, ty + 6], fill=(90, 60, 30))


def capitol_icon(d, x, y, w, h):
    """Tiny US Capitol dome in navy/red."""
    cx = x + w // 2
    d.rectangle([x, y + h - 8, x + w, y + h], fill=NAVY)
    for i in range(6):
        colx = x + 6 + i * ((w - 12) // 5)
        d.rectangle([colx, y + h // 2 + 6, colx + 5, y + h - 8], fill=NAVY)
    d.rectangle([x + 4, y + h // 2, x + w - 4, y + h // 2 + 6], fill=NAVY)
    d.pieslice([cx - w // 4, y, cx + w // 4, y + h // 2 + 8], 180, 360, fill=RED)
    d.rectangle([cx - 3, y - 8, cx + 3, y + 2], fill=RED)


def gulf_icon(d, x, y, w, h):
    """Sea, missile arcs and burst over the Gulf."""
    d.rectangle([x, y + h * 2 // 3, x + w, y + h], fill=(70, 110, 150))
    for i in range(3):
        d.arc([x + 6 + i * 8, y + 4, x + w - 6 - i * 8, y + h - 6], 200, 340, fill=RED, width=3)
    cx, cy = x + w // 2, y + h // 3
    for k in range(8):
        import math
        a = math.radians(k * 45)
        d.line([(cx, cy), (cx + int(16 * math.cos(a)), cy + int(16 * math.sin(a)))],
               fill=GOLD, width=3)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=GOLD)


# ---------------------------------------------------------------- V1: front-page grid
def build_v1():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    y = masthead(d)
    # --- lead panel: Vice City
    LX0, LX1, LY0, LY1 = 36, 648, y, 596
    vice_city_scene(d, LX0, LY0, LX1, LY0 + 218)
    yy = LY0 + 232
    d.text((LX0 + 12, yy), "LEAD  ·  ENTERTAINMENT", font=F(SANS_B, 15), fill=RED)
    yy += 24
    yy = headline(d, LX0 + 12, yy, "Vice City opens its doors",
                  F(SERIF, 34), LX1 - LX0 - 24, max_lines=1)
    yy += 4
    yy = para(d, LX0 + 12, yy,
              "Grand Theft Auto VI begins its global rollout today — gamers "
              "return to Vice City after a 13-year wait.",
              F(SANS, 17), LX1 - LX0 - 24)
    # --- right column: Jeffries + Iran
    RX0, RX1 = 664, 988
    # Jeffries
    d.rectangle([RX0, LY0, RX1, 392], outline=LINE, width=1)
    capitol_icon(d, RX0 + 14, LY0 + 8, 110, 56)
    d.text((RX0 + 138, LY0 + 12), "WASHINGTON", font=F(SANS_B, 15), fill=RED)
    yy = headline(d, RX0 + 14, LY0 + 72, "Democrats nominate Jeffries",
                  F(SERIF, 25), RX1 - RX0 - 28, max_lines=2)
    yy = para(d, RX0 + 14, yy + 2,
              "Set to become the first African-American Speaker of the House.",
              F(SANS, 14), RX1 - RX0 - 28)
    # Iran
    d.rectangle([RX0, 406, RX1, LY1], outline=LINE, width=1)
    gulf_icon(d, RX0 + 14, 414, 110, 52)
    d.text((RX0 + 138, 420), "THE GULF", font=F(SANS_B, 15), fill=RED)
    yy = headline(d, RX0 + 14, 474, "US and Iran exchange fire again",
                  F(SERIF, 25), RX1 - RX0 - 28, max_lines=2)
    yy = para(d, RX0 + 14, yy + 2,
              "Iran widens attacks on Gulf states, hitting a US base in Kuwait and Bahrain.",
              F(SANS, 14), RX1 - RX0 - 28)
    # --- middle grid: 6 stories, 3 cols x 2 rows
    rule(d, 36, 612, W - 36, 2)
    d.text((36, 622), "THE DAY IN BRIEF", font=F(SANS_B, 18), fill=RED)
    cells = [
        ("FAITH  ·  PEW RESEARCH", "Islam set to be world's largest faith by 2035",
         "Pew report projects the crossover within a decade."),
        ("CHINA  ·  APEC", "Trump arrives in China for Xi–Putin talks",
         "Trilateral meeting set for Shenzhen during the APEC summit."),
        ("TECH  ·  NVIDIA", "Nvidia founder Huang resigns",
         "Acting CEO Kress promises earlier pay rises; H-series chip sales to China halted."),
        ("ECONOMY  ·  THE FED", "Fed minutes point to more rate hikes",
         "Most officials at the 27–28 October meeting expect further tightening."),
        ("EUROPE  ·  UKRAINE", "EU proposes €45bn loan for Ukraine",
         "To be repaid after Russia pays reparations, Brussels says."),
        ("WEATHER  ·  BAY OF BENGAL", "Cyclone Akvan bears down on India",
         "Storm intensifies off Andhra Pradesh; landfall expected around 20 November."),
    ]
    cw = (W - 72 - 2 * 24) // 3
    for i, (kick, head, deck) in enumerate(cells):
        cx = 36 + (i % 3) * (cw + 24)
        cy = 652 + (i // 3) * 122
        d.text((cx, cy), kick, font=F(SANS_B, 13), fill=RED)
        yy = headline(d, cx, cy + 20, head, F(SERIF, 19), cw, max_lines=2)
        para(d, cx, yy + 2, deck, F(SANS, 14), cw)
    # --- footer: also today
    rule(d, 36, 906, W - 36, 2)
    d.text((36, 916), "ALSO TODAY", font=F(SANS_B, 18), fill=RED)
    also = [
        ("SPACE", "Voyager 1 reaches one light-day from Earth, nearly 50 years after launch."),
        ("SPORT", "India beat Pakistan 2–1 to win the SAFF Championship final in Dhaka."),
        ("BUSINESS", "Amazon pledges $7bn for renewable energy in India by 2030."),
    ]
    for i, (tag, txt) in enumerate(also):
        cx = 36 + i * (cw + 24)
        para(d, cx, 942, tag + " — " + txt, F(SANS, 14), cw)
    footer_sources(d, 996)
    return im


# ---------------------------------------------------------------- V2: world map + list
LONLAT = {
    "na": [(-168, 66), (-150, 70), (-130, 71), (-110, 72), (-95, 80), (-85, 73),
           (-80, 70), (-68, 62), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
           (-81, 26), (-84, 20), (-90, 14), (-95, 17), (-100, 22), (-108, 24),
           (-117, 33), (-124, 44), (-130, 55), (-150, 60), (-165, 60)],
    "greenland": [(-55, 60), (-44, 60), (-40, 64), (-32, 68), (-25, 70),
                  (-35, 76), (-55, 76), (-60, 70)],
    "sa": [(-80, 10), (-76, 4), (-70, 10), (-62, 6), (-52, 4), (-50, 0),
           (-42, -4), (-35, -9), (-39, -16), (-41, -23), (-48, -28),
           (-53, -34), (-58, -39), (-65, -45), (-69, -52), (-73, -55),
           (-74, -44), (-73, -34), (-72, -24), (-76, -16), (-80, -6)],
    "africa": [(-17, 15), (-12, 27), (-6, 33), (0, 36), (10, 37), (20, 32),
               (30, 31), (34, 28), (38, 20), (43, 12), (51, 11), (46, 5),
               (41, -2), (38, -10), (33, -18), (29, -26), (26, -33), (19, -35),
               (16, -29), (13, -18), (10, -6), (9, 3), (0, 5), (-8, 5), (-14, 10)],
    "eurasia": [(-10, 36), (-9, 43), (-2, 48), (-4, 50), (1, 51), (5, 53),
                (8, 57), (10, 59), (18, 56), (21, 55), (24, 58), (28, 60),
                (25, 65), (31, 69), (40, 68), (50, 69), (60, 69), (70, 72),
                (80, 73), (92, 75), (104, 77), (114, 74), (126, 72), (138, 71),
                (150, 70), (162, 69), (170, 66), (178, 65), (170, 60),
                (162, 56), (158, 52), (150, 59), (142, 56), (141, 46),
                (135, 42), (130, 35), (127, 38), (122, 32), (120, 26),
                (115, 22), (109, 18), (105, 9), (100, 7), (98, 12), (95, 16),
                (92, 21), (89, 22), (86, 19), (80, 13), (77, 8), (75, 14),
                (72, 20), (68, 22), (62, 25), (58, 25), (54, 27), (51, 29),
                (48, 29), (44, 29), (42, 27), (40, 22), (38, 20), (35, 28),
                (34, 31), (30, 36), (27, 37), (23, 36), (19, 40), (15, 44),
                (12, 44), (8, 39), (3, 38), (-2, 37)],
    "uk": [(-5, 50), (-3, 53), (-5, 56), (-2, 58), (0, 53), (1, 51)],
    "japan": [(130, 31), (132, 33), (135, 34), (138, 36), (140, 38), (141, 41), (143, 43), (141, 45)],
    "se_asia": [(100, 14), (103, 10), (105, 9), (107, 11), (109, 14), (106, 20), (104, 16), (101, 18)],
    "indonesia": [(95, 5), (100, 0), (106, -6), (112, -7), (118, -9), (122, -9), (128, -4), (132, -2), (138, -4), (140, -8), (132, -8), (124, -8), (118, -4), (112, -2), (104, -2), (98, 2)],
    "australia": [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32),
                  (130, -32), (135, -35), (140, -38), (146, -39), (150, -37),
                  (153, -32), (151, -26), (146, -19), (142, -14), (142, -11),
                  (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
                  (122, -17), (118, -20)],
    "nz": [(167, -45), (170, -42), (173, -40), (175, -38), (177, -38), (174, -41), (171, -43)],
}


def lonlat_to_xy(lon, lat, x0, y0, x1, y1):
    x = x0 + (lon + 170) / 360 * (x1 - x0)
    y = y0 + (78 - lat) / 136 * (y1 - y0)
    return (x, y)


def build_v2():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    y = masthead(d)
    MX0, MX1, MY0, MY1 = 36, 988, y, 528
    d.rectangle([MX0, MY0, MX1, MY1], fill=PAPER2, outline=LINE, width=1)
    # graticule
    for lon in range(-150, 181, 30):
        x = MX0 + (lon + 170) / 360 * (MX1 - MX0)
        d.line([(x, MY0), (x, MY1)], fill=(210, 200, 175), width=1)
    for lat in range(-45, 76, 30):
        yy = MY0 + (78 - lat) / 136 * (MY1 - MY0)
        d.line([(MX0, yy), (MX1, yy)], fill=(210, 200, 175), width=1)
    for pts in LONLAT.values():
        d.polygon([lonlat_to_xy(lo, la, MX0, MY0, MX1, MY1) for lo, la in pts], fill=NAVY)
    # pins: (n, lon, lat, label, badge_dx, badge_dy, label_dy)
    # badge_dx/dy shift the badge from its true geo point (leader line drawn);
    # label_dy is the label offset from the badge (negative = above).
    pins = [
        (1, -80, 25, "VICE CITY", 0, 0, 20),
        (2, -77, 39, "WASHINGTON", 52, -32, -30),
        (3, 52, 27, "THE GULF", 0, 0, 20),
        (4, 114, 22, "SHENZHEN", 0, 0, -32),
        (5, 88, 16, "BAY OF BENGAL", 0, 0, 20),
        (6, 4, 51, "BRUSSELS", 0, 0, -32),
    ]
    flab = F(SANS_B, 12)
    for n, lon, lat, lab, bdx, bdy, ldy in pins:
        px, py = lonlat_to_xy(lon, lat, MX0, MY0, MX1, MY1)
        bx, by = px + bdx, py + bdy
        if bdx or bdy:
            d.line([(px, py), (bx, by)], fill=RED_D, width=2)
            d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED_D)
        num_badge(d, bx, by, n, r=16)
        tw = d.textlength(lab, font=flab)
        lx = min(max(bx - tw / 2, MX0 + 4), MX1 - tw - 4)
        ly = by + ldy if ldy > 0 else by + ldy - 4
        # label backing so it stays legible over land
        d.rectangle([lx - 3, ly - 1, lx + tw + 3, ly + 15], fill=PAPER2)
        d.text((lx, ly), lab, font=flab, fill=RED_D)
    # --- story list
    y = MY1 + 14
    d.text((36, y), "WHERE THE DAY HAPPENED", font=F(SANS_B, 20), fill=RED)
    stories = [
        (1, "VICE CITY  ·  ENTERTAINMENT",
         "GTA VI begins its global rollout",
         "Gamers return to Vice City after a 13-year wait."),
        (2, "WASHINGTON  ·  POLITICS",
         "Democrats nominate Jeffries for Speaker",
         "Set to become the first African-American Speaker of the US House."),
        (3, "THE GULF  ·  CONFLICT",
         "US and Iran exchange fire again",
         "Iran hits a US base in Kuwait and strikes Bahrain; US struck Qeshm on the 17th."),
        (4, "SHENZHEN  ·  APEC",
         "Trump arrives in China for trilateral talks",
         "Trump, Xi and Putin to meet in Shenzhen during the APEC summit."),
        (5, "BAY OF BENGAL  ·  WEATHER",
         "Cyclone Akvan bears down on India",
         "Storm intensifies off Andhra Pradesh; landfall expected around 20 November."),
        (6, "WORLD  ·  FAITH",
         "Islam set to be the largest faith by 2035",
         "Pew Research projects the crossover within a decade."),
    ]
    cw = (W - 72 - 40) // 2
    for i, (n, kick, head, deck) in enumerate(stories):
        cx = 36 + (i % 2) * (cw + 40)
        cy = y + 30 + (i // 2) * 86
        num_badge(d, cx + 17, cy + 16, n, r=17)
        d.text((cx + 44, cy), kick, font=F(SANS_B, 13), fill=RED)
        yy = headline(d, cx + 44, cy + 19, head, F(SERIF, 20), cw - 44, max_lines=1)
        para(d, cx + 44, yy + 2, deck, F(SANS, 14), cw - 44)
    # --- also today: 6 items, 3 cols x 2 rows
    ay = y + 30 + 3 * 86 + 6
    rule(d, 36, ay, W - 36, 2)
    d.text((36, ay + 10), "ALSO TODAY", font=F(SANS_B, 18), fill=RED)
    also = [
        ("NVIDIA", "Founder Huang resigns; Kress is acting CEO; H-series sales to China halted."),
        ("THE FED", "Minutes from 27–28 Oct: most officials expect further rate hikes."),
        ("UKRAINE", "EU proposes €45bn loan, repaid after Russia pays reparations."),
        ("SPACE", "Voyager 1 reaches one light-day from Earth, nearly 50 years on."),
        ("SPORT", "India beat Pakistan 2–1 to win the SAFF final in Dhaka."),
        ("BUSINESS", "Amazon pledges $7bn for renewable energy in India by 2030."),
    ]
    acw = (W - 72 - 2 * 24) // 3
    for i, (tag, txt) in enumerate(also):
        cx = 36 + (i % 3) * (acw + 24)
        cy = ay + 40 + (i // 3) * 56
        d.text((cx, cy), tag + " — ", font=F(SANS_B, 14), fill=NAVY)
        tw = d.textlength(tag + " — ", font=F(SANS_B, 14))
        para(d, cx + tw, cy, txt, F(SANS, 14), acw - tw)
    footer_sources(d, 992)
    return im


# ---------------------------------------------------------------- V3: magazine cover
def build_v3():
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    # masthead band
    f = F(SERIF, 62)
    t = "THE DAILY GLOBE"
    tw = d.textlength(t, font=f)
    d.text(((W - tw) / 2, 22), t, font=f, fill=INK)
    f2 = F(SANS_B, 22)
    t2 = "THURSDAY  19  NOVEMBER  2026"
    tw = d.textlength(t2, font=f2)
    d.text(((W - tw) / 2, 96), t2, font=f2, fill=RED)
    rule(d, 36, 132, W - 36, 2)
    # hero scene
    HX0, HX1, HY0, HY1 = 36, 988, 144, 636
    vice_city_scene(d, HX0, HY0, HX1, HY1)
    # headline overlay: dark band across the sky for legibility
    d.rectangle([HX0, HY0 + 8, HX1, HY0 + 118], fill=(26, 20, 34))
    d.text((HX0 + 24, HY0 + 16), "GRAND THEFT AUTO VI  ·  THE WAIT IS OVER",
           font=F(SANS_B, 21), fill=(255, 205, 110))
    fbig = F(SERIF, 96)
    t = "VICE CITY"
    tw = d.textlength(t, font=fbig)
    d.text(((W - tw) / 2, HY0 + 40), t, font=fbig, fill=(255, 255, 255))
    # deck strip at bottom of hero
    d.rectangle([HX0, HY1 - 52, HX1, HY1], fill=(26, 20, 34))
    fdeck = F(SANS, 19)
    t = "After 13 years, the global rollout begins — gamers are going home."
    tw = d.textlength(t, font=fdeck)
    d.text(((W - tw) / 2, HY1 - 40), t, font=fdeck, fill=(255, 235, 200))
    # bottom navy band: the rest of the day
    BY0, BY1 = 652, 972
    d.rectangle([36, BY0, 988, BY1], fill=NAVY_D)
    d.text((60, BY0 + 14), "THE REST OF THE DAY", font=F(SANS_B, 19), fill=(255, 205, 110))
    lines = [
        ("JEFFRIES", "Democrats nominate Jeffries — set to become the first Black Speaker of the US House."),
        ("THE GULF", "US and Iran exchange fire again — Gulf states hit, a US base in Kuwait struck."),
        ("SHENZHEN", "Trump arrives in China; trilateral talks with Xi and Putin at the APEC summit."),
        ("FAITH", "Pew: Islam set to become the world's largest religion by 2035."),
        ("CYCLONE AKVAN", "Storm intensifies over the Bay of Bengal, heading for Andhra Pradesh."),
    ]
    yy = BY0 + 50
    for tag, txt in lines:
        d.text((60, yy), tag, font=F(SANS_B, 17), fill=(255, 205, 110))
        tw = d.textlength(tag, font=F(SANS_B, 17))
        para(d, 60 + tw + 16, yy, txt, F(SANS, 17), 988 - 60 - tw - 16 - 24,
             fill=(240, 240, 235))
        yy += 38
    rule(d, 60, yy + 8, 964, 1, fill=(120, 140, 170))
    yy += 20
    ticker = ("ALSO:  Nvidia founder Huang resigns  ·  Fed signals more rate hikes  ·  "
              "EU proposes €45bn Ukraine loan  ·  Voyager 1 one light-day out  ·  "
              "India win SAFF final 2–1  ·  Amazon $7bn India green pledge")
    yy = para(d, 60, yy, ticker, F(SANS, 15), 988 - 120, fill=(200, 210, 225))
    footer_sources(d, 984)
    return im


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "."
    build_v1().save(f"{out}/variant-v1.png")
    build_v2().save(f"{out}/variant-v2.png")
    build_v3().save(f"{out}/variant-v3.png")
    print("built 3 variants")
