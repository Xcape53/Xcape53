"""Grafiki profilu w stylu "szkicownika inżyniera": odręczne linie, kolory i fonty strony.

python scripts/build_sketch.py          wszystko (nagłówki, separatory, projekty, "teraz")
python scripts/build_sketch.py --now    tylko karta "teraz" z ostatnich pushy (codziennie w akcji)

Tekst jest zamieniany na krzywe (fontTools), bo GitHub nie wczytuje fontów w obrazkach SVG.
Każdy plik ma własne granatowe tło, więc wygląda tak samo w jasnym i ciemnym motywie.
"""
import sys
from pathlib import Path
# scripts/calendar.py zasłania moduł standardowy (potrzebny urllib i fontTools): katalog skryptu poza ścieżką importu
sys.path = [p for p in sys.path if Path(p or ".").resolve() != Path(__file__).resolve().parent]
import base64, json, math, os, random, urllib.request
from datetime import datetime
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
OUT, FD = ROOT / "assets" / "sketch", Path(__file__).resolve().parent / "fonts"
NAVY, GLOW, PANEL, TEXT, WHITE, P, S = "#020816", "#0a2a78", "#0e1216", "#b1b1b1", "#f2f4f8", "#2c7ffe", "#642efd"
W = 1200
USER, SKIP = "Xcape53", {"Xcape53", "portfolio"}

# ---------- tekst jako krzywe ----------
_fonts = {}
def _font(name, wght=None):
    if (name, wght) not in _fonts:
        f = TTFont(FD / name)
        if wght and "fvar" in f:
            f = instantiateVariableFont(f, {"wght": wght})
        _fonts[(name, wght)] = f
    return _fonts[(name, wght)]

FACE = {"display": ("Poppins-ExtraBold.ttf", None), "sans": ("SplineSans.ttf", 400), "sans6": ("SplineSans.ttf", 600),
        "mono": ("SplineSansMono.ttf", 400), "hand": ("Caveat.ttf", 600)}

def text(s, x, y, size, face="sans", fill=TEXT, ls=0.0, anchor="start"):
    f = _font(*FACE[face]); gs, cmap, sc = f.getGlyphSet(), f.getBestCmap(), size / f["head"].unitsPerEm
    names = [cmap.get(ord(c), ".notdef") for c in s]
    assert ".notdef" not in names, f"brak znaku w {FACE[face][0]}: {s!r}"
    adv = [f["hmtx"][g][0] * sc + ls for g in names]
    width = sum(adv) - ls
    x = x - width if anchor == "end" else x - width / 2 if anchor == "middle" else x
    pen = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    for g, a in zip(names, adv):
        gs[g].draw(TransformPen(pen, (sc, 0, 0, -sc, x, y)))
        x += a
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>', width

# ---------- odręczne kształty (uproszczony algorytm rough.js, deterministyczny) ----------
def _seg(r, x1, y1, x2, y2, rough, bow):
    L = math.hypot(x2 - x1, y2 - y1) or 1
    off, (nx, ny) = min(rough * 2.2, L / 10), (-(y2 - y1) / L, (x2 - x1) / L)
    b = bow * rough * L / 220 * r.uniform(-1, 1)
    j = lambda: r.uniform(-off, off)
    pt = lambda t: (x1 + (x2 - x1) * t + nx * b + j(), y1 + (y2 - y1) * t + ny * b + j())
    (ax, ay), (bx, by), (cx, cy), (dx, dy) = (x1 + j(), y1 + j()), pt(.33), pt(.66), (x2 + j(), y2 + j())
    return f"M{ax:.1f} {ay:.1f}C{bx:.1f} {by:.1f} {cx:.1f} {cy:.1f} {dx:.1f} {dy:.1f}"

def line(r, x1, y1, x2, y2, stroke=P, w=2.4, rough=1.3, bow=1.2, double=True):
    d = _seg(r, x1, y1, x2, y2, rough, bow) + (_seg(r, x1, y1, x2, y2, rough * .6, bow) if double else "")
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round"/>'

