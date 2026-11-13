#!/usr/bin/env python3
"""Draw 'Kitten and Yarn' — an original warm, joyful image, entirely in code.

A cute orange tabby kitten bats at a ball of red yarn in warm golden light,
little hearts floating, cozy rug and sunbeams. 1024x1024 PNG.
"""
import math
from PIL import Image, ImageDraw, ImageFilter

W = H = 1024
img = Image.new("RGB", (W, H), (255, 214, 140))
d = ImageDraw.Draw(img, "RGBA")

# ---- warm golden sky gradient ----
for y in range(H):
    t = y / H
    r = int(255 - 18 * t)
    g = int(214 - 52 * t)
    b = int(140 - 40 * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# ---- soft sun glow, top right ----
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for r, a in [(330, 26), (260, 38), (190, 52), (120, 70)]:
    gd.ellipse([830 - r, 150 - r, 830 + r, 150 + r], fill=(255, 240, 180, a))
img = Image.alpha_composite(img.convert("RGBA"), glow)
d = ImageDraw.Draw(img, "RGBA")

# ---- sunbeams ----
for ang in range(-70, 71, 14):
    rad = math.radians(ang - 90)
    x2 = 830 + 1200 * math.cos(rad)
    y2 = 150 + 1200 * math.sin(rad)
    d.polygon([(830, 150), (830 + 26 * math.cos(rad + 0.03), 150 + 26 * math.sin(rad + 0.03)),
               (x2, y2)], fill=(255, 246, 200, 34))

# ---- sun disc with a smile ----
d.ellipse([760, 80, 900, 220], fill=(255, 226, 110))
d.ellipse([760, 80, 900, 220], outline=(240, 180, 60), width=5)
d.arc([800, 140, 860, 180], 20, 160, fill=(150, 90, 20), width=5)
d.ellipse([792, 122, 806, 136], fill=(150, 90, 20))
d.ellipse([844, 122, 858, 136], fill=(150, 90, 20))
d.ellipse([772, 140, 792, 152], fill=(255, 150, 120, 180))
d.ellipse([858, 140, 878, 152], fill=(255, 150, 120, 180))

# ---- soft clouds ----
def cloud(cx, cy, s):
    for ox, oy, r in [(-70, 10, 42), (-20, -18, 55), (35, 5, 48), (80, 14, 36)]:
        d.ellipse([cx + ox * s - r * s, cy + oy * s - r * s,
                   cx + ox * s + r * s, cy + oy * s + r * s],
                  fill=(255, 250, 235, 225))

cloud(180, 210, 1.0)
cloud(560, 110, 0.8)
cloud(120, 430, 0.7)

# ---- floor / cozy rug ----
d.rectangle([0, 760, W, H], fill=(196, 128, 74))
d.rectangle([0, 760, W, 772], fill=(170, 100, 55))
# rug
d.rounded_rectangle([110, 800, 914, 1010], radius=60, fill=(232, 84, 96))
d.rounded_rectangle([140, 826, 884, 984], radius=46, fill=(255, 214, 140))
d.rounded_rectangle([170, 852, 854, 958], radius=34, fill=(232, 84, 96))
# rug fringe
for x in range(150, 880, 30):
    d.line([(x, 1010), (x, 1024)], fill=(255, 214, 140), width=6)
    d.line([(x, 800), (x, 786)], fill=(255, 214, 140), width=6)

# ---- little flowers on the grass strip ----
for cx in (60, 950, 990, 30):
    for petal in range(6):
        a = petal * math.pi / 3
        px, py = cx + 14 * math.cos(a), 745 + 14 * math.sin(a)
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(255, 255, 255))
    d.ellipse([cx - 8, 737, cx + 8, 753], fill=(255, 200, 40))

# ---- yarn ball (red) with loose curls ----
ball_cx, ball_cy, ball_r = 700, 800, 88
# loose yarn curls trailing from the ball
for pts, col in [
    ([(700, 850), (640, 900), (560, 880), (500, 930)], (214, 48, 70)),
    ([(700, 860), (760, 920), (830, 890), (880, 940)], (214, 48, 70)),
]:
    d.line(pts, fill=col, width=9, joint="curve")
