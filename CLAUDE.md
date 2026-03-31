# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GlobeMind institutional website — a static multi-page marketing site for a software services company ("Software Distillery"). Targets Spanish-speaking B2B clients (CTOs, business owners, product managers). No build tooling; pure HTML/CSS/vanilla JS.

## Development

Since there is no build step, development is just editing files and opening them in a browser. Use a local static server to preview:

```bash
# Python (usually available)
python3 -m http.server 8000

# Or Node-based
npx serve .
```

No linting, no tests, no package.json.

## Architecture

**Three-page site:**
- [index.html](index.html) — main corporate landing page
- [alycs.html](alycs.html) — specialized landing page for ALyCs (Argentine capital market agents)
- [consultoria-innovacion.html](consultoria-innovacion.html) — Innovation Consulting service page

**CSS structure — each page has its own stylesheet:**
- [styles.css](styles.css) — shared base styles (navbar, footer, buttons, layout), organized by component with comment headers
- [alycs.css](alycs.css) — page-specific styles for `alycs.html`
- [consultoria-innovacion.css](consultoria-innovacion.css) — page-specific styles for `consultoria-innovacion.html`

**Shared JS:**
- [script.js](script.js) — scroll animations, mobile nav, active link tracking

**Image assets in [img/](img/):** logos, client logos (`img/clients/`), service images (`img/services/`), tech stack icons (`img/stack/`).

## Key Conventions

**Language:** All UI copy is in Spanish (`lang="es"`).

**CSS variables** (defined in `:root` in `styles.css`):
- Primary blue: `#396bad`
- Secondary blue: `#79a9d6`

**Page-specific CSS:** Never add page-specific styles to `styles.css`. Each sub-page has its own `.css` file (see above).

**Animations:** Scroll-triggered fade-ins via IntersectionObserver. `script.js` handles `.fade-in` elements on `index.html`; sub-pages (`alycs.html`, `consultoria-innovacion.html`) each include their own inline `<script>` at the bottom of the file that observes `.alycs-fade-in` / `.inno-fade-in` elements respectively.

**Navigation:** Anchor-based on `index.html` (`#nosotros`, `#servicios`, `#stack`, `#contacto`). Sub-pages link back using `index.html#section`. The services dropdown currently lists two items: ALyCs and Innovación. Smooth scroll uses an 80px offset to account for the fixed header.

**Contact form:** Redirects to an external Google Form (not handled server-side).

**Google Analytics:** GA4 tag `G-MQXN4FXRMS` inline at the bottom of every HTML file.

## Business Context

- **ALyCs page:** Targets Argentine capital market agents needing regulatory compliance tooling (DDJJ management, operations registry). See [servicios-alycs.md](servicios-alycs.md).
- **Consultoría de Innovación page:** Positions GlobeMind as an innovation consultancy using Design Thinking, Design Sprints, and Agile. Based on the PDF brochure `GlobeMind_Consultoria_Innovacion.pdf`.
- **Full PRD:** [prd.md](prd.md).
