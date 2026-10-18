// MT6102 group investment proposal deck, styled after the CV6215 template
// (navy cover and dividers, white content slides, red eyebrow labels, Cambria titles, Calibri body).
const pptxgen = require("pptxgenjs");
const path = require("path");
const { applyTheme } = require("/root/.claude/skills/synced/9e270534-cdc3-450a-8ee7-fdaabd22c248_9f18941f-e424-49f8-b4d9-a6cfd73118a6/pptx/scripts/apply_theme.js");

const CH = "/home/user/MT6102/charts_deck/";
const NAVY = "142B4F", INK = "1A2433", SLATE = "5A6472", RED = "C8102E", PANEL = "EEF3FA", LINE = "D7DEE8",
  LB = "C9D6EA", PB = "9FB6D9", WHITE = "FFFFFF", PINK = "FBECEC", TINT = "F7F9FC", MUTED = "7F93B5", BLUE2 = "4A6FA5";
const HEAD = "Cambria", BODY = "Calibri";
const FOOT = "MT6102 Maritime Economics  ·  USD 250m Group Investment Proposal";

const THEME = {
  name: "MT6102 Proposal",
  headFontFace: HEAD, bodyFontFace: BODY,
  colors: { dk1: INK, lt1: WHITE, dk2: NAVY, lt2: PANEL, accent1: NAVY, accent2: RED, accent3: BLUE2,
    accent4: PB, accent5: SLATE, accent6: LB, hlink: BLUE2, folHlink: SLATE },
};

const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
pres.theme = { headFontFace: HEAD, bodyFontFace: BODY };
pres.title = "USD 250 Million Shipping Investment Proposal";
pres.author = "MT6102 Group";

pres.defineSlideMaster({
  title: "LIGHT", background: { color: WHITE },
  objects: [{ text: { text: FOOT, options: { x: 0.55, y: 7.08, w: 8.5, h: 0.3, fontSize: 9, color: SLATE, fontFace: BODY, margin: 0 } } }],
  slideNumber: { x: 12.3, y: 7.08, w: 0.5, h: 0.3, fontSize: 9, color: SLATE, fontFace: BODY, align: "right" },
});
pres.defineSlideMaster({
  title: "DARK", background: { color: NAVY },
  objects: [{ text: { text: FOOT, options: { x: 0.55, y: 7.08, w: 8.5, h: 0.3, fontSize: 9, color: MUTED, fontFace: BODY, margin: 0 } } }],
  slideNumber: { x: 12.3, y: 7.08, w: 0.5, h: 0.3, fontSize: 9, color: MUTED, fontFace: BODY, align: "right" },
});

let n = 0;
function light(section) { n++; return pres.addSlide({ masterName: "LIGHT", sectionTitle: section }); }
function dark(section) { n++; return pres.addSlide({ masterName: "DARK", sectionTitle: section }); }

function base(s, eyebrow, title, source) {
  s.addText(eyebrow.toUpperCase(), { x: 0.55, y: 0.36, w: 12.2, h: 0.3, fontSize: 11, bold: true, color: RED, fontFace: BODY, charSpacing: 2, margin: 0, isTextBox: true, objectName: "Eyebrow" });
  s.addText(title, { x: 0.55, y: 0.66, w: 12.2, h: 0.8, fontSize: 27, bold: true, color: NAVY, fontFace: HEAD, margin: 0, valign: "top", isTextBox: true, objectName: "Title" });
  if (source) s.addText("Source: " + source, { x: 0.55, y: 6.7, w: 12.2, h: 0.32, fontSize: 8.5, italic: true, color: SLATE, fontFace: BODY, margin: 0, isTextBox: true, objectName: "Source" });
}
function panel(s, x, y, w, h, title, body, opt = {}) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h, fill: { color: opt.fill || PANEL }, line: { color: opt.line || LINE, width: 0.75 }, rectRadius: 0.06, objectName: "Panel" });
  let ty = y + 0.14;
  if (title) { s.addText(title, { x: x + 0.2, y: ty, w: w - 0.4, h: 0.34, fontSize: opt.titleSize || 13.5, bold: true, color: opt.titleColor || NAVY, fontFace: BODY, margin: 0, isTextBox: true, valign: "top", objectName: "Panel title" }); ty += 0.38; }
  if (body) s.addText(body, { x: x + 0.2, y: ty, w: w - 0.4, h: y + h - ty - 0.12, fontSize: opt.bodySize || 11.5, color: opt.bodyColor || INK, fontFace: BODY, margin: 0, isTextBox: true, valign: "top", paraSpaceAfter: 4, objectName: "Panel body" });
}
function stat(s, x, y, w, value, label, opt = {}) {
  s.addShape(pres.ShapeType.roundRect, { x, y, w, h: opt.h || 1.25, fill: { color: opt.fill || PANEL }, line: { color: LINE, width: 0.75 }, rectRadius: 0.06, objectName: "Stat" });
  s.addText(value, { x: x + 0.15, y: y + 0.12, w: w - 0.3, h: 0.55, fontSize: opt.valueSize || 26, bold: true, color: opt.color || RED, fontFace: HEAD, margin: 0, isTextBox: true, align: opt.align || "left", objectName: "Stat value" });
  s.addText(label, { x: x + 0.15, y: y + 0.68, w: w - 0.3, h: (opt.h || 1.25) - 0.76, fontSize: opt.labelSize || 10.5, color: SLATE, fontFace: BODY, margin: 0, isTextBox: true, valign: "top", align: opt.align || "left", objectName: "Stat label" });
}
function circle(s, x, y, num, opt = {}) {
  const d = opt.d || 0.36;
  s.addShape(pres.ShapeType.ellipse, { x, y, w: d, h: d, fill: { color: opt.fill || RED }, line: { color: opt.fill || RED, width: 0 }, objectName: "Number" });
  s.addText(String(num), { x, y, w: d, h: d, fontSize: opt.size || 12, bold: true, color: WHITE, fontFace: BODY, align: "center", valign: "middle", margin: 0, isTextBox: true, objectName: "Number text" });
}
function hdr(cells, size = 10) { return cells.map(t => ({ text: t, options: { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: size, fontFace: BODY, valign: "middle" } })); }
function cell(t, o = {}) { return { text: t, options: Object.assign({ fontFace: BODY, fontSize: 10, color: INK, valign: "middle" }, o) }; }
function table(s, rows, x, y, w, colW, opt = {}) {
  s.addTable(rows, Object.assign({ x, y, w, colW, border: { type: "solid", pt: 0.5, color: LINE }, fontFace: BODY, fontSize: opt.fontSize || 10, color: INK, valign: "middle", margin: 0.06, autoPage: false, objectName: opt.name || "Table" }, opt.rowH ? { rowH: opt.rowH } : {}));
}
function img(s, file, x, y, w, h) { s.addImage({ path: CH + file, x, y, w, h, sizing: { type: "contain", w, h }, objectName: file }); }
function bullets(s, items, x, y, w, h, opt = {}) {
  s.addText(items.map((t, i) => ({ text: t, options: { bullet: true, breakLine: i < items.length - 1, paraSpaceAfter: opt.space || 6 } })),
    { x, y, w, h, fontSize: opt.size || 12, color: opt.color || INK, fontFace: BODY, margin: 0, isTextBox: true, valign: "top", objectName: "Bullets" });
}

