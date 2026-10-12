# -*- coding: utf-8 -*-
"""Build Harvest Moon: Back to Nature custom alert + widgets for Sociabuzz."""
import re, shutil
from pathlib import Path

ROOT = Path(__file__).parent
DOWNLOADS = Path("C:/Users/NASRU/Downloads")
HELC = Path("D:/KUMPULAN TUGAS/helcurt-collector-alert/widgets")
BASE = "https://raw.githubusercontent.com/MasAjie12/harvest-moon-alert-assets/main"

# ── 1. PROCESS IMAGES ──────────────────────────────────────────────
shutil.copy2(DOWNLOADS / "bg.png", ROOT / "bg.png")
from PIL import Image, ImageOps
im = Image.open(DOWNLOADS / "baru.png").convert("RGBA")
pix = im.load()
for y in range(im.height):
    for x in range(im.width):
        r, g, b, a = pix[x, y]
        if r < 30 and g < 30 and b < 30:
            pix[x, y] = (r, g, b, 0)
im.save(ROOT / "baru.png")
ImageOps.mirror(im).save(ROOT / "baru-right.png")
print("Images processed: bg.png + baru.png + baru-right.png")

# ── 2. ALERT HTML + CSS (strict sanitizer-safe) ─────────────────────
ALERT_CSS = (
    "@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&display=swap');"
    ".hm-card{box-sizing:border-box;position:relative;width:680px;max-width:96%;height:230px;margin:0 auto;overflow:hidden;border:5px solid #80552f;border-radius:24px;background:#f9e7ae;color:#3d291c;font-family:'Baloo 2',sans-serif;text-align:center;box-shadow:0 12px 30px rgba(48,27,10,.55),inset 0 0 0 3px #eacb72;animation:hm-in .8s cubic-bezier(.2,.9,.3,1.15) both,hm-breathe 5s ease-in-out 1s infinite}"
    ".hm-bg{position:absolute;z-index:0;top:0;left:0;width:100%;height:100%;object-fit:cover;object-position:center;filter:saturate(1.12) brightness(.72);animation:hm-zoom 18s ease-in-out infinite alternate}"
    ".hm-veil{position:absolute;z-index:1;top:0;left:0;width:100%;height:100%;background:linear-gradient(90deg,rgba(61,41,28,.82),rgba(249,231,174,.3) 38%,rgba(249,231,174,.42) 62%,rgba(61,41,28,.78))}"
    ".hm-panel{position:relative;z-index:4;width:72%;min-width:0;padding:18px 12px 20px;margin:auto;border:3px solid #b47a3c;border-radius:18px;background:rgba(255,245,201,.91);box-shadow:0 5px 0 #6d4728,0 0 0 3px rgba(255,248,210,.8);animation:hm-panel .9s .1s both}"
    ".hm-amount{color:#a94e2c;font-size:38px;font-weight:800;line-height:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;text-shadow:0 2px #fbe9a8;animation:hm-pop .7s .2s both,hm-pulse 2.8s 1.2s ease-in-out infinite}"
    ".hm-from{color:#587b38;font-size:14px;font-weight:800;letter-spacing:1px;text-transform:uppercase}"
    ".hm-who{max-width:100%;margin-top:2px;color:#4a6b36;font-size:25px;font-weight:800;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}"
    ".hm-msg{max-width:100%;margin-top:3px;color:#68462b;font-size:18px;line-height:1.2;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}"
    f".hm-side{{position:absolute;z-index:5;bottom:-13px;width:135px;height:145px;object-fit:contain;filter:drop-shadow(0 5px 5px rgba(47,28,12,.55));pointer-events:none;animation:hm-side 4.8s ease-in-out infinite}}"
    ".hm-left{left:8px}.hm-right{right:8px;animation-delay:.45s}"
    ".hm-flower{position:absolute;z-index:3;color:#fff2a8;font-size:25px;text-shadow:0 2px #a94e2c;animation:hm-float 3.4s ease-in-out infinite}"
    ".hm-f1{top:12px;left:25%}.hm-f2{top:20px;right:25%;animation-delay:1.1s}.hm-f3{bottom:12px;left:29%;font-size:18px;animation-delay:2s}.hm-f4{bottom:14px;right:29%;font-size:18px;animation-delay:.6s}"
    ".hm-shine{position:absolute;z-index:6;top:0;left:0;width:28%;height:100%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.38),transparent);pointer-events:none;animation:hm-shine 5s linear infinite}"
    "@keyframes hm-in{from{opacity:0;transform:translateY(22px) scale(.9)}to{opacity:1;transform:none}}"
    "@keyframes hm-panel{from{opacity:0;transform:scale(.8)}to{opacity:1;transform:none}}"
    "@keyframes hm-breathe{50%{box-shadow:0 16px 38px rgba(48,27,10,.65),0 0 25px rgba(255,218,111,.6),inset 0 0 0 3px #f3d77f}}"
    "@keyframes hm-zoom{to{transform:scale(1.18)}}"
    "@keyframes hm-pop{from{opacity:0;transform:scale(.6)}to{opacity:1;transform:scale(1)}}"
    "@keyframes hm-pulse{50%{transform:scale(1.05)}}"
    "@keyframes hm-side{0%,100%{transform:translateY(0) rotate(-3deg)}50%{transform:translateY(-9px) rotate(3deg)}}"
    "@keyframes hm-float{0%,100%{transform:translateY(0) rotate(-8deg);opacity:.65}50%{transform:translateY(-8px) rotate(8deg);opacity:1}}"
    "@keyframes hm-shine{from{transform:translateX(-150%)}to{transform:translateX(430%)}}"
)

