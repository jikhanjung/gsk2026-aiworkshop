# GSK 2026 AI Workshop — Building HTML Apps with Gemini

[한국어](README.md) | **English**

These are practice materials in which students **build a notebook by typing prompts to Gemini in Google Colab**,
and as a result create **an app that is a single HTML file**, download it, and use it in the browser on their own PC.
Instead of being given code from the start, students practice the process of **saying exactly what they want → checking the result → asking for fixes**.

There are two practices.

| | Practice 1. VWorld Map App | Practice 2. Conference Organizer (conference timetable app) |
|---|---|---|
| What you build | Mark and record **field survey / sampling sites** on a VWorld base map | View conference talks by date and room, and bookmark them to build **My Schedule** |
| What students are given | Nothing — students obtain a **VWorld API key** in advance | Conference program data `conference.json` |
| Internet | **Required** (map tiles; Leaflet CDN allowed) | **Not required** (data is embedded in the HTML; external libraries not allowed) |
| New things to learn | Map library, external API, **handling an API key safely** (Colab Secrets), `localStorage`, export/import | Putting a data file into HTML, filtering and search, managing screen state, calculating time overlaps |
| Advanced | **KIGAM geological map overlay** (API key needs approval → apply in advance, or do it as homework after class) | Per-session view, detail screen, bookmark export, etc. |
| Student guide | [`docs/vworld_map_practice_guide.en.md`](docs/vworld_map_practice_guide.en.md) | [`docs/conference_organizer_practice_guide.en.md`](docs/conference_organizer_practice_guide.en.md) |
| Instructor guide | [`docs/vworld_map_instructor_guide.en.md`](docs/vworld_map_instructor_guide.en.md) | [`docs/conference_organizer_instructor_guide.en.md`](docs/conference_organizer_instructor_guide.en.md) |
| Reference solution / sample | [`examples/vworld_map_sample.html`](examples/vworld_map_sample.html) (API key not included) | Notebook `gsk2026_practice.ipynb` + [`docs/reference_notebook_guide.en.md`](docs/reference_notebook_guide.en.md) (released at the end of class) |

Both practices work the same way — while looking at the completion criteria table, **ask Gemini step by step → run → download and open → compare with the criteria**.
Do **Practice 1 (map app) first**. Its screen layout is simple (map + site records) and there is no data to handle, so it is a good way to get used to working with Gemini.
In Practice 2 (Conference Organizer), students put a large data file into HTML and build an app with more logic, such as filtering, search, and overlap calculation.
Be sure to point out to students that, unlike the map app, the condition changes to **no external libraries (CDN)**.

- Reference solution notebook Colab link (Practice 2): https://colab.research.google.com/github/jikhanjung/gsk2026-aiworkshop/blob/main/gsk2026_practice.ipynb
- Design decisions and rules: [`CLAUDE.md`](CLAUDE.md) (Korean) · Progress: [`HANDOFF.md`](HANDOFF.md) (Korean) · Development log: [`devlog/`](devlog/README.md) (Korean)

## Practice 1 (VWorld Map App) summary

