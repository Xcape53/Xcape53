# Profile repository context

Public engineering profile for Piotr Jeleniewicz (Xcape53).

- README.md is English; README.pl.md is independently written Polish.
- Keep descriptions professional, specific and proportionate. Yapper is speech-to-text. SeeSky is radio telescope software; hardware and SDR integration are a future stage.
- No private repositories, personal settings, credentials, recordings or CV uploads. Contact through the public portfolio. CV on request.
- Use only ASCII hyphens, never U+2013 or U+2014.
- Main profile projects: Yapper, SeeSky, JobManager and portfolio. JobManager code stays private; its public overview and screenshots are on the portfolio.
- Source artwork is scripts/build_visuals.py. Regenerate with Python. Use code-native SVG for illustrations; original public screenshots are in assets/screenshots/.
- Project covers use individual flat palettes, large titles, the original SeeSky mark and embedded public screenshots. Preserve their clean composition; avoid placeholder interfaces, repeated technical grids and decorative status labels. After regenerating, run node scripts/render_social.mjs to keep the social PNGs consistent with their SVG sources.
- Activity source: scripts/activity.py, restricted to four public repositories. Arcade uses unauthenticated public commit search. Its calendar shows searchable public commits, not all GitHub contributions or private work.
- Verification: python -m unittest discover -s tests -v; python scripts/build_visuals.py; python scripts/activity.py --offline; npm ci --ignore-scripts; npm run arcade; parse all SVG files with xml.etree.ElementTree.
- Daily automation lives in .github/workflows/update-profile.yml. Do not commit generated results if any generation or validation step fails.
- Preserve GitHub dark/light pictures, accessible text, Polish/English links and mobile readability.
- Responsive artwork uses complete HTML blocks with one picture per theme and a theme-only fragment on each enclosing link. GitHub discards width conditions combined with theme media queries; do not combine them.

## Asset provenance

Original circuit, project and workflow SVGs belong to this profile. Project screenshots were taken from the public portfolio or the public SeeSky interface demo. Arcade output uses pacman-contribution-graph 5.3.1; retain upstream attribution in THIRD-PARTY-NOTICES.md. Do not invent a license for the upstream package.
