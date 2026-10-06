# Instructor Guide — Building a VWorld Map App with Gemini

[한국어](vworld_map_instructor_guide.md) | **English**

Student guide: `docs/vworld_map_practice_guide.en.md`. **This is the workshop's first practice.** Starting from an empty Colab notebook, students write prompts asking Gemini to build a map app that is
**a single HTML file**. The second practice (Conference Organizer, `docs/conference_organizer_instructor_guide.en.md`) works the same way.

Because this is the first practice, use it to give students plenty of practice in **how to work with Gemini** itself: state the requirements first, ask in small steps, keep a file for each version, download the file to check it,
and pass console errors to Gemini exactly as they appear. The screen layout is simple and there is no dataset to handle, so students can focus on these habits.

What students learn for the first time in this practice:
- Getting and managing an **external API key** (VWorld sign-up → API key → service URL)
- **Keeping secret values out of the code**: Colab Secrets (`google.colab.userdata`)
- **Checking the API response**: when an error XML arrives where an image should be
- A map library (Leaflet) and tile URL rules, saving user input (localStorage) and exporting it

| What students receive | When |
|------------------|------|
| API key instructions (student guide §2-1) + **the value to enter as the service URL** | **1 week before class** (homework) |
| `docs/vworld_map_practice_guide.en.md` | Start of class |
| Reference sample `examples/vworld_map_sample.html` (optional) | End of class |

---

## Pre-class checks: try these yourself

### 1) The API key and the "service URL": the biggest unknown

A VWorld API key may be rejected if the **service URL (domain)** entered when applying differs from where the request actually comes from
(there have been `INCORRECT_KEY` cases with the data API). The result of this practice is **an HTML file opened via `file://`**, so it has no domain,
and the Colab preview opens at a Colab address. **You must check for yourself whether the background map WMTS checks the domain.**
(Confirmed as of 2026-10-06: a request without a key gets an XML saying `등록되지 않은 인증키입니다.` ("This API key is not registered.") with HTTP 200.)

Test your instructor key in three places, and tell students **the service URL value that passed**.

| Check | How | Result |
|------|------|-----------|
| ① Python request | In a Colab cell, `requests.get("https://api.vworld.kr/req/wmts/1.0.0/{KEY}/Base/7/49/109.png")` → is the `Content-Type` `image/png`? | |
| ② Colab preview | Show the map HTML inside Colab; do the tiles appear? | |
| ③ Downloaded file | Open it via `file://`; do the tiles appear? (F12 → Network, check the tile responses) | |

- Service URL candidates: a school or personal homepage address, `http://localhost`, `https://colab.research.google.com`, etc.
  Also check whether one key can have several URLs registered, and whether the URL can be changed later.
- **If ③ fails** (`file://` blocked):
  - (A) Have students serve the result with `python -m http.server` and open it at `http://localhost:8000/…`, with the service URL set to `http://localhost:8000`.
    This only relaxes the "opens with a double-click" requirement.
  - (B) Use the old keyless address `https://xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png` (what the sample uses;
    working as of 2026-10-06). It is **unofficial**, so it could be blocked at any time. Practice the API key step only up to ① (the Python check), and use the old address for the map.
  - Either way, revise completion criterion #2 in the student guide accordingly before handing it out.
- **Validity period and usage**: On the key issuance screen, check the key type (development/production), its validity period and the daily usage limit, and tell students.
  When 30 people zoom and pan at once, there are many tile requests. This is also why each student should use their own key.

### 1-1) (Advanced) KIGAM geological map WMS: student guide §9

The geological map overlay in student guide §9 is **outside this practice's completion criteria** (advanced/homework). If you still want to recommend it to students, first do the following yourself:

