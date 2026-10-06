# Building a VWorld Map App with Gemini — Student Practice Guide

[한국어](vworld_map_practice_guide.md) | **English**

In this practice you ask **Gemini**, right next to Google Colab, in plain words to build a **map app (a single HTML file)** that records
the sites you mark (field trip sites, sampling sites …) on top of a **VWorld base map**.
This is the **first practice** of the workshop. Here you learn how to ask Gemini step by step, check the result, and ask it to fix things.
Along the way you also learn how to get an **API key for an external service** and use it safely.
(The second practice, the Conference Organizer — `conference_organizer_practice_guide.en.md` — works the same way.)

---

## 1. What you build — completion criteria

**Must have**

| # | Criterion | How to check |
|---|------|-----------|
| 1 | It works as **a single HTML file** | Move only the downloaded file to another folder and open it — it still works |
| 2 | The **VWorld base map shows up using your own API key**, and the whole of South Korea is visible when you first open it | Zoom in and pan around |
| 3 | You **can switch the base map** (standard / satellite / satellite + place names, etc.) | Menu at the top right of the map |
| 4 | **Clicking the map adds a site at that spot**, and you can enter a name and a note | |
| 5 | Clicking a site shows **the information you entered and its coordinates**, and you can **delete** it | |
| 6 | **Sites are still there after you close and reopen the browser** | Close the tab and open the file again |
| 7 | You **can export the site list to a file and import it again** (JSON) | Import the exported file in a different browser |
| 8 | **The API key is not written as-is in the notebook code** | The key is not visible even when you share the notebook (§4 Step 1) |

> Unlike the Conference Organizer, this app **needs the internet**, because the map images (tiles) are downloaded from the VWorld server.
> So it is fine to load a map-drawing tool (e.g. Leaflet) from the internet too. Gemini decides which tool to use.

**Nice to have** — choosing your own input fields, viewing the site list as a table, jumping to a site when you click it in the list,
colors by site type, showing your current location, **geological map overlay (§9, requires a KIGAM API key obtained in advance)**, a "Check your API key" message when map tiles fail to load, CSV export, phone screen support …

---

## 2. Preparation

| What you need | Notes |
|--------|------|
| **A personal Google account** | School or work accounts may have Gemini turned off (§7-1) |
| PC + **Chrome** | |
| **VWorld sign-up + API key** | Get it **before class** (§2-1). Signing up and email verification take time |

### 2-1. Getting a VWorld API key (pre-class assignment)

The VWorld site is in Korean only; the menu names below are given in Korean as they appear on screen.

1. Go to https://www.vworld.kr → **sign up (회원가입)** and log in.
2. In the top menu, go to **오픈API → 인증키 → 인증키 발급** (Open API → API key → Issue API key) (menu names may change).
3. Fill in the application form:
   - Purpose / service name: e.g. `수업 실습 - 답사 지점 지도` (class practice – field site map)
   - **Service URL**: enter **the value your instructor gives you**, exactly as given. (It depends on where you will open the map, so we use a value the instructor has tested in advance.)
   - API to use: make sure **base map (배경지도, WMTS)** is included.
4. In the **verification email sent to the address you signed up with**, click the **인증키 사용** (use API key) button.
   If you skip this, the key will not work.
5. In the **인증키 관리** (API key management) menu, check that the status is **승인** (approved) and when the **expiry date** is.
6. Copy the API key (a long string of letters and numbers) and keep it.

> ⚠️ Treat your API key **like a password**. Do not post it in chat rooms, on bulletin boards, or on GitHub. Someone else could use up your quota with your key.

### 2-2. Preparing Colab

1. https://colab.research.google.com → **New notebook**, and rename it (e.g. `MapApp_YourName.ipynb`).
2. Click **the blue circle ✦ button at the bottom center of the screen** (hover over it and it says **Toggle Gemini**) to open the Gemini panel.
   When you open a new notebook, the Gemini panel is **closed by default**, so you won't see it at first. Click again to close it.
   If the button isn't there at all, see §7-1.

---

## 3. How to work — one loop

```
① Tell Gemini what you want
② Read the code Gemini gives you, put it in a cell, and run it
③ Download the resulting HTML and open it in your browser   ← always check the map app using the downloaded file (§7-3)
④ Compare with the completion criteria (§1) → say specifically what doesn't work
```

**Don't ask for everything at once.** Go one thing at a time: map → switch base map → add sites → save → export.

