# Profile repository context

Public engineering profile for Piotr Jeleniewicz (Xcape53).

- README.md is English; README.pl.md is independently written Polish.
- Keep descriptions professional, specific and proportionate. Yapper is speech-to-text. SeeSky is radio telescope software; hardware and SDR integration are a future stage.
- No private repositories, personal settings, credentials, recordings or CV uploads. Contact through the public portfolio. CV on request.
- Use only ASCII hyphens, never U+2013 or U+2014.
- Main profile projects: Yapper, SeeSky, JobManager and portfolio. JobManager code stays private; its public overview and screenshots are on the portfolio.
- README artwork (since 2026-10-28, "engineer's sketchbook" style matching piotrjeleniewicz.com): scripts/build_sketch.py writes assets/sketch/*.svg - hand-drawn lines, site colours (navy #020816, #2c7ffe, #642efd), text converted to outlines from the OFL fonts in scripts/fonts/ (needs fonttools). Every image has its own navy panel, so one file serves both themes; `-m` files are the phone variants used through `<picture media="(max-width: 600px)">`. `--now` rebuilds only the "now" card (2 latest public pushes) and runs daily in the workflow. READMEs are hand-written; the older build_readmes.py, build_visuals.py, activity, arcade and calendar artwork are no longer referenced.
- Verification: python scripts/build_sketch.py; python scripts/validate.py.
- Daily automation lives in .github/workflows/update-profile.yml. Do not commit generated results if any generation or validation step fails.
- Preserve GitHub dark/light pictures, accessible text, Polish/English links and mobile readability.
- Responsive artwork uses complete HTML blocks with one picture per theme and a theme-only fragment on each enclosing link. GitHub discards width conditions combined with theme media queries; do not combine them.

## Asset provenance

Original circuit, project and workflow SVGs belong to this profile. Project screenshots were taken from the public portfolio or the public SeeSky interface demo. Arcade output uses pacman-contribution-graph 5.3.1; retain upstream attribution in THIRD-PARTY-NOTICES.md. Do not invent a license for the upstream package.