def alert_html(token, from_token):
    return (
        f'<div class="hm-card">'
        f'<img class="hm-bg" src="{BASE}/bg.png" alt="">'
        f'<div class="hm-veil"></div>'
        f'<div class="hm-flower hm-f1">✿</div>'
        f'<div class="hm-flower hm-f2">✿</div>'
        f'<div class="hm-flower hm-f3">✦</div>'
        f'<div class="hm-flower hm-f4">✦</div>'
        f'<img class="hm-side hm-left" src="{BASE}/baru.png" alt="">'
        f'<img class="hm-side hm-right" src="{BASE}/baru-right.png" alt="">'
        f'<div class="hm-panel">'
        f'<div class="hm-amount">{{amount}}</div>'
        f'<div class="hm-from">{from_token}</div>'
        f'<div class="hm-who">{token}</div>'
        f'<div class="hm-msg">{{message}}</div>'
        f'</div>'
        f'<div class="hm-shine"></div>'
        f'</div>'
    )

(ROOT / "sociabuzz-alert.html").write_text(alert_html("{supporter}", "{from_text}"), encoding="utf-8")
(ROOT / "sociabuzz-alert-obs.css").write_text(ALERT_CSS, encoding="utf-8")
(ROOT / "saweria-alert.html").write_text(alert_html("{donator}", "Saweria"), encoding="utf-8")
(ROOT / "saweria-alert-obs.css").write_text(ALERT_CSS, encoding="utf-8")
print("Alert HTML + CSS built (sociabuzz + saweria)")

# ── 3. WIDGET CSS (transform from Helcurt pattern) ──────────────────
WIDGETS_DIR = ROOT / "widgets"
WIDGETS_DIR.mkdir(exist_ok=True)

