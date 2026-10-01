"""Build original SVG artwork for the engineering profile. No remote assets."""

from html import escape
from pathlib import Path
import math
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
    p = PALETTES[theme]
    labels = {'yapper': ('01 / DESKTOP AUDIO','Yapper','Speech to text'), 'seesky': ('02 / SCIENTIFIC SOFTWARE','SeeSky','Radio telescope software'), 'jobmanager': ('03 / PERSONAL AUTOMATION','JobManager','Job listing analysis'), 'portfolio': ('04 / WEB','Portfolio','Projects in Polish and English')}
    kicker, title, subtitle = labels[name]
    body = f'<rect x="305" y="2" width="293" height="296" rx="18" fill="url(#grid)" opacity="0.6"/>'
    body += text(28,42,kicker,11,p['sub'],600,'letter-spacing="1.4"')
    body += text(28,94,title,38,p['fg'],700)
    body += text(28,124,subtitle,17,p['sub'])
    body += '<rect x="28" y="145" width="52" height="3" fill="url(#signal)" rx="1.5"/>'
    if name == 'yapper':
        for y,label in [(178,'PTT 01'),(228,'PTT 02')]:
            body += f'<rect x="28" y="{y}" width="111" height="36" rx="7" fill="{p["panel"]}" stroke="{p["line"]}"/>'
            body += text(43,y+23,label,14,p['blue'],600,'class="mono"')
            body += f'<path d="M139 {y+18}H164L189 220H309" stroke="{p["blue"]}" fill="none" stroke-width="2"/>'
        body += f'<rect x="308" y="158" width="262" height="107" rx="12" fill="{p["panel"]}" stroke="{p["line"]}"/>'
        body += text(328,185,'TRANSCRIPT > CLIPBOARD',12,p['purple'],500,'class="mono"')
        for i,width in enumerate([212,172,190]):
            body += f'<rect x="328" y="{202+i*16}" width="{width}" height="5" rx="2" fill="{p["line"]}"/>'
    elif name == 'seesky':
        cx,cy=438,188
        for radius in (42,73,106):
            body += f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{p["line"]}"/>'
        for angle in range(0,360,45):
            rad=math.radians(angle)
            body += f'<path d="M{cx} {cy}L{cx+106*math.cos(rad):.1f} {cy+106*math.sin(rad):.1f}" stroke="{p["line"]}"/>'
        for dx,dy,r in [(22,-18,4),(-48,-58,2),(62,34,2),(-63,18,3),(7,59,2),(61,-65,2)]:
            body += f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{r}" fill="{p["blue"]}"/>'
        body += f'<circle cx="460" cy="170" r="12" fill="none" stroke="{p["purple"]}"/><path d="M460 150V161M460 179V190M440 170H451M469 170H480" stroke="{p["purple"]}"/>'
        body += text(28,199,'SKY MAP',15,p['blue'],600,'class="mono"')
        body += text(28,229,'PYTHON REST API',14,p['sub'],500,'class="mono"')
        body += text(28,259,'WEB DASHBOARD',14,p['sub'],500,'class="mono"')
    elif name == 'jobmanager':
        body += text(28,208,'SOURCES',14,p['blue'],600,'class="mono"')
        body += text(28,234,'FILTERS',14,p['sub'],500,'class="mono"')
        body += text(28,260,'RESEARCH',14,p['sub'],500,'class="mono"')
        for i,width in enumerate([242,206,223]):
            y=156+i*40
            body += f'<rect x="313" y="{y}" width="{width}" height="31" rx="6" fill="{p["panel"]}" stroke="{p["line"]}"/><circle cx="329" cy="{y+15}" r="4" fill="{p["purple"]}"/><path d="M342 {y+11}H{313+width-18}M342 {y+20}H{313+width-48}" stroke="{p["sub"]}" stroke-width="2"/>'
    else:
        body += text(28,208,'PL / EN',20,p['blue'],600,'class="mono"')
        body += text(28,242,'HTML / CSS / JS',14,p['sub'],500,'class="mono"')
        body += f'<rect x="314" y="128" width="260" height="135" rx="9" fill="{p["panel"]}" stroke="{p["line"]}"/><path d="M314 149H574" stroke="{p["line"]}"/>'
        for x in (326,337,348):
            body += f'<circle cx="{x}" cy="139" r="2.5" fill="{p["sub"]}"/>'
        body += f'<path d="M333 166H422M333 178H401M333 194H377M333 235H413" stroke="{p["sub"]}" stroke-width="4"/>'
        body += f'<path d="M462 164V192H443V231H515V211H552M443 219H422M494 231V249" stroke="{p["purple"]}" fill="none" stroke-width="2"/><circle cx="484" cy="202" r="20" fill="none" stroke="{p["blue"]}"/>'
    return svg(600,300,body,title,subtitle+'. Original functional illustration; not an application screenshot.',theme)


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
        content=''.join(ET.tostring(child,encoding='unicode') for child in root if child.tag.split('}')[-1] not in ('title','desc','defs','style'))
        return f'<g transform="{transform}">{content}</g>'
    if name=='profile':
        body+=artwork(header('dark',True),'translate(30 112) scale(0.95)')
        body+=text(42,555,'Applications / API integration / automation',28,p['blue'],500)
    else:
        body+=artwork(project(name,'dark'),'translate(144 90) scale(1.52)')
    body+=text(42,603,'github.com/Xcape53',20,p['sub'],500)
    body+=text(1158,603,'piotrjeleniewicz.com',20,p['sub'],500,'text-anchor="end"')
    return svg(1200,630,body,name+' project preview','Public engineering project by Piotr Jeleniewicz. Original functional illustration.')


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
