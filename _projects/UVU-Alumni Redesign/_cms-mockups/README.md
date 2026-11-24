# UVU Alumni Web System v1.5: CMS Mockups

Thirteen alumni pages rebuilt on one design system. They use UVU brand standards, UVU's existing CMS (OU section templates plus the global CSS), and Apple HIG basics. Open any `index.html` in Chrome.

**Start with `_styleguide/index.html`.** It shows the whole system rendered with the real CSS, plus the full list of what needed overhauling.

## v1.5: One System With Giving

The Alumni and Give pages now share one stylesheet (`_kit/css/12-alumni-system.css`, identical in both projects). Components built for Giving are available here too: stat cards (`al-stats`), quotes with a headshot (`al-quote--person`), the contact strip (`al-contact-strip`), fund directory (`al-funds`), fund search (`al-search`), pull quote (`al-pullquote`), and the embed poster.

- **Heroes:** every page has a photo hero except utility and roster pages (Board of Directors here; Find a Fund on Give), which use the compact plain hero. Podcast and Job Shadow moved to photo heroes in v1.5.
- **Podcast:** Home and the Podcast page feature the latest episode as a linked photo of the guest (no Spotify embed, so the show logo never appears). The Podcast hero is a WSB lifestyle podcast-studio shot (Oct. 15), replacing the overused photo; the phone crop is the guest at the mic.
- **Scholarships hero:** recropped so the student's head isn't cut off.
- **Where the latest changes live:** this local folder. The OneDrive copy is a round behind until the next push.

## Workflow: Work Local, Push Once

OneDrive sync is too slow and lock-prone (files lock mid-sync and writes fail) for active design work, so there are two copies:

| Copy | Location | Use |
|---|---|---|
| **Working** | `~/Documents/UVU-Alumni Redesign/_cms-mockups/` | All design work happens here. Claude reads and writes here. Not synced. |
| **Shared** | OneDrive `Web Page Redesigns/_cms-mockups/` | What Cesar, Monica, and the team see. Don't edit during a round. |

1. **Work** in the local copy. Open pages from there in Chrome.
2. **Source files stay in OneDrive.** `_abunchofphotos`, `APFY_Shapes File.ai`, `UVU_IconLibrary.ai`, and `_old/` are read-only references. Pull what a round needs into the local copy (`_work/photos/`, `_kit/`).
3. **Push once** when a round is done: one copy of the whole local `_cms-mockups/` folder to OneDrive. Files the push replaces move into `_archive-v1/` first; nothing is deleted.
4. **After the push**, tell Cesar it's ready. He pulls from OneDrive only.
5. **Never edit both.** If something changes in OneDrive between rounds (a new photo, a comment), copy it into the local copy before the next round starts.

## Pages

| Folder | Live URL |
|---|---|
| `alumni-home/` | /alumni/ |
| `alumni-benefits/` | /alumni/resources/benefits/alumni-benefits.html |
| `graduating-students/` | /alumni/students/graduating-students.html |
| `alumni-scholarships/` | /alumni/make-an-impact/alumni-scholarships.html |
| `about-saa/` | /alumni/students/about-saa.html |
| `uvu-license-plate/` | /alumni/make-an-impact/uvu-license-plate.html |
| `alumni-awards/` | /alumni/about/alumni-awards.html |
| `alumni-board/` | /alumni/about/alumni-association-advisory-board.html |
| `alumni-diplomas/` | /alumni/resources/diplomas.html |
| `career-networking-resources/` | /alumni/connect/career-networking-resources.html |
| `aviation-alumni-chapter/` | /alumni/connect/aviation-alumni-chapter.html |
| `alumni-job-shadow/` | /alumni/volunteer/job-shadow.html |
| `forever-wolverines-podcast/` | /alumni/connect/forever-wolverines-podcast.html |

Events link to the university calendar (uvu.edu/events). Alumni stories link to UVU News features (`/news/features/index.html#alumni`), which Central is building.

## The System in One Screen