// ============================================================ OPENING
pres.addSection({ title: "Opening" });
{
  const s = dark("Opening");
  s.addText("MT6102 MARITIME ECONOMICS  ·  GROUP INVESTMENT PROPOSAL", { x: 0.9, y: 1.15, w: 11.5, h: 0.35, fontSize: 12, bold: true, color: PB, fontFace: BODY, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText("USD 250 Million\nShipping Investment Proposal", { x: 0.9, y: 1.7, w: 11.5, h: 1.9, fontSize: 44, bold: true, color: WHITE, fontFace: HEAD, margin: 0, isTextBox: true, valign: "top" });
  s.addText("Skip the peak, buy value, lock income: five secondhand ships, three fixed charters, two spot ships and a cash reserve", { x: 0.9, y: 3.75, w: 11, h: 0.8, fontSize: 17, color: LB, fontFace: BODY, margin: 0, isTextBox: true, valign: "top" });
  s.addText("Group X  ·  Semester 1 2026/27  ·  Group members and matriculation numbers to be added here (10 members)", { x: 0.9, y: 4.85, w: 11.5, h: 0.35, fontSize: 13, color: LB, fontFace: BODY, margin: 0, isTextBox: true });
  s.addText("Every purchase price, charter rate and freight rate in this deck is the last transacted sale or fixture on the Clarksons Shipping Intelligence Network (SIN). Price series extracted 12 Sep 2026 and re-checked 15 Oct 2026; supply data extracted 10 Oct 2026.", { x: 0.9, y: 5.5, w: 11, h: 0.8, fontSize: 11, color: MUTED, fontFace: BODY, margin: 0, isTextBox: true, valign: "top" });
  s.addNotes("Opening (1 minute together with the agenda). The board asked for a USD 250m proposal. One sentence: buy five secondhand ships and keep a small cash reserve, fix three on period charters, trade two spot, and stay out of the large crude tanker market that has already peaked. Every number traces to a Clarksons SIN series or fixture.");
}
{
  const s = light("Opening");
  base(s, "Agenda", "How the proposal is built");
  const items = [
    ["The decision", "How the USD 250m is allocated, why each line is sized that way, and which data supports it. Five ships, four trades, one cash line."],
    ["Pricing basis", "Every purchase price, charter rate and freight rate is a last transacted sale or fixture on Clarksons SIN."],
    ["Demand and supply", "Three demand engines, deliveries against demolition, the 2027 to 2028 delivery wave, and a replacement test against the ageing fleet."],
    ["Market data and news", "Peak signals in large crude tankers, recovery in dry bulk, what changed since 12 September, and our freight-rate call."],
    ["Earnings", "One formula, the base case by vessel, three scenarios with an expected value, and sensitivity."],
    ["Shocks and mitigation", "Five shocks, charter expiry timed against the delivery wave, and the triggers we watch."],
    ["Conclusion", "The same three questions in the same order: how we allocate, why, and what data says so."],
  ];
  items.forEach((it, i) => {
    const y = 1.6 + i * 0.72;
    circle(s, 0.6, y + 0.03, i + 1);
    s.addText(it[0], { x: 1.15, y: y - 0.02, w: 4, h: 0.36, fontSize: 15, bold: true, color: NAVY, fontFace: BODY, margin: 0, isTextBox: true });
    s.addText(it[1], { x: 1.15, y: y + 0.33, w: 11.4, h: 0.34, fontSize: 11.5, color: SLATE, fontFace: BODY, margin: 0, isTextBox: true });
  });
  s.addNotes("Seven parts form one chain: the decision needs prices, prices need fundamentals, fundamentals need market confirmation, then we can compute earnings, and the downside is protected by the shock plan.");
}

// ============================================================ PART 1 THE DECISION
pres.addSection({ title: "Part 1 The decision" });
{
  const s = light("Part 1 The decision");
  base(s, "Part 1 · The decision", "Where the USD 250m goes, why, and the data behind it",
    "Clarksons SIN series and fixture register, extracted 12 Sep 2026, spot anchors week of 9 Oct 2026, supply data 10 Oct 2026. Full series list in the appendix.");
  const rows = [hdr(["Allocation", "USD m (share)", "Why this much", "Data behind the decision"], 10)];
  const R = [
    ["2× MR product tankers\n5-year-old Eco, 50k dwt. One on a 1-year TC at $30,000/day, one spot", "100 (40%)",
      "Closest to replacement cost of the five segments: 5-year-old $50m against newbuild $52m in September (0.96), $52m against $52.5m in October (0.99). Products trade +6.3% in 2027F. Spot earnings $53,741/day in the week of 9 Oct sit above the 1-year TC, so one ship stays open.",
      "Series 47130 / 71267 (prices), 98802 / 534403 (products trade), 543759 (MR Eco earnings). Fixtures PS Imabari to SUNCOR $30,000 and Challenge Pollux to ExxonMobil $27,000, 17 Aug 2026."],
    ["1× Aframax crude tanker\n2018 Japan-built, 110k dwt. 3-year TC at $40,000/day", "75 (30%)",
      "Lowest orderbook of any segment: 8.4% of dwt, 62 ships on order against 223 over 20 years old. A 3-year fixture at $40,000 exists (Torm Genesis to AET, 31 Aug), so income is certain through the 2027 to 2028 delivery wave. No Suezmax: 5-year-old $130m against newbuild $90m in October, 1-year TC $140,250 against 3-year $64,375.",
      "Series 534456 (orderbook), 531168 (earnings), 87302 / 53070 and 48989 / 49108 (Suezmax signals), datasets L13 to L16. Sales Southern Reverence and Pusaka Borneo at $75.0m."],
    ["2× Kamsarmax bulkers\n82k dwt, Japan-built 2019 and 2015. One on a 12-month TC at $22,000/day, one spot for the Q4 grain season", "70 (28%)",
      "Recovery, not peak: BDI 3,521 on 10 Sep and 2,801 on 13 Oct; 5-year-old price 9% above newbuild, against 23% to 44% for Suezmax. Orderbook 13.5%; 2025 deliveries 143 against demolition 14; 2027 deliveries 171 against 618 ships over 20 years old. Guinea bauxite +29% y/y, Simandou iron ore ramping up.",
      "Series 17259 (BDI), 534450, 540721, 557125, 534400 / 547349, 533288. Sales Aquavita Aim $38.0m and Medi Positano $32.0m. Fixtures Intensity to CNR $22,000, XH Hope to Cargill $23,000, coal DBCT to Vizag $25.60/t (SAIL)."],
    ["Cash reserve\nCounter-cyclical fund and working capital", "5 (2%)",
      "Dry powder for when tanker secondhand prices fall back below newbuild. Equals five months of fleet OPEX ($36,560/day). Fixed charters add about $2.7m a month.",
      "OPEX series 540687 / 540689 / 540683; scrap price series 542047."],
    ["Total", "250 (100%)",
      "Tankers 70%, dry bulk 28%, cash 2%. 60% of ship-days fixed, 65% of base income. Earnings before OPEX: Bear 17.9%, Base 19.9%, Bull 23.7%.",
      "MT6102_Earnings_Model.xlsx"],
  ];
  R.forEach((r, i) => {
    const bold = i === 4;
    rows.push([cell(r[0], { bold: true, color: NAVY, fontSize: 10.5, fill: { color: bold ? LB : TINT } }), cell(r[1], { bold: true, color: RED, fontSize: 12, align: "center", fontFace: HEAD, fill: { color: bold ? LB : TINT } }),
      cell(r[2], { fontSize: 10.5, fill: { color: bold ? LB : WHITE } }), cell(r[3], { fontSize: 9.5, color: SLATE, fill: { color: bold ? LB : WHITE } })]);
  });
  table(s, rows, 0.55, 1.55, 12.2, [2.55, 1.05, 5.0, 3.6]);
  s.addNotes("This table is the whole project, read in a fixed order: how much, why, which data. Four lines plus a total. The three locked ships produce 65% of base income, which is why the worst case still returns 17.9%.");
}
{
  const s = light("Part 1 The decision");
  base(s, "Part 1 · The decision", "Capital allocation: five ships and one cash line, exactly USD 250m",
    "SIN S&P Register and 5-year-old valuation series 47130, extracted 12 Sep 2026 (October assessment $52m). Screenshots of every record are on file.");
  const rows = [hdr(["Asset", "Specification", "Price USD m", "Basis: last transacted sale or assessment", "Employment"])];
  [["MR #1", "50k dwt, 5-year-old Eco", "50", "SIN 5-year-old MR assessment, series 47130", "1-year TC at $30,000/day"],
   ["MR #2", "50k dwt, 5-year-old Eco", "50", "Same basis", "Spot, clean products"],
   ["Aframax", "110k dwt, 2018 Japan-built", "75", "Southern Reverence and Pusaka Borneo, both $75.0m (May and Apr 2026)", "3-year TC at $40,000/day"],
   ["Kamsarmax #1", "82k dwt, 2019 Oshima (Japan)", "38", "Aquavita Aim, $38.0m (10 Aug 2026)", "12-month TC at $22,000/day"],
   ["Kamsarmax #2", "82k dwt, 2015 Tsuneishi (Japan)", "32", "Medi Positano, $32.0m (10 Aug 2026)", "Spot, Q4 grain season"],
   ["Vessels", "", "245", "", ""],
   ["Cash reserve", "Counter-cyclical fund", "5", "", "Buy the collapse"],
   ["Total", "", "250", "", ""]].forEach((r, i) => {
    const sum = i >= 5; rows.push(r.map((t, j) => cell(t, { bold: sum || j === 0, color: j === 2 ? RED : (sum ? NAVY : INK), fontSize: 10.5, align: j === 2 ? "center" : "left", fill: { color: sum ? PANEL : WHITE } })));
  });
  table(s, rows, 0.55, 1.55, 12.2, [1.5, 2.6, 1.2, 4.3, 2.6], { rowH: 0.36 });
  panel(s, 0.55, 5.05, 6.0, 1.5, "Financing in one line", "The USD 250m is treated as equity, so there is no interest and no repayment schedule to meet in a weak year. Banks lend 60 to 80 percent against 5-year-old tonnage if the board later wants leverage; the Aframax with its 3-year charter is the natural first asset to mortgage or to sell and lease back.", { bodySize: 11 });
  panel(s, 6.75, 5.05, 6.0, 1.5, "All five ships are Japan or Korea built", "They sit outside the US Section 301 port-fee regime whose suspension expires around 10 November 2026. The market already prices this: a 2015 Japan-built Kamsarmax sold for $32.0m against $29.25m for a China-built sister (Presinge), a $2.75m premium for the same insurance.", { bodySize: 11 });
  s.addNotes("Ship money 245m, cash 5m. Each row names the real transaction behind the price so the board can check it. Financing is not the focus of the brief, but we state it: all equity now, leverage optional later.");
}
{
  const s = light("Part 1 The decision");
  base(s, "Part 1 · The decision", "Buy secondhand, not charter-in, not newbuild",
    "SIN series 47130 / 542021 / 540721 / 38981 / 87302 (5-year-old prices) and 71267 / 23357 / 70747 / 35905 / 53070 (newbuild prices), September 2026; charter-in hire from fixtures Intensity ($22,000) and PS Imabari ($30,000); earnings series 533288 / 543759; 10-year-old prices dataset L3.");
  panel(s, 0.55, 1.6, 5.9, 1.5, "Charter-in rejected, for both segments", "A charterer keeps only the spread over hire. Kamsarmax: hire $22,000/day against $23,000 base earnings, so +$0.35m a year at best and −$3.2m at 2025 earnings. MR: hire $30,000 against $27,000 base. It also uses little capital and owns no asset.", { bodySize: 10.5 });
  panel(s, 0.55, 3.25, 5.9, 1.5, "Newbuild rejected", "Building a ship takes 1.5 to 3 years from contract, whichever yard builds it, so a newbuild earns nothing in our 12-month window and arrives after the 2027 to 2028 delivery wave. Newbuild prices are also at decade highs.", { bodySize: 11 });
  panel(s, 0.55, 4.9, 5.9, 1.65, "5-year-old Eco chosen over 10-year-old", "Cost per remaining service year is lower (MR $2.50m against $2.67m a year), the ships are Eco specification for EU ETS and FuelEU, and 5-year-old prices sit at or just above newbuild in our segments, while Suezmax trades at 1.44 times newbuild.", { bodySize: 11 });
  img(s, "07_replacement_cost.png", 6.7, 1.6, 6.1, 4.95);
  s.addNotes("The brief allows buying or chartering. We costed all three options for both segments. Chartering in keeps only a thin spread over hire, with a large downside, uses little capital and leaves no asset. A newbuild takes 1.5 to 3 years to build whichever yard takes the order, so it earns nothing inside the window. Five-year-old Eco ships are cheaper per remaining year than 10-year-old ships and are the only tonnage at or near replacement cost.");
}
{
  const s = light("Part 1 The decision");
  base(s, "Part 1 · The decision", "Which trades our ships go into",
    "SIN series 98802 / 534403 (products trade), 534456 (crude Aframax orderbook), 557125 (Guinea bauxite), 534400 / 547349 (grain); SIN news #224049, #227870, #191021.");
  const cards = [
    ["2× MR product tankers", "Clean products: Middle East and India refineries to East Africa and South East Asia", "Refining capacity is moving east, so each tonne travels further. Products trade +6.3% in 2027F and tonne-miles +6.5%. One ship fixed to SUNCOR for a year, one trading spot where earnings are $53,741/day."],
    ["1× Aframax crude tanker", "Crude oil worldwide, routed by an oil-major-class charterer under a 3-year charter", "The lowest orderbook of any segment (8.4% of dwt). We sell certainty rather than spot exposure: $40,000/day for three years, through the delivery wave and past any ceasefire."],
    ["1× Kamsarmax (fixed)", "Bauxite Guinea to China and Pacific coal, on a 12-month charter to CNR", "Guinea exports +29% y/y; the Guinea to China run is the longest haul in dry bulk, so volume growth counts twice. Kamsarmax is the largest ship Port Kamsar can take."],
    ["1× Kamsarmax (spot)", "Grain US Gulf and Black Sea to Asia in the Q4 season, then bauxite and coal", "Harvest seasonality lifts US Gulf exports from September; 2026 is a bumper grain year. If the Black Sea stays closed the ship shifts to bauxite and coal, where two recent coal fixtures confirm the cargo."],
  ];
  cards.forEach((c, i) => {
    const x = 0.55 + (i % 2) * 6.2, y = 1.6 + Math.floor(i / 2) * 2.55;
    s.addShape(pres.ShapeType.roundRect, { x, y, w: 6.0, h: 2.4, fill: { color: PANEL }, line: { color: LINE, width: 0.75 }, rectRadius: 0.06, objectName: "Trade card" });
    s.addText(c[0], { x: x + 0.2, y: y + 0.14, w: 5.6, h: 0.34, fontSize: 14, bold: true, color: NAVY, fontFace: BODY, margin: 0, isTextBox: true });
    s.addText(c[1], { x: x + 0.2, y: y + 0.5, w: 5.6, h: 0.5, fontSize: 11.5, italic: true, color: RED, fontFace: BODY, margin: 0, isTextBox: true, valign: "top" });
    s.addText(c[2], { x: x + 0.2, y: y + 1.02, w: 5.6, h: 1.3, fontSize: 12.5, color: INK, fontFace: BODY, margin: 0, isTextBox: true, valign: "top" });
  });
  s.addNotes("Four trades, one sentence each: products ride longer hauls from refineries moving east; the Aframax sells certainty; bauxite is volume plus distance; grain is seasonal. Part 3 gives the demand chart behind each trade.");
}

// ============================================================ PART 2 PRICING
pres.addSection({ title: "Part 2 Pricing basis" });
{
  const s = light("Part 2 Pricing basis");
  base(s, "Part 2 · Pricing basis", "Pricing basis I: secondhand prices from last transacted sales",
    "SIN S&P Register (Sales by vessel type), extracted 12 Sep 2026; all 18 records in the appendix with screenshots on file.");
  const rows = [hdr(["Date", "Vessel", "Type, dwt, built", "Price", "Used for"])];
  [["01 May 2026", "Southern Reverence", "Aframax, 108,534 dwt, 2018 Tsuneishi (Japan)", "$75.0m", "Our Aframax at $75m"],
   ["24 Apr 2026", "Pusaka Borneo", "Aframax, 108,667 dwt, 2018 Tsuneishi (Japan)", "$75.0m", "Second comparable at the same price"],
   ["10 Aug 2026", "Aquavita Aim", "Kamsarmax, 82,192 dwt, 2019 Oshima (Japan)", "$38.0m", "Our Kamsarmax #1"],
   ["10 Aug 2026", "Medi Positano", "Kamsarmax, 81,661 dwt, 2015 Tsuneishi (Japan)", "$32.0m", "Our Kamsarmax #2"],
   ["11 Aug 2026", "Presinge", "Kamsarmax, 81,886 dwt, 2015 Tsuneishi Zhoushan (China)", "$29.25m", "Control: the $2.75m discount for China-built tonnage prices the port-fee risk"],
   ["Sep 2026", "MR 5-year-old benchmark", "SIN assessment, series 47130 (October: $52m)", "$50.0m", "Our two MRs"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 10.5, bold: j === 3, color: j === 3 ? RED : INK, fill: { color: i % 2 ? TINT : WHITE } }))));
  table(s, rows, 0.55, 1.6, 12.2, [1.35, 2.2, 4.0, 1.0, 3.65], { rowH: 0.52 });
  panel(s, 0.55, 5.45, 12.2, 1.1, null, "Two same-type, same-age Aframax sales at an identical $75.0m make that price firm. The two Kamsarmaxes are benchmarked to two Japan-built sales on the same day. The Presinge control shows what the market charges for the port-fee insurance we are buying.", { bodySize: 11.5 });
  s.addNotes("First price family: what we pay for the ships. Two identical Aframax sales at 75m; two Kamsarmax sales on 10 August; the China-built sister sold 2.75m cheaper the next day, which is the market price of the port-fee risk.");
}
{
  const s = light("Part 2 Pricing basis");
  base(s, "Part 2 · Pricing basis", "Pricing basis II: time-charter rates from last transacted fixtures",
    "SIN Fixtures Register (Timecharter), extracted 12 Sep 2026; SIN 1-year MR Eco TC assessment series 541552, October 2026 value $43,000/day.");
  const rows = [hdr(["Date", "Vessel", "Charterer", "Period and rate", "Used for"])];
  [["17 Aug 2026", "PS Imabari (MR, 52,838 dwt, 2022)", "SUNCOR", "1 year at $30,000/day", "MR #1 fixed rate"],
   ["17 Aug 2026", "Challenge Pollux (MR, 50,068 dwt, 2017)", "EXXONMOBIL", "1 year at $27,000/day", "MR #2 base-case spot proxy"],
   ["31 Aug 2026", "Torm Genesis (Aframax, 119,456 dwt)", "AET", "3 years at $40,000/day", "Our Aframax 3-year charter"],
   ["07 Sep 2026", "Intensity (Kamsarmax, 82,000 dwt, 2026)", "CNR", "12 months at $22,000/day", "Kamsarmax #1 fixed rate"],
   ["03 Sep 2026", "XH Hope (Kamsarmax, 84,998 dwt, 2022)", "CARGILL", "10 to 12 months at $23,000/day", "Kamsarmax #2 base-case spot proxy"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 10.5, bold: j === 3 || i === 2, color: j === 3 ? RED : INK, fill: { color: i === 2 ? LB : (i % 2 ? TINT : WHITE) } }))));
  table(s, rows, 0.55, 1.6, 12.2, [1.35, 3.6, 1.6, 2.55, 3.1], { rowH: 0.52 });
  panel(s, 0.55, 4.85, 6.0, 1.7, "Why these charterers", "Oil majors, a Canadian integrated producer and the largest grain house. Counterparty risk on the fixed 60% of ship-days is as low as the market offers, and a long charter is itself bankable security.", { bodySize: 11 });
  panel(s, 6.75, 4.85, 6.0, 1.7, "What the October refresh adds", "The SIN 1-year MR Eco assessment rose from $29,000 in September to $43,000 in October, and MR spot earnings reached $53,741/day. The $30,000 fixture is kept as the last transacted rate; the final data cut will replace it with the October fixture, which only raises the fixed leg.", { bodySize: 11 });
  s.addNotes("Second price family: charter rates. Every daily rate in the forecast is a real fixture from the last fortnight of the data cut. Torm Genesis proves a 3-year Aframax at 40,000 is signable today.");
}
{
  const s = light("Part 2 Pricing basis");
  base(s, "Part 2 · Pricing basis", "Pricing basis III: spot freight rates from last transacted voyage fixtures",
    "SIN Fixtures Register (Voyage and spot), extracted 12 Sep 2026; voyage TCE calculation in MT6102_Earnings_Model.xlsx, sheet Voyage_TCE.");
  const rows = [hdr(["Date", "Route and cargo", "Rate", "Charterer", "Role in the proposal"])];
  [["10 Sep 2026", "Coal 80,000 t, DBCT (Australia) to Vizag (India)", "$25.60/t", "SAIL", "Kamsarmax spot leg; converts to about $27,400/day TCE at September bunker prices, above the $23,000 base assumption"],
   ["09 Sep 2026", "Coal, Newcastle (Australia) to Hadong (Korea)", "$23.21/t", "KEPCO", "Second coal fixture, same week"],
   ["10 Sep 2026", "Gasoline 37,000 t, Baltic to US Gulf (Dee4 Juniper)", "WS105", "VITOL", "MR spot leg, Atlantic"],
   ["10 Sep 2026", "Gasoil 35,000 t, Singapore to Balikpapan (Pacific Cobalt)", "$1.2m lump sum", "SEARIVER", "MR intra-Asia evidence"],
   ["03 Sep 2026", "Crude 130,000 t, West Africa to Mediterranean (Sea Amethyst)", "WS210", "SHELL", "Context: Suezmax spot at two to three times normal"],
   ["10 Sep 2026", "Crude, Brazil to Chile (Barcelona Spirit)", "WS388", "PETROBRAS", "Context: extreme rates we deliberately avoid"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 10.5, bold: j === 2, color: j === 2 ? RED : (i >= 4 ? SLATE : INK), fill: { color: i >= 4 ? TINT : WHITE } }))));
  table(s, rows, 0.55, 1.6, 12.2, [1.35, 4.2, 1.35, 1.3, 4.0], { rowH: 0.56 });
  panel(s, 0.55, 5.6, 12.2, 0.95, null, "Three price families, 17 transactions, all last done: purchase prices, charter rates and freight rates. Our spot exposure sits in coal and clean products, outside the war-premium crude market.", { bodySize: 11.5 });
  s.addNotes("Third family: freight rates, the explicit requirement of item 3. The coal and products routes our spot ships trade have fresh fixtures. The two Suezmax lines are context: crude spot is at war-premium levels and we are not there.");
}