- **Pre-class assignment**: Students sign up for VWorld (https://www.vworld.kr; the site is in Korean) → get an API key (including base map WMTS) → verify by email → confirm approval.
  The key is issued immediately on application, but because there are sign-up and email verification steps, have students get it **before class**. For the **service URL** on the application form, tell students a value the instructor has tested in advance.
- **The API key is not written in the notebook code.** Put it in Colab Secrets (the 🔑 key icon in the left sidebar) as `VWORLD_KEY` and read it from code.
  However, the finished HTML file contains the key, so **submit the HTML only to the instructor** and do not publish it.
- Completion criteria: base map displayed with your own key, base map switching, click to add / view info / delete sites, data kept after reopening (`localStorage`),
  JSON export/import, key not exposed in the notebook. See the guide for detailed steps, prompts, and cautions.
- **(Advanced) Geological map overlay**: Overlay the geological map WMS from the OpenAPI of the KIGAM GeoBigData Open Platform of the Korea Institute of Geoscience and Mineral Resources (KIGAM) (https://data.kigam.re.kr; the site is in Korean)
  (`https://data.kigam.re.kr/openapi/wms`, layers such as `L_50K_Geology_Map`) semi-transparently on top of the VWorld map.
  Sign-up is immediate, but **the API key requires approval, so it may be hard to get on the same day** (the VWorld key is issued immediately).
  → It is excluded from this practice's completion criteria and done by students who applied in advance or as homework after class. See guide §9.
- `examples/vworld_map_sample.html` is a reference sample built with Leaflet + VWorld tiles + `localStorage` (API key not included).
  If you put a key in `KIGAM_KEY` inside the file, a menu to turn 1:50,000 / 1:250,000 geological maps on and off appears.
- For service URL pre-checks, alternatives, and sample review points, see the instructor guide [`docs/vworld_map_instructor_guide.en.md`](docs/vworld_map_instructor_guide.en.md).

---

Below are the repository layout and the data and preparation procedures for **Practice 2 (Conference Organizer)**.

## Repository layout

```
data/conference.json                           Practice data (not tracked by git, generated by scripts/parse_program_book.py)
data/src/                                      Original PDF (not tracked by git) — gsk2025_program_book.pdf
steps/step2_list.html                          Step 2  Draw the list with JS
steps/step3_filter.html                        Step 3  Date/room filters, search (state + render)
steps/step4_bookmark.html                      Step 4  ☆ bookmarks (localStorage), My Schedule, time overlaps
steps/app.html                                 Step 5  Finished version: bottom tabs, talk detail (hash routing), sessions, abstract full-text search, bookmark export/import
build.py                                       Template + JSON → single HTML (for local use; does the same as build() in the notebook)
scripts/make_notebook.py                       Generates the notebook by putting steps/*.html into %%writefile cells
scripts/check.py                               Full verification (build, JS syntax, notebook, render smoke test)
scripts/smoke_test.js                          jsdom render smoke test (called by check.py)
docs/conference_organizer_practice_guide.md    Practice 2 student guide (Conference Organizer)
docs/conference_organizer_instructor_guide.md  Practice 2 instructor guide
docs/reference_notebook_guide.md               Practice 2 reference solution notebook guide (released at the end of class)
docs/vworld_map_practice_guide.md              Practice 1 student guide (VWorld Map App, §9 KIGAM geological map advanced)
docs/vworld_map_instructor_guide.md            Practice 1 instructor guide
examples/vworld_map_sample.html                Practice 1 reference sample
README.en.md, docs/*.en.md                     English versions of the guides above and of this README
```

Every template has a single placeholder `const DATA = __DATA__;`, and Python puts the JSON into that spot
(`</` is escaped as `<\/`). Because `fetch` is blocked when opening via `file://`, the data is embedded in the HTML.
The templates read the conference name, dates, rooms, and sessions entirely from `DATA`, so they work as-is with data from another conference that uses the same schema.

## Practice 2 — Data

Schema (`data/conference.json`):

| Key | Fields |
|---|---|
| `meta` | `name`, `full_name`, `place`, `days` (list of ISO dates), `note` |
| `sessions[]` | `code`, `title` |
| `talks[]` | `id`, `date` (ISO), `day_label`, `time_start`, `time_end` (`HH:MM`, two digits), `room`, `session`, `title`, `first_author`, `kind` (`talk`/`plenary`), `abstract_id` |
| `abstracts[]` | `id`, `session`, `title`, `authors[]`, `affiliations[]`, `abstract`, `keywords[]` |

- Times must always be in **two-digit** `HH:MM` format. Time overlap calculation and sorting rely on string comparison.
- Keep `talks` sorted by date and start time (My Schedule and overlap calculation use this order).
- Do not leave `room` empty (room filter). Talks without an abstract have `abstract_id: null`.
- The current data was extracted from the **2025 Joint Fall Meeting of Korean Geological Societies program book** (a PDF attached to a notice board post of the Geological Society of Korea (GSK)).
  382 oral talks (including 5 plenary ones such as special lectures), 229 posters (P001–P209, Next-Generation Geoscientist Program Y001–Y020), 38 sessions, 3 days · 9 rooms.
  - The program book **has no abstract text**, so `abstract`, `keywords`, and `affiliations` are empty; only the author lists are included.
    The abstract book PDF can only be downloaded after logging in as a society member.
  - Posters have no presentation time, so they were added not as `talks` but as **unscheduled `abstracts`** (with `[P001]` in front of the title).
  - Slots without a title, such as breaks, lunch, the opening ceremony, and the general assembly, were left out. One time typo in the original (`12:00-15:15`) is corrected to the start of the next talk.
- When the 2026 program book comes out (expected mid-October), put it in `data/src/`, run the same parser, and check with `python scripts/check.py`.
  If the page layout has changed, fix the coordinate and font size rules in the header comment of `scripts/parse_program_book.py`.
- These are conference materials, so **do not upload them to public repositories or the web** (`data/` and `dist/` are in `.gitignore`).

## Practice 2 — Pre-class preparation (instructor)

For class operation and checklist items, see [`docs/conference_organizer_instructor_guide.en.md`](docs/conference_organizer_instructor_guide.en.md). Below are the procedures for creating the materials,
and for preparing the reference solution notebook so that students can follow it right away.

1. Create the data: put the program book PDF in `data/src/`, then
   `python scripts/parse_program_book.py [PDF]` → `data/conference.json` (requires `pip install pymupdf`)
2. Create the notebook: `python scripts/make_notebook.py` → `gsk2026_practice.ipynb`
3. Verify: `python scripts/check.py` (see "Verification" below)
4. Upload the notebook to Drive, open it in Colab, and **run it once from top to bottom**.
   In particular, check that the `preview()` preview shows up on the lab network and that `download()` works.
5. Share the notebook link as **view-only**. Students work after "Save a copy in Drive".
6. Decide how to distribute the data (`docs/reference_notebook_guide.en.md` §3-2, `docs/conference_organizer_practice_guide.en.md` §2).
   - **Method A, upload**: hand out `conference.json` via messenger or LMS and have students upload it. The simplest.
   - **Method B, Drive**: put it in a shared folder; students "Add shortcut to My Drive" → edit `DATA_PATH` in the notebook.
     An extra Drive permission window appears, so it takes a little longer.
   - Either way, **restrict link sharing to enrolled students** and announce that redistribution is not allowed.
7. On the lab PCs, try *Chrome download → double-click the local HTML → bookmark, then reopen* in advance
   (some places block downloads or JS in local files due to security policies).

Also see "Pre-class checks" in `docs/conference_organizer_instructor_guide.en.md`.

## Practice 2 — (Alternative) Lecture-style session with the reference solution notebook (e.g., 3 hours)

The schedule for the default class format (Gemini practice) is in `docs/conference_organizer_instructor_guide.en.md`. Below is a lecture-style session that walks through the reference solution notebook together from the beginning.

| Time | Step | Key points |
|---|---|---|
| 0:00 | Introduction, save a copy, connect the runtime | Showing the finished version first motivates students |
| 0:10 | Preparation — helper functions, loading data | Check that everyone sees the counts (`sessions …, talks …`) |
| 0:20 | Step 0 — Exploring the data (pandas) | Link between `talks` ↔ `abstracts` (`abstract_id`) |
| 0:35 | Step 1 — Static HTML with f-strings | Why `html.escape` is needed. Lead into the need for JS with "What if we want to change the date?" |
| 0:55 | Step 2 — List with JS | `__DATA__` substitution, template literals, `esc()`, how to view the F12 console |
| 1:20 | Break | |
| 1:30 | Step 3 — Filtering and search | Explain the **state → render()** pattern by drawing it on the board |
| 2:00 | Step 4 — Bookmarks and My Schedule | `localStorage`, `Set`, event delegation, overlap calculation (string time comparison) |
| 2:30 | Step 5 — Finished version, download and open on the PC | Hash routing, bookmark export/import. Check that bookmarks persist |
| 2:45 | Assignment guidance, Q&A | "Assignment ideas" at the end of the notebook |

If time is short, skip the "Things to try" in Step 3; for Step 5, you can just show the features without explaining the code.

## Practice 2 — Cautions

- **Runtime reset**: after a long idle period, uploaded files and generated HTML disappear. Run "Runtime → Run all before" and upload the data again.
- Students often delete **the first line of `%%writefile` and `__DATA__`**. `build()` reports this with an error message in Korean.
- **Preview doesn't change**: in most cases the template cell was not re-run.
- **Blank white screen**: open the downloaded file in Chrome and press `F12` → Console. Most cases are mismatched backticks or brackets.
- **Bookmark storage**: the Colab preview and the downloaded file are stored separately. In Chrome, local HTML files share storage with each other,
  so it is normal for bookmarks from the Step 4 and Step 5 files to appear together (same key `gsk2026.bookmarks`).
- **Phones not recommended**: file app previews on phones don't handle JS and `localStorage` well. Run the class on PC Chrome.
- The resulting HTML (about 2 MB) contains **everything, including abstract text**. Tell students not to upload it to public places.

## Practice 2 — Development (when editing templates)

```bash
# Build one template and check it in the browser
python build.py steps/app.html data/conference.json dist/conference.html

# If you changed a template, regenerate the notebook (steps/*.html is the single source of truth)
python scripts/make_notebook.py

# Full verification
python scripts/check.py
```

### Verification

What `scripts/check.py` does:

1. Builds all templates into `dist/`, extracts the `<script>` blocks, and runs `node --check`
2. Checks that the script doesn't break even if the data contains `</script>` (`</` escaping)
3. Notebook JSON validity, Python cell syntax, and whether the `%%writefile` cells match `steps/*.html`
4. If jsdom is available, runs a render smoke test with `scripts/smoke_test.js` (filtering, search, bookmark saving, overlaps, detail, export/import, etc.).
   Test values are also picked from the data, so it still runs as-is if you change the data.

jsdom is not a project dependency. Install it anywhere and point to it with `NODE_PATH`.

```bash
mkdir -p /tmp/jsdom && (cd /tmp/jsdom && npm i jsdom)
NODE_PATH=/tmp/jsdom/node_modules python scripts/check.py
```
