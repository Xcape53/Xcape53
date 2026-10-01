"""Render a static isometric alternative from sanitized public commit counts."""
import json
from datetime import date,timedelta
from pathlib import Path
from build_visuals import PALETTES,svg,text

ROOT=Path(__file__).resolve().parents[1]


def render(data,theme):
    p=PALETTES[theme]
    end=date.today()
    start=end-timedelta(days=364)
    start-=timedelta(days=(start.weekday()+1)%7)
    counts=data['counts']
    body=text(32,42,'PUBLIC COMMITS / ISOMETRIC CALENDAR',17,p['sub'],600,'letter-spacing="2"')
    for week in range(53):
        for day in range(7):
            current=start+timedelta(days=week*7+day)
            if current>end:
                continue
            count=counts.get(current.isoformat(),0)
            x=40+week*19.7+day*10
            y=114+day*18-week*.25
            height=min(42,6+count*3) if count else 0
            color=p['purple'] if count>=4 else p['blue'] if count else p['line']
            points=f'{x},{y-height} {x+16},{y-5-height} {x+23},{y+4-height} {x+7},{y+9-height}'
            if height:
                body+=f'<path d="M{x+7} {y+9-height}L{x+23} {y+4-height}V{y+4}L{x+7} {y+9}Z" fill="{color}" opacity="0.55"/><path d="M{x} {y-height}L{x+7} {y+9-height}V{y+9}L{x} {y}Z" fill="{color}" opacity="0.35"/>'
            body+=f'<polygon points="{points}" fill="{color}" opacity="{0.95 if count else 0.4}"><title>{current.isoformat()}: {count} public commits</title></polygon>'
    body+=text(32,292,'Each tile is one day. Column height reflects public commits.',17,p['sub'])
    body+=text(1165,292,f'{sum(counts.values())} commits / past year',17,p['sub'],500,'text-anchor="end"')
    return svg(1200,321,body,'Isometric calendar of public commits','A static alternative to the arcade. Uses only publicly searchable commits.',theme)


if __name__=='__main__':
    data=json.loads((ROOT/'assets/data/public-commits.json').read_text())
    for theme in PALETTES:
        (ROOT/f'assets/calendar-{theme}.svg').write_text(render(data,theme),encoding='utf-8')
