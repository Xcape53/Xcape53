"""Validate generated artwork and public profile references before publication."""
from pathlib import Path
import re
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
errors=[]
svg_count=0
for path in (ROOT/'assets').rglob('*.svg'):
    source=path.read_text(encoding='utf-8')
    ET.fromstring(source)
    if '<script' in source.lower() or '<foreignObject' in source:
        errors.append(str(path.relative_to(ROOT))+': unsupported executable content')
    svg_count+=1
for path in [ROOT/'README.md',ROOT/'README.pl.md']:
    source=path.read_text(encoding='utf-8')
    for reference in re.findall(r'(?:src|srcset)="(assets/[^"]+)"',source):
        if not (ROOT/reference.split('#',1)[0]).is_file():
            errors.append(f'{path.name}: missing {reference}')
for path in ROOT.rglob('*'):
    if not path.is_file() or any(part in ('.git','node_modules','qa','__pycache__') for part in path.parts):
        continue
    if path.suffix not in ('.md','.py','.mjs','.svg','.json','.yml'):
        continue
    source=path.read_text(encoding='utf-8')
    if chr(0x2013) in source or chr(0x2014) in source:
        errors.append(str(path.relative_to(ROOT))+': forbidden punctuation')
    if re.search(r'gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}',source):
        errors.append(str(path.relative_to(ROOT))+': credential-like value')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'{svg_count} SVGs parsed; profile images exist; authored punctuation and credential scan passed.')