// ============================================================ PART 3 DEMAND AND SUPPLY
pres.addSection({ title: "Part 3 Demand and supply" });
{
  const s = light("Part 3 Demand and supply");
  base(s, "Part 3 · Demand and supply", "Demand: three trades, three different engines",
    "SIN series 557125 (Guinea bauxite exports), 98802 / 534403 (products trade), 98801 / 534402 (crude trade and tonne-miles); SIN news #224049, #227870, #191021, #219145. Extracted 12 Sep 2026.");
  stat(s, 0.55, 1.6, 3.9, "+29%", "Guinea bauxite exports, Jan to Apr 2026 y/y. Simandou iron ore now shipping; the Guinea to China haul ties up more ships per tonne.", { h: 1.5 });
  stat(s, 4.7, 1.6, 3.9, "+6.3%", "Seaborne products trade, 2027 forecast; tonne-miles +6.5%. Refining capacity shifting east lengthens product hauls.", { h: 1.5 });
  stat(s, 8.85, 1.6, 3.9, "−7.3%", "Seaborne crude volumes 2026, yet average haul +3.3%. Hormuz and Red Sea rerouting prop up tonne-miles: lock income with a 3-year charter.", { h: 1.5 });
  img(s, "06_bauxite_guinea.png", 0.55, 3.3, 6.0, 3.3);
  img(s, "08_average_haul.png", 6.75, 3.3, 6.0, 3.3);
  s.addNotes("Three engines. Bauxite: volume and distance both grow. Products: refineries moving east stretch hauls. Crude: volumes fell but average haul rose, the course formula tonne-miles divided by tonnes explains why ships stay busy while cargo shrinks.");
}
{
  const s = light("Part 3 Demand and supply");
  base(s, "Part 3 · Demand and supply", "Supply today: ships arrive, almost none leave",
    "SIN deliveries series 30301, 540953, 29984, 39696 and demolition series 30291, 540965, 29967, 39683, extracted 10 Oct 2026. Aframax crude = Aframax tanker series minus LR2. 2026 = year to date.");
  img(s, "12_deliveries_vs_demolition.png", 0.55, 1.6, 8.0, 4.95);
  stat(s, 8.8, 1.6, 3.95, "93 vs 609", "Kamsarmax and Panamax scrapped against delivered, 2021 to 2025: only about 15% of new ships were offset.", { h: 1.55, valueSize: 24 });
  stat(s, 8.8, 3.3, 3.95, "3 in, 8 out", "Crude Aframax in 2025: the fleet actually shrank.", { h: 1.55, valueSize: 24 });
  stat(s, 8.8, 5.0, 3.95, "153 vs 6", "Kamsarmax and Panamax delivered against scrapped, 2026 year to date: scrapping has almost stopped.", { h: 1.55, valueSize: 24 });
  s.addNotes("Fleet growth is deliveries minus scrapping. With earnings this high nobody scraps, so an overhang of old ships builds up, which Clarksons itself flagged on 9 October. Crude Aframax is the exception: more left than arrived in 2025.");
}
{
  const s = light("Part 3 Demand and supply");
  base(s, "Part 3 · Demand and supply", "Supply ahead: a delivery wave peaks in 2027 to 2028",
    "SIN Orderbook, Delivery Schedule and Fleet Register, extracted 10 Oct 2026. 2026 = deliveries still due Oct to Dec. MR = MR/Handy 25 to 55k dwt (incl. one ship due 2031). By number of ships.");
  img(s, "13_delivery_schedule.png", 0.55, 1.6, 8.0, 4.95);
  s.addText("Orderbook as % of current fleet (ships)", { x: 8.8, y: 1.6, w: 3.95, h: 0.3, fontSize: 12, bold: true, color: NAVY, fontFace: BODY, margin: 0, isTextBox: true });
  [["Kamsarmax", "472 / 3,487 ships", "13.5%"], ["MR", "367 / 2,351 ships", "15.6%"], ["Aframax crude", "62 / 696 ships", "8.9%"], ["LR2", "199 / 572 ships", "34.8%"]].forEach((r, i) => {
    const y = 2.0 + i * 1.12;
    s.addShape(pres.ShapeType.roundRect, { x: 8.8, y, w: 3.95, h: 1.0, fill: { color: i === 3 ? PINK : PANEL }, line: { color: LINE, width: 0.75 }, rectRadius: 0.06, objectName: "OB card" });
    s.addText(r[0], { x: 8.95, y: y + 0.12, w: 2.3, h: 0.32, fontSize: 13, bold: true, color: NAVY, fontFace: BODY, margin: 0, isTextBox: true });
    s.addText(r[1], { x: 8.95, y: y + 0.48, w: 2.3, h: 0.32, fontSize: 10.5, color: SLATE, fontFace: BODY, margin: 0, isTextBox: true });
    s.addText(r[2], { x: 11.2, y: y + 0.18, w: 1.45, h: 0.6, fontSize: 24, bold: true, color: i === 3 ? RED : NAVY, fontFace: HEAD, align: "right", margin: 0, isTextBox: true });
  });
  s.addNotes("The orderbook is already contracted, so 2027 and 2028 are known. Kamsarmax deliveries peak at 171 in 2027; MR runs above 100 a year; crude Aframax stays tiny; LR2 is the oversupplied one, and LR2s can switch into crude, which is why the Aframax is fixed for three years.");
}
{
  const s = light("Part 3 Demand and supply");
  base(s, "Part 3 · Demand and supply", "Replacement test: new ships against the ageing fleet",
    "SIN Orderbook Delivery Schedule and Fleet Register age profile, extracted 10 Oct 2026. Cover = orderbook divided by ships aged 20 years and over; below 1.0x the orderbook can largely replace scrapping once it resumes.");
  img(s, "14_replacement_test.png", 0.55, 1.6, 7.3, 3.6);
  const rows = [hdr(["Segment", "Cover", "Verdict and our action"])];
  [["Kamsarmax", "0.76x", "Balanced, 2027 wave: buy 2, fix 1 on a 1-year TC"], ["MR", "0.65x", "Balanced, 2027 to 2028 wave: buy 2, fix 1 on a 1-year TC"], ["Aframax crude", "0.28x", "Tightest supply: buy 1 on a 3-year TC"], ["LR2", "3.37x", "Oversupply, can switch to crude: avoid; the 3-year TC protects our Aframax"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 10.5, bold: j === 1, color: j === 1 ? (i === 3 ? RED : NAVY) : INK, fill: { color: i === 3 ? PINK : (i % 2 ? TINT : WHITE) } }))));
  table(s, rows, 8.05, 1.6, 4.7, [1.4, 0.75, 2.55], { rowH: 0.62 });
  panel(s, 0.55, 5.35, 12.2, 1.15, null, "Ships live about 25 years, so the 20-year-plus cohort is the pool that scrapping draws from. Kamsarmax, MR and crude Aframax orderbooks are all smaller than that pool; LR2 orders are 3.4 times it. Clarksons' 9 October note on the recycling overhang confirms that the deferred scrapping will come.", { bodySize: 12 });
  s.addNotes("The replacement test answers the obvious question: are the new ships net growth or just replacement? For our three segments the orderbook is smaller than the ships old enough to scrap. LR2 is the outlier and the hidden competitor to Aframax.");
}