- **Color:** UVU Green `#185C33` leads. Dark Green `#1A321C` is used for text. Warm `#F2F0EB` is the alternate section background. Pale Meadow is reserved for the hero eyebrow, footer headings, and focus rings.
- **Type:** Rajdhani (Stratum's web fallback) for display, Lato for reading. Every heading and button is in Title Case. Body copy is set at 18/1.6 with a 62-character measure.
- **Scale:** H1 72, H2 46, H3 26, H4 19, lead 21, body 18, meta 15 (desktop sizes; mobile steps down).
- **Spacing:** sections are 96px apart on desktop and 64px on mobile. Two white sections in a row share one gap.
- **Buttons:** primary, secondary, and light, all 52px tall. One primary per section. Secondary actions go in a link list. Labels name the destination. An arrow means it stays on uvu.edu; the external glyph means it leaves, opens a new tab, and says so to screen readers. A short note under a button flags a login, a fee, or another site. PDFs say "(PDF)".
- **Icons:** the UVU Icon Library only (`_kit/icons/`, 168 icons in green, white, and dark, re-extracted complete in v1.2), plus five UI glyphs drawn to match.
- **Imagery:** the uvu.edu image style. Plain photos (4:3, or 4:5 for a standing person) with 8px corners and APFY shapes layered around them (`_kit/shapes/`, exported from the APFY_Shapes file). Heroes are raw 1920×700 photos with the subject in the right half; the green fade is CSS. Product shots sit unframed.
- **Hero titles:** "UVU Alumni" (or "UVU") is a small eyebrow inside the H1, so the visual title is short ("Benefits") while the H1 and title tag keep the full name for search.
- **Rhythm:** each page runs hero → intro or split → splits (no more than two in a row) → band → alumni footer.
- **Alumni footer:** one compact band on every page with the alumni section nav (four groups), email, phone, and social. The current page is marked. It replaces the old contact band. The office name also sits in the CMS dept footer bar.
- **Grid:** one container, 1280px max with a 40px gutter (24px on phones). Hero headlines and section text share the same left edge.
- **Phones (under 768px):** heroes use a separate vertical photo (1080×1350, people centered, `-mobile.jpg`) with the headline on a green fade rising from the bottom. Cesar's copies are in `_handoff/mobile-headers/` (raw, plus `faded/` versions with the fade baked in, in case the CMS mobile slot can't take the CSS). Text and section heads go left-aligned, buttons go full width, quick links become a list, person cards become rows, news cards swipe sideways, and partner logos sit three across. Every tap target is 44px or taller. Audited at 390, 768, 1024, and 1440 with no sideways scroll.

## For the Developer

- **One stylesheet:** `_kit/css/12-alumni-system.css` (proposed CMS path `/alumni/lib/css/alumni-system.css`). It replaces `benefits.css` and the per-page CSS files. Icons go to `/alumni/lib/icons/`.
- **Heroes:** upload raw photos. The fade is `.page-header.al-hero::before` on desktop (same idea as the CMS `header-opacity` classes). On phones the `.al-hero-m` layer carries the vertical photo and its fade (`data-cms-bg` has the production path). `al-hero--plain` is the compact no-photo hero.
- **Images:** use `<figure class="al-media al-media--hatch|stairs|dot|half">` around a plain `<img>`. Add `al-media--portrait` for 4:5. Upload `_kit/shapes/` next to the stylesheet's icons.
- **Podcast:** the latest-episode feature (`al-media--episode`) links to the newest episode on Spotify; update its photo, date, and length when a new episode posts. All Episodes is one `al-episode` card per episode; a new episode means copying the top card. Thumbnails are Spotify's episode covers.
- **Dept footer:** set the department name to Office of Alumni Relations so `#globalFooter .footerDept` reads "Office of Alumni Relations | Utah Valley University."
- **Templates:** pages use only OU templates (`header-fullbleed`, `one-col`, `two-col`) plus `al-` classes. The comment on each section names its template, and every image has `data-cms-src`.
- **Splits:** region 1 is always text and region 2 is always media. `al-split--reverse` flips them on desktop, so mobile order stays consistent.
- **Accordions:** use the CMS's own `accordion-unstyled` opt-out plus `al-accordion`.
- **No inline styles:** use `al-center`, `al-actions--center`, `al-narrow`, and `al-section-head--left` so the phone rules can override them.
- **Partner logos:** one `<li>` per logo in `ul.al-logos`, so a partner can be added or dropped without a new graphic.
- **Live bug:** on phones, the live Benefits hero title renders `#275D38` on the green hero. Production dept.css forces that color below 768px. Confirmed on uvu.edu; fix it in production now. The system overrides it.