---

## 4. Step by step — prompt examples

The examples are **for reference only**. Put them in your own words and add to them as you look at the results.

> **You don't need to know programming terms.** Explain to Gemini in everyday words ① **what you want to do**, ② **how you'd like the screen to look**,
> and ③ **how you will check it**. Gemini chooses the technology.
> But be sure to state the **conditions that must be kept** (a single file, opens with a double-click, API key hidden) at the start.
> Only paste the §4-1 reference card below **when Gemini is lost because it doesn't know exact information** such as the VWorld map address.

### Step 0. Tell it what you want and your conditions

> I want to make a **map program** that I open by double-clicking on my PC. I want to mark places I visited on field trips or where I collected samples on a map and keep a record.
> I'd like to use the **VWorld** map from the Ministry of Land, Infrastructure and Transport, and I already have a VWorld **API key**.
> Here are my conditions:
> - I'd like the result to be **one file**. I download it, double-click it, and it opens right away. No need to install or keep any other program running.
> - You can assume I'm connected to the internet.
> - The API key is like a password, so even if I show this notebook to someone else, I want **the key to stay hidden**.
>
> I don't know much about programming. Let's not build it all at once — let's do it together step by step.
> For each step, also tell me what I need to do (which cell to run and what to check).

- If Gemini uses a word you don't know, ask right away: "What is ○○? Explain it simply."

### Step 1. Store the API key safely and check that it works

First ask Gemini where to keep the key.

> How can I store my API key safely without writing it directly in the notebook?

Gemini will tell you about Colab's **Secrets** feature. The steps are:

1. In Colab, click the **key (🔑, Secrets) icon in the vertical icon bar on the left** → **Add new secret** →
   name `VWORLD_KEY`, paste your API key as the value → turn on **Notebook access**.
2. Then tell Gemini:

> I put my API key in Secrets under the name `VWORLD_KEY`.
> First I want to test whether this key works. Download just **one map image** from VWorld,
> and if it works say "success"; if not, tell me why it failed. **Don't show the key on screen.**

- If you get "success", the key works. If it fails, read the message that comes up (§7-2).
- If Gemini keeps failing because it doesn't know the address, paste **§4-1 Reference Card A**.
- Why use Secrets? When you share or submit a notebook, **everything written in the cells is visible.** Secrets are not saved in the notebook file.

### Step 2. First map

> The key works. Now make the actual map screen.
> When I open it I want to see **the whole of South Korea**, and be able to zoom in and out with the mouse and drag it around. I'd like the map to fill **the whole window**.
> Make the result a file `map_v1.html` that I can download to my PC.

- **Double-click** the downloaded file and see if the map shows up.
- If it's white, gray, or broken into scattered pieces, tell Gemini **exactly what you see** (§7-3).

### Step 3. Switching the base map

> Keep everything that works now as it is, and **let me switch the base map**.
> I'd like a regular map, **aerial photos**, aerial photos with **place names and roads** on top, and maybe a plain white map.
> A menu in a corner of the screen to pick from is fine. Name the file `map_v2.html`.

- If the aerial photos don't show up, or only place names appear, say what you see; if it still doesn't work, paste Reference Card A.

### Step 4. Marking, viewing, deleting, and keeping sites

> Now I want to add a recording feature. Keep everything that works now as it is, and:
> - When I **click a spot on the map, put a pin** there and let me write a **name and a note** for that site.
> - Later, when I click the pin, show what I wrote and its **location (latitude and longitude)**, and let me **delete** it too.
> - The sites I marked must still be there **after I close and reopen** the program.
>
> Name the file `map_v3.html`.

- Check: mark 3 sites → close the tab → open the file again.
- Try typing `<b>굵게</b>` (`<b>bold</b>`) in the name field. It is correct if it shows **as plain text, exactly as typed**.
  If it shows up in bold: "I typed `<b>굵게</b>` in the name field and the text came out bold. Make what I type show up **exactly as I typed it**.
  And make sure the screen doesn't break even if I type strange characters." (If you're curious why this matters, ask Gemini.)

### Step 5. Saving to a file and loading it again

> I want to **save the sites I marked to a file** so I can move them to another computer.
> Make a save button and a load button. When loading, ask me whether to **replace or merge** with the sites I have now.
> Name the file `map_v4.html`.

- Try loading the saved file in **a different browser (or an incognito window)**.

