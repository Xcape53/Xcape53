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

# ---------- C: nagłówek jak terminal (linie pojawiają się po kolei, kursor mruga) ----------
ANIM = ("<style>.ln{opacity:0;animation:in .35s ease-out forwards}.cur{animation:bl 1s steps(1) infinite}"
        ".c{opacity:0;animation:in .4s ease-out forwards}"
        "@keyframes in{to{opacity:1}}@keyframes bl{50%{opacity:0}}"
        "@media (prefers-reduced-motion:reduce){.ln,.c{opacity:1;animation:none}.cur{animation:none}}</style>")
ROLE = {"en": "Software development & system integration", "pl": "Tworzenie oprogramowania i integracja systemów"}

def ln(i, body, step=.55):
    return f'<g class="ln" style="animation-delay:{.3 + i * step:.2f}s">{body}</g>'

def prompt(cmd, x, y, size=19):
    return text("$", x, y, size, "mono", P)[0] + text(cmd, x + size * 1.1, y, size, "mono", TEXT)[0]

def term_bar(w):
    return "".join(f'<circle cx="{34 + i * 22}" cy="34" r="6" fill="{c}" opacity=".85"/>' for i, c in enumerate((P, S, MUTED))) + \
           text("xcape@gdynia: ~", w / 2, 40, 14, "mono", MUTED, anchor="middle")[0] + f'<line x1="1" y1="62" x2="{w - 1}" y2="62" stroke="{LINE}" stroke-width="1.2"/>'

def build_header(lang):
    h = 330
    b = frame(W, h) + [ANIM, term_bar(W),
         ln(0, prompt("whoami", 44, 112)), ln(1, text("PIOTR JELENIEWICZ", 42, 176, 54, "display", WHITE)[0]),
         ln(2, prompt("cat role.txt", 44, 226)), ln(3, text(ROLE[lang], 44, 262, 22, "sans", TEXT)[0]),
         ln(4, text("$", 44, 304, 19, "mono", P)[0] + f'<rect class="cur" x="68" y="288" width="11" height="20" fill="{P}"/>'),
         f'<image href="{logo_uri()}" x="930" y="92" width="200" height="200"/>', f'<circle cx="1030" cy="192" r="112" fill="none" stroke="{LINE}" stroke-width="1.5"/>']
    svg(f"header-{lang}.svg", h, b, "Piotr Jeleniewicz")

def build_header_m(lang):
    h = 430
    b = frame(M, h) + [ANIM, term_bar(M), f'<image href="{logo_uri()}" x="468" y="78" width="96" height="96"/>',
         ln(0, prompt("whoami", 32, 112, 18)), ln(1, text("PIOTR", 30, 186, 54, "display", WHITE)[0] + text("JELENIEWICZ", 30, 244, 54, "display", WHITE)[0]),
         ln(2, prompt("cat role.txt", 32, 300, 18))]
    words, lines, cur = ROLE[lang].split(" "), [], ""
    for wd in words:
        if text((cur + " " + wd).strip(), 0, 0, 22)[1] > M - 64: lines.append(cur); cur = wd
        else: cur = (cur + " " + wd).strip()
    lines.append(cur)
    b.append(ln(3, "".join(text(l, 32, 336 + i * 30, 22, "sans", TEXT)[0] for i, l in enumerate(lines))))
    yc = 336 + len(lines) * 30 + 12
    b.append(ln(4, text("$", 32, yc, 18, "mono", P)[0] + f'<rect class="cur" x="54" y="{yc - 16}" width="10" height="19" fill="{P}"/>'))
    svg(f"header-{lang}-m.svg", h, b, "Piotr Jeleniewicz", M)

