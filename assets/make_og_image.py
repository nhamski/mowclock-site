from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#2d6a4f")
draw = ImageDraw.Draw(img)

# Diagonal-ish gradient: top-left darker green -> bottom-right lighter green
top_left = (27, 67, 50)      # #1b4332
bottom_right = (64, 145, 108)  # #40916c
for y in range(H):
    for_x_ratio = y / H
    r = int(top_left[0] + (bottom_right[0] - top_left[0]) * for_x_ratio)
    g = int(top_left[1] + (bottom_right[1] - top_left[1]) * for_x_ratio)
    b = int(top_left[2] + (bottom_right[2] - top_left[2]) * for_x_ratio)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

FONT_DIR = r"C:\Windows\Fonts"

def load_font(names, size):
    for n in names:
        p = os.path.join(FONT_DIR, n)
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

serif_bold = load_font(["georgiab.ttf", "georgia.ttf"], 68)
sans_bold = load_font(["segoeuib.ttf", "arialbd.ttf"], 22)
sans_reg = load_font(["segoeui.ttf", "arial.ttf"], 27)
sans_bold_badge = load_font(["segoeuib.ttf", "arialbd.ttf"], 28)
sans_small = load_font(["segoeuisb.ttf", "segoeuib.ttf", "arialbd.ttf"], 20)

INK_LIGHT = (250, 246, 238)
WHITE = (255, 255, 255)
WASH = (216, 243, 220)

pad_x = 90

# Eyebrow
draw.text((pad_x, 66), "GPS TIME TRACKING FOR LAWN CARE & LANDSCAPING", font=sans_bold, fill=WASH)

# Headline (3 lines)
lines = ["Clock in.", "Get paid.", "Go home."]
y = 118
for line in lines:
    draw.text((pad_x, y), line, font=serif_bold, fill=WHITE)
    y += 82

# Subtitle
sub = "Geofenced time tracking built for solo field crews. Free to start."
draw.text((pad_x, y + 34), sub, font=sans_reg, fill=INK_LIGHT)

# Badge top-right
INK = (42, 33, 24)          # #2a2118
ACCENT = (45, 106, 79)      # #2d6a4f
badge_w, badge_h = 250, 62
bx, by = W - pad_x - badge_w, 56
draw.rounded_rectangle([bx, by, bx + badge_w, by + badge_h], radius=16, fill=INK_LIGHT)
leaf_size = 42
draw.rounded_rectangle([bx + 12, by + 10, bx + 12 + leaf_size, by + 10 + leaf_size], radius=10, fill=ACCENT)
try:
    emoji_font = ImageFont.truetype(os.path.join(FONT_DIR, "seguiemj.ttf"), 24)
    draw.text((bx + 21, by + 16), "\U0001F331", font=emoji_font, embedded_color=True)
except Exception:
    pass
draw.text((bx + 66, by + 17), "MowClock", font=sans_bold_badge, fill=INK)

# URL bottom-right
url_text = "mowclock.app"
bbox = draw.textbbox((0, 0), url_text, font=sans_small)
tw = bbox[2] - bbox[0]
draw.text((W - pad_x - tw, H - 74), url_text, font=sans_small, fill=WASH)

out_path = os.path.join(os.path.dirname(__file__), "og-image.png")
img.save(out_path, "PNG")
print("saved", out_path, img.size)