// ============================================================ PART 4 MARKET DATA
pres.addSection({ title: "Part 4 Market data and news" });
{
  const s = light("Part 4 Market data and news");
  base(s, "Part 4 · Market data and news", "Skip Suezmax: three peak signals, all louder in October",
    "SIN series 87302 / 53070 (5-year-old and newbuild prices), 48989 / 49108 (1-year and 3-year TC), 531088 (earnings), dataset L6 (Hormuz transits), L11 (sanctioned fleet); news #221824, #227050, #228241. Chart: grey = 12 Sep extract, navy = October re-pull of 15 Oct 2026.");
  img(s, "01_peak_signals_suezmax.png", 0.55, 1.6, 7.9, 4.95);
  stat(s, 8.7, 1.6, 4.05, "1.44x", "5-year-old Suezmax against newbuild in October ($130m against $90m); 1.23x in September. Secondhand above replacement cost is the textbook over-trading signal.", { h: 1.55, valueSize: 24 });
  stat(s, 8.7, 3.3, 4.05, "$140k vs $64k", "1-year against 3-year TC in October. Spot earnings $718,165/day. The market itself prices today's rates as temporary.", { h: 1.55, valueSize: 22 });
  stat(s, 8.7, 5.0, 4.05, "2 to 7 a week", "Crude tankers transiting Hormuz (Aug to Oct). Rates reflect a supply shock, and 20% of crude tanker capacity is sanctioned: both reverse quickly.", { h: 1.55, valueSize: 24 });
  s.addNotes("Suezmax earns the most and is the one segment we refuse. All three peak signals from the cycle framework are present: secondhand above newbuild, steep backwardation between 1-year and 3-year rates, and earnings many times OPEX. The cause is a supply shock, not demand, so it can unwind fast.");
}
{
  const s = light("Part 4 Market data and news");
  base(s, "Part 4 · Market data and news", "Buy value: dry bulk is recovering, MR sits at replacement cost",
    "SIN series 17259 (BDI daily to 10 Sep, plus 6 and 13 Oct readings), 5-year-old and newbuild prices 47130 / 71267, 540721 / 70747, 38981 / 35905, 87302 / 53070 (Sep extract against Oct re-pull); news #225971, #228048, #219145, #191021.");
  img(s, "05_drybulk_recovery.png", 0.55, 1.6, 7.9, 4.95);
  stat(s, 8.7, 1.6, 4.05, "2,801", "BDI on 13 Oct, down 20% from the 3,521 peak of 10 Sep. Strong but off the high: the recovery stage, not the peak.", { h: 1.55, valueSize: 24, color: NAVY });
  stat(s, 8.7, 3.3, 4.05, "1.09x", "5-year-old Kamsarmax against newbuild ($42m against $38.5m), unchanged from September. A 9% premium, against 44% for Suezmax.", { h: 1.55, valueSize: 24, color: NAVY });
  stat(s, 8.7, 5.0, 4.05, "0.99x", "5-year-old MR against newbuild in October (0.96x in September). The lowest ratio of the five segments: we buy at replacement cost.", { h: 1.55, valueSize: 24, color: NAVY });
  s.addNotes("Dry bulk prices are rising gently while rates have come off the September high. MR is at replacement cost, which is where we want to buy. We are honest about the MR orderbook at 18% of dwt and offset it with the price we pay and with demand growth.");
}
{
  const s = light("Part 4 Market data and news");
  base(s, "Part 4 · Market data and news", "What changed since 12 September, and our freight-rate call",
    "SIN series re-pulled 15 Oct 2026 (October monthly assessments, weekly earnings to 9 Oct, BDI to 13 Oct); SIN news #229922 (9 Oct), #217187, #228241, #224049, #227789; USTR notice on the port-fee suspension.");
  const rows = [hdr(["Indicator", "12 Sep", "October", "Read"], 9.5)];
  [["Suezmax 5-year-old price, $m", "111", "130", "Peak signal stronger"], ["Suezmax 1-year TC, $/day", "90,250", "140,250", "Backwardation steeper"], ["MR 1-year TC assessment, $/day", "29,000", "43,000", "Fixed leg has upside"],
   ["MR Eco spot earnings, $/day", "35,804", "53,741", "Bull case raised"], ["Kamsarmax Eco spot, $/day", "24,484", "23,389", "Stable, above the $22,000 fix"], ["BDI", "3,521", "2,801", "Off the high, trigger 2,000 not hit"],
   ["Singapore VLSFO, $/t", "811.69", "874.94", "Charterers pay fuel on our fixed ships"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 9.5, bold: j === 2, color: j === 2 ? RED : INK, align: j === 1 || j === 2 ? "center" : "left", fill: { color: i % 2 ? TINT : WHITE } }))));
  table(s, rows, 0.55, 1.6, 6.3, [2.5, 0.85, 0.95, 2.0], { rowH: 0.4 });
  bullets(s, ["Torm ordered six MR2s on 26 Aug: new MR supply, but delivery after 2028.", "VLCC spot about $1.3m/day in early October: the war premium is still intact.", "The US and China port-fee suspension expires around 10 November 2026, inside our presentation window.", "Clarksons, 9 Oct: recycling has run below 0.5% of the fleet a year for five years; an overhang of old ships is building."], 0.55, 5.0, 6.3, 1.6, { size: 10.5, space: 3 });
  const calls = [["MR", "Firm into the first half of 2027 (spot $53,741 against our $30,000 fix), softer once 2027 deliveries land. So one ship fixed for a year, one kept open."],
    ["Aframax", "Today's rate is a war premium that falls on a ceasefire or sanctions relief. So the whole ship is fixed for three years at $40,000."],
    ["Kamsarmax", "Firm through the Q4 grain season, then pressured by 171 deliveries in 2027. The spot ship is reviewed against the BDI trigger in Q1 2027."]];
  s.addText("Our rate call for the next 6 to 12 months", { x: 7.05, y: 1.6, w: 5.7, h: 0.3, fontSize: 12, bold: true, color: NAVY, fontFace: BODY, margin: 0, isTextBox: true });
  calls.forEach((c, i) => panel(s, 7.05, 2.0 + i * 1.55, 5.7, 1.4, c[0], c[1], { bodySize: 10.5, titleSize: 12.5 }));
  s.addNotes("The brief asks whether rates will rise or fall and why. We answer per segment, with the news that supports it. Every October change strengthens the diagnosis: the Suezmax peak is more extreme, MR fixed rates have moved above our fixture, dry bulk is firm but off its high.");
}

