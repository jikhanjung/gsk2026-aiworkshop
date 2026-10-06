# Reference Solution Notebook Guide — Building the Conference Organizer (conference timetable app)

[한국어](reference_notebook_guide.md) | **English**

> **This document is released at the end of the class.** In the main class, students build their own notebook
> by chatting with Gemini in Colab ([`conference_organizer_practice_guide.en.md`](conference_organizer_practice_guide.en.md)). This document is for
> following the instructor's pre-built reference solution notebook `gsk2026_practice.ipynb` and **comparing it with what you made**.
> Notebook link: https://colab.research.google.com/github/jikhanjung/gsk2026-aiworkshop/blob/main/gsk2026_practice.ipynb
> **Note:** the notebook itself (explanations and code comments) is written in Korean. This guide walks through the same steps in English.

In this practice you take conference presentation data (JSON), build a web app HTML file in **Google Colab**, download it,
and **use it directly in the browser on your own PC**. At the end you will have a single HTML file with the following features:

- View the presentation program by date and room
- Search titles, authors, and abstracts
- ☆ bookmarks → **My Schedule** (a chronological timetable that marks presentations whose times overlap)
- Presentation details (abstract, authors, affiliations, keywords)

> All the data is inside this one file, so it opens with a simple double-click — no internet or server needed.

---

## 0. What you need

| Item | Description |
|------|------|
| Google account | For using Colab and Google Drive |
| PC + **Chrome** browser | Other browsers work too, but this practice assumes Chrome. **Phones and tablets are not recommended** |
| Practice notebook link | Shared by the instructor (`gsk2026_practice.ipynb`) |
| Data file | `conference.json` — distributed by the instructor (via a shared Drive folder or handed out directly) |

---

## 1. Opening the notebook — always start with a "copy"

1. Open the notebook from the link the instructor gave you.
2. In the menu, click **File → Save a copy in Drive**.
   When a `Copy of …` notebook opens in a new tab, **work only in that copy from now on**.
   - ⚠️ If you work in the original, your changes won't be saved (it is view-only) or will get mixed up with other people's.
3. Click the **Connect** button at the top right to connect to a runtime (a virtual computer).
   If you see the warning "This notebook was not authored by Google", click **Run anyway**.

---

## 2. Notebook structure at a glance

| Step | What you do | What you learn |
|------|---------|-----------|
| Setup | Define helper functions, load the data | Uploading files, reading JSON |
| Step 0 | Explore the data | JSON structure, pandas tables |
| Step 1 | Build HTML with Python only | How data becomes HTML (f-strings) |
| Step 2 | Draw the presentation list with JS | Array → HTML, `innerHTML`, escaping |
| Step 3 | Date/room filters, search | The state + `render()` pattern, events |
| Step 4 | ☆ bookmarks and My Schedule | `localStorage`, computing time overlaps |
| Step 5 | Finished version | Tabs, detail view (address `#` routing), exporting bookmarks |
| Assignment | Add your own features | |

Every step follows the same sequence.

```
Run template cell (%%writefile)  →  build()  →  preview()  →  download()  →  Open on my PC
   Save the HTML skeleton to a file     Insert data    Preview in Colab     Download
```

---

## 3. Setup cells

### 3-1. Run the helper function cell

Run the **Setup** cell at the very top of the notebook (the ▶ on the left of the cell, or `Ctrl+Enter`).
This creates the three functions below. You don't need to understand their code, but do learn their names and what they do.

| Function | What it does |
|------|---------|
| `build("template.html", "result.html")` | Inserts the data into the `__DATA__` spot of the template to create the result HTML |
| `preview("result.html")` | Shows the result HTML inside the Colab screen |
| `download("result.html")` | Downloads the result HTML to your PC |

### 3-2. Loading the data

Use whichever of the two methods your instructor tells you to.

**Method A — Upload the file**
1. When you run the data cell, a **Choose Files** button appears.
2. Select the `conference.json` you downloaded beforehand.
3. If counts like `sessions …, talks …, abstracts …` are printed, it worked.

**Method B — Connect Google Drive**
1. When you run the Drive cell, a permission window pops up → choose your account → **Allow**.
2. Add the `conference.json` shared by the instructor to your Drive with **Add shortcut to Drive** (or make a copy).
3. Edit the path in the cell (`/content/drive/MyDrive/…`) to match your file's location, then run it.

> 💡 Open the 📁 **Files** panel on the left to see the files in the runtime. If you see `conference.json`, you're ready.

---

## 4. Step 0 — Exploring the data

The data has four parts.