def rect(r, x, y, w, h, stroke=P, sw=2.2, fill=None, rough=1.2):
    out = []
    if fill:
        j = lambda: r.uniform(-1.5, 1.5)
        out.append(f'<path d="M{x+j():.1f} {y+j():.1f}L{x+w+j():.1f} {y+j():.1f}L{x+w+j():.1f} {y+h+j():.1f}L{x+j():.1f} {y+h+j():.1f}Z" fill="{fill}"/>')
    for a, b, c, d in ((x, y, x + w, y), (x + w, y, x + w, y + h), (x + w, y + h, x, y + h), (x, y + h, x, y)):
        out.append(line(r, a, b, c, d, stroke, sw, rough, 1))
    return "".join(out)

def ellipse(r, cx, cy, rx, ry, stroke=P, w=2.2, fill=None, rough=1.2):
    out = []
    for k in (1, .6):
        start, pts = r.uniform(0, 2 * math.pi), []
        for i in range(37):
            a = start + i / 36 * (2 * math.pi + .35 * k)
            q = 1 + r.uniform(-.02, .02) * rough
            pts.append(f"{cx + rx * q * math.cos(a):.1f} {cy + ry * q * math.sin(a):.1f}")
        out.append(f'<path d="M{"L".join(pts)}" fill="{fill if k == 1 and fill else "none"}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round"/>')
    return "".join(out)

def arrow(r, x1, y1, x2, y2, stroke=P, w=2.4):
    a = math.atan2(y2 - y1, x2 - x1)
    h = [(x2 - 16 * math.cos(a - .5), y2 - 16 * math.sin(a - .5)), (x2 - 16 * math.cos(a + .5), y2 - 16 * math.sin(a + .5))]
    return line(r, x1, y1, x2, y2, stroke, w, 1.2, 1.6) + "".join(line(r, hx, hy, x2, y2, stroke, w, .8, .4, False) for hx, hy in h)

def sine(r, x0, x1, y, amp, k, stroke="url(#g)", w=3):
    d = "M" + "L".join(f"{x:.1f} {y + amp * math.sin((x - x0) / k) + r.uniform(-.5, .5):.1f}" for x in range(x0, x1 + 1, 6))
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'

def svg(name, h, body, title, w=W):
    grad = f'<defs><linearGradient id="g" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0"><stop offset="0" stop-color="{P}"/><stop offset="1" stop-color="{S}"/></linearGradient></defs>'
    doc = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img"><title>{title}</title>{grad}{"".join(body)}</svg>\n'
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / name).write_text(doc, encoding="utf-8")
    print(f"{name:22} {len(doc) // 1024} KB")

def panel(r, h, w=W):
    return rect(r, 6, 6, w - 12, h - 12, stroke="#1d3157", sw=2, fill=NAVY, rough=1.1)

M = 600   # wersje na telefon: GitHub skaluje obrazek do ~360 px, więc tekst musi być większy względem szerokości

# ---------- treść ----------
COPY = {
    "en": {"kicker": "SOFTWARE DEVELOPMENT & SYSTEM INTEGRATION", "logo": "my logo, Gdynia", "projects": "PROJECTS",
           "now": "now:", "now_note": "from my latest pushes, updates itself",
           "rows": [("JobManager", "listings from 8 job portals, offers researched by an LLM", "Node.js · LLM"),
                    ("SeeSky", "software for the SimLE radio telescope", "Python · Flask"),
                    ("LabInc", "incremental game about chemical production", "Java · Swing"),
                    ("Yapper", "lightweight speech-to-text app", "Python · PyQt6")]},
    "pl": {"kicker": "TWORZENIE OPROGRAMOWANIA I INTEGRACJA SYSTEMÓW", "logo": "moje logo, Gdynia", "projects": "PROJEKTY",
           "now": "teraz:", "now_note": "z ostatnich pushy, odświeża się samo",
           "rows": [("JobManager", "oferty z 8 portali, analiza modelem językowym", "Node.js · LLM"),
                    ("SeeSky", "oprogramowanie radioteleskopu SimLE", "Python · Flask"),
                    ("LabInc", "gra inkrementalna o produkcji chemicznej", "Java · Swing"),
                    ("Yapper", "lekka aplikacja speech-to-text", "Python · PyQt6")]},
}