REPLACEMENTS = [
    # URLs
    ("MasAjie12/helcurt collector-alert-assets/main/kiri.png", f"MasAjie12/harvest-moon-alert-assets/main/baru.png"),
    ("MasAjie12/helcurt-collector-alert-assets/main/kiri.png", f"MasAjie12/harvest-moon-alert-assets/main/baru.png"),
    ("MasAjie12/helcurt collector-alert-assets/main/bg.jpg", f"MasAjie12/harvest-moon-alert-assets/main/bg.png"),
    ("MasAjie12/helcurt-collector-alert-assets/main/bg.jpg", f"MasAjie12/harvest-moon-alert-assets/main/bg.png"),
    # Text
    ("HELCURT COLLECTOR", "HARVEST MOON"),
    ("Helcurt Collector", "Harvest Moon"),
    ("helcurt collector", "harvest moon"),
    # Prefix
    ("helc-", "hm-"),
    ("helc_", "hm_"),
    # Colors (case-insensitive pairs)
    ("#e91e63", "#a94e2c"), ("#E91E63", "#A94E2C"),
    ("#2d0b40", "#3d291c"), ("#2D0B40", "#3D291C"),
    ("#1a0526", "#1f1208"), ("#1A0526", "#1F1208"),
    ("#3b1152", "#5a3a1e"), ("#3B1152", "#5A3A1E"),
    ("#7b1fa2", "#b47a3c"), ("#7B1FA2", "#B47A3C"),
    ("#00e5ff", "#f0c040"), ("#00E5FF", "#F0C040"),
    ("#84ffff", "#ffe49b"), ("#84FFFF", "#FFE49B"),
    ("#ff4081", "#d4691e"), ("#FF4081", "#D4691E"),
    ("#fce4ec", "#f9e7ae"), ("#FCE4EC", "#F9E7AE"),
    ("#f8bbd0", "#fff5c9"), ("#F8BBD0", "#FFF5C9"),
    ("#062a33", "#2c1a0e"), ("#062A33", "#2C1A0E"),
    ("#053543", "#3d291c"), ("#053543", "#3D291C"),
    ("#12718f", "#80552f"), ("#12718F", "#80552F"),
    # RGBA colors
    ("rgba(18,113,143", "rgba(180,122,60"),
    ("rgba(75,224,138", "rgba(88,123,56"),
    ("rgba(233,30,99", "rgba(169,78,44"),
    ("rgba(6,42,51", "rgba(44,26,14"),
    ("rgba(45,11,64", "rgba(61,41,28"),
    ("rgba(26,5,38", "rgba(31,18,8"),
    ("rgba(5,53,67", "rgba(90,58,30"),
    ("rgba(255,107,74", "rgba(212,105,30"),
    ("rgba(123,31,162", "rgba(180,122,60"),
    ("rgba(0,229,255", "rgba(240,192,64"),
    ("rgba(132,255,255", "rgba(255,228,155"),
    ("rgba(255,64,129", "rgba(212,105,30"),
    ("rgba(252,228,236", "rgba(249,231,174"),
    ("rgba(248,187,208", "rgba(255,245,201"),
]

for f in HELC.glob("sociabuzz-*-obs.css"):
    content = f.read_text("utf-8")
    for old, new in REPLACEMENTS:
        content = content.replace(old, new)
    out_name = f.name.replace("helc", "hm")
    (WIDGETS_DIR / out_name).write_text(content, encoding="utf-8")
    print(f"Widget built: {out_name} ({len(content)} bytes)")