d.ellipse([ball_cx - ball_r, ball_cy - ball_r, ball_cx + ball_r, ball_cy + ball_r],
          fill=(232, 60, 80), outline=(170, 25, 45), width=4)
# yarn wraps, clipped to the ball circle so nothing spills outside it
wrap_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
wd = ImageDraw.Draw(wrap_layer)
wd.ellipse([ball_cx - ball_r, ball_cy - ball_r, ball_cx + ball_r, ball_cy + ball_r],
           fill=(232, 60, 80, 255))
for k in range(-3, 4):
    wd.arc([ball_cx - ball_r + 6, ball_cy - ball_r + 6 + k * 22,
            ball_cx + ball_r - 6, ball_cy + ball_r - 6 + k * 22],
           200, 340, fill=(255, 120, 130, 255), width=7)
    wd.arc([ball_cx - ball_r + 6, ball_cy - ball_r + 6 + k * 22,
            ball_cx + ball_r - 6, ball_cy + ball_r - 6 + k * 22],
           20, 160, fill=(170, 25, 45, 255), width=7)
mask = Image.new("L", (W, H), 0)
md = ImageDraw.Draw(mask)
md.ellipse([ball_cx - ball_r, ball_cy - ball_r, ball_cx + ball_r, ball_cy + ball_r], fill=255)
img = Image.composite(wrap_layer, img.convert("RGBA"), mask)
d = ImageDraw.Draw(img, "RGBA")
d.ellipse([ball_cx - 62, ball_cy - 66, ball_cx - 8, ball_cy - 12],
          fill=(255, 150, 160, 160))

# ---- kitten ----
# tail (curled, behind body) — smooth tapered curve with stripe bands
tail_pts = [(330, 700), (220, 640), (170, 560), (190, 470)]
d.line(tail_pts, fill=(255, 170, 80), width=44, joint="curve")
for (tx, ty, a) in [(232, 655, -40), (185, 585, -75), (183, 515, -100)]:
    d.arc([tx - 34, ty - 34, tx + 34, ty + 34], a, a + 110, fill=(235, 120, 40), width=12)
d.ellipse([168, 448, 214, 494], fill=(255, 170, 80))  # rounded tail tip
d.ellipse([168, 448, 214, 494], outline=(230, 140, 55), width=3)

# body (sitting, plump)
d.ellipse([250, 560, 560, 880], fill=(255, 178, 92))
d.ellipse([250, 560, 560, 880], outline=(230, 140, 55), width=4)
# belly patch
d.ellipse([330, 640, 500, 880], fill=(255, 226, 180))
# back stripes
for y0 in (600, 650, 700):
    d.arc([270, y0 - 40, 470, y0 + 60], 200, 340, fill=(235, 140, 50), width=10)

# hind paw
d.ellipse([270, 820, 360, 880], fill=(255, 178, 92))
d.ellipse([270, 820, 360, 880], outline=(230, 140, 55), width=3)
# front leg reaching toward the yarn (right paw extended)
d.line([(540, 700), (640, 760), (668, 782)], fill=(255, 178, 92), width=46, joint="curve")
d.ellipse([640, 750, 700, 810], fill=(255, 178, 92), outline=(230, 140, 55), width=3)
# toe beans on the reaching paw
for dx, dy in [(0, 0), (14, 8), (-2, 14)]:
    d.ellipse([668 + dx - 6, 782 + dy - 6, 668 + dx + 6, 782 + dy + 6], fill=(255, 150, 160))
# other front paw resting
d.ellipse([470, 830, 540, 880], fill=(255, 178, 92), outline=(230, 140, 55), width=3)

