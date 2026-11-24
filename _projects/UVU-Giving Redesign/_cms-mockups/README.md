# UVU Giving v1.6: CMS Mockups

Fifteen Give pages rebuilt on the same IA web system as the Alumni pages: UVU brand, UVU's CMS (OU section templates plus the global CSS), and the same components, so the two sites read as one. Open any `index.html` in Chrome. Turn on **Show copy edits** in the mockup toolbar to see every flagged change.

**For reviewers:** `_review-pdfs/ALL-PAGES--design.pdf` (the look) and `ALL-PAGES--copy-review.pdf` (every flagged copy edit, numbered), with a bookmark per page, plus one of each per page. Regenerated Oct. 15, 2026. Fund pages print every department, not just the open tab.

## Pages (15)

| Folder | Live URL | Role |
|---|---|---|
| `give-home/` | /give/index.html | The hub: why give, fund search, featured funds, every area, a story, ways to give, larger gifts |
| `find-a-fund/` | /give/find-a-fund.html (new) | Every fund (439) in one searchable list, each linking straight to its form |
| `ways-to-give/` | /give/ways-to-give/index.html | Give today, give over time, give stock, Annual Giving contacts |
| `employee-giving/` | /give/ways-to-give/employeegiving.html | Internal campaign |
| `memorial-gifts/` | /give/ways-to-give/memorial-gifts.html | Obituary "in lieu of flowers" traffic lands here |
| `college-health-public-service/`, `smith-college-engineering-technology/`, and five more college pages | /give/colleges-schools/[college]/ | Fund directory per college |
| `programs-centers/` | /give/programs-centers/index.html | Fund directory |
| `student-affairs/` | /give/student-affairs/index.html | Four areas + scholarships |
| `athletics/` | /give/athletics/wolverine-club/index.html | Thirteen teams + Wolverine Club |

**Merged (redirects for Cesar):**
- /give/ways-to-give/annual-giving.html → /give/ways-to-give/index.html (contacts section)
- /give/ways-to-give/gifts-of-securities.html → /give/ways-to-give/index.html#give-stock
- /give/colleges-schools/index.html → /give/index.html#give-by-area
- The seven per-college "Search for a Fund" pages → /give/find-a-fund.html?area=[College name]

## v1.4: Why It Changed

The old structure followed the org chart: a first-gen gift took Give → Programs and Centers → find the row → open it → fund → form, and only if you knew First-Gen counts as a "Program or Center." Now every fund is one click from Give (featured) or two (search). The short version:

- **$5 donor:** types what they care about. Give now opens with a fund search (Michigan pattern) and six featured funds that go straight to their forms (University of Utah / ASU pattern). Monthly giving gets an entry point (NextAfter: a short monthly note lifted new recurring donors 48%). The $35 license plate is now a way to give.
- **$10M donor:** a "Planning a Larger Gift?" band on the hub with a named contact (placeholder), gift planning, stock, and the impact report. Stock now leads with transfer instructions (placeholder) instead of a tax lecture. The footer adds tax ID, Annual Impact Report, and IRS Form 990 (ASU pattern).
- **Designer:** the $25/$50/$250/$500 cards are gone (suggested amounts belong on the form, pre-selected, per Blackbaud). One real story replaces them: Kyrsi Zamora's first-gen quote with a "Join Kyrsi" button. Duplicate units (Baugh Institute, Museum of Art) drop out of Programs and Centers. Every college page has a "why give" copy slot (NextAfter: adding a real reason to give lifted gifts 150%).

**CMS scope:** everything uses OU section templates, Blackbaud form links with the fund pre-filled (already how live works), and the CMS dataview component for Find a Fund (already behind the live per-college search pages). The mockup filters with `_kit/js/fund-finder.js` as a stand-in. No giving basket or custom apps.

