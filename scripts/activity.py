"""Generate a small activity panel from selected public projects."""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path

OWNER = 'Xcape53'
REPOSITORIES = ('Yapper', 'SeeSky-tracking', 'portfolio', 'LabInc')
THEMES = {
    'dark': {'bg': '#0d1117', 'card': '#151b26', 'line': '#283445', 'text': '#e6edf3', 'muted': '#93a4bb'},
    'light': {'bg': '#ffffff', 'card': '#f6f8fc', 'line': '#d8e0ec', 'text': '#18283b', 'muted': '#52667e'},
}


def parse_date(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).astimezone(timezone.utc)


def normalize_repository(metadata, commits, release):
    if metadata.get('private') is not False:
        return None
    clean = []
    for record in commits:
        author = (record.get('author') or {}).get('login', '')
        if author.endswith('[bot]') or author.lower() in ('github-actions', 'dependabot'):
            continue
        details = record.get('commit') or {}
        date = (details.get('author') or {}).get('date')
        if not date:
            continue
        title = details.get('message', '').split('\n', 1)[0].strip()
        title = title.replace(chr(0x2013), '-').replace(chr(0x2014), '-')
        clean.append({'sha': record['sha'], 'title': title, 'date': date, 'url': record['html_url']})
    published = None
    if release and not release.get('draft') and not release.get('prerelease'):
        published = {'tag': release['tag_name'], 'date': release['published_at'], 'url': release['html_url']}
    return {'name': metadata['name'], 'url': metadata['html_url'], 'commits': clean, 'release': published}