# head
hx, hy = 405, 470
d.ellipse([hx - 135, hy - 125, hx + 135, hy + 125], fill=(255, 186, 100))
d.ellipse([hx - 135, hy - 125, hx + 135, hy + 125], outline=(230, 140, 55), width=4)
# ears
d.polygon([(hx - 118, hy - 80), (hx - 150, hy - 215), (hx - 45, hy - 125)], fill=(255, 186, 100))
d.polygon([(hx - 118, hy - 80), (hx - 150, hy - 215), (hx - 45, hy - 125)], outline=(230, 140, 55), width=4)
d.polygon([(hx - 105, hy - 95), (hx - 128, hy - 180), (hx - 62, hy - 118)], fill=(255, 160, 175))
d.polygon([(hx + 118, hy - 80), (hx + 150, hy - 215), (hx + 45, hy - 125)], fill=(255, 186, 100))
d.polygon([(hx + 118, hy - 80), (hx + 150, hy - 215), (hx + 45, hy - 125)], outline=(230, 140, 55), width=4)
d.polygon([(hx + 105, hy - 95), (hx + 128, hy - 180), (hx + 62, hy - 118)], fill=(255, 160, 175))
# head stripes
for x0 in (hx - 55, hx - 18, hx + 18):
    d.line([(x0, hy - 122), (x0 + 12, hy - 88)], fill=(235, 140, 50), width=9)
# cheeks
d.ellipse([hx - 118, hy + 18, hx - 62, hy + 58], fill=(255, 190, 190, 170))
d.ellipse([hx + 62, hy + 18, hx + 118, hy + 58], fill=(255, 190, 190, 170))

# big eyes (green, sparkling)
for ex in (hx - 58, hx + 58):
    d.ellipse([ex - 34, hy - 42, ex + 34, hy + 34], fill=(255, 255, 255))
    d.ellipse([ex - 26, hy - 34, ex + 26, hy + 26], fill=(90, 160, 80))
    d.ellipse([ex - 12, hy - 20, ex + 12, hy + 20], fill=(30, 40, 30))
    d.ellipse([ex - 18, hy - 30, ex - 2, hy - 14], fill=(255, 255, 255))
    d.ellipse([ex + 8, hy + 6, ex + 16, hy + 14], fill=(255, 255, 255, 220))
# happy closed-eye lashes above
d.arc([hx - 92, hy - 78, hx - 24, hy - 10], 180, 360, fill=(120, 70, 30), width=4)
d.arc([hx + 24, hy - 78, hx + 92, hy - 10], 180, 360, fill=(120, 70, 30), width=4)
# nose + mouth (joyful open smile)
d.polygon([(hx - 18, hy + 52), (hx + 18, hy + 52), (hx, hy + 74)], fill=(235, 90, 110))
d.arc([hx - 46, hy + 66, hx, hy + 112], 0, 180, fill=(120, 70, 30), width=5)
d.arc([hx, hy + 66, hx + 46, hy + 112], 0, 180, fill=(120, 70, 30), width=5)
# whiskers
for sx, sy, ex, ey in [(-120, 40, -200, 18), (-120, 58, -198, 62), (-120, 74, -190, 104),
                       (120, 40, 200, 18), (120, 58, 198, 62), (120, 74, 190, 104)]:
    d.line([(hx + sx, hy + sy), (hx + ex, hy + ey)], fill=(90, 60, 30), width=3)

# ---- floating hearts ----
def heart(cx, cy, s, col):
    pts = []
    for t in range(0, 101):
        a = 2 * math.pi * t / 100
        x = 16 * math.sin(a) ** 3
        y = 13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)
        pts.append((cx + x * s, cy - y * s))
    d.polygon(pts, fill=col)

heart(180, 340, 2.6, (255, 90, 120))
heart(620, 300, 2.0, (255, 120, 150))
heart(880, 420, 2.2, (255, 90, 120))
heart(120, 560, 1.6, (255, 140, 165))
heart(920, 600, 1.8, (255, 110, 140))
heart(540, 210, 1.4, (255, 150, 175))
# sparkles
for cx, cy, s in [(250, 480, 14), (760, 500, 12), (480, 330, 10), (330, 250, 12)]:
    d.polygon([(cx, cy - s), (cx + 4, cy - 4), (cx + s, cy), (cx + 4, cy + 4),
               (cx, cy + s), (cx - 4, cy + 4), (cx - s, cy), (cx - 4, cy - 4)],
              fill=(255, 250, 200))

# ---- soft vignette for warmth ----
vig = Image.new("L", (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-220, -220, W + 220, H + 220], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(140))
warm = Image.new("RGBA", (W, H), (255, 190, 90, 0))
img = Image.composite(img.convert("RGBA"), Image.blend(img.convert("RGBA"), warm, 0.18), vig)

img.convert("RGB").save("entry.png", optimize=True)
print("saved entry.png")