- [ ] **Apply for a KIGAM OpenAPI key in advance and get it approved** (https://data.kigam.re.kr → OpenAPI application; the site is in Korean). Approval takes time, so
      apply about 2 weeks before class. Record how long approval took, so you can tell students the deadline for applying.
- [ ] Test your instructor key in the same three places as VWorld: ① a Python `GetMap` request ② the Colab preview ③ **the downloaded file (`file://`)**.
      Check whether the application form asks for a domain/service URL and **whether there is a domain restriction**. If there is, it may not work from `file://`.
- [ ] Check the layer names (`L_50K_Geology_Map`, `L_250K_Geology_Map`, `L_1M_Geology_Map`), the coordinate system (whether requesting in `EPSG:3857` works),
      and whether `transparent=true` really returns a transparent PNG. At 1:50,000, areas with no map sheet look empty, so 1:250,000 is a safe choice for the demo.
- [ ] Put your instructor key into `KIGAM_KEY` in the sample `examples/vworld_map_sample.html` for the demo → **hand out the file with the key removed after the demo**.
- **Caution: the error looks like a "server failure"** (confirmed 2026-10-06): requesting `GetMap` without a key or with a wrong key returns
  **HTTP 500 + an HTML page saying "서비스에 일시적인 오류가 발생했습니다." ("A temporary service error has occurred.")** (not an error XML or a blank image).
  If a student says "the KIGAM server is down", suspect the key first (approval status, typos). In Leaflet it only shows up as a tile error.
  (`GetCapabilities` returns a 404 XML at the same address; it may not be a documented request.)
- The site notes that excessive calls may lead to usage restrictions → it is safer not to have 30 people test it at the same time during class.

### 2) Student homework before class

- [ ] **Sign up and get the API key before class.** Sign-up and email verification take time, and if 30 people do it at once in class, some students will certainly get stuck.
      Make "bring a screenshot of the key management screen showing status **승인** (approved)" the homework. (The VWorld site is in Korean.)
- [ ] For students who could not get a key: have them work with a partner (key sharing only within the pair), or use option (B) above.

### 3) Colab and Gemini

- [ ] **The Gemini panel is closed in a new notebook.** It is the blue ✦ "Toggle Gemini" button at the bottom center of the screen. Show it at the start of class.
- [ ] **Colab Secrets**: the 🔑 key icon in the vertical icon bar on the left sidebar. Check whether a "Notebook access" permission window appears the first time a secret is read.
- [ ] Go through the whole process once yourself with Gemini, to see in advance how Gemini writes (or gets wrong) the VWorld tile URL.
- [ ] Check that `unpkg.com` (Leaflet CDN) and `api.vworld.kr` are not blocked on the lab PCs (school firewall).

---

## Sample schedule (2–3 hours)

| Time | Content |
|------|------|
| 0:00–0:15 | Goals and completion criteria. Demo of the finished app (on the instructor's screen only). **What an API key is and why it is secret** |
| 0:15–0:35 | Steps 0–1: Gemini panel, **registering Colab Secrets**, requesting one tile to check the key. Read the failure messages together |
| 0:35–1:05 | Step 2: first map → **download it and double-click** to check. Fix the white map / scattered tiles |
| 1:05–1:20 | Step 3: switching background maps (satellite jpeg, hybrid overlay) |
| 1:20–1:30 | Break |
| 1:30–2:10 | Step 4: adding sites, popups, deleting, localStorage. Test typing `<b>` (escaping) |
| 2:10–2:30 | Step 5: export/import |
| 2:30–2:50 | Step 6: free polishing (fields for geological field trips: lithology, strike/dip …) |
| 2:50–3:00 | Compare with the sample and with each other's results, reflection |

Since this is the first practice, in the 0:15–0:35 slot make sure everyone does each of these once: **open the Gemini panel (✦ at the bottom), run a cell, download the file and open it with a double-click**.
The habits learned here (state the requirements first, keep a file for each version, pass on console errors) carry straight over to Practice 2 (Conference Organizer).

---

## Where students get stuck, and hints for stepping in

| Symptom | Cause | Hint |
|------|------|------|
| Gemini is not visible | The panel is closed | ✦ at the bottom center (Toggle Gemini) |
| `등록되지 않은 인증키입니다` ("This API key is not registered") | Email not verified, key copied wrong (spaces), not yet approved | Check the key management screen |
| Domain/URL mismatch error | Service URL differs from the value from the pre-class check | Edit the service URL in key management |
| `NameError: z` / `KeyError` | The tile URL `{z}/{y}/{x}` was put inside an f-string | "How does Python read curly braces?" → template + `replace` |
| White screen | `#map` height is 0 | Check the map div's size in developer tools |
| Tile pieces scattered | leaflet.css missing | |
| Gray map | `{x}/{y}` order, `.png`/`.jpeg`, layer name capitalization | Open the tile response in the Network tab (an image? XML?) |
| Only the Colab preview fails | The preview address fails the service URL check | Judge by the downloaded file |
| Key written directly in a cell | Convenience | "If you submit this notebook, who will see your key?" |
| Key printed in cell output | `print(key)` | Clear outputs (Edit → Clear all outputs) |
| Uses folium | Gemini interpreted it as a Python map tool | Click-to-add and saving end up in JS anyway → use the Leaflet template |
| Other sites get deleted | Sites identified by coordinates | Unique id |
| Typing `<b>` shows bold text | Missing escaping | Connect to XSS: "What if you import JSON someone else gave you?" |
| (Advanced) Geological map does not overlay, `openapi/wms` 500 in Network | KIGAM key not approved or typo (the error text says "temporary error") | Check the key approval status first |

---

## Grading criteria (example)

| Area | Weight | Content |
|------|------|------|
| Meets completion criteria | 50% | The 8 items in student guide §1 |
| API key management | 15% | No key in the notebook (uses Colab Secrets), none in cell outputs either, follows the submission route |
| Process | 20% | Step-by-step progress, results for each version, evidence of asking again after hitting errors |
| Reflection | 15% | Prompts that worked well, moments Gemini got it wrong, how they handled the key |

Quick grading check:
1. Open the submitted HTML in an empty folder → background map (#1–#2). Background switching (#3).
2. Add 2 sites, delete 1 (#4–#5), close the tab and reopen it (#6).
   (Chrome lets local HTML files share storage, so **sites from another student's file that used the same localStorage key may appear.**
   Use a separate Chrome profile for grading, or delete the sites before checking.)
3. Import the submitted JSON (#7). Search the notebook for the key string (#8).
4. When grading is done, **delete the HTML files that contain student keys**.

---

## Reference sample `examples/vworld_map_sample.html`

An example map app made with Gemini + Colab. Features: VWorld base map, click to add a site, **user-defined input fields (schema management)**,
localStorage saving, JSON export/import (choice of overwrite or merge). Good points for comparison and discussion at the end of class:

- It uses the **old address without an API key** (`xdworld.vworld.kr/2d/Base/service/{z}/{x}/{y}.png`) → compare with the official WMTS (`api.vworld.kr/req/wmts/1.0.0/{KEY}/…/{z}/{y}/{x}`):
  URL format (x/y order), the key, and the fact that it could be blocked at any time.
- It puts input values and field names into popups via `innerHTML` **without escaping** → importing someone else's JSON could run a script.
- It **identifies sites by coordinates (6 decimal places)** to build the delete button id → problems when coordinates are duplicated; why a unique id is better.
- What it does well: wraps localStorage in try/catch, offers overwrite/merge on import, removes duplicate schema fields.
- Discussion questions: How did your result include the key? If you give the HTML to a friend, what happens to the key? How could you keep the key out of the file?
  (e.g. ask for the key the first time the app runs and store it only in that browser's localStorage)