def build_snapshot(repositories, now):
    start = now - timedelta(days=90)
    repos = []
    recent = []
    weeks = [0] * 13
    for source in repositories:
        if source is None:
            continue
        repo = dict(source)
        repo['commits'] = [c for c in source['commits'] if start <= parse_date(c['date']) <= now]
        repos.append(repo)
        for record in repo['commits']:
            recent.append({**record, 'repo': repo['name']})
            age = (now - parse_date(record['date'])).days
            weeks[12 - min(12, age // 7)] += 1
    recent.sort(key=lambda record: record['date'], reverse=True)
    return {'updated_at': now.strftime('%Y-%m-%dT%H:%M:%SZ'), 'window_days': 90,
            'repositories': repos, 'commit_count': len(recent), 'recent': recent[:4], 'weeks': weeks}


def render(snapshot, theme):
    palette = THEMES[theme]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="350" viewBox="0 0 1200 350" role="img" aria-labelledby="title desc">',
             '<title id="title">Public project activity</title>',
             '<desc id="desc">Selected public project commits over the last 90 days, excluding bot commits.</desc>',
             f'<rect x="1" y="1" width="1198" height="348" rx="18" fill="{palette["bg"]}" stroke="{palette["line"]}"/>',
             '<g font-family="Inter,Segoe UI,Arial,sans-serif">',
             f'<text x="34" y="43" fill="{palette["muted"]}" font-size="14" letter-spacing="3">PUBLIC PROJECT ACTIVITY</text>',
             f'<text x="1165" y="43" text-anchor="end" fill="{palette["muted"]}" font-size="14">90 DAYS</text>',
             f'<path d="M34 61H1165" stroke="{palette["line"]}"/>',
             f'<text x="34" y="123" fill="{palette["text"]}" font-size="49" font-weight="700">{snapshot["commit_count"]}</text>',
             f'<text x="34" y="151" fill="{palette["muted"]}" font-size="16">project commits</text>',
             f'<text x="225" y="123" fill="{palette["text"]}" font-size="49" font-weight="700">{len(snapshot["repositories"])}</text>',
             f'<text x="225" y="151" fill="{palette["muted"]}" font-size="16">public projects</text>']
    maximum = max(snapshot['weeks'] + [1])
    for index, value in enumerate(snapshot['weeks']):
        height = max(3, round(value / maximum * 76))
        x = 35 + index * 27
        parts.append(f'<rect x="{x}" y="{253-height}" width="18" height="{height}" rx="3" fill="{"#3b82f6" if index%3 else "#8b5cf6"}" opacity="{0.85 if value else 0.16}"/>')
    parts += [f'<text x="34" y="279" fill="{palette["muted"]}" font-size="13">13 weeks of project updates</text>',
              f'<path d="M426 82V285" stroke="{palette["line"]}"/>']
    if not snapshot['recent']:
        parts.append(f'<text x="462" y="128" fill="{palette["muted"]}" font-size="19">No public project changes in this period</text>')
    for index, record in enumerate(snapshot['recent']):
        y = 98 + index * 47
        title = record['title'][:58] + ('...' if len(record['title']) > 58 else '')
        parts += [f'<circle cx="467" cy="{y+6}" r="4" fill="{"#8b5cf6" if index%2 else "#3b82f6"}"/>',
                  f'<text x="483" y="{y}" fill="{palette["muted"]}" font-size="12">{escape(record["repo"])} / {escape(record["date"][:10])}</text>',
                  f'<text x="483" y="{y+23}" fill="{palette["text"]}" font-size="17">{escape(title)}</text>']
    date = snapshot['updated_at'][:10]
    parts += [f'<text x="34" y="322" fill="{palette["muted"]}" font-size="12">Public repositories only. Automated profile refreshes excluded.</text>',
              f'<text x="1165" y="322" text-anchor="end" fill="{palette["muted"]}" font-size="12">Updated {date} UTC</text>', '</g></svg>']
    return '\n'.join(parts)


def fetch_json(path):
    if os.getenv('PROFILE_USE_GH') == '1':
        result = subprocess.run(['gh', 'api', path], capture_output=True, text=True, encoding='utf-8', check=True)
        return json.loads(result.stdout)
    headers = {'Accept': 'application/vnd.github+json', 'User-Agent': 'Xcape53-profile', 'X-GitHub-Api-Version': '2022-11-28'}
    token = os.getenv('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    request = urllib.request.Request(f'https://api.github.com/{path}', headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        return json.load(response)


def render_mobile(snapshot, theme):
    palette = THEMES[theme]
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="600" height="550" viewBox="0 0 600 550" role="img">',
             '<title>Recent public project activity</title>',
             f'<rect x="1" y="1" width="598" height="548" rx="18" fill="{palette["bg"]}" stroke="{palette["line"]}"/>',
             '<g font-family="Inter,Segoe UI,Arial,sans-serif">',
             f'<text x="28" y="43" font-size="21" fill="{palette["muted"]}">PUBLIC PROJECT ACTIVITY / 90 DAYS</text>',
             f'<text x="28" y="103" font-size="38" font-weight="700" fill="{palette["text"]}">{snapshot["commit_count"]} commits / {len(snapshot["repositories"])} projects</text>']
    maximum=max(snapshot['weeks']+[1])
    for i,value in enumerate(snapshot['weeks']):
        height=max(3,round(value/maximum*64))
        parts.append(f'<rect x="{28+i*42}" y="{193-height}" width="27" height="{height}" rx="3" fill="{"#3b82f6" if i%3 else "#8b5cf6"}" opacity="{0.85 if value else 0.16}"/>')
    for i,record in enumerate(snapshot['recent']):
        y=242+i*68
        title=record['title'][:40]+('...' if len(record['title'])>40 else '')
        parts += [f'<text x="28" y="{y}" font-size="17" fill="{palette["muted"]}">{escape(record["repo"])} / {record["date"][:10]}</text>',
                  f'<text x="28" y="{y+26}" font-size="21" fill="{palette["text"]}">{escape(title)}</text>']
    if not snapshot['recent']:
        parts.append(f'<text x="28" y="260" font-size="21" fill="{palette["muted"]}">No public project changes in this period</text>')
    parts += [f'<text x="28" y="524" font-size="16" fill="{palette["muted"]}">Updated {snapshot["updated_at"][:10]} UTC / bots excluded</text>', '</g></svg>']
    return '\n'.join(parts)


def refresh(output_dir, fetch=fetch_json, now=None):
    now = now or datetime.now(timezone.utc)
    since = (now - timedelta(days=90)).strftime('%Y-%m-%dT%H:%M:%SZ')
    repositories = []
    try:
        for name in REPOSITORIES:
            route = f'repos/{OWNER}/{name}'
            metadata = fetch(route)
            if metadata.get('private') is not False:
                continue
            commits = []
            page = 1
            while True:
                batch = fetch(f'{route}/commits?since={urllib.parse.quote(since)}&per_page=100&page={page}')
                if not isinstance(batch, list):
                    raise ValueError('Invalid commit response')
                commits.extend(batch)
                if len(batch) < 100:
                    break
                page += 1
                if page > 20:
                    raise ValueError('Commit pagination exceeds configured public activity limit')
            releases = fetch(f'{route}/releases?per_page=1')
            repositories.append(normalize_repository(metadata, commits, releases[0] if releases else None))
        snapshot = build_snapshot(repositories, now)
        rendered = {f'activity-{theme}': render(snapshot, theme) for theme in THEMES}
        rendered.update({f'activity-mobile-{theme}': render_mobile(snapshot, theme) for theme in THEMES})
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError):
        print('Activity update failed; keeping the previously published files.', file=sys.stderr)
        return False
    output = Path(output_dir)
    (output / 'data').mkdir(parents=True, exist_ok=True)
    (output / 'data' / 'activity.json').write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    for name, svg in rendered.items():
        (output / f'{name}.svg').write_text(svg, encoding='utf-8')
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--offline', action='store_true', help='Render the last fetched snapshot without API access')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'assets')
    args = parser.parse_args()
    if args.offline:
        snapshot = json.loads((args.output / 'data' / 'activity.json').read_text(encoding='utf-8'))
        for theme in THEMES:
            (args.output / f'activity-{theme}.svg').write_text(render(snapshot, theme), encoding='utf-8')
            (args.output / f'activity-mobile-{theme}.svg').write_text(render_mobile(snapshot, theme), encoding='utf-8')
    elif not refresh(args.output):
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
