// 빌드된 HTML 을 jsdom 으로 열어 화면이 그려지고 주요 동작이 되는지 확인한다.
//   NODE_PATH=<jsdom 이 설치된 node_modules> node scripts/smoke_test.js dist
// (jsdom 은 프로젝트 의존성이 아니므로 아무 곳에나 `npm i jsdom` 해서 NODE_PATH 로 지정)
const { JSDOM } = require("jsdom");
const fs = require("fs");
const path = require("path");

const dir = process.argv[2] || "dist";
let failed = 0;
function check(name, cond, detail = "") {
  console.log(`${cond ? "  ok  " : "  FAIL"} ${name}${detail ? " — " + detail : ""}`);
  if (!cond) failed++;
}

function open(file, { storage = {}, hash = "" } = {}) {
  const html = fs.readFileSync(path.join(dir, file), "utf8");
  const errors = [];
  const dom = new JSDOM(html, {
    runScripts: "dangerously",
    url: "http://localhost/" + file + hash,
    pretendToBeVisual: true,
    beforeParse(win) {
      for (const [k, v] of Object.entries(storage)) win.localStorage.setItem(k, v);
      win.scrollTo = () => {};
      win.addEventListener("error", e => errors.push(e.message));
    },
  });
  return { dom, win: dom.window, doc: dom.window.document, errors };
}
// 특정 학회 데이터에 묶이지 않도록 테스트 값도 데이터에서 고른다
const DATA = JSON.parse(fs.readFileSync("data/conference.json", "utf8"));
const lower = s => String(s ?? "").toLowerCase();
const firstWord = DATA.talks[0].title.split(/\s+/).find(w => w.length >= 3) || DATA.talks[0].title;
const twoChars = lower(DATA.talks[0].title).slice(0, 2);
// 같은 날 겹치지 않는 두 발표 / 같은 시각에 시작하는 두 발표
const pairs = DATA.talks.flatMap(a => DATA.talks.filter(b => b.date === a.date && b.id > a.id).map(b => [a, b]));
const noClash = pairs.find(([a, b]) => a.time_end <= b.time_start);
const clash = pairs.find(([a, b]) => a.time_start === b.time_start);
// 초록 본문에만 있고 제목·저자에는 없는 단어
const heads = lower(DATA.talks.map(t => t.title + " " + t.first_author).concat(DATA.abstracts.map(a => a.title)).join(" "));
const bodyOnly = DATA.abstracts.flatMap(a => lower(a.abstract).match(/[a-z가-힣]{7,}/g) || []).find(w => !heads.includes(w));
const session = DATA.sessions.find(s => DATA.talks.some(t => t.session === s.code));

const tick = () => new Promise(r => setTimeout(r, 20));
function click(win, el) { el.dispatchEvent(new win.MouseEvent("click", { bubbles: true })); }
function type(win, el, value) { el.value = value; el.dispatchEvent(new win.Event("input", { bubbles: true })); }