### Step 6. Polishing (free)

Use it yourself and tell Gemini what's inconvenient. For example:

> I want to use this for field notes. Let **me decide which fields** to fill in for each site (e.g. site name, lithology, strike/dip, date, note).

> Show a list of sites on the left side of the screen, and when I click one in the list, move the map to that site.

> When the map doesn't show up, don't just leave it gray — **tell me the reason on screen**, like "Check your API key".

### 4-1. Reference card — information to paste when Gemini is lost

**You don't need to understand the contents.** When Gemini keeps failing because it makes up VWorld map addresses, copy the box below and paste it as is.

**Reference Card A — VWorld base map**

```
Here is the VWorld base map information. Please use it exactly as given.
- Map image (tile) address: https://api.vworld.kr/req/wmts/1.0.0/{API_KEY}/{LAYER}/{z}/{y}/{x}.{EXT}
  (The order is z, y, x — y comes before x)
- Layers and extensions: Base (standard map, png), Satellite (aerial photos, jpeg), Hybrid (transparent image with only place names and roads, png — must be laid on top of the aerial photos),
  white (white background, png), midnight (dark background, png)
- Example: standard map at zoom 7, y=49, x=109 → https://api.vworld.kr/req/wmts/1.0.0/{API_KEY}/Base/7/49/109.png
- If the key is wrong, instead of an image you get a text (XML) saying "등록되지 않은 인증키입니다." (unregistered API key).
- You can draw the map with Leaflet.
```

---

## 5. How to write good prompts

**Instead of technical terms, describe specifically what you want and what you saw.**

