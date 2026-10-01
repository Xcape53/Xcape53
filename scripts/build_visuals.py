"""Build original SVG artwork for the engineering profile. No remote assets."""

from html import escape
from pathlib import Path
import base64
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
PALETTES = {
    'dark': {'bg': '#0d1117', 'panel': '#141c2b', 'line': '#29364c', 'fg': '#eef3fb', 'sub': '#9aaec9', 'blue': '#60a5fa', 'purple': '#a78bfa'},
    'light': {'bg': '#ffffff', 'panel': '#f2f6fd', 'line': '#d2deef', 'fg': '#15243d', 'sub': '#526985', 'blue': '#2563eb', 'purple': '#7c3aed'},
}


def text(x, y, value, size, fill, weight=400, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}" font-weight="{weight}" {extra}>{escape(value)}</text>'


def svg(width, height, body, title, desc, theme='dark'):
    p = PALETTES[theme]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc)}</desc>
<defs><linearGradient id="signal"><stop stop-color="{p['blue']}"/><stop offset="1" stop-color="{p['purple']}"/></linearGradient>
<pattern id="grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" fill="none" stroke="{p['line']}" stroke-width="0.6"/></pattern></defs>
<style>text{{font-family:Inter,Segoe UI,Arial,sans-serif}} .mono{{font-family:Consolas,monospace}} @media(prefers-reduced-motion:reduce){{.moving{{display:none}}}}</style>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="20" fill="{p['bg']}" stroke="{p['line']}"/>
{body}</svg>'''


def header(theme, static=False):
    p = PALETTES[theme]
    body = f'<rect x="665" y="2" width="533" height="356" rx="18" fill="url(#grid)" opacity="0.6"/>'
    body += text(42, 57, 'PIOTR JELENIEWICZ / XCAPE53', 17, p['sub'], 600, 'letter-spacing="3"')
    body += text(40, 135, 'Software development', 49, p['fg'], 700)
    body += text(40, 195, '& system integration', 49, p['fg'], 700)
    body += '<rect x="42" y="226" width="64" height="4" rx="2" fill="url(#signal)"/>'
    body += text(42, 277, 'PYTHON', 18, p['blue'], 600, 'letter-spacing="2"')
    body += text(160, 277, 'JAVASCRIPT', 18, p['blue'], 600, 'letter-spacing="2"')
    body += text(325, 277, 'REST APIs', 18, p['purple'], 600, 'letter-spacing="2"')
    body += text(42, 322, 'Electronics background. Applications, APIs and automation.', 18, p['sub'])
    body += f'<g fill="none" stroke="{p["line"]}" stroke-width="2"><path d="M706 42H754L790 78H894V136H949L984 171H1159"/><path d="M693 290H780L819 251H877V199H950"/><path d="M1159 59H1075L1038 96H987V136"/><path d="M1128 323H1050L1017 290H923V252"/></g>'
    for x, y in [(706,42),(1159,171),(693,290),(1159,59),(1128,323)]:
        body += f'<circle cx="{x}" cy="{y}" r="5" fill="{p["bg"]}" stroke="{p["blue"]}" stroke-width="2"/>'
    body += f'<rect x="818" y="126" width="184" height="109" rx="14" fill="{p["panel"]}" stroke="{p["purple"]}" stroke-width="1.5"/>'
    body += text(910, 167, 'SYSTEM', 17, p['sub'], 600, 'text-anchor="middle" letter-spacing="4"')
    wave = 'M837 199H851L858 185L866 213L875 177L886 219L896 190L904 199H923L932 185L940 207L950 199H983'
    body += f'<path d="{wave}" stroke="url(#signal)" stroke-width="2.5" fill="none"/>'
    for x,y,label in [(715,110,'INPUT'),(1030,197,'API'),(940,305,'OUTPUT')]:
        body += text(x,y,label,14,p['sub'],500,'class="mono" letter-spacing="2"')
    if not static:
        for path,duration,delay in [('M706 42H754L790 78H894V126', '6s','0s'),('M1002 171H1159','5s','2s'),('M877 235V251H819L780 290H693','7s','1s')]:
            body += f'<circle r="4" fill="{p["blue"]}" class="moving"><animateMotion dur="{duration}" begin="{delay}" repeatCount="indefinite" path="{path}"/></circle>'
    return svg(1200,360,body,'Piotr Jeleniewicz: software development and system integration','Electronic circuit panel with a subtle signal animation. Python, JavaScript and REST APIs.',theme)


def project(name, theme):
    """Editorial project covers: two original motifs and two real interfaces."""
    dark = theme == 'dark'
    ink = '#f4f6fb' if dark else '#182335'
    muted = '#aab4c4' if dark else '#536174'
    surfaces = {
        'yapper': ('#172237', '#eff4fc', '#83abff', '#365fba'),
        'seesky': ('#1c1a2b', '#f7f1f5', '#e17fa7', '#a3295a'),
        'jobmanager': ('#182520', '#eef6f1', '#84caa4', '#347553'),
        'portfolio': ('#202035', '#f2f1fa', '#b4acf0', '#6353b6'),
    }
    bg_dark, bg_light, accent_dark, accent_light = surfaces[name]
    bg, accent = (bg_dark, accent_dark) if dark else (bg_light, accent_light)
    title, subtitle = {
        'yapper': ('Yapper', 'Speech to text for Windows'),
        'seesky': ('SeeSky', 'Radio telescope software'),
        'jobmanager': ('JobManager', 'Job search and offer research'),
        'portfolio': ('Portfolio', 'Selected work in Polish and English'),
    }[name]
    body = f'<rect width="600" height="320" rx="12" fill="{bg}"/>'
    body += text(30, 61, title, 44, ink, 600, 'letter-spacing="-1.5"')
    body += text(32, 93, subtitle, 19, muted)
    body += f'<path d="M32 116H568" stroke="{accent}" stroke-opacity="0.26"/>'
    if name == 'yapper':
        # An illustrated voice signal, not a recording or invented app screenshot.
        amplitudes = [6, 8, 5, 11, 18, 31, 46, 34, 58, 76, 61, 35, 20, 29,
                      47, 65, 49, 26, 13, 8, 6, 12, 24, 39, 53, 32, 18, 8]
        for i, amplitude in enumerate(amplitudes):
            x = 34 + i * 10
            body += f'<rect x="{x}" y="{218-amplitude/2}" width="4" height="{amplitude}" rx="2" fill="{accent}"/>'
        body += f'<path d="M333 218H365M357 210L365 218L357 226" fill="none" stroke="{muted}" stroke-width="1.5"/>'
        body += text(387, 235, 'Text', 48, ink, 600, 'letter-spacing="-1"')
        body += f'<path d="M493 200V241" stroke="{accent}" stroke-width="2"/>'
        body += text(32, 288, 'Two push-to-talk channels', 16, muted)
    elif name == 'seesky':
        # Original path geometry and colours from the public SeeSky project mark.
        body += '<g transform="translate(396 142) scale(1.35)"><g transform="translate(-25.971687,-15.020365)">'
        triangle = 'M127.99846,74.744104 76.996428,104.20427 76.984194,45.305132Z'
        body += f'<path fill="#7b1b38" d="{triangle}"/>'
        body += f'<path fill="#b22f57" d="{triangle}" transform="rotate(180,76.991193,74.754134)"/>'
        body += '<path fill="#b22f57" d="m109.99519,76.610842 -26.230151,15.139174 0.0042,-30.285564z" transform="matrix(1,0,0,-1,-6.7812061,106.77038)"/>'
        body += '<path fill="#b22f57" d="M117.85623,76.958871 79.533118,98.38386 80.140088,54.482579Z" transform="rotate(-90,90.701625,116.46298)"/>'
        body += f'<path fill="#7b1b38" d="{triangle}" transform="translate(-51.012506,-29.438889)"/>'
        body += '</g>'
        body += '</g>'
        body += f'<g fill="none" stroke="{accent}" stroke-width="0.8" opacity="0.42"><path d="M31 229C140 125 268 137 327 251"/><path d="M40 166C156 213 278 281 333 291"/><path d="M102 133C103 212 145 278 184 304"/><path d="M235 133C213 205 207 260 218 306"/></g>'
        for x, y, radius in [(72,198,2.5),(117,174,1.8),(167,191,3.2),(211,220,2),(279,247,2.8),(309,167,1.2),(51,269,1.3),(253,155,1.2)]:
            body += f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{accent}"/>'
        body += text(568, 57, 'SimLE', 18, accent, 600, 'text-anchor="end"')
    else:
        filename = 'jobmanager-analysis.png' if name == 'jobmanager' else 'portfolio.jpg'
        image_path = OUT / 'screenshots' / filename
        mime = 'image/png' if image_path.suffix == '.png' else 'image/jpeg'
        payload = base64.b64encode(image_path.read_bytes()).decode('ascii')
        clip_id = f'{name}-interface-clip'
        body += f'<defs><clipPath id="{clip_id}"><rect x="32" y="138" width="536" height="182" rx="7"/></clipPath></defs>'
        body += f'<rect x="32" y="138" width="536" height="280" rx="7" fill="#050b13" stroke="{accent}" stroke-opacity="0.2"/>'
        # The portfolio crop omits only the captured browser scrollbar at right.
        width, height = (536, 234) if name == 'jobmanager' else (544, 306)
        body += f'<image href="data:{mime};base64,{payload}" x="32" y="138" width="{width}" height="{height}" clip-path="url(#{clip_id})"/>'
    description = subtitle + '. '
    description += ('Original voice illustration.' if name == 'yapper' else
                    'SeeSky project emblem and illustrative sky coordinates.' if name == 'seesky' else
                    'Original public application screenshot, shown in an editorial crop.')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="600" height="320" viewBox="0 0 600 320" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<style>text{{font-family:Segoe UI,Arial,sans-serif}}</style>
{body}</svg>'''