// ============================================================ PART 5 EARNINGS
pres.addSection({ title: "Part 5 Earnings" });
{
  const s = light("Part 5 Earnings");
  base(s, "Part 5 · Earnings before OPEX", "Method: one formula, three assumptions", "MT6102_Earnings_Model.xlsx (sheets Notes and Inputs); OPEX reference series 540687 / 540689 / 540683.");
  s.addShape(pres.ShapeType.roundRect, { x: 0.55, y: 1.65, w: 12.2, h: 1.5, fill: { color: NAVY }, line: { color: NAVY, width: 0 }, rectRadius: 0.06, objectName: "Formula band" });
  s.addText("Annual earnings  =  daily rate  ×  350 operating days  ×  number of ships", { x: 0.8, y: 1.75, w: 11.7, h: 0.8, fontSize: 26, bold: true, color: WHITE, fontFace: HEAD, align: "center", valign: "middle", margin: 0, isTextBox: true });
  s.addText("Return on capital = fleet earnings ÷ USD 250m. Forecast window October 2026 to September 2027.", { x: 0.8, y: 2.55, w: 11.7, h: 0.45, fontSize: 13, color: LB, fontFace: BODY, align: "center", margin: 0, isTextBox: true });
  panel(s, 0.55, 3.45, 3.9, 2.4, "350 operating days", "365 days less 15 days of off-hire for repairs, surveys and the first special survey due on the 5-year-old MRs. Each month of delivery delay removes one twelfth of that ship's year.", { bodySize: 12.5 });
  panel(s, 4.7, 3.45, 3.9, 2.4, "Before OPEX, at TCE level", "The brief asks for revenue, not operating costs. On a time charter the charterer pays bunkers, port and canal costs; on the spot ships the TCE already nets them out. OPEX is kept as a reference line for questions.", { bodySize: 12.5 });
  panel(s, 8.85, 3.45, 3.9, 2.4, "Commission 0%", "Set to zero so the slide figures match gross hire. At the industry norm of 3.75% (address plus brokerage) the base case is $47.8m, or 19.1%, with every scenario reduced by the same share.", { bodySize: 12.5 });
  s.addNotes("One formula. Three assumptions are stated up front so that questions land on known ground: operating days, the before-OPEX convention, and commission.");
}
{
  const s = light("Part 5 Earnings");
  base(s, "Part 5 · Earnings before OPEX", "Base case by vessel: USD 49.7m, 19.9% on capital", "MT6102_Earnings_Model.xlsx, sheets Inputs and Forecast; rates from the fixtures on the Part 2 slides.");
  const rows = [hdr(["Vessel", "Employment", "Rate, $/day", "Annual earnings, $m", "Share of fleet income"])];
  [["MR #1", "1-year TC, SUNCOR", "30,000", "10.5", "21%"], ["MR #2", "Spot, base proxy Challenge Pollux fixture", "27,000", "9.45", "19%"], ["Aframax", "3-year TC, AET benchmark", "40,000", "14.0", "28%"],
   ["Kamsarmax #1", "12-month TC, CNR", "22,000", "7.7", "15%"], ["Kamsarmax #2", "Spot, base proxy XH Hope fixture", "23,000", "8.05", "16%"], ["Fleet", "60% of ship-days fixed", "142,000", "49.7", "100%"]].forEach((r, i) => {
    const sum = i === 5; rows.push(r.map((t, j) => cell(t, { fontSize: 11, bold: sum || j === 0, color: j === 3 ? RED : (sum ? NAVY : INK), align: j >= 2 ? "center" : "left", fill: { color: sum ? LB : (i % 2 ? TINT : WHITE) } })));
  });
  table(s, rows, 0.55, 1.6, 7.9, [1.6, 3.1, 1.1, 1.1, 1.0], { rowH: 0.42 });
  stat(s, 8.7, 1.6, 4.05, "$142,000", "fleet income per day in the base case", { h: 1.15, valueSize: 24, color: NAVY });
  stat(s, 8.7, 2.9, 4.05, "19.9%", "return on USD 250m before OPEX; 14.8% after OPEX of $12.8m", { h: 1.15, valueSize: 24 });
  stat(s, 8.7, 4.2, 4.05, "65%", "of base income comes from the three fixed ships ($32.2m), identical in every scenario", { h: 1.15, valueSize: 24, color: NAVY });
  panel(s, 0.55, 4.85, 7.9, 1.7, null, "Each line is the daily rate times 350 days. MR #1: 30,000 × 350 = $10.5m. Aframax: 40,000 × 350 = $14.0m. The two spot ships use the latest one-year fixtures as a conservative proxy; the coal voyage fixture converts to about $27,400/day, above the $23,000 used here.", { bodySize: 11.5 });
  s.addNotes("Five rows, one multiplication each. The fixed ships give 32.2m whatever happens; the spot ships add 17.5m in the base case. Base-case spot proxies are one-year fixtures, which are below current spot, so the base case is conservative.");
}
{
  const s = light("Part 5 Earnings");
  base(s, "Part 5 · Earnings before OPEX", "Three scenarios: the floor is 17.9% with 60% of days fixed",
    "Bear = 2025 average of SIN earnings series 543759 (MR Eco) and 533288 (Kamsarmax Eco); Base = last-done 1-year fixtures; Bull = the same series in the week of 9 Oct 2026. Weights are the group's judgement.");
  img(s, "11_scenarios.png", 0.55, 1.6, 8.0, 4.95);
  const rows = [hdr(["Scenario", "Spot legs, $/day", "Earnings", "Return"], 9.5)];
  [["Bear", "22,950 / 12,880", "$44.7m", "17.9%"], ["Base", "27,000 / 23,000", "$49.7m", "19.9%"], ["Bull", "53,741 / 23,389", "$59.2m", "23.7%"], ["Expected (30 / 50 / 20)", "", "$50.1m", "20.0%"], ["Base after OPEX", "", "$36.9m", "14.8%"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 10, bold: j === 3 || i >= 3, color: j === 3 ? RED : INK, align: j > 0 ? "center" : "left", fill: { color: i >= 3 ? PANEL : (i % 2 ? TINT : WHITE) } }))));
  table(s, rows, 8.8, 1.6, 3.95, [1.5, 1.05, 0.7, 0.7], { rowH: 0.42 });
  panel(s, 8.8, 4.3, 3.95, 2.25, "Why the bear case still works", "Only the two spot ships move. Even at 2025 average earnings, the year before the tanker boom, the fleet returns 17.9%. The bull case has already been overtaken by the October market, so our upside is stated conservatively.", { bodySize: 10.5, titleSize: 12.5 });
  s.addNotes("Three scenarios change only two ships' rates. Bear takes the 2025 averages, base the last one-year fixtures, bull the latest week. The floor of 17.9% is the direct answer to the black-swan question: we do not forecast the market, we lock the structure.");
}
{
  const s = light("Part 5 Earnings");
  base(s, "Part 5 · Earnings before OPEX", "Sensitivity: the fleet stays above 16.8% even if both spot ships collapse",
    "MT6102_Earnings_Model.xlsx, sheets Sensitivity and Voyage_TCE; Singapore VLSFO September 2026 average $874.94/t (SIN series 542456).");
  const mr = [15000, 20000, 25000, 30000, 35000], km = [13000, 18000, 23000, 28000];
  const rows = [[cell("MR #2 spot, $/day  →  Kamsarmax #2 spot, $/day", { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 9.5 })].concat(km.map(k => cell(k.toLocaleString(), { bold: true, color: WHITE, fill: { color: NAVY }, fontSize: 10, align: "center" })))];
  mr.forEach(m => {
    const row = [cell(m.toLocaleString(), { bold: true, color: NAVY, fill: { color: PANEL }, fontSize: 10.5, align: "center" })];
    km.forEach(k => { const r = (32.2e6 + (m + k) * 350) / 250e6 * 100; row.push(cell(r.toFixed(1) + "%", { align: "center", fontSize: 11, bold: r >= 20, color: r < 17.5 ? RED : INK, fill: { color: r < 17.5 ? PINK : (r >= 20 ? LB : WHITE) } })); });
    rows.push(row);
  });
  table(s, rows, 0.55, 1.6, 7.3, [2.5, 1.2, 1.2, 1.2, 1.2], { rowH: 0.5 });
  panel(s, 0.55, 4.75, 7.3, 1.5, "Reading the grid", "Every $1,000/day on both spot ships moves annual earnings by $0.7m (2 ships × 350 days). The worst cell, both ships at $15,000 and $13,000, still returns 16.8%. The return falls below 15% only if the two ships together earn less than $15,100/day.", { bodySize: 11 });
  const rows2 = [hdr(["Voyage cross-check: coal DBCT to Vizag", ""], 9.5)];
  [["Cargo and rate", "80,000 t at $25.60/t, SAIL, 10 Sep 2026"], ["Gross freight", "$2.05m"], ["Round voyage", "39 days, 4,600 nm each way"], ["Bunkers", "848 t VLSFO at $874.94/t, $0.74m"], ["Port costs and commission", "$0.16m and 3.75%"], ["Voyage TCE", "about $27,400/day"], ["Base assumption", "$23,000/day: base case is conservative"]].forEach((r, i) => rows2.push([cell(r[0], { fontSize: 10, bold: true, color: NAVY, fill: { color: i % 2 ? TINT : WHITE } }), cell(r[1], { fontSize: 10, color: i === 5 ? RED : INK, bold: i === 5, fill: { color: i % 2 ? TINT : WHITE } })]));
  table(s, rows2, 8.05, 1.6, 4.7, [1.9, 2.8], { rowH: 0.4 });
  s.addNotes("Two checks. The grid shows the return for any pair of spot rates; the floor is 16.8%. The voyage conversion turns the last coal fixture into a daily rate using September bunker prices and confirms the base assumption is conservative.");
}

