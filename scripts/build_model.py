# -*- coding: utf-8 -*-
"""MT6102 12-month earnings model (before OPEX, with after-OPEX bridge)."""
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

BLUE = Font(name="Arial", color="0000FF")          # hardcoded inputs
BLACK = Font(name="Arial")                          # formulas
BOLD = Font(name="Arial", bold=True)
H1 = Font(name="Arial", bold=True, size=14)
GREEN = Font(name="Arial", color="008000")          # cross-sheet links
YELLOW = PatternFill("solid", fgColor="FFFF00")
GRAYF = PatternFill("solid", fgColor="F2F2F2")
THIN = Border(bottom=Side(style="thin", color="BFBFBF"))
M = '#,##0'; USD = '$#,##0'; USD1 = '$#,##0.0,,"m"'; PCT = '0.0%'

wb = Workbook()

# ---------------- Assumptions ----------------
ws = wb.active; ws.title = "Assumptions"
ws.column_dimensions["A"].width = 46
for c in "BCDE": ws.column_dimensions[c].width = 15
ws["A1"] = "MT6102 Group Investment Proposal — Key Assumptions"; ws["A1"].font = H1
ws["A2"] = "All rates/prices = last transacted sale/fixture, Clarksons SIN, extracted 12 Sep 2026"
ws["A3"] = "Legend:  blue = input (edit these) | black = formula | yellow = key scenario levers"
ws["A3"].font = Font(name="Arial", italic=True, size=9)

rows = [
    ("Fund size (USD m)", 250, None, None, "Assignment brief"),
    ("Operating days per ship per year", 350, None, None, "15 days off-hire/dry-dock allowance"),
    ("", None, None, None, ""),
    ("OPEX $/day — MR product tanker", 7990, None, None, "Clarksons OPEX series [540687], 2026"),
    ("OPEX $/day — Aframax", 8280, None, None, "[540689], 2026"),
    ("OPEX $/day — Kamsarmax bulker", 6150, None, None, "[540683], 2026"),
    ("", None, None, None, ""),
    ("SCENARIO SPOT-LEG RATES ($/day)", "Bear", "Base", "Bull", ""),
    ("MR spot leg", 17600, 27000, 35800, "Bear=2025 avg MR clean [545055]; Base=last-done 1yr fixture Challenge Pollux; Bull=spot 11 Sep [L5]"),
    ("Kamsarmax spot leg", 14000, 23000, 24500, "Bear=long-run 1yr TC mid [540614]; Base=last-done fixture XH Hope; Bull=spot 11 Sep [533288]"),
    ("", None, None, None, ""),
    ("LOCKED RATES ($/day) — same in all scenarios", None, None, None, ""),
    ("MR #1 — 1-yr TC (PS Imabari→SUNCOR, 17 Aug 26)", 30000, None, None, "SIN Fixtures Register"),
    ("Aframax — 3-yr TC (Torm Genesis→AET, 31 Aug 26)", 40000, None, None, "SIN Fixtures Register"),
    ("Kamsarmax #1 — 12-mo TC (Intensity, 7 Sep 26)", 22000, None, None, "SIN Fixtures Register"),
]
r = 5
for label, b, c, d, note in rows:
    ws.cell(r, 1, label).font = BOLD if (b in ("Bear",) or "SCENARIO" in str(label) or "LOCKED" in str(label)) else BLACK
    for col, v in ((2, b), (3, c), (4, d)):
        if v is not None:
            cell = ws.cell(r, col, v)
            cell.font = BLUE if isinstance(v, (int, float)) else BOLD
            if isinstance(v, (int, float)) and v > 1000: cell.number_format = M
    if note: ws.cell(r, 5, note).font = Font(name="Arial", size=8, color="808080")
    r += 1
for rr in (13, 14):
    for cc in (2, 3, 4): ws.cell(rr, cc).fill = YELLOW
ws.column_dimensions["E"].width = 70

# ---------------- Acquisition ----------------
ws2 = wb.create_sheet("Acquisition")
ws2.column_dimensions["A"].width = 34
for c in "BCDEFG": ws2.column_dimensions[c].width = 16
ws2["A1"] = "USD 250m Capital Allocation (prices = last-done S&P comparables)"; ws2["A1"].font = H1
hdr = ["Vessel", "Type / dwt", "Built / builder pref", "Price (USD m)", "Pricing comparable (last done)", "Employment"]
for i, h in enumerate(hdr, 1):
    cell = ws2.cell(3, i, h); cell.font = BOLD; cell.fill = GRAYF; cell.border = THIN
fleet = [
    ("MR #1", "MR2 product / 50k", "2016-17, Korea/Japan", 50, "5yo benchmark $50m [47130]; High Discovery 2026-08-11", "1-yr TC $30,000 (locked)"),
    ("MR #2", "MR2 product / 50k", "2016-17, Korea/Japan", 50, "5yo benchmark $50m [47130]", "Spot (scenario)"),
    ("Aframax", "Crude / 110-115k", "2018, Japan (Tsuneishi)", 75, "Southern Reverence / Pusaka Borneo $75.0m (Apr-May 26)", "3-yr TC $40,000 (locked)"),
    ("Kamsarmax #1", "Bulker / 82k", "2019, Japan (Oshima)", 38, "Aquavita Aim $38.0m (10 Aug 26)", "12-mo TC $22,000 (locked)"),
    ("Kamsarmax #2", "Bulker / 82k", "2015, Japan (Tsuneishi)", 32, "Medi Positano $32.0m (10 Aug 26)", "Spot (scenario)"),
]
r = 4
for v in fleet:
    for i, x in enumerate(v, 1):
        cell = ws2.cell(r, i, x)
        cell.font = BLUE if i == 4 else BLACK
        if i == 4: cell.number_format = USD
    r += 1