def workflow(theme):
    p=PALETTES[theme]
    body=text(34,42,'AI-ASSISTED DEVELOPMENT / HUMAN-LED INTEGRATION',14,p['sub'],600,'letter-spacing="2"')
    stages=[('01','Requirements','Goal + constraints'),('02','Modules','Responsibilities'),('03','Implementation','Code + debugging'),('04','Integration','APIs + data flow'),('05','Validation','Behaviour + tests')]
    for i,(number,title,subtitle) in enumerate(stages):
        x=34+i*235
        body+=f'<rect x="{x}" y="68" width="190" height="106" rx="12" fill="{p["panel"]}" stroke="{p["line"]}"/>'
        body+=text(x+16,94,number,13,p['purple'],600,'class="mono"')
        body+=text(x+16,126,title,21,p['fg'],600)
        body+=text(x+16,153,subtitle,14,p['sub'])
        if i<4:
            body+=f'<path d="M{x+200} 120H{x+224}L{x+218} 114M{x+224} 120L{x+218} 126" fill="none" stroke="{p["blue"]}" stroke-width="2"/>'
    body+=f'<path d="M1064 184V216H129V184M123 191L129 184L135 191" stroke="{p["purple"]}" fill="none" stroke-width="1.5"/>'
    body+=text(591,207,'REVIEW / ITERATE',12,p['sub'],500,'text-anchor="middle" letter-spacing="2"')
    return svg(1200,241,body,'How I develop systems with AI','Requirements, modules, implementation, integration and validation, followed by review and iteration.',theme)


