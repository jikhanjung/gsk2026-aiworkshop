# Instructor's Class Guide — Building the Conference Organizer (conference timetable app) with Gemini

[한국어](conference_organizer_instructor_guide.md) | **English**

## Class format

- Students start from an **empty Colab notebook** and build up the notebook by **typing prompts to Gemini** in the side panel.
- Deliverable: the conference timetable web app **Conference Organizer** — **a single HTML file** (downloaded and opened in a PC browser).
- At the start, the instructor gives only **the goal and the completion criteria**. The reference solution notebook is **released at the end of class** so students can compare.
- The core of the assessment is not the code itself but **the process of stating requirements precisely in words, verifying the results, and asking for fixes**.
- This is the **second practice** of the workshop. We assume students already learned how to work with Gemini in Practice 1 (VWorld Map App, `docs/vworld_map_instructor_guide.en.md`).
  **Be sure to point out what changes**: the map app used the internet and a CDN (Leaflet), but this app must open **without the internet** and uses no external libraries.
  Expect more students to slip into map-app habits, such as adding a CDN or loading the data separately with `fetch`.

| What students get | When |
|------------------|------|
| `docs/conference_organizer_practice_guide.en.md` (completion criteria, prompt examples, cautions) | Start of class |
| `conference.json` (shared via Google Drive or distributed as a file) | Start of class |
| Reference solution notebook link + `docs/reference_notebook_guide.en.md` | End of class |

> If you want to keep things more open without handing out the prompt examples (guide §4), give only the §1 completion criteria first and show §4 only to students who get stuck.

Reference solution notebook: https://colab.research.google.com/github/jikhanjung/gsk2026-aiworkshop/blob/main/gsk2026_practice.ipynb

---

## Pre-class checklist

- [ ] **Check that Gemini in Colab turns on for the lab PCs and student accounts** — school Workspace accounts often have it disabled by the administrator.
      If it doesn't work, tell students to use a personal Gmail account. (There may also be age or region restrictions.)
      **The Gemini panel is closed by default in a new notebook** — it opens only when you click the blue ✦ "Toggle Gemini" button at the bottom center
      of the screen. Most "I can't see Gemini" questions come from this, so show it on screen at the start of class.
- [ ] **Go through the whole process with Gemini yourself once** — the Gemini UI and features change often. Check that the button names and positions
      in the guide match the current ones, and update the guide if they differ.
- [ ] On the lab PCs, check that **Chrome download → double-click the local HTML → bookmarks persist** works (some PCs block this through security policies).
- [ ] Test the data distribution route (Google Drive share link permission: "Anyone with the link – Viewer").
- [ ] Gemini **usage limits**: free accounts may hit the limit. In a long class, some students may get blocked partway through,
      so prepare spare accounts or pair work.
- [ ] Decide whether to allow Colab's **agent-style features** (a mode that generates the whole notebook at once) and announce it.
      If allowed, results come faster, but students get less practice in asking for and verifying things step by step.
- [ ] Announce that redistributing the data is prohibited.

---

## Sample schedule (3 hours)

| Time | Content |
|------|------|
| 0:00–0:15 | Introduce the goal — demo of the finished app (show the reference solution HTML on the instructor's screen only; files and code are not shared). Explain the completion criteria |
| 0:15–0:30 | Setup — new notebook, Gemini panel, data upload. Stress **the importance of the Step 0 prompt (stating the conditions)** |
| 0:30–0:50 | Step 1: understand the data structure. Let students experience "Gemini makes up field names" firsthand |
| 0:50–1:30 | Steps 2–3: list, date/room filters, search. **Make sure they download the file and open it by double-clicking** |
| 1:30–1:40 | Break |
| 1:40–2:20 | Step 4: bookmarks, My Schedule, overlaps. Check by closing and reopening the browser |
| 2:20–2:40 | Step 5: free polishing |
| 2:40–3:00 | Release the reference solution → comparison discussion, share reflections |

---

## Where students get stuck and intervention hints

Rather than giving students the answer right away, ask them **which prompt they should rewrite**.

| Symptom | Cause | Hint |
|------|------|------|
| Colab preview works but **the downloaded file shows a blank screen** | `fetch("conference.json")` — blocked under `file://` | "When you only have the one downloaded file, where does the data come from?" |
| Breaks when the internet is turned off | CDN (Bootstrap, etc.) | Have them reread completion criterion #2 |
| Flask/Streamlit code | Interpreted as a server app | Have them restate the Step 0 conditions to Gemini |
| Python f-string `KeyError`/`SyntaxError` | Conflicts with JS `{}` | Suggest "separate the HTML into a template and substitute into it" |
| Earlier features disappear after adding a feature | Whole thing rewritten | Explicitly say "keep the existing features" + save a file per version |
| Bookmarks don't persist | Incognito window / different browser / confused with the preview | Check which file was opened in which window |
| Overlap display is wrong | String comparison like `"9:00" < "10:00"`, date ignored | Have them check the time format in the data themselves |
| Files disappear after runtime reset | Long idle time | Re-upload the data + "Run all previous cells" |
| Gemini goes off track as the conversation gets long | Lost context | New conversation + a prompt summarizing the requirements |

> In the data, all times are normalized to two-digit `HH:MM`, so string comparison happens to work.
> If you want to use overlap calculation as a discussion topic, ask "What if it were another conference's data?"

---

## Assessment criteria (example)

| Area | Weight | Content |
|------|------|------|
| Meeting the completion criteria | 50% | The 9 items in guide §1 (equal points per item). The instructor opens the submitted HTML directly to check |
| Process | 30% | Step-by-step progress left in the notebook, results per version, traces of re-requesting after hitting errors |
| Reflection | 20% | Prompts that worked well, moments Gemini was wrong and how they handled it, differences compared with the reference solution |

Quick grading check:
1. Put the submitted HTML **alone in an empty folder** and open it **with Wi-Fi turned off** → #1, #2.
2. Change the date and room, search for an author → #3–#5.
3. Bookmark 2 talks in different rooms at the same time slot → My Schedule, overlap display → #6, #7, #9.
4. Close the tab and reopen → #8. (Before grading, use a separate Chrome profile or clear the bookmarks so no bookmarks from another student's file remain —
   Chrome shares storage among local HTML files, so **bookmarks from another student's file that used the same localStorage key may show up.**)

---

## Wrap-up: comparing with the reference solution

The reference solution notebook (`gsk2026_practice.ipynb`) produces the same result using **step-by-step templates**. Discussion questions:

- How the data gets into the HTML: how does your notebook do it? (f-string / substitution / fetch …) — the reference solution substitutes at the `__DATA__` placeholder + escapes `</`.
- Screen updates: does each button patch the DOM separately, or is everything redrawn from **one state + `render()`**?
- The bookmark storage format and the localStorage key name. What if the key collides with another app?
- How time overlap is calculated. What if a time has a single-digit hour like `9:00`?
- Which parts of the code Gemini wrote did you **move past without understanding**?

---

## Replacing the data

- Current practice data: extracted from the program book of the 2025 Joint Fall Meeting of Korean Geological Societies (no abstract text).
- Once the GSK 2026 program book is released (expected mid-October), regenerate it with `scripts/parse_program_book.py`.
  See the "Data" section of the README for the detailed procedure. The reference solution does not depend on the data, so it can be used as is.