def logo_uri():
    return "data:image/png;base64," + base64.b64encode((ROOT / "assets" / "sketch-src" / "logo-240.png").read_bytes()).decode()

def build_header(lang):
    c, r, h = COPY[lang], random.Random(1), 380
    b = [panel(r, h), text(c["kicker"], 72, 104, 19, "sans6", P, ls=5)[0],
         text("PIOTR", 66, 206, 92, "display", WHITE)[0], text("JELENIEWICZ", 66, 294, 92, "display", WHITE)[0],
         line(r, 70, 318, 720, 324, "url(#g)", 5, 1.2, 1)]
    cx, cy, rad = 960, 180, 118
    b.append(f'<image href="{logo_uri()}" x="{cx - rad}" y="{cy - rad}" width="{2 * rad}" height="{2 * rad}"/>')
    b.append(ellipse(r, cx, cy, rad + 16, rad + 12, "#2c7ffe99", 2.2))
    b.append(arrow(r, 905, 352, 916, 318, TEXT, 2.2))
    b.append(text(c["logo"], 930, 352, 30, "hand", TEXT)[0])
    svg(f"header-{lang}.svg", h, b, "Piotr Jeleniewicz")

def build_divider(lang):
    c, r, h = COPY[lang], random.Random(2), 120
    b = [sine(r, 20, W - 20, 44, 16, 34), text(c["projects"], 24, 106, 18, "sans6", P, ls=5)[0]]
    svg(f"divider-{lang}.svg", h, b, c["projects"])

def build_rows(lang):
    for i, (name, desc, tech) in enumerate(COPY[lang]["rows"]):
        r, h = random.Random(10 + i), 112
        b = [rect(r, 10, 10, W - 20, h - 20, stroke="#2c7ffe66", sw=2, fill=NAVY, rough=1.4),
             text(name, 44, 70, 33, "sans6", WHITE)[0], text(desc, 330, 68, 22, "sans", TEXT)[0],
             text(tech, W - 92, 68, 19, "mono", P, anchor="end")[0], arrow(r, W - 70, 70, W - 46, 46, P, 2.4)]
        svg(f"project-{i + 1}-{lang}.svg", h, b, name)

def latest_repos(n=2):
    req = urllib.request.Request(f"https://api.github.com/users/{USER}/repos?sort=pushed&per_page=30", headers={"Accept": "application/vnd.github+json"})
    if os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", "Bearer " + os.environ["GITHUB_TOKEN"])
    repos = json.load(urllib.request.urlopen(req, timeout=20))
    keep = [x for x in repos if not x["fork"] and not x["archived"] and not x["private"] and x["name"] not in SKIP]
    return [(x["name"], datetime.strptime(x["pushed_at"][:10], "%Y-%m-%d")) for x in keep[:n]]

def build_now(lang, repos):
    c, r, h = COPY[lang], random.Random(3), 240
    b = [panel(r, h), text(c["now_note"], 70, 132, 34, "hand", TEXT)[0], arrow(r, 560, 122, 690, 122, TEXT, 2.4),
         rect(r, 720, 34, 430, 172, stroke=S, sw=2.6, fill=GLOW, rough=1.6), ellipse(r, 935, 36, 11, 11, S, 2, fill=S),
         text(c["now"], 750, 98, 44, "hand", WHITE)[0]]
    for i, (name, d) in enumerate(repos):
        when = d.strftime("%d.%m") if lang == "pl" else d.strftime("%b %d")
        b.append(text(f"{name} · {when}", 752, 142 + i * 38, 22, "sans", WHITE if i == 0 else TEXT)[0])
    svg(f"now-{lang}.svg", h, b, c["now"] + " " + ", ".join(n for n, _ in repos))