| Do this | Instead of this |
|--------|----------------------|
| "When I click the map, put **a pin at that spot** and let me write a name and a note" | "Add a marker feature" |
| Say **exactly what you saw**: "I deleted one pin and **a different pin** disappeared" | "It doesn't work" |
| If there's an error, **copy the red text exactly** and paste it | "There's an error" |
| "**Keep everything that works now as it is** and just add ○○" | Mentioning only the new feature (old features sometimes disappear) |
| Name result files **by version** (`map_v1`, `map_v2` …) | Overwriting the same name again and again |
| "Use the **VWorld** map, not Google Maps" | "Add a map" (it may use another company's map) |
| When you see a word you don't know: "What is ○○? Explain it simply" | Moving on without understanding |
| If the same failure repeats, paste the **reference card** (§4-1) | Trying to fix the code yourself |
| Put the API key **only in Secrets** | Pasting the API key into the chat |

- When a conversation gets long, Gemini forgets the earlier conditions. If things get strange, open a **new conversation** and restate the conditions from Step 0
  together with a summary of the features you've built so far. ("So far I've built these features: … Next I want to do ○○")
- You don't have to understand all the code Gemini gives you. But get into the habit of asking, **before running it**, "Explain in one or two lines what this code does."
- It's normal for every student's result to be different. All you need is to meet the completion criteria (§1).

---

## 6. Checking the result

1. **Double-click** the downloaded HTML → Chrome. If the address bar starts with `file:///…`, that's correct.
2. Check the §1 completion criteria one by one.
3. If the map doesn't show up or a button doesn't work: press **`F12`** on the keyboard → the **Console** tab at the top → copy the **red text**,
   and tell Gemini **what you saw + the error message**, like "I opened the downloaded file and it's ○○. I see this error: …".
   (Gemini cannot see your browser screen.) If **your API key appears in the error message, delete that part** before pasting.

---

## 7. ⚠️ Things to watch out for

### 7-1. When you can't see the Gemini button

- **First, click the blue ✦ button (Toggle Gemini) at the bottom center of the screen.** The panel is closed at first.
  You can also open it with the "generate with AI" link inside a cell.
- If the button itself is missing:
  - Colab's AI features appear only if your **account age is 18 or older** and you are in a **supported region**.
  - With a **school or work (Workspace) account**, the administrator may have turned it off → reopen in a window logged in with your **personal Gmail**.
    (Check which account the profile picture at the top right belongs to. If several accounts are logged in, it's easy to end up in a different one.)
  - Refresh (`F5`), open in an incognito window with your personal account, or turn off ad-blocking extensions.
  - If it still doesn't work, tell the instructor and work with a partner. (It may also be a temporary error on Colab's side.)

### 7-2. API key problems

| Symptom | Cause | Fix |
|------|------|------|
| Response says `등록되지 않은 인증키입니다` (unregistered API key) | Typo in the key, spaces before/after it, **didn't click the email verification (인증키 사용)** | Copy the key again, check your email, confirm "승인" (approved) in API key management |
| Response says the domain/URL doesn't match (`INCORRECT_KEY`, etc.) | The **service URL** you entered when applying differs from where you opened the map | Change the service URL to the value your instructor gave (edit it in API key management) |
| Worked yesterday, not today | **Expired** or usage limit exceeded | Extend the period in API key management |
| Can't read the secret (`SecretNotFoundError`, etc.) | Typo in the name, **Notebook access** turned off | In the 🔑 panel, check the name `VWORLD_KEY` and the access switch |

- The API key **goes inside the HTML file you make.** Giving the HTML file to someone means giving them your key too (§7-5).

### 7-3. Common Gemini mistakes — ask again if you get results like these

The key to "What to say" is **describing exactly what you saw, and pasting the error message if there is one**. You don't need to know the "Why" column.

| If this happens | What to say | Why (no need to know) |
|------------------|---------------|------------------------|
| Running a cell gives a red error (`NameError: name 'z' …`, `KeyError`, etc.) | "When I run the cell I get this error: (paste the error)". If the same error repeats: "Keep the screen content (HTML) separate from the Python code, and just swap in the key where it goes" | Python mistakes the `{z}/{y}/{x}` in the map address for its own variables (f-string) |
| When you open the file, the map area is **completely white** and empty | "The map area is completely white and empty. Make the map fill the whole window" | The map area's height is 0 |
| Map pieces look **jumbled and scattered** | "The map pieces look scattered" | The map tool's (Leaflet's) style file (CSS) wasn't loaded |
| The background is **gray** and no map images appear | "The map only shows up gray" + paste the F12 error. If it repeats, **Reference Card A** | Wrong map address format (y/x order, aerial photos are jpeg, layer names) or an API key problem |
| No place names on top of the aerial photos / only place names and no photos | Say what you see + Reference Card A | The place-name image is transparent and must be laid on top of the aerial photos |
| **A different map** such as Google Maps or Kakao Map shows up | "Use the VWorld map, not a different one" | The map wasn't specified |
| The map shows up but **clicking doesn't create a pin** (in the downloaded file) | "In the downloaded file, clicking the map doesn't create a pin. I need to be able to click and record using just the file" | A fixed map made with a Python map tool (folium) |
| The **API key is visible as-is** in a notebook cell | "My API key is visible in the notebook. Keep it in Secrets so others can't see it" | The key was written in the code for convenience |
| Typing `<b>` in a name makes it **bold** / the screen breaks | "Make what I type show up exactly as I typed it. Make sure the screen doesn't break even if I type strange characters" | The typed text is interpreted as screen code (missing escaping) |
| You deleted one pin and **a different pin** was deleted | "I deleted the ○○ pin but the △△ pin disappeared" | Pins are identified only by location (no unique ID) |
| **All pins disappear** after closing and reopening | "When I close the tab and reopen it, all the pins are gone" — first check you're not in an incognito window | Missing save feature, or an incognito window |
| After adding a new feature, **an old feature disappeared** | "The ○○ feature is gone. Keep all the features that worked before and fix it" | It rewrote the code from scratch and left things out |
| The map doesn't show in the Colab preview but works in the downloaded file (or vice versa) | Don't ask for a fix; judge **by the downloaded file** | The preview opens at a Colab address and can fail the key check |

### 7-4. Colab runtime

- If the runtime disconnects, the HTML you made disappears → **Runtime → Run all before** (run all previous cells). Your Secrets remain.
- Download a version that works right away.

### 7-5. Sharing keys and location information

- The finished HTML **contains your API key.** Do not post it on the web, GitHub, or social media.
  When submitting, follow the instructor's directions.
- The exported JSON contains the **locations** you marked. Don't include personal locations such as your home address.
- Before sharing or submitting the notebook, check that the key isn't printed in any cell output.

---

## 8. Submission (follow the instructor's directions)

- The finished HTML file (e.g. `map_final.html`) — only to the instructor, since it contains your API key
- The exported site JSON (3 or more sites)
- The Colab notebook (share link or `.ipynb`) — after checking the key isn't visible
- A short reflection: the prompt that worked best, a moment when Gemini got it wrong and how you fixed it, and how you handled the API key

---