# ── 4. PREVIEW HTML ─────────────────────────────────────────────────
PREVIEW = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Harvest Moon Back to Nature — Sociabuzz Alert Preview</title>
<style>
body{{margin:0;padding:40px;background:#1a1208;font-family:'Baloo 2',sans-serif}}
.g-wrap{{width:100%;min-height:100vh;display:flex;flex-direction:column;align-items:center;gap:30px}}
h2{{color:#f9e7ae;text-align:center;margin:0 0 10px;font-size:22px;text-shadow:0 2px 6px rgba(0,0,0,.8)}}
.alert-wrap{{width:680px;max-width:100%}}
.widget-section{{width:680px;max-width:100%}}
.widget-section .card,.widget-section .subathon-container{{
  box-sizing:border-box;border-radius:12px;padding:16px 20px;margin:0 auto;
  font-family:'Trebuchet MS','Segoe UI',sans-serif;
}}
.card{{position:relative;overflow:hidden;border:2px solid #80552f;
  background:linear-gradient(135deg,#5a3a1e,#3d291c);color:#f9e7ae;
  box-shadow:0 4px 16px rgba(0,0,0,.5)}}
.card .card-header{{text-align:center;padding:8px 0}}
.card .card-header h4{{color:#f0c040;font-size:18px;margin:0;letter-spacing:1px;text-transform:uppercase}}
.card .card-body{{padding:10px 0}}
.card .show_donate{{width:100%;border-collapse:separate;border-spacing:0 4px}}
.card .show_donate td{{padding:6px 10px;color:#f9e7ae;background:rgba(44,26,14,.4);border-radius:6px;font-size:14px}}
.card .show_donate td:first-child{{width:30px;text-align:center;color:#f0c040;font-weight:900}}
.card .show_donate .text-limit{{font-weight:600}}
.card .show_donate .text-limit-r{{color:#ffe49b;text-align:right;white-space:nowrap}}
.card .progress{{height:8px;border-radius:999px;background:rgba(44,26,14,.5);overflow:hidden;margin:8px 0}}
.card .progress-bar{{height:100%;border-radius:999px;background:linear-gradient(90deg,#a94e2c,#f0c040)}}
.subathon-container{{position:relative;overflow:hidden;border:2px solid #80552f;
  background:linear-gradient(135deg,#5a3a1e,#3d291c);color:#f9e7ae;
  text-align:center;padding:20px;border-radius:12px}}
.subathon-container .sub_judul{{color:#f0c040;font-size:20px;font-weight:800;text-transform:uppercase;letter-spacing:1px}}
.subathon-container .sub_timer{{color:#ffe49b;font:900 30px 'Courier New',monospace;margin-top:8px}}
</style>
</head>
<body>
<div class="g-wrap">

<h2>🌾 ALERT DONASI — Harvest Moon: Back to Nature</h2>
<div class="alert-wrap">
{alert_html("Pete", "Transfer Bank")}
</div>

<h2>⏱️ SUBATHON TIMER</h2>
<div class="widget-section w-sub">
<div class="subathon-container">
<div class="sub_judul">Harvest Moon Subathon</div>
<div class="sub_timer">02:34:56</div>
</div>
</div>

<h2>🎯 MILESTONE</h2>
<div class="widget-section w-mile">
<div class="card">
<div class="card-header"><h4>Target Panen Musim Ini</h4></div>
<div class="card-body">
<div class="progress"><div class="progress-bar" style="width:67%"></div></div>
<div style="text-align:center;color:#f0c040;font-weight:800">Rp 6.700.000 / Rp 10.000.000</div>
</div>
</div>
</div>

<h2>📋 QUEUE</h2>
<div class="widget-section w-queue">
<div class="card">
<div class="card-header"><h4>Antrian Media Share</h4></div>
<div class="card-body">
<table class="show_donate">
<tr><td>1</td><td class="text-limit">Pete</td><td class="text-limit-r">Rp 50.000</td></tr>
<tr><td>2</td><td class="text-limit">Ann</td><td class="text-limit-r">Rp 25.000</td></tr>
<tr><td>3</td><td class="text-limit">Cliff</td><td class="text-limit-r">Rp 20.000</td></tr>
</table>
</div>
</div>
</div>

<h2>🏆 TOP DONATOR</h2>
<div class="widget-section w-top">
<div class="card">
<div class="card-header"><h4>Top Donator Musim Ini</h4></div>
<div class="card-body">
<table class="show_donate">
<tr><td>1</td><td class="text-limit">Karen</td><td class="text-limit-r">Rp 500.000</td></tr>
<tr><td>2</td><td class="text-limit">Popuri</td><td class="text-limit-r">Rp 350.000</td></tr>
<tr><td>3</td><td class="text-limit">Mary</td><td class="text-limit-r">Rp 200.000</td></tr>
</table>
</div>
</div>
</div>

</div>
</body>
</html>"""

(ROOT / "preview.html").write_text(PREVIEW, encoding="utf-8")
print("Preview HTML built")

# ── 5. README ───────────────────────────────────────────────────────
(ROOT / "README.md").write_text(
    "# Harvest Moon: Back to Nature — Sociabuzz Custom Alert\n\n"
    "Assets: `bg.png`, `baru.png`, `baru-right.png`\n\n"
    "Generated by `build_theme.py`\n", encoding="utf-8")

# ── 6. ASSERTIONS ───────────────────────────────────────────────────
h = (ROOT / "sociabuzz-alert.html").read_text()
c = ALERT_CSS
assert 'style="' not in h, "inline style found"
assert "<style" not in h, "style tag found"
assert "<link" not in h, "link tag found"
assert "important" not in c.lower(), "!important found in alert CSS"
assert "::before" not in c and "::after" not in c, "pseudo-element in alert CSS"
assert ";content:" not in c, "content: in alert CSS"
# url() only in @import
non_import_urls = [m.start() for m in re.finditer(r"url\(", c) if not c[max(0,m.start()-8):m.start()].endswith("@import ")]
assert len(non_import_urls) == 0, f"url() found outside @import in alert CSS"
# images use <img src> not background
assert h.count("<img") == 3, f"expected 3 <img> tags, got {h.count('<img')}"
print("All assertions passed ✓")
print("BUILD COMPLETE")