# ---------- dane ----------
def activity():
    q = '{ user(login: "%s") { contributionsCollection { totalCommitContributions contributionCalendar { totalContributions weeks { contributionDays { date contributionCount } } } } } }' % sk.USER
    req = urllib.request.Request("https://api.github.com/graphql", data=json.dumps({"query": q}).encode(), headers={"Authorization": "Bearer " + gh_token()})
    cc = json.load(urllib.request.urlopen(req, timeout=20))["data"]["user"]["contributionsCollection"]
    weeks = [(w["contributionDays"][0]["date"], [d["contributionCount"] for d in w["contributionDays"]]) for w in cc["contributionCalendar"]["weeks"]]
    pub = json.load(urllib.request.urlopen(f"https://api.github.com/users/{sk.USER}", timeout=20))["public_repos"]
    return dict(total=cc["contributionCalendar"]["totalContributions"], commits=cc["totalCommitContributions"], pub=pub, weeks=weeks)

def api(url):
    req = urllib.request.Request("https://api.github.com" + url, headers={"Authorization": "Bearer " + gh_token(), "Accept": "application/vnd.github+json"})
    return json.load(urllib.request.urlopen(req, timeout=30))

def commit_hours():
    # godziny commitów z publicznych repozytoriów, ostatnie 12 miesięcy, czas polski (CEST kwiecień-październik, ponytail: przybliżenie DST)
    since = (datetime.now(timezone.utc) - timedelta(days=365)).strftime("%Y-%m-%dT%H:%M:%SZ")
    hours = [0] * 24
    for r in api(f"/users/{sk.USER}/repos?per_page=100&type=owner"):
        if r["fork"] or r["private"]: continue
        for page in range(1, 11):
            batch = api(f"/repos/{sk.USER}/{r['name']}/commits?author={sk.USER}&since={since}&per_page=100&page={page}")
            for c in batch:
                d = datetime.strptime(c["commit"]["author"]["date"], "%Y-%m-%dT%H:%M:%SZ")
                hours[(d.hour + (2 if 4 <= d.month <= 10 else 1)) % 24] += 1
            if len(batch) < 100: break
    return hours

MONTHS = {"en": "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split(), "pl": "sty lut mar kwi maj cze lip sie wrz paź lis gru".split()}

def nice(v):
    e = 10 ** math.floor(math.log10(max(v, 1)))
    return next(m * e for m in (1, 2, 2.5, 5, 10) if m * e >= v)

def month_ticks(dates, lang, every=1):
    out, prev, k = [], None, 0
    for i, d in enumerate(dates):
        m = int(d[5:7])
        if m != prev and i > 0:
            if k % every == 0: out.append((i, MONTHS[lang][m - 1]))
            k += 1
        prev = m
    return out

def chart(weeks, lang, x0, y0, w, h, every=1):
    vals = [sum(c) for _, c in weeks]
    vals = [sum(vals[max(0, i - 1):i + 2]) / len(vals[max(0, i - 1):i + 2]) for i in range(len(vals))]   # średnia z 3 tygodni
    step = nice(max(vals) / 2); top = step * 2
    X = lambda i: x0 + i * w / (len(vals) - 1); Y = lambda v: y0 + h - v / top * h
    out = []
    for k in range(3):   # oś Y: 0, połowa, góra
        yy, dash = Y(k * step), "" if k == 0 else 'stroke-dasharray="3 5"'
        out += [f'<line x1="{x0}" y1="{yy:.1f}" x2="{x0 + w}" y2="{yy:.1f}" stroke="{LINE}" stroke-width="1" {dash}/>',
                text(f"{k * step:g}", x0 - 10, yy + 4, 12, "mono", MUTED, anchor="end")[0]]
    for i, lab in month_ticks([d for d, _ in weeks], lang, every):   # oś X: miesiące
        out += [f'<line x1="{X(i):.1f}" y1="{y0 + h}" x2="{X(i):.1f}" y2="{y0 + h + 5}" stroke="{MUTED}" stroke-width="1"/>',
                text(lab, X(i), y0 + h + 22, 12, "mono", MUTED, anchor="middle")[0]]
    pts = [(X(i), Y(v)) for i, v in enumerate(vals)]
    d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}" + "".join(f"C{(ax + bx) / 2:.1f} {ay:.1f} {(ax + bx) / 2:.1f} {by:.1f} {bx:.1f} {by:.1f}" for (ax, ay), (bx, by) in zip(pts, pts[1:]))
    out.append(f'<defs><linearGradient id="wg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{P}" stop-opacity=".35"/><stop offset="1" stop-color="{P}" stop-opacity="0"/></linearGradient>'
               f'<linearGradient id="wl" gradientUnits="userSpaceOnUse" x1="{x0}" y1="0" x2="{x0 + w}" y2="0"><stop offset="0" stop-color="{P}"/><stop offset="1" stop-color="{S}"/></linearGradient></defs>'
               f'<path d="{d}L{x0 + w} {y0 + h}L{x0} {y0 + h}Z" fill="url(#wg)"/><path d="{d}" fill="none" stroke="url(#wl)" stroke-width="2.4" stroke-linejoin="round"/>')
    return out

