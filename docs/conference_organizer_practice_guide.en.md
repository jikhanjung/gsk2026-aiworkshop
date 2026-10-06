# Building a Conference Organizer (conference timetable app) with Gemini — Student Practice Guide

[한국어](conference_organizer_practice_guide.md) | **English**

In this practice, you ask **Gemini** (next to Google Colab) in plain words to build
**Conference Organizer, a conference timetable app that runs in your own PC's browser (a single HTML file)**, from conference talk data (JSON).
You will not write all the code yourself. Instead, you practice **explaining exactly what you want, checking the result, and asking for fixes**.

---

## 1. What are we building — completion criteria

If everything below works, you have succeeded. Keep this table next to you throughout the practice and check against it.

**Must have**

| # | Criterion | How to check |
|---|------|-----------|
| 1 | Works as **a single HTML file** (no other files or server needed) | Move just that one file from your Downloads folder to another folder and open it — it still works |
| 2 | Opens **without internet** | Turn off Wi-Fi and open it — the screen looks normal |
| 3 | You can view talks by date | Changing the date changes the list |
| 4 | You can view talks by room | You can pick among rooms running at the same time |
| 5 | You can **search** by title and author | Try an author name you know |
| 6 | You can **bookmark (☆)** a talk | |
| 7 | Bookmarked talks are collected in **My Schedule** in time order | Check they are grouped by date and in time order |
| 8 | **Bookmarks remain after you close and reopen the browser** | Close the tab and open the file again |
| 9 | It warns you about **bookmarks whose times overlap** | Bookmark two talks at the same time in different rooms |

**Nice to have** — talk details when you click a talk, viewing by session, a design that fits phone screens,
exporting/importing bookmarks, automatically selecting today's date, a printable My Schedule …