ws2.cell(r, 1, "Total vessel capex").font = BOLD
ws2.cell(r, 4, "=SUM(D4:D8)").font = BOLD; ws2.cell(r, 4).number_format = USD
ws2.cell(r + 1, 1, "Cash reserve / opportunity fund (buy the collapse)").font = BLACK
ws2.cell(r + 1, 4, "=Assumptions!B5-D9").font = GREEN; ws2.cell(r + 1, 4).number_format = USD
ws2.cell(r + 2, 1, "Total fund").font = BOLD
ws2.cell(r + 2, 4, "=D9+D10").font = BOLD; ws2.cell(r + 2, 4).number_format = USD

# ---------------- Earnings ----------------
ws3 = wb.create_sheet("Earnings")
ws3.column_dimensions["A"].width = 34
for c in "BCDE": ws3.column_dimensions[c].width = 16
ws3["A1"] = "12-Month Earnings Forecast, before OPEX (assignment basis)"; ws3["A1"].font = H1
for i, h in enumerate(["Vessel ($/yr)", "Bear", "Base", "Bull"], 1):
    cell = ws3.cell(3, i, h); cell.font = BOLD; cell.fill = GRAYF; cell.border = THIN
# rates: locked from Assumptions B17/B18/B19 ; spot from B13:D13 (MR), B14:D14 (Kams); days B6
DAYS = "Assumptions!$B$6"
rows3 = [
    ("MR #1 (locked)", ["=Assumptions!$B$17*" + DAYS] * 3),
    ("MR #2 (spot)", [f"=Assumptions!{c}$13*" + DAYS for c in "BCD"]),
    ("Aframax (locked 3-yr)", ["=Assumptions!$B$18*" + DAYS] * 3),
    ("Kamsarmax #1 (locked)", ["=Assumptions!$B$19*" + DAYS] * 3),
    ("Kamsarmax #2 (spot)", [f"=Assumptions!{c}$14*" + DAYS for c in "BCD"]),
]
r = 4
for name, fs in rows3:
    ws3.cell(r, 1, name)
    for i, f in enumerate(fs, 2):
        cell = ws3.cell(r, i, f); cell.font = GREEN; cell.number_format = USD
    r += 1
ws3.cell(r, 1, "Total gross earnings (before OPEX)").font = BOLD
for i, c in enumerate("BCD", 2):
    cell = ws3.cell(r, i, f"=SUM({c}4:{c}8)"); cell.font = BOLD; cell.number_format = USD
ws3.cell(r + 1, 1, "Yield on USD 250m fund (before OPEX)")
for i, c in enumerate("BCD", 2):
    cell = ws3.cell(r + 1, i, f"={c}9/(Assumptions!$B$5*1000000)"); cell.number_format = PCT
ws3.cell(r + 3, 1, "OPEX (5 ships)").font = BOLD
for i, c in enumerate("BCD", 2):
    cell = ws3.cell(r + 3, i, "=(2*Assumptions!$B$8+Assumptions!$B$9+2*Assumptions!$B$10)*" + DAYS)
    cell.font = GREEN; cell.number_format = USD
ws3.cell(r + 4, 1, "Net earnings (after OPEX) — Q&A reference").font = BOLD
for i, c in enumerate("BCD", 2):
    cell = ws3.cell(r + 4, i, f"={c}9-{c}12"); cell.font = BOLD; cell.number_format = USD
ws3.cell(r + 5, 1, "Net yield on fund")
for i, c in enumerate("BCD", 2):
    cell = ws3.cell(r + 5, i, f"={c}13/(Assumptions!$B$5*1000000)"); cell.number_format = PCT
ws3.cell(r + 7, 1, "Note: 60% of operating days fixed to SUNCOR/AET/first-class charterers — bear-case floor.")
ws3.cell(r + 7, 1).font = Font(name="Arial", italic=True, size=9)

# ---------------- Sensitivity ----------------
ws4 = wb.create_sheet("Sensitivity")
ws4.column_dimensions["A"].width = 44
for c in "BC": ws4.column_dimensions[c].width = 18
ws4["A1"] = "Sensitivity — Base scenario, before OPEX"; ws4["A1"].font = H1
ws4["A3"] = "Δ spot rate ($/day, applied to both spot ships)"; ws4["A3"].font = BOLD
ws4["B3"] = "Δ earnings ($/yr)"; ws4["B3"].font = BOLD
ws4["C3"] = "Portfolio total ($/yr)"; ws4["C3"].font = BOLD
deltas = [-5000, -2500, -1000, 0, 1000, 2500, 5000]
r = 4
for d in deltas:
    ws4.cell(r, 1, d).font = BLUE; ws4.cell(r, 1).number_format = '+#,##0;-#,##0;0'
    ws4.cell(r, 2, f"=2*A{r}*Assumptions!$B$6").font = BLACK; ws4.cell(r, 2).number_format = USD
    ws4.cell(r, 3, f"=Earnings!$C$9+B{r}").font = GREEN; ws4.cell(r, 3).number_format = USD
    r += 1
ws4.cell(r + 1, 1, "Rule of thumb: every $1,000/day on the spot legs = $0.7m per year.")
ws4.cell(r + 1, 1).font = Font(name="Arial", italic=True, size=9)

wb.save("MT6102_Earnings_Model.xlsx")
print("saved workbook")