TITLES = {"en": dict(heat="CONTRIBUTION CALENDAR", hours="WHEN I COMMIT", peak="busiest hour", unit="commits", none="less", more="more"),
          "pl": dict(heat="KALENDARZ KONTRYBUCJI", hours="KIEDY COMMITUJĘ", peak="najczęściej", unit="commitów", none="mniej", more="więcej")}

def build_stats(lang, data, repos):
    c = COPY[lang]; when = lambda d: d.strftime("%d.%m") if lang == "pl" else d.strftime("%b %d")
    nums = (data["total"], data["commits"], data["pub"])
    h = 360
    b = frame(W, h) + [text(c["activity"], 44, 62, 14, "sans6", P, ls=3.6)[0]]
    for i, (v, l) in enumerate(zip(nums, c["stats"])):
        b += [text(str(v), 44 + i * 140, 150, 44, "sans6", WHITE)[0], text(l, 46 + i * 140, 178, 14, "sans", MUTED)[0]]
    b += chart(data["weeks"], lang, 560, 60, 600, 190) + [text(c["weeks"], 44, 230, 13, "mono", MUTED)[0],
          f'<line x1="44" y1="296" x2="1156" y2="296" stroke="{LINE}" stroke-width="1.2"/>',
          text(f'{c["now"]}: ' + "  ·  ".join(f"{n} {when(d)}" for n, d in repos), 44, 330, 17, "mono", TEXT)[0]]
    svg(f"stats-{lang}.svg", h, b, c["activity"])
    h = 540
    b = frame(M, h) + [text(c["activity"], 30, 56, 13, "sans6", P, ls=2.6)[0]]
    for i, (v, l) in enumerate(zip(nums, c["stats"])):
        b += [text(str(v), 30 + i * 182, 124, 42, "sans6", WHITE)[0], text(l, 32 + i * 182, 152, 15, "sans", MUTED)[0]]
    b += chart(data["weeks"], lang, 74, 190, M - 104, 180, every=2) + [f'<line x1="30" y1="420" x2="{M - 30}" y2="420" stroke="{LINE}" stroke-width="1.2"/>']
    b += [text((f'{c["now"]}: ' if i == 0 else "") + f"{n} · {when(d)}", 30 if i == 0 else 30 + text(c["now"] + ": ", 0, 0, 18, "mono")[1], 458 + i * 32, 18, "mono", TEXT)[0] for i, (n, d) in enumerate(repos)]
    svg(f"stats-{lang}-m.svg", h, b, c["activity"], M)

LEVELS = ("#0f1a2e", "#123a86", "#1f5fd6", P, S)
def level(v):
    return 0 if v == 0 else 1 if v <= 2 else 2 if v <= 5 else 3 if v <= 10 else 4

