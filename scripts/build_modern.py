"""Nowoczesne grafiki profilu (bez odręcznych linii), w kolorach i fontach piotrjeleniewicz.com.

python scripts/build_modern.py flow     wariant B: profil jako schemat blokowy z pulsami jak na stronie
python scripts/build_modern.py cards    wariant C: nagłówek, karty projektów, karta aktywności z prawdziwych danych

Narzędzia do tekstu (krzywe z fontów) i zapis SVG są wspólne z build_sketch.py.
"""
import sys
from pathlib import Path
sys.path = [p for p in sys.path if Path(p or ".").resolve() != Path(__file__).resolve().parent]
import importlib.util, json, math, os, subprocess, urllib.request
from datetime import datetime, timedelta, timezone

_spec = importlib.util.spec_from_file_location("sk", Path(__file__).with_name("build_sketch.py"))
sk = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(sk)
text, svg, logo_uri, latest_repos = sk.text, sk.svg, sk.logo_uri, sk.latest_repos
NAVY, GLOW, PANEL, TEXT, WHITE, P, S, W, M = sk.NAVY, sk.GLOW, sk.PANEL, sk.TEXT, sk.WHITE, sk.P, sk.S, sk.W, sk.M
MUTED, LINE = "#6b7686", "#1d2b48"
sk.OUT = Path(__file__).resolve().parents[1] / "assets" / "modern"

COPY = {
    "en": {"kicker": "SOFTWARE DEVELOPMENT & SYSTEM INTEGRATION", "me": "me", "problem": "problem", "works": "working tools",
           "loop": "daily use -> fixes", "projects": "PROJECTS", "activity": "ACTIVITY · LAST 12 MONTHS", "now": "now",
           "stats": ("contributions", "commits", "public repos"), "weeks": "weekly contributions",
           "rows": [("JobManager", "Listings from 8 job portals, offers researched by an LLM", "Node.js · LLM", "#3af555"),
                    ("SeeSky", "Software for the SimLE radio telescope", "Python · Flask · Astropy", S),
                    ("LabInc", "Incremental game about chemical production", "Java · Swing", P),
                    ("Yapper", "Lightweight speech-to-text app", "Python · PyQt6", "#8a8a93")]},
    "pl": {"kicker": "TWORZENIE OPROGRAMOWANIA I INTEGRACJA SYSTEMÓW", "me": "ja", "problem": "problem", "works": "działające narzędzia",
           "loop": "codzienne użycie -> poprawki", "projects": "PROJEKTY", "activity": "AKTYWNOŚĆ · OSTATNIE 12 MIESIĘCY", "now": "teraz",
           "stats": ("kontrybucji", "commitów", "publicznych repo"), "weeks": "kontrybucje tygodniowo",
           "rows": [("JobManager", "Oferty z 8 portali, analiza modelem językowym", "Node.js · LLM", "#3af555"),
                    ("SeeSky", "Oprogramowanie radioteleskopu SimLE", "Python · Flask · Astropy", S),
                    ("LabInc", "Gra inkrementalna o produkcji chemicznej", "Java · Swing", P),
                    ("Yapper", "Lekka aplikacja speech-to-text", "Python · PyQt6", "#8a8a93")]},
}