> **How this differs from Practice 1 (VWorld Map App)**: The map app downloaded map images from the internet, so it was fine to use external libraries (CDN) like Leaflet.
> This app must open **without internet**, so it uses no external libraries, and the data also goes inside the HTML (criteria #1, #2).
> Make this condition clear to Gemini in Step 0.

---

## 2. Preparation

| What you need | Notes |
|--------|------|
| **Personal Google account** | School or work accounts may have Gemini turned off (§7-1) |
| PC + **Chrome** | Phones and tablets are not recommended |
| Data file `conference.json` | Provided by the instructor |

1. https://colab.research.google.com → **New notebook**.
2. Rename the notebook (e.g. `ConferenceApp_YourName.ipynb`). The notebook is saved in the `Colab Notebooks` folder in your My Drive.
3. Click **the blue round ✦ button at the bottom center** of the screen (hover over it and it says **Toggle Gemini**) to open the Gemini panel.
   When you open a new notebook, the Gemini panel is **closed by default**, so you won't see it at first. Clicking again closes it.
   If the button isn't there at all, see §7-1.
4. Upload the data file to the runtime. Either:
   - **Upload**: 📁 Files panel on the left → upload button → `conference.json`
     (or ask Gemini: "Make a cell that uploads a file")
   - **Drive**: put `conference.json` in your Drive and ask Gemini: "Connect to my Drive and make code that reads this file"
     (allow it in the permission window)

> ⚠️ Uploaded files **disappear when the runtime disconnects.** If you come back after a long break, you need to upload them again (§7-2).

---

## 3. How to work — one round

```
① Tell Gemini what you want
② Read the code Gemini gives you, put it in a cell, and run it
③ Preview / download the resulting HTML and open it in the browser
④ Compare with the completion criteria (§1) → describe again, specifically, what isn't working
```

You go around this loop many times. **Don't ask for everything at once.** The smaller the steps, the better it works.

---

## 4. Step by step — example prompts

The prompts below are **examples**. Rather than copying them as-is, rephrase them in your own words and add to them as you see the results.

> **You don't need to know programming terms.** Tell Gemini in everyday words ① **what you want to do**, ② **how you'd like the screen to look**,
> and ③ **how you will check it**. Gemini chooses which technology to use.
> But be sure to state the **conditions that must be met** (a single file, opens by double-clicking, works without internet) at the start. These conditions matter most.

### Step 0. Tell Gemini what you want and the conditions

> I have a file with a conference talk schedule (`conference.json`). I want to use it to make **a program for choosing which talks I'll attend and planning my schedule** during the conference.
> Here are the conditions:
> - I'd like the result to be **a single file**. I should be able to download it and **just double-click it** to open. No need to install or keep anything else running.
> - The Wi-Fi might not work at the conference venue, so it has to open and work the same way **even without internet**.
>   That means all the talk information has to be inside that one file too.
>
> I don't know much about programming. Let's not do it all at once — let's go step by step together.
> At each step, tell me what I need to do (which cell to run and what to check). First, let's see what's in this file.

- If Gemini uses a word you don't know, ask right away: "What is ○○? Explain it simply."

### Step 1. See what's in the data

> Show me **simply** what's inside the `conference.json` I uploaded.
> What groups of data are there and how many of each, and show me one example of what information a single talk has.

- **Look at the output yourself.** Check under what **English names** the talk list, date, start/end time, room, title, author … are stored.
- Gemini often **makes up** these names. If you **copy the names exactly** as shown on screen (e.g. `talks`, `room`) into your next requests, things become accurate.
  You don't need to know what they mean — just copy what you see.

> Show me a table of how many talks there are for each date and each room.

### Step 2. First screen — the talk list

> Now make a screen that shows the list of talks. **Just the first day's talks** for now.
> Show each talk like a card with the **time, room, title, and first author**.
> Make the result a file `app_v1.html` that I can download to my PC, and also let me preview it inside Colab.

- **Double-click the downloaded file to open it in your browser.** Don't stop at the Colab preview.
- If it works in the preview but the downloaded file is empty, see the first row of the table in §7-3.

### Step 3. Choosing date and room, search

> Keep everything that works now as it is, and add **date buttons** and **room buttons** at the top of the screen.
> When I click them, show only the talks for that date and that room. And also add **a search box to find talks by title or author name**.
> Name the file `app_v2.html`.

- Check: search for an author name you know, and try changing the date.

### Step 4. Marking talks I'm interested in, and My Schedule

> Now I want to plan my schedule. Keep everything that works now as it is, and:
> - Put a **star (☆) button** on each talk, so clicking it marks the talk as one I'm interested in.
> - What I marked should still be there **even after I close and reopen** the program.
> - Make a separate **"My Schedule"** screen that collects the marked talks by date, **in time order**.
> - If talks **overlap in time so I can't attend both**, mark them in red to let me know.
>
> Name the file `app_v3.html`.

- Checking overlaps: mark two talks in different rooms at the same time slot.
- Checking close-and-reopen: close the tab and open the file again.

### Step 5. Polishing (free)

Use your own app and ask Gemini to fix whatever is inconvenient. For example:

> When I click a talk, show its detailed information (all authors, etc.). Also show the list of other talks in the same session.

> Make it look good on a phone screen too. I'd like menu buttons along the bottom.

> Let me **save my schedule to a file** and **load it** on another computer.

---

## 5. How to write good prompts

**Instead of technical terms, be specific about what you want and what you saw.**

| Do this | Instead of this |
|--------|----------------------|
| "When I click a date button, show **only that date's talks**" | "Add a filter feature" |
| "**Keep everything that works now as it is** and just add a search box" | "Add a search feature" (other features sometimes disappear) |
| Say **exactly what you saw**: "I clicked the star but it doesn't show up in My Schedule" + copy the red error message | "It doesn't work" |
| Copy **the names exactly** as shown in Step 1 (`talks`, `room` …) | Only using words like "time" or "place" (Gemini makes up names) |
| Give result files **versioned names** (`app_v1`, `app_v2` …) | Keep overwriting the same name |
| When an unfamiliar word comes up: "What is ○○? Explain it simply" | Moving on without understanding |

- When the conversation gets long, Gemini forgets the earlier conditions. If things get strange, open a **new conversation** and tell it again, summarizing the conditions from Step 0
  and the features you've built so far. ("So far I've built these features: … Next I want to do ○○")
- You don't have to understand all the code Gemini gives you. But make it a habit to ask, **before running it**, "Explain what this code does in a line or two."
- It's normal for every student's result to be different. All that matters is meeting the completion criteria (§1).

---

## 6. Checking the result

1. **Double-click** the HTML file in your Downloads folder → it opens in Chrome. If the address bar starts with `file:///…`, that's correct.
2. Check the completion criteria in §1 one by one.
3. If the screen is blank white or buttons don't respond, check the red errors in the **`F12` → Console** tab, and
   **copy that error message exactly** and give it to Gemini.
   (Gemini cannot see your browser screen. Unlike Colab cell errors, you have to pass browser errors along yourself.)

---

## 7. ⚠️ Things to watch out for

### 7-1. Using Gemini

**If you can't see the Gemini panel**

- **First, click the blue ✦ button (Toggle Gemini) at the bottom center of the screen.** The panel starts out closed.
  You can also open it with the "generate with AI" link inside a cell.
- If that button doesn't exist at all:
  - Colab's AI features only appear if your **account age is 18 or older** and you are in a **supported region**.
  - **School or work (Workspace) accounts** may have it turned off by an administrator → reopen it in a window signed in with your **personal Gmail**.
    (Check which account the profile picture at the top right belongs to. If several accounts are signed in, it's easy to end up in a different account.)
  - Refresh (`F5`), open it in an incognito window with your personal account, or turn off ad-blocker extensions.
  - If it still doesn't work, tell the instructor and continue with a partner. (It may be a temporary error on Colab's side.)

**Other things**

- **Usage limits**: free accounts have a limit on how many requests they can make within a certain time. Rather than sending many short questions,
  gather your requirements and send them accurately in one go.
- **Don't paste the data into the chat.** The file is large, so it gets cut off and Gemini judges based on only part of it.
  Upload the file to the runtime and say "Read it with code and check."
- Gemini can confidently give plausible but **wrong answers**. Always check by running it.

### 7-2. Colab runtime

- **When the runtime disconnects, uploaded files and the HTML you made disappear** (notebook cells remain).
  → Upload the data again and recover with the menu **Runtime → Run before** (run all previous cells).
  → Download a version that works right away, or save it to Drive.
- Cells must be run **in order from the top**. If you run only a cell in the middle, you get a `… is not defined` error.

### 7-3. Common Gemini mistakes — ask again if you get results like these

The key to "What to say" is **describing exactly what you saw, and pasting the error message if there is one**. You don't need to understand the "Why it happens" column.

| If this happens | What to say | Why it happens (you don't need to know) |
|------------------|---------------|------------------------|
| It works in the Colab preview, but **when you open the downloaded file, the list is empty** | "I can see the talks in the preview, but when I open the downloaded file it's empty. It has to show them with just that one file" | It reads the talk data separately from outside the file (`fetch`) — this is blocked on your PC |
| The layout breaks **when you turn off the internet** | "I opened it with the internet off and the layout broke. It has to look the same without internet" | It loads design tools from the internet (CDN) |
| Words like "run the server", Flask, Streamlit, or `localhost` appear | "Make it open just by double-clicking the file, without having to keep anything running" | It was built as a web server program |
| A red error after running a cell (`KeyError`, `SyntaxError`, etc.) | "I ran the cell and got this error: (paste error)". If the same error keeps coming back: "Keep the screen part (HTML) separate from the Python code, and just swap the data into its placeholder" | Python mistakes the `{ }` in the screen code for its own (f-string) |
| The screen **suddenly goes blank white** | "The screen comes out blank white. There's this red text in the F12 console: (paste)" | Certain characters in the data (`</script>`) cut off the screen code, etc. |
| After adding a new feature, **an old feature disappeared** | "The date buttons disappeared. Keep all the features that used to work and fix it" | It rewrote the code from scratch and left things out |
| **The screen breaks** on a talk whose title has a symbol like `<` | "The screen breaks on this talk: (title). Make it show any characters exactly as they are" | The text is interpreted as screen code (missing escaping) |
| **The time order is strange** (a 9 o'clock talk comes after 10 o'clock) | "The 9 o'clock talk comes after the 10 o'clock talk. Show them in time order" | Times are compared as text |
| `undefined` appears on screen or information is blank | "It says undefined where ○○ should be. The name I saw in Step 1 is `…`" | Gemini made up the data names |

### 7-4. Downloads and bookmarks

- **Chrome recommended.** If "Allow multiple file downloads" pops up the first time you download, allow it.
  If downloading doesn't work, right-click the file (⋮) in the 📁 Files panel on the left → Download.
- If you download the same name several times, files pile up like `app (1).html`. Make sure **you are opening the latest file**.
- Bookmarks are saved only **in that browser on that PC**. In an incognito window they disappear when you close it.
- In Chrome, HTML files on your PC share the same storage, so bookmarks made in v2 may show up in v3 (this is normal).
- Bookmarks in the Colab preview and bookmarks in the downloaded file are **separate**.

### 7-5. Data and results

- The HTML you make **contains the entire dataset.** Sharing the file = sharing the data.
- The practice data is **for class use only**. Do not post it anywhere public such as websites, GitHub, or social media.

---

## 8. Submission (follow the instructor's directions)

- The finished HTML file (e.g. `app_final.html`)
- Your Colab notebook (share link or `.ipynb` download)
- A short reflection: the one prompt that worked best, and a moment when Gemini was wrong and how you fixed it

At the end of class, the instructor will release the **reference solution notebook**. Compare it with yours —
the final task is to see how the following are the same or different: how the data is put into the HTML, how the screen is redrawn (state + render), how bookmarks are saved, and how time overlaps are calculated.