| Key | Contents | Main fields |
|----|------|-----------|
| `meta` | Conference info | `name` (conference name), `place`, `days` (list of dates) |
| `sessions` | Sessions | `code`, `title` |
| `talks` | Presentation schedule | `id`, `date`, `day_label`, `time_start`, `time_end`, `room`, `session`, `title`, `first_author`, `kind`, `abstract_id` |
| `abstracts` | Abstracts | `id`, `session`, `title`, `authors[]`, `affiliations[]`, `abstract`, `keywords[]` |

- Presentations (`talks`) and abstracts (`abstracts`) are linked via `talks[i].abstract_id` ↔ `abstracts[j].id`.
  Some presentations have an empty (`None`) `abstract_id` (workshops, etc.).
  Some abstracts, such as posters, have no presentation slot, and depending on the data the abstract body (`abstract`) may be empty.
- Run the cell to view the data as a table (DataFrame), and try counting presentations by date and by room.

---

## 5. Step 1 — Building HTML with Python only

Without any JS, you build an HTML file by joining `<li>…</li>` pieces with Python f-strings.

1. Running the cell creates `step1.html` and shows a preview.
2. Download it with `download("step1.html")` and double-click it to open.

**Key idea**: a web page is ultimately just text (HTML), and you can build it by looping over the data and joining text together.
However, this approach makes it hard to build **features that react instantly on screen**, like filtering and search → so from Step 2 on we use JS.

---

## 6. Steps 2–5 — Edit the template → build → view

### 6-1. Template cells

Each step has a cell that starts like this.

```
%%writefile step2_list.html
<!doctype html>
<html lang="ko">
…
<script>
const DATA = __DATA__;
…
</script>
```

- **Do not delete the first line `%%writefile filename` or add spaces to it.** This line means "save the contents of this cell to a file".
- The contents of this cell are **HTML/CSS/JS, not Python**. When you run it, the screen only shows `Writing step2_list.html`.
- **Leave the `__DATA__` in `const DATA = __DATA__;` as is.** `build()` puts the data in this spot.
  (If you delete it or write it twice, `build()` will raise an error.)

### 6-2. Build and view

The cell right below the template cell:

```python
build("step2_list.html", "out_step2.html")
preview("out_step2.html")
```

- If you edited the template, you must re-run both cells in the order **template cell → the cell below** for the changes to take effect.
- If the preview doesn't change: re-run the cell, or right-click inside the preview → **Reload**.

### 6-3. Checkpoints for each step

| Step | What to check in the preview | Things to try (see the comments at the end of the cell) |
|------|------------------------|---------------------------|
| Step 2 | Are the first day's presentations listed as cards? | Show the number of presentations, show the session code |
| Step 3 | Does the list change when you click the date/room chips? Is the search term highlighted in yellow? | Add chips that filter by session code |
| Step 4 | Does ☆ turn into ★ when clicked, and do the bookmarked talks gather in the **My Schedule** tab? Are overlapping presentations marked? | Dim overlapping presentations |
| Step 5 | Does clicking a presentation go to its detail (abstract) view, and does the Back button work? | See "Assignment" below |

---

## 7. Downloading and opening on your PC

```python
download("out_step5.html")
```

1. When you run the cell, the download appears at the bottom (or top right) of the browser.
2. In your **Downloads folder**, **double-click** the file → it opens in Chrome.
   If the address bar shows something like `file:///C:/Users/…/out_step5.html`, it's working correctly.
3. Bookmark a few talks, close the tab, and open it again — **if they are still there, it worked**.

> You can rename the downloaded file to whatever you like (e.g. `my_conference_schedule.html`) and keep it on your desktop.

---

## 8. ⚠️ Things to watch out for

### 8-1. Using Colab

- **Always work in your copy.** The original notebook is view-only. (§1)
- **When the runtime disconnects, your files disappear.** If you're idle for about 90 minutes, or leave the window closed for a long time, the runtime is reset and
  the uploaded `conference.json` and the HTML files you made are all deleted (the notebook cell contents remain).
  → Recover with the menu **Runtime → Run before** (or run the cells in order from the top). Upload the data again.
  → `download()` your results right away or save them to Drive.
- **Run cells in order from the top.** If you skip the "Setup" cell, you'll get errors like `build is not defined`.
- **If a cell is running (shown with ◼), other cells wait.** If it seems stuck, click ◼ to stop it.
- Whether to use Colab's **AI autocomplete/code generation** (Gemini) follows your instructor's guidance.

### 8-2. Editing template cells