def mobile_header(theme, static=False):
    p=PALETTES[theme]
    body=text(30,49,'PIOTR JELENIEWICZ / XCAPE53',17,p['sub'],600,'letter-spacing="1.8"')
    body+=text(28,118,'Software development',41,p['fg'],700)
    body+=text(28,170,'& system integration',41,p['fg'],700)
    body+='<rect x="30" y="197" width="65" height="4" fill="url(#signal)" rx="2"/>'
    body+=text(30,239,'PYTHON / JAVASCRIPT / REST APIs',18,p['blue'],600,'class="mono"')
    body+=text(30,276,'Electronics, applications and automation.',19,p['sub'])
    body+=f'<path d="M30 331H127L160 309H349L380 331H567" stroke="{p["line"]}" stroke-width="2" fill="none"/>'
    if not static:
        body+=f'<circle r="4" fill="{p["purple"]}" class="moving"><animateMotion dur="7s" repeatCount="indefinite" path="M30 331H127L160 309H349L380 331H567"/></circle>'
    return svg(600,364,body,'Software development and system integration','Python, JavaScript, REST APIs and an electronics background.',theme)


def mobile_workflow(theme):
    p=PALETTES[theme]
    body=text(28,43,'AI-ASSISTED DEVELOPMENT',20,p['sub'],600)
    stages=[('Requirements','Goal and constraints'),('Modules','Responsibilities and interfaces'),('Implementation','AI-assisted code and debugging'),('Integration','APIs and data flow'),('Validation','Behaviour, tests and iteration')]
    for i,(title,subtitle) in enumerate(stages):
        y=67+i*87
        body+=f'<rect x="28" y="{y}" width="544" height="71" rx="11" fill="{p["panel"]}" stroke="{p["line"]}"/>'
        body+=text(43,y+42,f'0{i+1}',18,p['purple'],600,'class="mono"')
        body+=text(92,y+28,title,23,p['fg'],600)
        body+=text(92,y+54,subtitle,18,p['sub'])
        if i<4:
            body+=f'<path d="M60 {y+71}V{y+87}" stroke="{p["blue"]}" stroke-width="2"/>'
    return svg(600,510,body,'AI-assisted development workflow','Requirements, modules, implementation, integration and validation.',theme)