def build_header_m(lang):
    c, r, h = COPY[lang], random.Random(1), 420
    b = [panel(r, h, M), text("PIOTR", 40, 120, 64, "display", WHITE)[0], text("JELENIEWICZ", 40, 186, 64, "display", WHITE)[0],
         line(r, 42, 206, 470, 210, "url(#g)", 4, 1.2, 1)]
    cx, cy, rad = 300, 310, 72
    b.append(f'<image href="{logo_uri()}" x="{cx - rad}" y="{cy - rad}" width="{2 * rad}" height="{2 * rad}"/>')
    b.append(ellipse(r, cx, cy, rad + 12, rad + 10, "#2c7ffe99", 2))
    b.append(text(c["logo"], 400, 360, 26, "hand", TEXT)[0])
    b.append(text(c["kicker"].split(" & ")[0].split(" I ")[0], 42, 64, 15, "sans6", P, ls=3)[0])
    svg(f"header-{lang}-m.svg", h, b, "Piotr Jeleniewicz", M)

def build_divider_m(lang):
    c, r = COPY[lang], random.Random(2)
    svg(f"divider-{lang}-m.svg", 110, [sine(r, 12, M - 12, 34, 12, 22), text(c["projects"], 16, 96, 22, "sans6", P, ls=4)[0]], c["projects"], M)

def build_rows_m(lang):
    for i, (name, desc, tech) in enumerate(COPY[lang]["rows"]):
        lines = [desc]
        if text(desc, 0, 0, 21)[1] > M - 64:   # za długi opis: łamany na dwie linie przy spacji najbliżej środka
            words = desc.split(" "); k = min(range(1, len(words)), key=lambda k: abs(len(" ".join(words[:k])) - len(desc) / 2))
            lines = [" ".join(words[:k]), " ".join(words[k:])]
        r, h = random.Random(10 + i), 124 + 28 * len(lines)
        b = [rect(r, 8, 8, M - 16, h - 16, stroke="#2c7ffe66", sw=2, fill=NAVY, rough=1.4),
             text(name, 32, 56, 32, "sans6", WHITE)[0], arrow(r, M - 62, 58, M - 36, 32, P, 2.4),
             text(tech, 32, h - 30, 18, "mono", P)[0]]
        b += [text(t, 32, 92 + 28 * j, 21, "sans", TEXT)[0] for j, t in enumerate(lines)]
        svg(f"project-{i + 1}-{lang}-m.svg", h, b, name, M)

def build_now_m(lang, repos):
    c, r, h = COPY[lang], random.Random(3), 230
    b = [panel(r, h, M), rect(r, 30, 30, M - 60, 170, stroke=S, sw=2.6, fill=GLOW, rough=1.6), ellipse(r, M / 2, 32, 10, 10, S, 2, fill=S),
         text(c["now"], 58, 92, 44, "hand", WHITE)[0]]
    for i, (name, d) in enumerate(repos):
        when = d.strftime("%d.%m") if lang == "pl" else d.strftime("%b %d")
        b.append(text(f"{name} · {when}", 60, 136 + i * 38, 24, "sans", WHITE if i == 0 else TEXT)[0])
    svg(f"now-{lang}-m.svg", h, b, c["now"], M)

if __name__ == "__main__":
    repos = latest_repos()
    for lang in COPY:
        if "--now" not in sys.argv:
            build_header(lang); build_divider(lang); build_rows(lang); build_header_m(lang); build_divider_m(lang); build_rows_m(lang)
        build_now(lang, repos); build_now_m(lang, repos)