- Don't touch the `%%writefile` first line or the `__DATA__` spot. (§6-1)
- In JS, a single-character mistake can turn **the whole screen blank white**. Common mistakes:
  - Writing a template string's **backtick (`` ` ``)** as a quote (`'`) by mistake, or forgetting the closing backtick
  - Mismatched braces in `${ … }`
  - Mismatched parentheses `( )` or braces `{ }`, or a comma instead of a semicolon
- **Wrap data in `esc()`** when putting it on screen. If a title contains `<` or `&`, the page will break.
- If you broke something while editing: undo the cell contents with **Ctrl+Z**, or copy the cell again from the original notebook.

### 8-3. Finding errors — Developer Tools

If the screen is blank or buttons don't respond, **open the downloaded file in Chrome and press `F12`** → look at the **Console** tab.
The red error messages and line numbers tell you the cause.

| Example error message | Meaning |
|----------------|-----|
| `Uncaught SyntaxError: Unexpected token` | Mismatched parentheses, quotes, or backticks |
| `… is not defined` | A typo in a name, or using something before it is defined |
| `Cannot read properties of null` | The id in `getElementById("…")` doesn't exist in the HTML |
| `Unexpected identifier '__DATA__'` | You opened a template file that didn't go through `build()` |

> You can also see the console inside the Colab preview with right-click → **Inspect**, but checking in the downloaded file is more accurate.

### 8-4. Downloading

- **Chrome is recommended.** In Safari and some other browsers, `download()` may do nothing at all.
- If a "**Download multiple files**" prompt appears on your first download, click **Allow**.
- If `download()` doesn't work: in the 📁 Files panel on the left → right-click the file (or ⋮) → **Download**.
- If you download the same name several times, files pile up as `out_step5 (1).html`, `(2)` …. Make sure **you're opening the most recent file**.
- School or company PCs may block downloads or running local HTML due to security policies → let the instructor know.

### 8-5. Using it on your PC (saving bookmarks)

- Bookmarks are saved only in **that browser on that PC** (`localStorage`). If you open the file on another PC or in another browser, they'll be empty.
  → To move them, use **⬇ Export → ⬆ Import** in the finished version.
- If you open it in an **Incognito (InPrivate) window**, bookmarks disappear when you close the window.
- Chrome makes HTML files on your PC **share the same storage.** So bookmarks you made in Step 4 may also
  show up in the Step 5 file — this is normal, not a bug.
- **Bookmarks in the Colab preview and in the downloaded file are separate.**
- Clearing your browser's "browsing data (cookies and site data)" deletes your bookmarks.
- **If you move the file to a phone and open it**, JS may not run in the file app's preview, or bookmarks may not be saved.

### 8-6. Sharing data and results

- The HTML file you made contains **the entire dataset, including the abstract texts.**
  Sharing the file is the same as sharing the data.
- The practice data is **for class use only**. **Do not post it in public places** such as websites, GitHub, or social media.

---

## 9. Quick troubleshooting table

| Symptom | What to check |
|------|-----------|
| `NameError: name 'build' is not defined` | Did you run the Setup cell? Was the runtime reset? (§8-1) |
| `FileNotFoundError: conference.json` | Did you upload the data? Was it deleted by a runtime reset? |
| `build()` gives a `__DATA__` error | You deleted `__DATA__` from the template or wrote it twice |
| The preview doesn't change | Did you re-run starting from the template cell? Reload the preview |
| The preview area is empty | Re-run the cell. If it still fails, `download()` and check on your PC |
| The downloaded page is blank white | `F12` → check the Console for errors (§8-3) |
| My bookmarks disappeared | Incognito window? Different browser? Cleared history? (§8-5) |
| Downloads don't work | Using Chrome? Allowed downloads? Download directly from the Files panel (§8-4) |

---

## 10. Assignment ideas

Listed in order of difficulty. Try them by editing the finished (Step 5) template.

1. Show a summary like "N talks total · M sessions" at the top of the first screen
2. Show the session title on a presentation card when you hover the mouse over it (`title` attribute)
3. In My Schedule, show the number of bookmarks as a badge next to the tab name
4. A dark mode button (change CSS variables)
5. Make My Schedule look clean **for printing** (`@media print`)
6. Keyword cloud: collect abstract keywords, show them ordered by frequency, and search when one is clicked
7. Export My Schedule as a calendar file (`.ics`)

---

## Appendix — Instructor checklist (before class)

- [ ] Distribute the notebook share link as **view-only** (students save a copy)
- [ ] Decide on and test the data distribution method (file for upload / shared Drive path)
- [ ] On a lab PC, try **Chrome download → open local HTML → bookmarks persist** once (check security policies)
- [ ] Check that the Colab preview (`preview`) loads on the lab network (if blocked, proceed with `download` only)
- [ ] Prepare for runtime resets: demonstrate the "Run before" recovery method early in class
- [ ] Announce whether Colab AI features are allowed
- [ ] Announce that redistributing the data is prohibited