## 9. (Advanced) Geological map overlay — KIGAM geological map overlay

You can lay the **geological map of the Korea Institute of Geoscience and Mineral Resources (KIGAM)** semi-transparently on top of the VWorld base map, to see which strata and rocks your sites sit on.
The geological map is fetched through the OpenAPI (WMS) of KIGAM's **KIGAM GeoBigData Open Platform**.

> ⚠️ **This is hard to do on the day of class.** Signing up is immediate, but the OpenAPI key requires **approval after you apply**,
> so you may not get it on the same day (the VWorld key is issued immediately on application).
> → Students who want to try it should **apply a few days before class**, or do it as an **after-class assignment**.
> It is not part of the completion criteria for the main practice (§1–§8).

### 9-1. Applying for a KIGAM API key (in advance)

The KIGAM site is in Korean only.

1. https://data.kigam.re.kr (KIGAM GeoBigData Open Platform) → **sign up (회원가입)** and log in.
2. Submit an application from the **OpenAPI 신청** (OpenAPI application) menu (under My Page; address `https://data.kigam.re.kr/my-openapi/request/`).
   For the purpose, e.g. `수업 실습 - 답사 지점 지도에 지질도 오버레이` (class practice – geological map overlay on a field site map). (Form fields and menu names may change.)
3. **Wait for approval** → once approved, find your API key in the OpenAPI menu. Check the approval status on the site yourself.
4. Usage guide: https://data.kigam.re.kr/guide/openapi ,
   layer list: https://data.kigam.re.kr/map/openapimanual/openapiLayerList.html
5. Contact: Geoscience Data Research Department (지질자원데이터연구실), Korea Institute of Geoscience and Mineral Resources (042-868-3111).

> Like the VWorld key, treat this API key **like a password**. Put it in Colab 🔑 Secrets as `KIGAM_KEY`.

### 9-2. Reference Card B — geological map information (paste when Gemini is lost)

You don't need to understand it. If Gemini is lost about the address or method for the request in 9-3, paste the box below as is.

```
Here is the KIGAM (Korea Institute of Geoscience and Mineral Resources) geological map information. Please use it exactly as given.
- WMS address: https://data.kigam.re.kr/openapi/wms
- Attach the API key as the key parameter (key=YOUR_ISSUED_KEY)
- Layers: L_50K_Geology_Map (1:50,000), L_250K_Geology_Map (1:250,000), L_1M_Geology_Map (1:1,000,000)
- Standard WMS GetMap request: format=image/png, transparent=true
- In Leaflet you can overlay it with L.tileLayer.wms.
```

Good to know:
- The site states that **excessively frequent requests may lead to restricted access**. Don't test by zooming and panning wildly.
- On the 1:50,000 geological map, **areas with no map sheet** may look empty. In that case, switch to 1:250,000.

### 9-3. Prompt examples

> I want to lay the **KIGAM geological map** half-transparently over the current map, so I can see which rocks and strata the sites I marked are on.
> I got a KIGAM API key too and put it in Secrets as `KIGAM_KEY`.
> Let me turn the geological map on and off, and choose between 1:50,000 and 1:250,000. Keep the features that work now as they are.
> When there's no KIGAM key, make it work as before, without the geological map menu.

More things to try:

> The geological map is so dark I can't see the base map. Let me adjust how strong it is.

> When I place a pin, can you look up which rock or stratum is at that spot on the geological map and record it too? If that's not possible, tell me.

### 9-4. When it doesn't work

| Symptom | What to check |
|------|-----------|
| The geological map menu is there but nothing is overlaid | First check for a typo in the key, or whether the **key isn't approved yet**. Paste the `F12` error to Gemini |
| The response is `500` + a "서비스에 일시적인 오류가 발생했습니다." (a temporary service error occurred) page | It looks like a server failure, but this also appears when **the key is missing, wrong, or not yet approved**. Check the key first |
| The response is `400 Bad Request` / `Request Blocked` | Check the key and parameters. If you're making too many requests, try again a bit later |
| Only certain areas are empty | Area with no 1:50,000 map sheet → switch to 1:250,000 |
| So dark the base map can't be seen | "Make the geological map more transparent" |

> Reference sample: the `KIGAM_KEY` part of `examples/vworld_map_sample.html` (a geological map menu appears once you add the key).
> The KIGAM WMS usage in this document is based on the official guide pages and **has not yet been tested with a real key.**