## Review PDFs

`_review-pdfs/` has a `--design` and a `--copy-review` PDF for each of the 13 pages and the styleguide, plus `ALL-PAGES` bundles with a bookmark per page. Regenerated Oct. 15, 2026 (v1.6). Each PDF is one continuous page at desktop width. The copy-review version numbers every highlighted edit and lists them at the bottom.

**For reviewers:** open `ALL-PAGES--design.pdf` for the look, or `ALL-PAGES--copy-review.pdf` to mark up copy. Both are in the shared OneDrive copy.

To export your own after edits, use **Save as PDF** in the mockup toolbar. Turn on **Show copy edits** first for copy review.

## Folder

```
_cms-mockups/
  _styleguide/          the system, rendered + overhaul flags
  _review-pdfs/         design + copy-review PDFs
  _shared-assets/       footer and plain-hero texture
  _handoff/mobile-headers/   vertical phone heroes for Cesar (raw + faded/)
  _kit/
    shapes/             APFY shapes as SVG (image accents)
    css/01–11           UVU production CSS snapshot (see note)
    css/12-alumni-system.css
    css/99-mockup-tools.css, js/   toolbar, copy flags, print (mockup only)
    icons/green|white|dark/        UVU Icon Library as SVG
    partials/           global header/footer markup (CMS provides)
    page-template.html  copy into a new page folder to start a page
    tools/              XD exporter, frame/hero generator, PDF renderer
  _xd-source/           data + images pulled from the XD file
  _work/photos/         working copies of _abunchofphotos
  _archive-v0/          first-round files replaced by v1
  _archive-v1/          v1 and v1.1 files replaced since, plus the broken icon set
  <page>/index.html, <page>/assets/
```

**CSS snapshot note:** the files are UVU production CSS from 2026-10-14, with mockup-only changes:
- `url()` paths point at uvu.edu.
- `@media print` blocks are removed.
- `only screen and` is removed from media queries.

The last two exist so Save as PDF keeps the desktop layout. Production keeps all of them.

## Open Items

The styleguide's **What Needs Overhauling** section has the full list. The ones that need an owner:

- **Imagery:** the photo set skews current students. Home, Benefits, and Alumni Awards need alumni-aged photography.
- **Brand:** the Athletics Wolverine mark appears in the Benefits partner-logo strip. Confirm it's approved or swap it.
- **Copy:** the Scholarships section headings are functional placeholders. SAA eligibility conflicts with the Scholarships page. SAA dates and the plate launch date are stale.
- **Assets:** the nomination form URL and full YouTube playlist URL are still missing. The plate photo shows a personalized (GO UVU) plate; swap for a standard plate shot if one exists.
- **Events:** the uvu.edu calendar is university-wide. If it has an alumni filter or category URL, use that in the footer, Home, and Graduates.
- **Benefits (Monica, Oct. 1):** Jazz and Mammoth band added. The team is the Utah Mammoth (singular); confirm the heading. Splash Summit isn't on this page.
- **Scholarships:** both giving pages work but live under `/give/…/archive/`. Confirm they're the permanent URLs.
- **Board:** the H1 says "Board of Directors," but the title tag and URL say "Advisory Board." The past presidents list has Gappmayer and Blair both at 2013–16 and nobody at 2016–19. Skyler Payne's year conflicts with the UVU style guide example. Jordan Perry has no class year.
- **Aviation:** no upcoming event (the June 5, 2026 lunch has passed). The mentor contact is a personal Gmail address.
- **Job Shadow:** applications are closed and the latest recap is 2024. Confirm whether the program runs in 2026. Two testimonial quotes have likely typos, flagged but not changed.
- **Directory links:** the "contact" links on Aviation and Job Shadow need their full directory-message URLs copied from the live pages.