**Sources:** [NextAfter, higher-ed donation pages](https://www.nextafter.com/blog/5-ways-higher-education-organizations-can-improve-their-donation-pages/) · [Blackbaud Institute, donation pages](https://institute.blackbaud.com/explorer/donation-pages/) · [M+R Benchmarks 2025 summary](https://idonate.com/blog/2025-mr-benchmarks-what-nonprofits-must-know-about-online-giving-and-donation-pages) · [University of Arizona fund search](https://giving.arizona.edu/designation-search-tips) · [University of Michigan Giving](https://giving.umich.edu/) · [University of Utah Giving](https://giving.utah.edu/) · [ASU Foundation](https://www.asufoundation.org/)

## v1.6: Fund Pages on Cesar's June 2026 Template

All seven college pages and Programs and Centers now use Cesar's `new-format-26` layout (from `_old/New Format - June 2026`), so his build carries over as is. Only the header is ours.

- **Header:** our hero (raw photo, CSS fade, tagline eyebrow, H1, phone layer, scholarship button) replaces the template's h2/h1 with text shadows over the dark overlay.
- **Section 2 (one-col):** Cesar's markup and class names (MAIN MENU bar and popover, sidebar tabs, `content-panel`, `fund-item`, Search panel), designed on the system. A layer in the system file scoped to `.al-nf` restyles them; his stylesheet stays loaded underneath.
  - **Sidebar:** sticky on desktop, active row marked with a green bar, Search styled as a field at the top.
  - **Department header:** the department's fund photo, a count line ("5 Programs · 1 Scholarship"), the why-give copy slot, and an "About [Department]" link in place of the Learn More button.
  - **Fund rows:** each fund is a full-width link to its Blackbaud form with "Give" and the external glyph, 56px tall. Programs and Scholarships get subheads with counts.
  - **Phones:** the green bar shows the department you're on and opens the menu; choosing one scrolls back to the bar.
  - **New labels (flagged):** "Browse Funds" (was MAIN MENU), "Search All Funds" (was Search), "About [Department]" (was Learn More), "Give" on each row.
- **Section 3 (one-col, header region + region 1):** `divider-header` plus contacts. Pages that use the directory widget have Cesar's widget markup in a comment with the employee ID.
- **Search panel:** production gets each college's Blackbaud designation search embed (the template's is CHPS). The mockup uses the Give search, filtered to that area on Find a Fund.
- **CSS:** `_kit/css/13-give-new-format-26.css` is a copy of his `/give/lib/css/new-format-26.css`, loaded before the system file. His file sets a few page-wide rules (`body` background, Arial, `#555`, a dark overlay on every `.fullbleed`, `iframe { position: inherit !important }`). The system file neutralizes the first four on these pages; worth scoping them in production so they can't leak.
- **Tabs:** `_kit/js/funds-tabs.js` stands in for the CMS tab script. Search is a panel like the others, since the global CSS only shows `.tab-container.open`.
- **College of Health and Public Service (new in v1.6):** CHPS was the template's own example and had no mockup before. It now has the same page as the other colleges: 13 departments and 54 funds pulled from the live CHPS page on Oct. 15, each linking to its Blackbaud form. Give, Find a Fund (now 439 funds), and the Give by Area list link to it instead of the live page.
  - **Hero:** the nurse and patient from the April 2025 CHPS IA shoot (`_images/20250410_ CHPS IA Photo Shoot_KE_00044.jpg`), with a vertical phone crop.
  - **Department photos:** five use the new CHPS and Dental Hygiene shoots (CHPS Heroes Fund, Criminal Justice, Dental Hygiene, Emergency Services, Nursing). The other eight load from the live CHPS page (uvu.edu), so they show online but drop out of the PDFs. Copy them into `college-health-public-service/assets/` before handoff.
  - **Live typo:** "Capital Reef Fieldwork" is flagged as Capitol Reef (the form's own name says Capitol). Alt text spelling fixed ("their," "practicing").
- **Removed (Oct. 15):** the "Opens the secure UVU Foundation giving form." note under hero buttons (all pages), and the fund counts in the sidebar.
- **Not converted:** Student Support and Athletics keep the system layout (four areas and a team grid, not fund directories).

## v1.5: Visual Pass

- **Contacts:** single contact cards floating in empty sections became a compact strip (initials badge, name, title, phone, message link). Contact sections run shorter.
- **Give page rhythm:** sections now alternate white and warm, and the Larger Gift band moved off green so the page no longer ends in three greens in a row. "See All Funds" is a button, not a small link. Give by Area balances its two columns (General Scholarships and Search All Funds added).
- **Find a Fund:** shows the first 30, A to Z, with a Show All button (the CMS dataview paginates the same way), so the footer isn't 439 rows away.
- **Fund directories:** held to the same 900px measure as Find a Fund instead of running the full 1200px under a centered heading.
- **Ways to Give:** cards with no copy (In-Kind, Service) became links; Give Over Time is a 2 × 2.
- **Employee Giving:** now has a photo hero like every other page.
- **Athletics:** Wolverine Club leads the team grid, so the last row isn't a lone card. Eyebrows: Athletics reads "Wolverine Club," Programs and Centers reads "Give to UVU" (was "Support").
- **Photos:** Kyrsi Zamora's real portrait on the Give story and her Employee Giving quote. New heroes from your uploads: Student Support (CARE Hub), College of Science (lab), School of Education (classroom), Humanities and Social Sciences (library), Programs and Centers, Employee Giving.

## Earlier Changes (v1.3)

- **One system with Alumni.** Same stylesheet, heroes, cards, buttons, APFY shapes, and phone rules. Components added for Giving and back-ported to Alumni: stat cards, quotes with a headshot, contact cards, embedded-form frame, fund directory, card tags, tagline eyebrow, fund search, fund finder rows, pull quote.
- **Give footer** on every page: where to give, ways to give, contact, mail-a-check.
- **Employee Giving:** the six "I AM UVU" graphics are real text quotes now, transcribed verbatim.
- **Memorial Gifts:** the form gets its own section and the hero button jumps to it.
- **College pages:** tagline above the H1, scholarship form as the hero button, departments as accordions with counts.
- **Athletics:** one grid of teams with Men's / Women's tags instead of three repeated lists.

## Imagery

Heroes use your `_images` picks where they fit (aerials, bookstore, sign, classroom) plus the live pages and the Alumni photo set. Heroes are raw 1920×700 photos (the fade is CSS); phones use a vertical 1080×1350 crop. Cesar's phone crops are in `_handoff/mobile-headers/`.

Placeholders worth replacing:
- **School of the Arts:** violin section from the live SOA page, upscaled from 1200px. Needs a full-resolution arts photo (performance, studio, or rehearsal).
- **Memorial Gifts:** the flower photo is 600px wide on the live site; needs the original.
- **Featured fund cards:** First Generation Center, Fulton Library, Social Impact, and Culinary use live thumbnails (800px). The CARE Hub set would make a strong Student Emergency and Care Fund card once its form link is known.
- Many department thumbnails on the live fund tiles are small (some under 400px). They hold up at thumbnail size only.

## Open Items

- **Featured funds:** the six on Give are placeholders chosen for range. IA picks and rotates them.
- **Story:** confirm Kyrsi Zamora is OK headlining Give, and the "monthly donor" caption (inferred from Employee Giving).
- **Larger gifts:** name the leadership contact; add the impact report URL, IRS Form 990 URL, and UVU Foundation tax ID.
- **Give Stock:** add brokerage, DTC number, and account details.
- **Monthly giving:** confirm the Blackbaud forms offer a recurring monthly option.
- **Why-give copy:** each college page has a placeholder for 3 to 5 sentences.
- **Give Now destination:** confirm the default fund, or use a form with a fund picker.
- **Directory contacts:** College of Science, School of Education, and Woodbury load their contact from the directory widget.
- **Event name:** "President's Scholarship Ball … 115 students." Confirm the current name and number.
- **Stats:** "Eighty-seven percent of UVU graduates remain in the state" needs a current source.
- **Programs and Centers:** the Gary R. Herbert Institute list has a stray "Scholarship List" link to the First Generation Center form.
- **Student Support funds:** the area sub-pages weren't saved, so Find a Fund lists only Student Affairs Scholarships for that area.
- **Dept footer:** set to "Institutional Advancement." Confirm.

## Workflow

Same as Alumni: work in the local folder (`~/Documents/UVU-Giving Redesign/_cms-mockups/`), push once to the shared OneDrive copy (`'26-'27/Annual Giving/Web Redesign/_cms-mockups/`) when a round is done, and archive replaced files instead of deleting them. The styleguide lives with the Alumni mockups (`_styleguide/index.html`). The builder, crop, and fund-parsing scripts are in `_kit/tools/` for reference.
