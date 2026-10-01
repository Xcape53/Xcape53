"""Keep profile copy and theme-aware markup in one editable source."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def picture(name, alt, mobile=False):
    if mobile:
        # GitHub replaces theme media queries, discarding combined width rules.
        # Keep responsive art direction separate from its theme-only fragments.
        variants=[]
        for theme in ('dark','light'):
            variants.append(f'''<a href="assets/{name}-{theme}.svg#gh-{theme}-mode-only"><picture>
<source media="(max-width: 600px)" srcset="assets/{name}-mobile-{theme}.svg">
<img alt="{alt}" src="assets/{name}-{theme}.svg" width="100%">
</picture></a>''')
        return '<div>\n'+'\n'.join(variants)+'\n</div>'
    return f'''<picture>
<source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">
<img alt="{alt}" src="assets/{name}-light.svg" width="100%">
</picture>'''


def project_picture(name, alt):
    return f'''<picture><source media="(prefers-color-scheme: dark)" srcset="assets/projects/{name}-dark.svg"><img alt="{alt}" src="assets/projects/{name}-light.svg" width="100%"></picture>'''


def cards(pl=False):
    descriptions = [
        ('yapper','Yapper','https://github.com/Xcape53/Yapper',
         'A Windows speech-to-text app with two push-to-talk channels, online/offline transcription and clipboard output. I use it daily.',
         'Aplikacja Windows do zamiany mowy na tekst: dwa kanały push-to-talk, transkrypcja online i offline oraz wynik w schowku. Korzystam z niej na co dzień.',
         'Python / PyQt6 / speech APIs','Repository','Repozytorium','https://github.com/Xcape53/Yapper/releases','Releases','Wydania'),
        ('seesky','SeeSky','https://github.com/Xcape53/SeeSky-tracking',
         'Radio telescope software for SimLE. I lead software development, covering the backend, web interface and interactive sky visualisation.',
         'Oprogramowanie radioteleskopu zespołu SeeSky w SimLE. Jestem główną osobą odpowiedzialną za jego rozwój: backend, interfejs webowy i interaktywną wizualizację nieba.',
         'Python / Flask / Astropy / JavaScript','Repository','Repozytorium','https://xcape53.github.io/SeeSky-tracking/','UI demo','Demo interfejsu'),
        ('jobmanager','JobManager','https://piotrjeleniewicz.com/#p-jobagg',
         'A personal tool that brings job listings from multiple portals into one workflow, with shared filters, AI-assisted research and notifications.',
         'Własne narzędzie łączące oferty z wielu portali, wspólne filtry, analizę z wykorzystaniem AI i powiadomienia.',
         'Data aggregation / Gemini API / automation','Project overview','Opis projektu','https://piotrjeleniewicz.com/#p-jobagg','Screenshots','Zrzuty ekranu'),
        ('portfolio','Portfolio','https://piotrjeleniewicz.com/',
         'My Polish and English portfolio: project galleries, responsive layouts and custom electronics-inspired visual effects.',
         'Moje portfolio w wersji polskiej i angielskiej: galerie projektów, responsywny układ i autorskie efekty inspirowane elektroniką.',
         'HTML / CSS / JavaScript / GitHub Pages','Website','Strona','https://github.com/Xcape53/portfolio','Source','Kod')]
    rows=[]
    for i in range(0,4,2):
        row='<tr>\n'
        for name,title,url,en,polish,stack,label,pl_label,extra,extra_label,extra_pl in descriptions[i:i+2]:
            row+=f'''<td width="50%" valign="top">
<a href="{url}">{project_picture(name,title)}</a>
<p><strong><a href="{url}">{title}</a></strong></p>
<p>{polish if pl else en}</p>
<p><sub>{stack}</sub></p>
<p><a href="{url}">{pl_label if pl else label}</a> · <a href="{extra}">{extra_pl if pl else extra_label}</a></p>
</td>\n'''
        rows.append(row+'</tr>')
    return '<table>\n'+ '\n'.join(rows)+'\n</table>'


def build(pl=False):
    header=picture('header','Piotr Jeleniewicz - software development and system integration',True)
    language='[English](README.md) · **Polski**' if pl else '**English** · [Polski](README.pl.md)'
    links='[Portfolio](https://piotrjeleniewicz.com/pl/) · [LinkedIn](https://www.linkedin.com/in/piotr-jeleniewicz/)' if pl else '[Portfolio](https://piotrjeleniewicz.com/) · [LinkedIn](https://www.linkedin.com/in/piotr-jeleniewicz/)'
    intro='''Tworzę aplikacje w Pythonie i JavaScripcie, integruję usługi przez API i rozwijam narzędzia automatyzujące codzienną pracę. Interesuje mnie projektowanie systemów oraz łączenie oprogramowania z urządzeniami.

Studiuję elektronikę i telekomunikację na Politechnice Gdańskiej. Jestem na ostatnim semestrze studiów inżynierskich, w strumieniu Elektronika, na specjalności Komputerowe Systemy Elektroniczne.''' if pl else '''I develop Python and JavaScript applications, integrate services through APIs and build automation tools. I am interested in system design and software that connects with devices.

I study Electronics and Telecommunications at Gdańsk University of Technology, in the Electronics stream, specialising in Computer Electronic Systems. I am in the final semester of my engineering degree.'''
    projects='Wybrane projekty' if pl else 'Selected projects'
    caveat='SeeSky: integracja ze sprzętem i odbiornikiem SDR to kolejny etap projektu. Demo pokazuje interfejs bez bieżących danych z gwiazd i czujników.' if pl else 'SeeSky: hardware and SDR integration are the next stage. The demo shows the interface without live star or sensor data.'
    method='Jak pracuję z AI' if pl else 'How I work with AI'
    paragraph='''Zaczynam od problemu i oczekiwanego działania. Dzielę system na moduły, określam ich odpowiedzialność i interfejsy, a następnie łączę komponenty w spójną aplikację. Narzędzia AI wspierają mnie w implementacji i diagnozowaniu błędów; ja prowadzę rozwój i sprawdzam zachowanie systemu.

**Przykład - JobManager:** zbieranie ofert, filtrowanie, analiza i powiadomienia mają osobne zadania, ale współpracują w jednym przepływie. Rozwijam je iteracyjnie na podstawie codziennego używania aplikacji.''' if pl else '''I start with the problem and expected behaviour, define module responsibilities and interfaces, then integrate the components. AI development tools support implementation and debugging; I guide development and verify how the system behaves.

**Example - JobManager:** collection, filtering, research and notifications have separate responsibilities within one workflow. I improve them iteratively through daily use.'''
    workflow=picture('workflow','Requirements, modules, implementation, integration and validation',True)
    tooltext='**Główne narzędzia:** Python · JavaScript · REST APIs · Git. Moje przygotowanie z elektroniki obejmuje także pomiary, symulacje i projektowanie układów.' if pl else '**Core tools:** Python · JavaScript · REST APIs · Git. My electronics background also includes measurement, simulation and circuit-design labs.'
    activity='Aktywność w publicznych projektach' if pl else 'Public project activity'
    activitypic=picture('activity','Recent changes in four selected public projects over the last 90 days',True)
    calendar=picture('arcade/galaga','Arcade animation of publicly searchable commits over the past year')
    alternative=picture('arcade/breakout','Breakout animation of publicly searchable commits over the past year')
    activityscope='Panel obejmuje Yapper, SeeSky-tracking, portfolio i LabInc z ostatnich 90 dni, z pominięciem botów. Animacja poniżej korzysta z publicznie wyszukiwalnych commitów z ostatniego roku.' if pl else 'The panel covers Yapper, SeeSky-tracking, portfolio and LabInc over the past 90 days, excluding bots. The arcade below uses publicly searchable commits from the past year.'
    arcadehint='Animacja SVG odtwarza rozgrywkę automatycznie. Dane odświeżają się codziennie; prywatna aktywność nie jest uwzględniana.' if pl else 'The SVG plays automatically. Data refreshes daily; private activity is not included.'
    optional='Więcej projektów i wariant arcade' if pl else 'More projects and an alternative arcade'
    static_calendar=picture('calendar','Static isometric calendar of publicly searchable commits')
    screenshots=f'''<details>
<summary>{'Zrzuty aplikacji' if pl else 'Application screenshots'}</summary>

**JobManager** - {'widok analizy oferty z publicznego portfolio.' if pl else 'offer research view from my public portfolio.'}

<img src="assets/screenshots/jobmanager-analysis.png" alt="JobManager offer research interface" width="100%">

**SeeSky** - {'demo interfejsu, bez podłączonego backendu i danych z czujników.' if pl else 'interface demo, without a connected backend or sensor data.'}

<img src="assets/screenshots/seesky-demo.jpg" alt="SeeSky tracking dashboard in interface demo mode" width="100%">

**Portfolio**

<img src="assets/screenshots/portfolio.jpg" alt="Live portfolio home page" width="100%">

</details>'''
    more='''- **[LabInc: Chemical Tycoon](https://github.com/Xcape53/LabInc)** - gra ekonomiczna w Javie, z modelem produkcji, zapisem stanu i interfejsem Swing.
- **[Generator ekwipunku](https://piotrjeleniewicz.com/inventoryGen/index.html)** - interaktywne narzędzie webowe do układania ekwipunku w stylu Minecrafta.
- **[Turf Matchmaking](https://github.com/Xcape53/TurfMatchMaking)** - wyszukiwanie lobby gry z filtrami, walidacją danych i ponawianiem zapytań.''' if pl else '''- **[LabInc: Chemical Tycoon](https://github.com/Xcape53/LabInc)** - a Java economy game with production modelling, state persistence and a Swing interface.
- **[Inventory generator](https://piotrjeleniewicz.com/inventoryGen/index.html)** - an interactive web tool for arranging Minecraft-style inventories.
- **[Turf Matchmaking](https://github.com/Xcape53/TurfMatchMaking)** - a game-lobby finder with filters, live-data validation and retries.'''
    contact='Kontakt i dostępność' if pl else 'Contact and availability'
    contactbody='''Szukam **płatnego stażu lub pracy na pół etatu** w rozwoju oprogramowania, integracji systemów lub automatyzacji. Preferuję pracę **zdalną lub hybrydową w Trójmieście**.

[Napisz do mnie przez portfolio](https://piotrjeleniewicz.com/pl/#contact) · [LinkedIn](https://www.linkedin.com/in/piotr-jeleniewicz/)

CV dostępne na prośbę.''' if pl else '''I am looking for a **paid internship or part-time role** in software development, system integration or automation. I prefer **remote work or a hybrid role in Tricity, Poland**.

[Contact me through my portfolio](https://piotrjeleniewicz.com/#contact) · [LinkedIn](https://www.linkedin.com/in/piotr-jeleniewicz/)

CV available on request.'''
    return f'''<!-- Copy source: scripts/build_readmes.py -->
{header}

{language} &nbsp; | &nbsp; {links}

{intro}

## {projects}

{cards(pl)}

<sub>{caveat}</sub>

{screenshots}

## {method}

{paragraph}

{workflow}

{tooltext}

## {activity}

{activitypic}

{activityscope}

{calendar}

<sub>{arcadehint} Animation: <a href="https://github.com/abozanona/pacman-contribution-graph">pacman-contribution-graph</a>.</sub>

<details>
<summary>{optional}</summary>

{more}

{alternative}

{static_calendar}

</details>

## {contact}

{contactbody}

<details>
<summary>{'Grafika bez animacji' if pl else 'Static artwork'}</summary>

{picture('header','Static software development and system integration panel').replace('header-dark.svg','header-dark-static.svg').replace('header-light.svg','header-light-static.svg')}

</details>
'''


if __name__=='__main__':
    (ROOT/'README.md').write_text(build(),encoding='utf-8')
    (ROOT/'README.pl.md').write_text(build(True),encoding='utf-8')