# ---------- czyste kształty ----------
def box(x, y, w, h, stroke=P, fill=NAVY, sw=1.6, r=12, op=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{op}"/>'

def path(d, stroke=P, sw=1.8, op=1, dash=None, marker=True, pid=None):
    extra = (f' id="{pid}"' if pid else "") + (f' stroke-dasharray="{dash}"' if dash else "") + (' marker-end="url(#ar)"' if marker else "")
    return f'<path d="{d}" fill="none" stroke="{stroke}" stroke-width="{sw}" stroke-opacity="{op}" stroke-linecap="round" stroke-linejoin="round"{extra}/>'

def pulse(pid, dur, delay, color=WHITE):
    # puls jedzie po ścieżce jak na schemacie na stronie; SMIL działa w obrazkach SVG na GitHubie
    return (f'<circle r="3.6" fill="{color}" opacity="0"><animateMotion dur="{dur}s" begin="{delay}s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.85;1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/></circle>')

DEFS = (f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M1 1L9 5L1 9" fill="none" stroke="{P}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></marker>'
        f'<radialGradient id="glow" cx=".12" cy="0" r=".9"><stop offset="0" stop-color="{GLOW}" stop-opacity=".9"/><stop offset="1" stop-color="{NAVY}" stop-opacity="0"/></radialGradient></defs>')

def frame(w, h):
    return [DEFS, f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="{NAVY}" stroke="{LINE}" stroke-width="1.5"/>',
            f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="16" fill="url(#glow)"/>']

def name_block(c, x, y, size, kicker_size):
    return [text(c["kicker"], x + 2, y, kicker_size, "sans6", P, ls=kicker_size / 3.6)[0],
            text("PIOTR JELENIEWICZ", x, y + size * 1.05, size, "display", WHITE)[0]]

# ---------- B: schemat blokowy ----------
def build_flow(lang):
    c, h = COPY[lang], 640
    b = frame(W, h) + name_block(c, 56, 70, 52, 15)
    y0, cyc = 360, 300
    # wejście: ja, sumator
    b += [f'<circle cx="110" cy="{y0}" r="38" fill="#120a2e" stroke="{S}" stroke-width="1.8"/>', text(c["me"], 110, y0 + 7, 21, "sans6", WHITE, anchor="middle")[0],
          text(c["problem"], 110, y0 + 66, 15, "mono", MUTED, anchor="middle")[0],
          path(f"M150 {y0}H232", pid="u"), f'<circle cx="262" cy="{y0}" r="26" fill="{NAVY}" stroke="{P}" stroke-width="1.8"/>',
          text("+", 262, y0 + 9, 28, "sans6", P, anchor="middle")[0]]
    ys = [y0 - 150, y0 - 50, y0 + 50, y0 + 150]
    for i, (yy, (n, d, t, col)) in enumerate(zip(ys, c["rows"])):
        b.append(path(f"M288 {y0}C330 {y0} 330 {yy} 372 {yy}", pid=f"s{i}"))
        b.append(box(376, yy - 36, 380, 72, stroke=col, op=.85))
        b.append(f'<rect x="376" y="{yy - 36}" width="5" height="72" rx="2.5" fill="{col}"/>')
        b.append(text(n, 400, yy - 4, 21, "sans6", WHITE)[0])
        b.append(text(t, 400, yy + 22, 14, "mono", MUTED)[0])
        b.append(path(f"M756 {yy}C812 {yy} 812 {y0} 866 {y0}", pid=f"m{i}"))
    b += [box(870, y0 - 40, 270, 80, stroke=S, fill="#0d0a24", sw=2), text(c["works"], 1005, y0 + 8, 20, "sans6", WHITE, anchor="middle")[0]]
    # sprzężenie zwrotne pod spodem
    b.append(path(f"M1005 {y0 + 40}V{y0 + 232}H262V{y0 + 28}", stroke=S, op=.9, dash="6 6", pid="fb"))
    b.append(text(c["loop"], 633, y0 + 222, 15, "mono", S, anchor="middle")[0])
    b += [pulse("u", 2.4, 0, "#b9a6ff")] + [pulse(f"s{i}", 2.4, .6 + i * .25) for i in range(4)] + [pulse(f"m{i}", 2.4, 1.8 + i * .25) for i in range(4)] + [pulse("fb", 4.8, 3, "#b9a6ff")]
    svg(f"flow-{lang}.svg", h, b, "Piotr Jeleniewicz")

def build_flow_m(lang):
    c, w, h = COPY[lang], M, 1060
    b = frame(w, h) + [text(c["kicker"].split(" & ")[0].split(" I ")[0], 36, 58, 13, "sans6", P, ls=3.4)[0],
                       text("PIOTR", 32, 118, 50, "display", WHITE)[0], text("JELENIEWICZ", 32, 170, 50, "display", WHITE)[0]]
    cx = 270
    b += [f'<circle cx="{cx}" cy="250" r="36" fill="#120a2e" stroke="{S}" stroke-width="1.8"/>', text(c["me"], cx, 257, 20, "sans6", WHITE, anchor="middle")[0],
          path(f"M{cx} 286V330", pid="u"), f'<circle cx="{cx}" cy="356" r="24" fill="{NAVY}" stroke="{P}" stroke-width="1.8"/>',
          text("+", cx, 365, 26, "sans6", P, anchor="middle")[0], path(f"M{cx} 380V412", pid="d0")]
    for i, (n, d, t, col) in enumerate(c["rows"]):
        y = 416 + i * 120
        b += [box(60, y, 420, 92, stroke=col, op=.85), f'<rect x="60" y="{y}" width="5" height="92" rx="2.5" fill="{col}"/>',
              text(n, 86, y + 40, 24, "sans6", WHITE)[0], text(t, 86, y + 70, 15, "mono", MUTED)[0]]
        if i < 3:
            b.append(path(f"M{cx} {y + 92}V{y + 118}", marker=True, pid=f"d{i + 1}"))
    yb = 416 + 4 * 120
    b += [path(f"M{cx} {yb - 28}V{yb + 8}", pid="d4"), box(110, yb + 12, 320, 70, stroke=S, fill="#0d0a24", sw=2),
          text(c["works"], cx, yb + 55, 20, "sans6", WHITE, anchor="middle")[0],
          path(f"M430 {yb + 47}H530V356H296", stroke=S, op=.9, dash="6 6", pid="fb"),
          f'<g transform="translate(552 {(356 + yb + 47) / 2}) rotate(-90)">{text(c["loop"], 0, 0, 14, "mono", S, anchor="middle")[0]}</g>']
    b += [pulse("u", 2, 0, "#b9a6ff")] + [pulse(f"d{i}", 1.4, .5 + i * .45) for i in range(5)] + [pulse("fb", 4.4, 3, "#b9a6ff")]
    svg(f"flow-{lang}-m.svg", h, b, "Piotr Jeleniewicz", w)

# ---------- C: karty + aktywność ----------
def build_header(lang):
    c, h = COPY[lang], 300
    b = frame(W, h) + [text(c["kicker"], 58, 96, 16, "sans6", P, ls=4.4)[0], text("PIOTR", 52, 180, 80, "display", WHITE)[0],
                       text("JELENIEWICZ", 52, 256, 80, "display", WHITE)[0]]
    d = "M" + "L".join(f"{x} {280 + 5 * math.sin(x / 16):.1f}" for x in range(58, 700, 4))
    b.append(f'<path d="{d}" fill="none" stroke="{S}" stroke-width="2.4" stroke-linecap="round"/>')
    b += [f'<image href="{logo_uri()}" x="890" y="45" width="210" height="210"/>', f'<circle cx="995" cy="150" r="118" fill="none" stroke="{LINE}" stroke-width="1.5"/>']
    svg(f"header-{lang}.svg", h, b, "Piotr Jeleniewicz")

def build_header_m(lang):
    c, h = COPY[lang], 380
    b = frame(M, h) + [text(c["kicker"].split(" & ")[0].split(" I ")[0], 40, 62, 14, "sans6", P, ls=3.6)[0],
                       text("PIOTR", 36, 132, 62, "display", WHITE)[0], text("JELENIEWICZ", 36, 196, 62, "display", WHITE)[0],
                       f'<image href="{logo_uri()}" x="230" y="222" width="140" height="140"/>']
    svg(f"header-{lang}-m.svg", h, b, "Piotr Jeleniewicz", M)

def card(x, y, w, h, n, d, t, col, big=False):
    s = 1.12 if big else 1
    out = [box(x, y, w, h, stroke=LINE, fill=PANEL, sw=1.5, r=14), f'<rect x="{x + 22}" y="{y + 22}" width="38" height="4" rx="2" fill="{col}"/>',
           text(n, x + 22, y + 64, 26 * s, "sans6", WHITE)[0], text(t, x + 22, y + h - 24, 14.5 * s, "mono", P)[0]]
    line, lines = "", []
    for word in d.split(" "):   # opis łamany do szerokości karty
        if text((line + " " + word).strip(), 0, 0, 17 * s)[1] > w - 44: lines.append(line); line = word
        else: line = (line + " " + word).strip()
    lines.append(line)
    out += [text(l, x + 22, y + 96 + i * 24 * s, 17 * s, "sans", TEXT)[0] for i, l in enumerate(lines)]
    return out

def build_cards(lang):
    c, h = COPY[lang], 400
    b = [DEFS]
    for i, row in enumerate(c["rows"]):
        b += card(4 + (i % 2) * 600, 4 + (i // 2) * 200, 592, 188, *row)
    svg(f"cards-{lang}.svg", h, b, c["projects"])
    b = [DEFS]
    for i, row in enumerate(c["rows"]):
        b += card(4, 4 + i * 214, M - 8, 202, *row, big=True)
    svg(f"cards-{lang}-m.svg", 4 * 214 + 4, b, c["projects"], M)

def gh_token():
    if os.environ.get("GITHUB_TOKEN"): return os.environ["GITHUB_TOKEN"]
    return subprocess.run(["gh", "auth", "token"], capture_output=True, text=True).stdout.strip()

def activity():
    q = '{ user(login: "%s") { contributionsCollection { totalCommitContributions contributionCalendar { totalContributions weeks { contributionDays { contributionCount } } } } } }' % sk.USER
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": q}).encode(), headers={"Authorization": "Bearer " + gh_token()})
    cc = json.load(urllib.request.urlopen(req, timeout=20))["data"]["user"]["contributionsCollection"]
    weeks = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in cc["contributionCalendar"]["weeks"]]
    pub = json.load(urllib.request.urlopen(f"https://api.github.com/users/{sk.USER}", timeout=20))["public_repos"]
    return cc["contributionCalendar"]["totalContributions"], cc["totalCommitContributions"], pub, weeks

def wave(weeks, x0, y0, w, h):
    weeks = [sum(weeks[max(0, i - 1):i + 2]) / len(weeks[max(0, i - 1):i + 2]) for i in range(len(weeks))]   # średnia z 3 tygodni: mniej poszarpana fala
    mx = max(weeks) or 1
    pts = [(x0 + i * w / (len(weeks) - 1), y0 + h - math.sqrt(v / mx) * h) for i, v in enumerate(weeks)]   # pierwiastek: pojedyncze piki nie spłaszczają reszty
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):   # wygładzona fala (krzywe przez środki odcinków)
        mxp = (ax + bx) / 2
        d += f"C{mxp:.1f} {ay:.1f} {mxp:.1f} {by:.1f} {bx:.1f} {by:.1f}"
    area = d + f"L{x0 + w} {y0 + h}L{x0} {y0 + h}Z"
    return (f'<defs><linearGradient id="wg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P}" stop-opacity=".35"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></linearGradient>'
            f'<linearGradient id="wl" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x0 + w}" y2="0"><stop offset="0" stop-color="{P}"/><stop offset="1" stop-color="{S}"/></linearGradient></defs>'
            f'<path d="{area}" fill="url(#wg)"/><path d="{d}" fill="none" stroke="url(#wl)" stroke-width="2.4" stroke-linejoin="round"/>')

def build_stats(lang, data, repos):
    c, (tot, com, pub, weeks) = COPY[lang], data
    when = lambda d: d.strftime("%d.%m") if lang == "pl" else d.strftime("%b %d")
    now_line = f'{c["now"]}: ' + "  ·  ".join(f"{n} {when(d)}" for n, d in repos)
    h = 300
    b = frame(W, h) + [text(c["activity"], 44, 64, 14, "sans6", P, ls=3.6)[0]]
    for i, (v, l) in enumerate(zip((tot, com, pub), c["stats"])):
        b += [text(str(v), 44 + i * 150, 140, 46, "sans6", WHITE)[0], text(l, 46 + i * 150, 170, 14, "sans", MUTED)[0]]
    b += [wave(weeks, 520, 64, 640, 130), text(c["weeks"], 1160, 222, 13, "mono", MUTED, anchor="end")[0],
          f'<line x1="44" y1="240" x2="1156" y2="240" stroke="{LINE}" stroke-width="1.2"/>', text(now_line, 44, 274, 17, "mono", TEXT)[0]]
    svg(f"stats-{lang}.svg", h, b, c["activity"])
    h = 470
    b = frame(M, h) + [text(c["activity"], 30, 56, 13, "sans6", P, ls=2.6)[0]]
    for i, (v, l) in enumerate(zip((tot, com, pub), c["stats"])):
        b += [text(str(v), 30 + i * 182, 126, 44, "sans6", WHITE)[0], text(l, 32 + i * 182, 154, 15, "sans", MUTED)[0]]
    b += [wave(weeks, 30, 190, M - 60, 150), text(c["weeks"], M - 30, 366, 14, "mono", MUTED, anchor="end")[0],
          f'<line x1="30" y1="386" x2="{M - 30}" y2="386" stroke="{LINE}" stroke-width="1.2"/>']
    b += [text(f'{c["now"]}: {n} · {when(d)}' if i == 0 else f"{n} · {when(d)}", 30 if i == 0 else 30 + text(c["now"] + ": ", 0, 0, 18, "mono")[1], 422 + i * 30, 18, "mono", TEXT)[0] for i, (n, d) in enumerate(repos)]
    svg(f"stats-{lang}-m.svg", h, b, c["activity"], M)

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("flow", "all"):
        for lang in COPY: build_flow(lang); build_flow_m(lang)
    if what in ("cards", "stats", "all"):
        data, repos = activity(), latest_repos()
        for lang in COPY:
            if what != "stats": build_header(lang); build_header_m(lang); build_cards(lang)
            build_stats(lang, data, repos)