(async () => {
  // ── Step 2 ──
  {
    const { doc, errors } = open("step2_list.html");
    check("step2: 오류 없음", errors.length === 0, errors.join("; "));
    check("step2: 첫날 발표 렌더", doc.querySelectorAll(".talk").length > 50, doc.querySelectorAll(".talk").length + "건");
  }
  // ── Step 3 ──
  {
    const { win, doc, errors } = open("step3_filter.html");
    const n0 = doc.querySelectorAll(".talk").length;
    click(win, doc.querySelectorAll("#days .chip")[1]);
    const n1 = doc.querySelectorAll(".talk").length;
    type(win, doc.getElementById("q"), firstWord);
    check("step3: 오류 없음", errors.length === 0, errors.join("; "));
    check("step3: 날짜 칩 전환", n0 > 0 && n1 > 0 && n0 !== n1, `${n0} → ${n1}`);
    check("step3: 검색 하이라이트", doc.querySelectorAll("mark").length > 0, doc.getElementById("count").textContent);
  }
  // ── Step 4 ──
  {
    const { win, doc, errors } = open("step4_bookmark.html");
    click(win, doc.querySelectorAll(".bm")[0]);
    click(win, doc.querySelectorAll(".bm")[1]);
    const saved = JSON.parse(win.localStorage.getItem("gsk2026.bookmarks"));
    check("step4: localStorage 저장", saved.length === 2, JSON.stringify(saved));
    click(win, doc.querySelector('[data-tab="my"]'));
    check("step4: 내 일정 2건", doc.querySelectorAll("#my-view .talk").length === 2);
    click(win, doc.querySelectorAll("#my-view .bm")[0]);
    check("step4: 내 일정에서 해제", doc.querySelectorAll("#my-view .talk").length === 1);
    check("step4: 오류 없음", errors.length === 0, errors.join("; "));
  }
  for (const [name, pair, expected] of [["겹치지 않는 두 발표", noClash, 0], ["같은 시각 두 발표", clash, 2]]) {
    if (!pair) { console.log(`  skip step4: ${name} 없음`); continue; }
    const { doc } = open("step4_bookmark.html", { storage: { "gsk2026.bookmarks": JSON.stringify(pair.map(t => t.id)) } });
    doc.querySelector('[data-tab="my"]').click();
    check(`step4: ${name} → 겹침 ${expected}`, doc.querySelectorAll("#my-view .clash").length === expected);
  }
  {
    // localStorage 가 깨져 있어도 동작
    const { doc, errors } = open("step4_bookmark.html", { storage: { "gsk2026.bookmarks": "{broken" } });
    check("step4: 깨진 저장값 무시", errors.length === 0 && doc.querySelectorAll(".talk").length > 0, errors.join("; "));
  }
  // ── 완성본 ──
  {
    const { win, doc, errors } = open("app.html");
    const view = () => doc.getElementById("view");
    const go = async h => { win.location.hash = h; await tick(); };
    check("app: 프로그램 렌더", view().querySelectorAll(".talk").length > 50);
    check("app: 프로그램 탭 활성", doc.querySelector(".tab.on")?.dataset.tab === "program");
    click(win, view().querySelectorAll('[data-set="room"] .chip')[1]);
    check("app: 장소 칩", view().querySelectorAll(".place").length === 0 && view().querySelectorAll(".talk").length > 0);

    await go("#/sessions");
    check("app: 세션 목록", view().querySelectorAll(".slist li").length === DATA.sessions.length);
    await go("#/session/" + encodeURIComponent(session.code));
    check("app: 세션 상세", view().querySelectorAll(".talk").length > 0 && view().textContent.includes(session.title));

    const data = DATA;
    // 초록 본문이 있는 발표를 우선 고른다 (프로그램북 데이터는 본문 없이 저자만 있을 수 있음)
    const absOf = t => DATA.abstracts.find(a => a.id === t.abstract_id);
    const withAbs = data.talks.find(t => t.abstract_id && absOf(t).abstract) || data.talks.find(t => t.abstract_id);
    const abs = absOf(withAbs);
    await go("#/talk/" + withAbs.id);
    check("app: 발표 상세 + 저자", view().querySelector(".detail-authors")?.textContent.includes(abs.authors[0]));
    check("app: 초록 본문·키워드 (있을 때)",
      !!view().querySelector(".detail-abstract") === !!abs.abstract && !!view().querySelector(".kw") === abs.keywords.length > 0);
    click(win, view().querySelector(".bm"));
    check("app: 상세에서 북마크", view().querySelector(".bm").classList.contains("on"));

    const noAbs = data.talks.find(t => !t.abstract_id);
    if (noAbs) {
      await go("#/talk/" + noAbs.id);
      check("app: 초록 없는 발표", view().textContent.includes("연결된 초록이 없습니다"));
    }
    await go("#/talk/999999");
    check("app: 없는 발표 id", view().textContent.includes("찾을 수 없습니다"));
    const linked = new Set(DATA.talks.map(t => t.abstract_id));
    const lone = DATA.abstracts.find(a => !linked.has(a.id)) || DATA.abstracts[0];
    await go("#/abstract/" + lone.id);
    check("app: 초록 단독 상세", view().querySelector(".detail-title")?.textContent === lone.title);

    await go("#/search");
    if (bodyOnly) {
      type(win, doc.getElementById("q"), bodyOnly);   // 초록 본문에만 있는 단어
      check("app: 본문 검색 + 스니펫", view().querySelectorAll("#results .snippet mark").length > 0, `"${bodyOnly}" ` + view().querySelector(".count")?.textContent);
    } else console.log("  skip app: 본문 검색 (초록 본문 없는 데이터)");
    if (lone.authors.length) {
      type(win, doc.getElementById("q"), lone.authors.at(-1));   // 일정 없는 초록(포스터)도 저자로 찾아진다
      check("app: 일정 없는 초록 검색", [...view().querySelectorAll("#results .talk-title")].some(a => a.textContent === lone.title));
    }
    type(win, doc.getElementById("q"), "a<b");
    check("app: 특수문자 검색 안전", errors.length === 0);
    type(win, doc.getElementById("q"), twoChars);
    const total = parseInt(view().querySelector(".count").textContent);
    check("app: 결과는 최대 100건 표시", total > 0 && view().querySelectorAll("#results .talk").length === Math.min(100, total), view().querySelector(".count")?.textContent);

    await go("#/my");
    check("app: 내 일정 1건", view().querySelectorAll(".talk").length === 1);
    check("app: 내보내기 버튼", !!doc.getElementById("export"));
    check("app: 오류 없음", errors.length === 0, errors.join("; "));
  }
  {
    // step4 에서 쓰던 북마크가 완성본으로 이어지는지 + 불러오기
    const { win, doc, errors } = open("app.html", { hash: "#/my", storage: { "gsk2026.bookmarks": JSON.stringify(DATA.talks.slice(0, 3).map(t => t.id)) } });
    check("app: step4 북마크 이어받기", doc.querySelectorAll("#view .talk").length === 3);
    const input = doc.getElementById("import");
    const file = new win.File([JSON.stringify({ bookmarks: [...DATA.talks.slice(2, 5).map(t => t.id), 999999] })], "bookmarks.json", { type: "application/json" });
    Object.defineProperty(input, "files", { value: [file] });
    input.dispatchEvent(new win.Event("change", { bubbles: true }));
    await new Promise(r => setTimeout(r, 100));
    check("app: 불러오기 병합", doc.querySelectorAll("#view .talk").length === 5, doc.querySelector(".msg")?.textContent);
    check("app: 불러오기 오류 없음", errors.length === 0, errors.join("; "));
  }

  console.log(failed ? `\n${failed}개 실패` : "\n모두 통과");
  process.exit(failed ? 1 : 0);
})();