def heat(weeks, lang, x0, y0, cell=17, gap=4):
    out, step = [], cell + gap
    for i, (_, days) in enumerate(weeks):
        for j, v in enumerate(days):
            out.append(f'<rect class="c" style="animation-delay:{.2 + i * .022 + j * .01:.2f}s" x="{x0 + i * step}" y="{y0 + j * step}" width="{cell}" height="{cell}" rx="3.5" fill="{LEVELS[level(v)]}"/>')
    for i, lab in month_ticks([d for d, _ in weeks], lang):
        out.append(text(lab, x0 + i * step, y0 - 10, 12, "mono", MUTED)[0])
    return out

def legend(lang, x, y):
    t = TITLES[lang]
    out = [text(t["none"], x - 8, y + 12, 12, "mono", MUTED, anchor="end")[0]]
    out += [f'<rect x="{x + k * 18}" y="{y}" width="14" height="14" rx="3" fill="{c}"/>' for k, c in enumerate(LEVELS)]
    return out + [text(t["more"], x + 5 * 18 + 6, y + 12, 12, "mono", MUTED)[0]]

def build_heat(lang, data):
    t, wk = TITLES[lang], data["weeks"][-53:]
    h = 270
    b = frame(W, h) + [ANIM, text(t["heat"], 44, 62, 14, "sans6", P, ls=3.6)[0]] + heat(wk, lang, 44, 100) + legend(lang, 1040, 244)
    svg(f"heat-{lang}.svg", h, b, t["heat"])
    wk = data["weeks"][-26:]
    h = 290
    b = frame(M, h) + [ANIM, text(t["heat"], 27, 56, 13, "sans6", P, ls=2.6)[0]] + heat(wk, lang, 27, 96) + legend(lang, 460, 264)
    svg(f"heat-{lang}-m.svg", h, b, t["heat"], M)

def bars(hours, x0, y0, w, h, every=3):
    mx, bw = max(hours) or 1, w / 24
    out = [f'<defs><linearGradient id="bg" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{P}"/><stop offset="1" stop-color="{S}"/></linearGradient></defs>',
           f'<line x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}" stroke="{LINE}" stroke-width="1.2"/>']
    for i, v in enumerate(hours):
        bh = max(2, v / mx * h)
        out.append(f'<rect class="c" style="animation-delay:{.2 + i * .04:.2f}s" x="{x0 + i * bw + bw * .18:.1f}" y="{y0 + h - bh:.1f}" width="{bw * .64:.1f}" height="{bh:.1f}" rx="3" fill="url(#bg)" opacity="{1 if v else .25}"/>')
        if i % every == 0:
            out.append(text(f"{i:02d}", x0 + i * bw + bw / 2, y0 + h + 22, 12, "mono", MUTED, anchor="middle")[0])
    return out

def build_hours(lang, hours):
    t = TITLES[lang]; peak = max(range(24), key=lambda i: hours[i])
    note = f'{t["peak"]}: {peak:02d}:00-{(peak + 1) % 24:02d}:00 · {sum(hours)} {t["unit"]}'
    h = 280
    b = frame(W, h) + [ANIM, text(t["hours"], 44, 62, 14, "sans6", P, ls=3.6)[0], text(note, 1156, 62, 14, "mono", MUTED, anchor="end")[0]] + bars(hours, 44, 90, 1112, 140)
    svg(f"hours-{lang}.svg", h, b, t["hours"])
    h = 320
    b = frame(M, h) + [ANIM, text(t["hours"], 30, 56, 13, "sans6", P, ls=2.6)[0], text(note, 30, 84, 13, "mono", MUTED)[0]] + bars(hours, 30, 112, M - 60, 150, every=6)
    svg(f"hours-{lang}-m.svg", h, b, t["hours"], M)

if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    if what in ("flow", "all"):
        for lang in COPY: build_flow(lang); build_flow_m(lang)
    if what in ("cards", "stats", "all"):
        data, repos, hours = activity(), latest_repos(), commit_hours()
        for lang in COPY:
            if what != "stats": build_header(lang); build_header_m(lang); build_cards(lang)
            build_stats(lang, data, repos); build_heat(lang, data); build_hours(lang, hours)