// ============================================================ PART 6 SHOCKS
pres.addSection({ title: "Part 6 Shocks and mitigation" });
{
  const s = light("Part 6 Shocks and mitigation");
  base(s, "Part 6 · Shocks and mitigation", "Five shocks, five prepared answers",
    "SIN news #217187, #227049 (port fees), #227789 (Black Sea), #226856 (EU ETS review), #228241; USTR notice on the Section 301 suspension; SIN TC assessment series 48989 / 49108.");
  const rows = [hdr(["Shock", "Probability signal", "Impact on the fleet", "Our answer"], 10)];
  [["Middle East ceasefire or sanctions relief, tanker rates collapse", "The forward curve already prices it: Suezmax 1-year TC $140k against 3-year $64k", "We own no Suezmax; the Aframax 3-year charter is untouched; the MR spot leg falls, and the bear case already uses 2025 averages", "Cash plus about $2.7m a month of fixed hire buys tankers once secondhand prices fall below newbuild"],
   ["US and China port-fee suspension expires around 10 Nov 2026", "Dated event; USTR notice, news #217187 and #227049", "China-built ships calling at US ports pay fees", "All five ships are Japan or Korea built; the premium is already in our purchase prices"],
   ["Black Sea escalation blocks grain exports", "Attacks on ships and ports continued through August and October, news #227789", "Kamsarmax #2 loses one cargo source", "Shift to Guinea bauxite and Australian coal; two September coal fixtures prove the cargo is there"],
   ["Global recession", "World seaborne trade already −0.4% in 2026", "All three trades cool at once", "60% of ship-days fixed, floor 17.9%; both spot ships can be fixed for a year within weeks"],
   ["Carbon rules tighten (EU ETS, FuelEU, IMO)", "EU ETS review opened, news #226856; FuelEU limits step up from 2030", "Older, less efficient ships lose value and charterers", "Only Eco ships under 10 years old; on time charter the charterer carries fuel and allowances"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 9.5, bold: j === 0, color: j === 0 ? NAVY : INK, fill: { color: i % 2 ? TINT : WHITE } }))));
  table(s, rows, 0.55, 1.6, 12.2, [2.6, 3.0, 3.2, 3.4], { rowH: 0.78 });
  s.addNotes("Five shocks, each with a signal, an impact and a prepared answer. The ceasefire is the big one and it is the reason the portfolio avoids Suezmax. The port-fee expiry is a dated event inside the presentation window; we are immune by construction.");
}
{
  const s = light("Part 6 Shocks and mitigation");
  base(s, "Part 6 · Shocks and mitigation", "Charter expiry is timed against the delivery wave",
    "SIN Orderbook Delivery Schedule (dataset L15), extracted 10 Oct 2026; fixture Torm Genesis 3 years at $40,000/day, 31 Aug 2026.");
  // timeline: Oct 2026 (month 0) to Dec 2029 (month 38)
  const X0 = 2.6, X1 = 12.75, M = 39, px = (X1 - X0) / M;
  const mx = m => X0 + m * px;
  s.addShape(pres.ShapeType.rect, { x: mx(3), y: 1.95, w: mx(27) - mx(3), h: 3.75, fill: { color: PINK }, line: { color: PINK, width: 0 }, objectName: "Delivery wave band" });
  s.addText("Delivery wave 2027 to 2028: Kamsarmax 171 ships in 2027, MR above 100 a year, LR2 62 and 71", { x: mx(3) + 0.1, y: 2.0, w: mx(27) - mx(3) - 0.2, h: 0.3, fontSize: 10, italic: true, color: RED, fontFace: BODY, margin: 0, isTextBox: true });
  [["Oct 2026", 0], ["Jan 2027", 3], ["Jan 2028", 15], ["Jan 2029", 27], ["Dec 2029", 38]].forEach(t => {
    s.addShape(pres.ShapeType.line, { x: mx(t[1]), y: 1.9, w: 0, h: 3.85, line: { color: LINE, width: 0.75, dashType: "dash" }, objectName: "Tick" });
    s.addText(t[0], { x: mx(t[1]) - 0.5, y: 5.78, w: 1.0, h: 0.28, fontSize: 9.5, color: SLATE, fontFace: BODY, align: "center", margin: 0, isTextBox: true });
  });
  const ships = [["MR #1", "1-year TC, SUNCOR $30,000", 0, 12, NAVY], ["Kamsarmax #1", "12-month TC, CNR $22,000", 0, 12, NAVY], ["Aframax", "3-year TC, AET benchmark $40,000", 0, 36, NAVY], ["MR #2", "Spot; fixed for a year if MR spot stays below $20,000 for 8 weeks", 0, 38, PB], ["Kamsarmax #2", "Spot; fixed for 12 months if BDI stays below 2,000 for 8 weeks", 0, 38, PB]];
  ships.forEach((sh, i) => {
    const y = 2.45 + i * 0.64;
    s.addText(sh[0], { x: 0.55, y: y - 0.02, w: 2.0, h: 0.3, fontSize: 11.5, bold: true, color: NAVY, fontFace: BODY, margin: 0, isTextBox: true });
    s.addShape(pres.ShapeType.roundRect, { x: mx(sh[2]), y, w: mx(sh[3]) - mx(sh[2]), h: 0.3, fill: { color: sh[4] }, line: { color: sh[4], width: 0 }, rectRadius: 0.05, objectName: "Charter bar" });
    s.addText(sh[1], { x: mx(sh[2]) + 0.12, y, w: mx(sh[3]) - mx(sh[2]) - 0.2, h: 0.3, fontSize: 9.5, color: sh[4] === NAVY ? WHITE : INK, fontFace: BODY, valign: "middle", margin: 0, isTextBox: true });
  });
  panel(s, 0.55, 6.0, 12.2, 0.62, null, "MR #1 and Kamsarmax #1 expire around September 2027, before the wave peaks: renew or go spot one quarter ahead. The Aframax charter runs to 2029, across the whole wave; LR2 orders at 3.37 times the old LR2 fleet are the hidden competitor it hedges.", { bodySize: 10.5 });
  s.addNotes("Timing matters as much as rates. The two one-year charters end before the wave crests, so the decision point comes early. The Aframax is covered through the wave. Spot ships carry explicit triggers that convert them to period charters.");
}
{
  const s = light("Part 6 Shocks and mitigation");
  base(s, "Part 6 · Shocks and mitigation", "What we watch, when we act, and two weaknesses we state ourselves",
    "SIN dataset L6 (Hormuz transits), series 17259 (BDI), 543759 (MR Eco earnings), 534440 (product tanker orderbook); OPEX series 540687 / 540689 / 540683.");
  const rows = [hdr(["Trigger", "Action"])];
  [["Hormuz crude tanker transits above 50 a week for four consecutive weeks", "Normalisation signal. Our income is unchanged; start screening secondhand Suezmaxes with a target price below newbuild"],
   ["BDI below 2,000 for eight consecutive weeks", "Fix Kamsarmax #2 on a 12-month charter"],
   ["MR spot earnings below $20,000/day for eight consecutive weeks", "Fix MR #2 on a 1-year charter"],
   ["Port-fee suspension not renewed in November", "No action needed (Japan and Korea built); re-check charterers' US calling plans"],
   ["Every Friday", "One member scans the SIN weekly: fixtures, sanctions lists, ceasefire and tariff news"]].forEach((r, i) => rows.push([cell(r[0], { fontSize: 10.5, bold: true, color: NAVY, fill: { color: i % 2 ? TINT : WHITE } }), cell(r[1], { fontSize: 10.5, fill: { color: i % 2 ? TINT : WHITE } })]));
  table(s, rows, 0.55, 1.6, 7.6, [3.5, 4.1], { rowH: 0.66 });
  panel(s, 8.4, 1.6, 4.35, 2.0, "Weakness 1: MR orderbook", "18% of dwt is high. We offset it with the purchase price (at replacement cost), with 2027 products demand (+6.3%) and with one MR fixed for a year.", { fill: PINK, line: "F2C9C9", bodySize: 12 });
  panel(s, 8.4, 3.8, 4.35, 2.3, "Weakness 2: a thin cash line", "2% of capital is deliberate, because idle cash earns nothing in a strong market. It covers five months of OPEX, and fixed hire adds about $2.7m a month. A variant with one ship fewer and more cash is kept in reserve.", { fill: PINK, line: "F2C9C9", bodySize: 12 });
  s.addNotes("Triggers turn the plan into actions with numbers and dates. We name our own two weak points before anyone asks: the MR orderbook and the thin cash line, and we show how each is handled.");
}