def social(name):
    p=PALETTES['dark']
    body=text(42,58,'XCAPE53 / ENGINEERING PROJECTS',22,p['sub'],600,'letter-spacing="3"')
    def artwork(source,transform):
        ET.register_namespace('', 'http://www.w3.org/2000/svg')
        root=ET.fromstring(source)
        for child in list(root):
            if child.tag.split('}')[-1] in ('title', 'desc'):
                root.remove(child)
        root.attrib.pop('aria-labelledby', None)
        root.attrib.pop('role', None)
        content=ET.tostring(root,encoding='unicode')
        return f'<g transform="{transform}">{content}</g>'
    if name=='profile':
        body+=artwork(header('dark',True),'translate(30 112) scale(0.95)')
        body+=text(42,555,'Applications / API integration / automation',28,p['blue'],500)
    else:
        body+=artwork(project(name,'dark'),'translate(144 90) scale(1.52)')
    body+=text(42,603,'github.com/Xcape53',20,p['sub'],500)
    body+=text(1158,603,'piotrjeleniewicz.com',20,p['sub'],500,'text-anchor="end"')
    return svg(1200,630,body,name+' project preview','Public engineering project by Piotr Jeleniewicz. Project artwork and original public interface screenshots.')


def main():
    (OUT/'projects').mkdir(parents=True,exist_ok=True)
    (OUT/'social').mkdir(parents=True,exist_ok=True)
    for theme in PALETTES:
        for static in (False,True):
            (OUT/f'header-{theme}{"-static" if static else ""}.svg').write_text(header(theme,static),encoding='utf-8')
            (OUT/f'header-mobile-{theme}{"-static" if static else ""}.svg').write_text(mobile_header(theme,static),encoding='utf-8')
        (OUT/f'workflow-{theme}.svg').write_text(workflow(theme),encoding='utf-8')
        (OUT/f'workflow-mobile-{theme}.svg').write_text(mobile_workflow(theme),encoding='utf-8')
        for name in ('yapper','seesky','jobmanager','portfolio'):
            (OUT/'projects'/f'{name}-{theme}.svg').write_text(project(name,theme),encoding='utf-8')
    for name in ('profile','yapper','seesky','portfolio'):
        (OUT/'social'/f'{name}.svg').write_text(social(name),encoding='utf-8')
    for path in OUT.rglob('*.svg'):
        ET.fromstring(path.read_text(encoding='utf-8'))
    print('Original artwork generated and SVG XML verified.')


if __name__=='__main__':
    main()