// ============================================================ CLOSE
pres.addSection({ title: "Close" });
{
  const s = dark("Close");
  s.addText("CONCLUSION", { x: 0.9, y: 0.9, w: 11.5, h: 0.3, fontSize: 12, bold: true, color: PB, fontFace: BODY, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText("Skip the peak. Buy value. Lock income.", { x: 0.9, y: 1.3, w: 11.5, h: 0.9, fontSize: 36, bold: true, color: WHITE, fontFace: HEAD, margin: 0, isTextBox: true });
  const rec = [["How we allocate", "Tankers 70%, dry bulk 28%, cash 2%: two MRs, one Aframax, two Kamsarmaxes, five ships at or near replacement cost."],
    ["Why", "We avoid Suezmax at 1.44 times newbuild and steep backwardation; we buy segments with the smallest orderbooks against their ageing fleets; we fix 60% of ship-days so the worst case still returns 17.9%."],
    ["What the data says", "60 time series, 40 last-done transactions and 55 news items from Clarksons SIN, every figure with a series number and a screenshot. Base case 19.9%, expected value 20.0%, floor 17.9% before OPEX."]];
  rec.forEach((r, i) => {
    const y = 2.55 + i * 1.05;
    circle(s, 0.95, y + 0.05, i + 1);
    s.addText(r[0], { x: 1.5, y, w: 10.8, h: 0.34, fontSize: 15, bold: true, color: WHITE, fontFace: BODY, margin: 0, isTextBox: true });
    s.addText(r[1], { x: 1.5, y: y + 0.36, w: 10.8, h: 0.62, fontSize: 12, color: LB, fontFace: BODY, margin: 0, isTextBox: true, valign: "top" });
  });
  s.addText("We do not forecast the market. We lock the structure. Thank you, we welcome your questions.", { x: 0.9, y: 5.95, w: 11.5, h: 0.5, fontSize: 16, italic: true, color: PB, fontFace: HEAD, margin: 0, isTextBox: true });
  s.addNotes("Close in the same order as the opening: how we allocate, why, and what the data says. One sentence to end: we do not forecast the market, we lock the structure.");
}

// ============================================================ APPENDIX
pres.addSection({ title: "Appendix" });
{
  const s = dark("Appendix");
  s.addText("APPENDIX", { x: 0.9, y: 2.3, w: 11.5, h: 0.3, fontSize: 12, bold: true, color: PB, fontFace: BODY, charSpacing: 3, margin: 0, isTextBox: true });
  s.addText("Reference pages for questions", { x: 0.9, y: 2.7, w: 11.5, h: 0.9, fontSize: 40, bold: true, color: WHITE, fontFace: HEAD, margin: 0, isTextBox: true });
  s.addText("A1 Fleet and orderbook detail  ·  A2 Deliveries and demolition by year  ·  A3 Sale and purchase records  ·  A4 Time-charter fixtures  ·  A5 Spot fixtures and voyage conversion  ·  A6 News evidence library  ·  A7 Earnings model structure  ·  A8 Course concepts applied  ·  A9 Glossary  ·  A10 Market backdrop charts", { x: 0.9, y: 3.75, w: 11.5, h: 1.2, fontSize: 13, color: LB, fontFace: BODY, margin: 0, isTextBox: true, valign: "top" });
}
{
  const s = light("Appendix");
  base(s, "Appendix A1", "Fleet and orderbook detail, two bases side by side",
    "SIN Fleet Development and Orderbook series (dataset L4, Sep 2026 and 1 Oct 2026), Orderbook Delivery Schedule and Fleet Register age profile (L15, L16, 10 Oct 2026).");
  const rows = [hdr(["Segment", "Fleet, ships", "Fleet, m dwt", "Orderbook, ships (Sep)", "Orderbook, ships (1 Oct)", "Orderbook, m dwt", "Orderbook % of fleet (dwt)", "Ships aged 20+", "Orderbook ÷ 20+ fleet"], 9.5)];
  [["MR 40 to 55k dwt", "1,906", "92.5", "340", "347", "16.7", "18.0%", "568 (MR/Handy 25 to 55k)", "0.65x"],
   ["Aframax incl. LR2", "1,257", "139.2", "254", "260", "29.0", "20.8%", "223 crude + 59 LR2", "0.28x crude, 3.37x LR2"],
   ["Suezmax", "725", "113.8", "211", "213", "33.2", "29.1%", "not held", "not held"],
   ["Panamax and Kamsarmax", "3,467", "282.1", "463", "474", "38.6", "13.7%", "618", "0.76x"],
   ["Handymax and Ultramax", "4,574", "263.2", "568", "647", "35.8", "13.6%", "not held", "not held"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 10, bold: j === 0, color: j === 0 ? NAVY : INK, align: j > 0 ? "center" : "left", fill: { color: i % 2 ? TINT : WHITE } }))));
  table(s, rows, 0.55, 1.6, 12.2, [1.9, 1.0, 1.0, 1.35, 1.35, 1.1, 1.35, 1.7, 1.45], { rowH: 0.55 });
  panel(s, 0.55, 5.2, 12.2, 1.35, "Why two bases", "The dwt basis (Sep) is the standard orderbook ratio; the ship basis (10 Oct) is what the replacement test needs. Crude Aframax on its own is 8.4% of dwt and 62 ships; including LR2 the figure is 20.8%, because LR2 newbuilds can trade crude. That is why we hold one Aframax only and fix it for three years.", { bodySize: 11 });
}
{
  const s = light("Appendix");
  base(s, "Appendix A2", "Deliveries and demolition by year, ships", "SIN deliveries series 30301 / 540953 / 29984 / 39696 and demolition series 30291 / 540965 / 29967 / 39683, extracted 10 Oct 2026. Crude Aframax = Aframax tanker minus LR2. 2026 = year to date.");
  const rows = [hdr(["Year", "Kamsarmax / Panamax delivered", "scrapped", "MR 40 to 55k delivered", "scrapped", "Aframax crude delivered", "scrapped", "LR2 delivered", "scrapped"], 9.5)];
  [["2021", "103", "9", "66", "35", "25", "26", "28", "8"], ["2022", "119", "10", "51", "11", "20", "7", "19", "4"], ["2023", "130", "31", "28", "4", "16", "2", "22", "0"], ["2024", "121", "21", "20", "1", "7", "3", "20", "0"], ["2025", "136", "22", "86", "13", "3", "8", "54", "2"], ["2021 to 2025", "609", "93", "251", "64", "71", "46", "143", "14"], ["2026 YTD", "153", "6", "84", "10", "9", "5", "62", "0"]].forEach((r, i) => {
    const sum = i === 5; rows.push(r.map((t, j) => cell(t, { fontSize: 10.5, bold: sum || j === 0, color: sum ? NAVY : INK, align: j > 0 ? "center" : "left", fill: { color: sum ? LB : (i % 2 ? TINT : WHITE) } })));
  });
  table(s, rows, 0.55, 1.6, 12.2, [1.5, 1.7, 1.05, 1.5, 1.05, 1.5, 1.05, 1.5, 1.35], { rowH: 0.5 });
  panel(s, 0.55, 5.75, 12.2, 0.8, null, "Across 2021 to 2025, only 15% of new Kamsarmax tonnage was offset by scrapping and 25% of new MRs; crude Aframax scrapped two thirds of what it took delivery of. In 2026 scrapping has almost stopped in every segment.", { bodySize: 11 });
}
{
  const s = light("Appendix");
  base(s, "Appendix A3", "Sale and purchase records, 18 last-done transactions", "SIN S&P Register by vessel type, extracted 12 Sep 2026. Prices undisclosed where the register shows none. * = en bloc resale of newbuildings.");
  const rows = [hdr(["Type", "Date", "Vessel", "dwt", "Built", "Yard (country)", "Price $m", "Seller", "Buyer"], 9)];
  [["MR", "14 Aug 2026", "On Promise*", "50,000", "2026", "HD Hyundai Medium (Korea)", "undisclosed", "Onex DMCC", "Undisclosed"], ["MR", "14 Aug 2026", "On Prosper*", "50,000", "2026", "HD Hyundai Medium (Korea)", "undisclosed", "Onex DMCC", "Undisclosed"], ["MR", "11 Aug 2026", "High Discovery", "49,999", "2014", "HD Hyundai Mipo (Korea)", "15.30", "Japanese interests", "d'Amico clients"], ["MR", "07 Aug 2026", "Atlantic Eagle", "47,128", "2007", "HD Hyundai Mipo (Korea)", "undisclosed", "Cido Shipping", "Undisclosed"],
   ["Ultramax", "19 Aug 2026", "Amaryllis", "63,301", "2013", "Sinopacific Dayang (China)", "24.00", "Livanos N.G.", "Chinese interests"], ["Ultramax", "01 Aug 2026", "Gramos", "61,171", "2019", "Nantong COSCO KHI (China)", "34.50", "Helikon", "Livanos clients"], ["Ultramax", "20 Jul 2026", "Seacon Tokyo", "66,628", "2023", "Tsuneishi Zhoushan (China)", "41.60", "Seacon Shipping", "OBE Ships clients"],
   ["Suezmax", "27 Aug 2026", "Cape Benat", "156,719", "2010", "Jiangsu Rongsheng (China)", "62.50", "Pareto Maritime", "Lila Global clients"], ["Suezmax", "27 Aug 2026", "Hedda Knutsen", "154,348", "2024", "COSCO HI Zhoushan (China)", "113.00 (TC incl.)", "Knutsen NYK", "KNOT clients"], ["Suezmax", "11 Aug 2026", "Bristol", "157,077", "2024", "HD Hyundai Samho (Korea)", "undisclosed", "Euronav", "Undisclosed"],
   ["Aframax", "01 May 2026", "Southern Reverence", "108,534", "2018", "Tsuneishi Zosen (Japan)", "75.00", "Nissen Kaiun", "Undisclosed"], ["Aframax", "24 Apr 2026", "Pusaka Borneo", "108,667", "2018", "Tsuneishi Zosen (Japan)", "75.00", "Pusaka Laut", "Undisclosed"], ["Aframax", "31 Mar 2026", "Penelop", "115,091", "2006", "Daewoo DSME (Korea)", "undisclosed", "Lundqvist", "Undisclosed"], ["Aframax", "05 Mar 2026", "Green Attitude", "112,532", "2018", "COSCO HI Zhoushan (China)", "70.00", "Aegean Shipping", "Minerva clients"],
   ["Kamsarmax", "14 Aug 2026", "BBG Wuzhou", "81,895", "2016", "Tsuneishi Zhoushan (China)", "29.00 (auction)", "CDB Leasing", "Undisclosed"], ["Kamsarmax", "11 Aug 2026", "Presinge", "81,886", "2015", "Tsuneishi Zhoushan (China)", "29.25", "SwissMarine", "Indian interests"], ["Kamsarmax", "10 Aug 2026", "Aquavita Aim", "82,192", "2019", "Oshima (Japan)", "38.00", "Olive Shipmanagement", "Undisclosed"], ["Kamsarmax", "10 Aug 2026", "Medi Positano", "81,661", "2015", "Tsuneishi Zosen (Japan)", "32.00", "d'Amico Dry", "Greek interests"]].forEach((r, i) => {
    const used = ["Southern Reverence", "Pusaka Borneo", "Aquavita Aim", "Medi Positano", "Presinge"].includes(r[2]);
    rows.push(r.map((t, j) => cell(t, { fontSize: 8.5, bold: j === 6 || used, color: j === 6 ? RED : INK, fill: { color: used ? LB : (i % 2 ? TINT : WHITE) } })));
  });
  table(s, rows, 0.55, 1.5, 12.2, [0.95, 1.1, 1.65, 0.8, 0.6, 2.3, 1.3, 1.75, 1.75], { rowH: 0.26 });
}
{
  const s = light("Appendix");
  base(s, "Appendix A4", "Time-charter fixtures, 16 last-done records", "SIN Fixtures Register (Timecharter), extracted 12 Sep 2026. Highlighted rows are the five rates used in the earnings model.");
  const rows = [hdr(["Type", "Date", "Vessel", "dwt", "Built", "Charterer", "Delivery", "Period", "Rate $/day", "Owner"], 9)];
  [["MR", "17 Aug 2026", "PS Imabari", "52,838", "2022", "SUNCOR", "", "1 year", "30,000", "Shoei Kisen"], ["MR", "17 Aug 2026", "Challenge Pollux", "50,068", "2017", "EXXONMOBIL", "", "1 year", "27,000", "NYK Line"], ["MR", "31 Aug 2026", "SM Falcon", "50,017", "2017", "CLEARLAKE", "W Med", "2 years", "25,500", "Korea Line"], ["MR", "31 Aug 2026", "Stena Imagination", "49,689", "2016", "ESSAR", "UK Cont", "2 years", "27,750", "Stena Bulk"],
   ["Ultramax", "26 Aug 2026", "W-Lion", "63,308", "2014", "NOVA MARINE", "Port Qasim", "10 to 13 months", "19,000", "W Marine"], ["Ultramax", "19 Aug 2026", "Yuan Hai Qing Han", "63,776", "2025", "CHINALAND", "Qinzhou", "8 to 10 months", "20,750", "JIC Leasing"], ["Ultramax", "14 Aug 2026", "Gramba", "61,233", "2021", "CTM", "Dalian", "10 to 13 months", "19,000", "Susesea"],
   ["Suezmax", "17 Aug 2026", "Monte Urbasa", "156,400", "2018", "ST SHIPPING", "Singapore", "1 year", "74,500", "Ibaizabal"], ["Suezmax", "09 Mar 2026", "Ithaki Warrior", "159,962", "2017", "TRAFIGURA", "Baltic", "10 to 14 months", "86,000", "Polembros"], ["Suezmax", "09 Mar 2026", "Kapsali", "158,546", "2011", "MERCURIA", "Korea", "11 to 13 months", "80,000", "Centrofin"],
   ["Aframax", "24 Aug 2026", "TP Spirit", "114,139", "2016", "MERCURIA", "Singapore", "1 year", "53,250", "Transpetrol"], ["Aframax", "31 Aug 2026", "Torm Genesis", "119,456", "2011", "AET", "Singapore", "3 years", "40,000", "TORM"], ["Aframax", "24 Aug 2026", "Hafnia Despina", "109,990", "2019", "MERCURIA", "W Med", "2 years", "50,000", "Hafnia"],
   ["Kamsarmax", "07 Sep 2026", "Intensity", "82,000", "2026", "CNR", "Yeosu", "12 months", "22,000", "Aegean Bulk"], ["Kamsarmax", "03 Sep 2026", "XH Hope", "84,998", "2022", "CARGILL", "Qinzhou", "10 to 12 months", "23,000", "Zhejiang Xiehai"], ["Kamsarmax", "27 Aug 2026", "Lestari Kuala Lumpur", "82,074", "2026", "CNR", "Maoming", "9 to 11 months", "21,000", "Lestari Maritime"]].forEach((r, i) => {
    const used = ["PS Imabari", "Challenge Pollux", "Torm Genesis", "Intensity", "XH Hope"].includes(r[2]);
    rows.push(r.map((t, j) => cell(t, { fontSize: 8.5, bold: j === 8 || used, color: j === 8 ? RED : INK, fill: { color: used ? LB : (i % 2 ? TINT : WHITE) } })));
  });
  table(s, rows, 0.55, 1.5, 12.2, [0.95, 1.1, 1.75, 0.8, 0.6, 1.3, 1.0, 1.35, 1.0, 2.35], { rowH: 0.28 });
}
{
  const s = light("Appendix");
  base(s, "Appendix A5", "Spot fixtures and the voyage-to-TCE conversion", "SIN Fixtures Register (Voyage and spot), extracted 12 Sep 2026; MT6102_Earnings_Model.xlsx sheet Voyage_TCE; Singapore VLSFO series 542456.");
  const rows = [hdr(["Date", "Vessel", "Built", "Cargo", "Load", "Discharge", "Rate", "Charterer"], 9.5)];
  [["10 Sep 2026", "TBN (Kamsarmax)", "", "Coal 80,000 t", "DBCT, Australia", "Vizag, India", "$25.60/t", "SAIL"], ["09 Sep 2026", "TBN (Kamsarmax)", "", "Coal 80,000 t", "Newcastle, Australia", "Hadong, Korea", "$23.21/t", "KEPCO"], ["03 Sep 2026", "Sea Amethyst", "2022", "Crude 130,000 t", "West Africa", "Mediterranean", "WS210", "SHELL"], ["10 Sep 2026", "Barcelona Spirit", "2011", "Crude 130,000 t", "Brazil", "Chile", "WS388", "PETROBRAS"], ["10 Sep 2026", "Dee4 Juniper", "2022", "Gasoline 37,000 t", "Ventspils, Baltic", "US Gulf", "WS105", "VITOL"], ["10 Sep 2026", "Pacific Cobalt", "2020", "Gasoil 35,000 t", "Singapore", "Balikpapan, Indonesia", "$1.2m lump sum", "SEARIVER"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 10, bold: j === 6, color: j === 6 ? RED : INK, fill: { color: i % 2 ? TINT : WHITE } }))));
  table(s, rows, 0.55, 1.6, 12.2, [1.2, 1.7, 0.6, 1.6, 1.9, 1.9, 1.4, 1.9], { rowH: 0.36 });
  const rows2 = [hdr(["Step", "Value"], 9.5)];
  [["Gross freight", "80,000 t × $25.60 = $2,048,000"], ["Sea days", "4,600 nm laden at 12.5 kn + 4,600 nm ballast at 13 kn = 30.1 days; port 9 days; total 39.1 days"], ["Bunkers", "30.1 × 27 t + 9 × 4 t = 848 t × $874.94 = $742,000"], ["Port costs and commission", "$160,000 + 3.75% × $2,048,000 = $76,800"], ["Net voyage result", "$1,069,000"], ["TCE", "$1,069,000 ÷ 39.1 days = about $27,400/day, 19% above the $23,000 base assumption"]].forEach((r, i) => rows2.push([cell(r[0], { fontSize: 10, bold: true, color: NAVY, fill: { color: i % 2 ? TINT : WHITE } }), cell(r[1], { fontSize: 10, bold: i === 5, color: i === 5 ? RED : INK, fill: { color: i % 2 ? TINT : WHITE } })]));
  table(s, rows2, 0.55, 4.45, 12.2, [2.2, 10.0], { rowH: 0.29 });
}
{
  const s = light("Appendix");
  base(s, "Appendix A6", "News evidence library: which decision each item supports", "Clarksons Research news on SIN (article numbers shown), 55 items collected; the 19 below enter the argument. Tags: skip tanker, buy bulk, buy MR, buy Aframax, ship choice, risk.");
  const rows = [hdr(["Date", "Clarksons headline and article number", "Point and use", "Supports"], 9)];
  [["04 Mar 2026", "Middle East Conflict: Update No.3, #221824", "Day 5 of the conflict, Hormuz transits collapse: the start of the tanker spike", "skip tanker"], ["24 Jul 2026", "Middle East Update: Disruption Doubling Up?, #227050", "Red Sea attacks restart in 2026; VLCC Bab el-Mandeb transits fall; supports longer hauls", "skip tanker"], ["26 Aug 2026", "Sanctioned Vessels Update, #228241", "1,004 sanctioned tankers = 20% of crude tanker capacity (Aframax 35%)", "skip tanker, buy Aframax"], ["28 Jul 2026", "Sanctioned Vessels Update, #227115", "EU adds 13 ships on 24 Jul: sanctions tighten month by month", "skip tanker"], ["10 Jul 2026", "Middle East Conflict: Shipping Market Update, #226516", "How the conflict feeds through to each segment's rates", "skip tanker"],
   ["07 May 2026", "Guinea Bauxite and Iron Ore Exports Update, #224049", "Guinea bauxite exports Jan to Apr +29%; Simandou ramping up", "buy bulk"], ["25 Jun 2026", "Bulkcarrier Markets Enjoying The Summer Sun, #225971", "Clarksons confirms bulk at a two-year high: recovery stage", "buy bulk"], ["21 Aug 2026", "Bulkcarrier Market Outlook, August 2026, #228048", "Ore plus grain on the demand side, moderate ordering on supply", "buy bulk"], ["17 Aug 2026", "A Bumper Year For Grain Trade (So Far), #227870", "2026 a bumper grain year: basis for the Q4 spot Kamsarmax", "buy bulk"], ["09 Oct 2026", "Ship Recycling: Building Up An Overhang, #229922", "Recycling under 0.5% of the fleet a year for five years; the overhang backs the replacement test", "buy bulk, buy Aframax"],
   ["22 Dec 2025", "Seaborne Oil Trade: Bouncing Back, #219145", "Products trade recovering since mid-2025: the MR turning point", "buy MR"], ["28 Jul 2023", "Products Trade: In It For The Long Haul?, #191021", "Refineries moving east lengthen product hauls: the MR long story", "buy MR"],
   ["17 Oct 2025", "US And Chinese Port Fees: Taking Stock, #216732", "US fees on China-built ships start, China retaliates: build country becomes a cost variable", "ship choice, risk"], ["30 Oct 2025", "US-China Policy: 30th Oct Update, #217187", "One-year suspension on both sides; expiry around 10 Nov 2026 inside the presentation window", "ship choice, risk"], ["24 Jul 2026", "US Section 301 Tariff Update, #227049", "Latest 301 developments ahead of the expiry", "risk"], ["21 Jul 2026", "EU Review of the Emissions Trading Scheme, #226856", "EU ETS review opens: the case for Eco ships under 10 years", "ship choice, risk"], ["14 Aug 2026", "Russia-Ukraine: Vessel and Infrastructure Attacks, #227789", "Black Sea attacks hit oil and grain exports: cargo flexibility for Kamsarmax #2", "buy bulk, risk"],
   ["13 Oct 2026", "BDI 2,801 (SIN series 17259, refreshed 15 Oct)", "Dry bulk strong but off the September high", "buy bulk, risk"], ["26 Aug 2026", "Torm orders six MR2s (industry news, not SIN)", "A leading owner still invests in MR; delivery after 2028, outside our window", "buy MR, risk"]].forEach((r, i) => rows.push(r.map((t, j) => cell(t, { fontSize: 8.5, bold: j === 3, color: j === 3 ? NAVY : INK, fill: { color: i % 2 ? TINT : WHITE } }))));
  table(s, rows, 0.55, 1.45, 12.2, [1.1, 4.3, 5.2, 1.6], { rowH: 0.24 });
}
{
  const s = light("Appendix");
  base(s, "Appendix A7", "Earnings model structure: eight sheets, seven steps", "MT6102_Earnings_Model.xlsx; every input cell carries its SIN series number or fixture.");
  const sheets = [["Inputs", "Every number used, with its source; yellow cells are assumptions"], ["Forecast", "Per-ship annual earnings, three scenarios, expected value, return, after-OPEX line"], ["Monthly", "The chosen scenario spread over 12 calendar months"], ["Sensitivity", "Fleet earnings for any pair of spot rates"], ["Voyage_TCE", "Converts the coal fixture into a daily rate"], ["Notes and Sources", "Formula, caveats, series list"]];
  sheets.forEach((sh, i) => panel(s, 0.55 + (i % 3) * 4.15, 1.6 + Math.floor(i / 3) * 1.35, 3.9, 1.2, sh[0], sh[1], { bodySize: 10.5, titleSize: 12.5 }));
  const steps = ["Fix the rates: three ships at their fixture rates, two spot ships at the one-year fixture proxies", "Scenario values for the two spot ships: bear 2025 average, base fixture, bull latest week", "Each ship: rate × 350 days", "Add the five ships: $142,000 × 350 = $49.7m base", "Divide by $250m: 19.9%; bear 17.9%, bull 23.7%", "Weight 30 / 50 / 20: expected $50.1m, 20.0%", "Deduct OPEX of $36,560/day × 350 = $12.8m for the after-OPEX reference: $36.9m, 14.8%"];
  steps.forEach((t, i) => { const y = 4.45 + i * 0.31; circle(s, 0.6, y + 0.02, i + 1, { d: 0.26, size: 9.5, fill: NAVY }); s.addText(t, { x: 1.0, y, w: 11.7, h: 0.3, fontSize: 10.5, color: INK, fontFace: BODY, margin: 0, isTextBox: true }); });
}
{
  const s = light("Appendix");
  base(s, "Appendix A8", "Course concepts applied in the proposal", "Concepts from the MT6102 lecture series; page references held in the group's working notes.");
  const rows = [hdr(["Concept", "Where it is used"], 10)];
  [["Derived demand", "Shipping demand follows cargo trade: Part 3 starts from bauxite, products and crude volumes, not from ships"], ["Four shipping markets and the last-done convention", "Part 2: every price is the last transacted sale or fixture, the starting point of any negotiation"], ["Cost split under a time charter", "Owner pays capital and operating costs, charterer pays voyage costs: the before-OPEX convention and the fuel and allowance exposure of the fixed ships"], ["Cycle stages and peak signals", "Secondhand above newbuild, old ships chartered, rates many times OPEX, zero scrapping: the Suezmax diagnosis and the dry bulk recovery call"], ["Ship price determinants, 5 to 6% a year depreciation", "The 5-year-old against 10-year-old comparison and the replacement-cost ratio"], ["Demand and supply five-factor model, tonne-miles and average haul", "Part 3 structure; crude volumes −7.3% with average haul +3.3%"], ["Supply is inelastic in the short run; build time one to four years", "Why a Hormuz closure multiplies rates, and why the 2027 to 2028 wave is already fixed"], ["Scrapping determinants: age, obsolescence, scrap price, earnings, expectations", "Why scrapping stopped in 2025 and why the overhang will return"], ["Financiers prefer predictable earnings; debt means fixed repayments", "60% of ship-days fixed; all-equity base case; leverage optional later"], ["Regulatory cost incidence and marginal abatement cost", "Eco ships abate cheaply; on time charter the charterer carries fuel and allowances"]].forEach((r, i) => rows.push([cell(r[0], { fontSize: 10, bold: true, color: NAVY, fill: { color: i % 2 ? TINT : WHITE } }), cell(r[1], { fontSize: 10, fill: { color: i % 2 ? TINT : WHITE } })]));
  table(s, rows, 0.55, 1.6, 12.2, [4.2, 8.0], { rowH: 0.46 });
}
{
  const s = light("Appendix");
  base(s, "Appendix A9", "Glossary", "");
  const rows = [hdr(["Term", "Meaning"], 10)];
  [["Time charter (TC)", "The charterer hires the ship for a period at a daily rate and pays voyage costs; the owner pays capital and operating costs"], ["Spot / voyage charter", "One voyage at a freight rate per tonne or in Worldscale; the owner pays voyage costs"], ["TCE", "Time-charter equivalent: voyage income net of voyage costs, per day, comparable with a TC rate"], ["Worldscale (WS)", "Tanker freight index; WS100 is the published flat rate for the route, quotes are a percentage of it"], ["Last done", "The most recent transaction at the time of extraction; the starting point of charter negotiations"], ["Orderbook", "Ships contracted but not yet delivered, as a share of the fleet in dwt or in ships"], ["Tonne-miles, average haul", "Cargo tonnes times distance; average haul = tonne-miles ÷ tonnes"], ["OPEX", "Crew, insurance, stores, repair and maintenance; excludes capital and voyage costs"], ["Eco ship", "Post-2013 design with lower fuel consumption; better placed under EU ETS and FuelEU"], ["BDI", "Baltic Dry Index, a weighted average of Capesize, Panamax and Supramax time-charter averages"], ["Kamsarmax", "Bulk carrier of about 80,000 to 85,000 dwt, the largest size Port Kamsar in Guinea can load"], ["Replacement cost", "The newbuild price of an equivalent ship; secondhand above replacement cost signals over-trading"]].forEach((r, i) => rows.push([cell(r[0], { fontSize: 10, bold: true, color: NAVY, fill: { color: i % 2 ? TINT : WHITE } }), cell(r[1], { fontSize: 10, fill: { color: i % 2 ? TINT : WHITE } })]));
  table(s, rows, 0.55, 1.6, 12.2, [2.6, 9.6], { rowH: 0.4 });
}
{
  const s = light("Appendix");
  base(s, "Appendix A10", "Market backdrop: a supply shock, and a reversible one",
    "SIN series 98801 / 546177 (crude volumes and earnings), L11 (sanctioned fleet), L6 (chokepoint transits), 534438 (crude orderbook); news #221824, #227050, #228241.");
  img(s, "02_supply_shock.png", 0.55, 1.6, 6.0, 2.45);
  img(s, "09_chokepoints.png", 6.75, 1.6, 6.0, 2.45);
  img(s, "10_sanctioned_fleet.png", 0.55, 4.15, 6.0, 2.45);
  img(s, "04_fleet_growth.png", 6.75, 4.15, 6.0, 2.45);
}

(async () => {
  await pres.writeFile({ fileName: "MT6102_Investment_Proposal.pptx" });
  await applyTheme("MT6102_Investment_Proposal.pptx", THEME);
  console.log("written", n, "slides");
})();
