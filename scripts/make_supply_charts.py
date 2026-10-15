# -*- coding: utf-8 -*-
"""Supply-side charts 12-14 from datasets L13-L16 (Clarksons SIN, extracted 10 Oct 2026)."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]; RAW = ROOT / "data/raw"; OUT = ROOT / "charts"
BLUE, ORANGE, AQUA, YELLOW, GRAY, INK, INK2, GRID = "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#b9b8b1", "#1a1a19", "#5f5e58", "#e7e6e2"
plt.rcParams.update({"figure.dpi": 200, "savefig.dpi": 200, "font.size": 10, "axes.edgecolor": GRID, "axes.linewidth": 0.8,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.7, "axes.axisbelow": True, "xtick.color": INK2, "ytick.color": INK2,
    "text.color": INK, "axes.labelcolor": INK2, "font.family": "DejaVu Sans", "figure.facecolor": "white", "axes.facecolor": "white"})
def rd(name):
    with open(RAW / name, encoding="utf-8-sig") as f: return list(csv.reader(f))
def style(ax, ylab=""):
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.grid(axis="x", visible=False)
    if ylab: ax.set_ylabel(ylab, fontsize=9)
def finish(fig, name, src):
    fig.text(0.01, 0.012, src, fontsize=7, color=INK2); fig.savefig(OUT / name, bbox_inches="tight"); plt.close(fig); print("saved", name)
SRC = "Source: Clarksons Research, Shipping Intelligence Network"

# ---- 12. deliveries vs demolition 2021-2025 (ships) ----
dl, dm = rd("L13_deliveries_20261010.csv"), rd("L14_demolition_20261010.csv")
def yr(rows, y): return next(r for r in rows if r[0].startswith(str(y)))
def tot(rows, col, years=range(2021, 2026)): return sum(float(yr(rows, y)[col] or 0) for y in years)
# columns: 1 Panamax No, 3 MR No, 5 Aframax tanker No (incl LR2), 7 LR2 No
segs = ["Kamsarmax / Panamax", "MR 40-55k dwt", "Aframax crude", "LR2"]
deliv = [tot(dl, 1), tot(dl, 3), tot(dl, 5) - tot(dl, 7), tot(dl, 7)]
demo = [tot(dm, 1), tot(dm, 3), tot(dm, 5) - tot(dm, 7), tot(dm, 7)]
x = np.arange(4); fig, ax = plt.subplots(figsize=(9, 4.4))
ax.bar(x - 0.19, deliv, 0.36, color=BLUE, label="Delivered 2021-2025", zorder=3)
ax.bar(x + 0.19, demo, 0.36, color=GRAY, label="Scrapped 2021-2025", zorder=3)
for i in range(4):
    ax.text(x[i] - 0.19, deliv[i] + 8, f"{deliv[i]:.0f}", ha="center", fontsize=9, fontweight="bold")
    ax.text(x[i] + 0.19, demo[i] + 8, f"{demo[i]:.0f}", ha="center", fontsize=9, color=INK2)
ax.set_xticks(x, segs, fontsize=9); ax.legend(frameon=False, loc="upper right", fontsize=9)
ax.set_title("Ships In vs Ships Out, 2021-2025: scrapping has almost stopped, except crude Aframax", loc="left", fontweight="bold", fontsize=12)
style(ax, "Number of ships"); ax.set_ylim(0, max(deliv) * 1.18)
finish(fig, "12_deliveries_vs_demolition.png", SRC + " [L13: 30301/540953/29984/39696; L14: 30291/540965/29967/39683]. Crude Aframax = Aframax tanker minus LR2. Extracted 10 Oct 2026.")

# ---- 13. orderbook delivery schedule 2026-2030 ----
sch = rd("L15_delivery_schedule_20261010.csv")
def ob(seg_prefix):
    d = {}
    for r in sch[1:]:
        if r[0].startswith(seg_prefix) and r[4]: d[int(r[1])] = int(r[4])
    return d
series = [("Kamsarmax", ob("Panamax/Kamsarmax"), BLUE), ("MR / Handy 25-55k", ob("MR/Handy"), ORANGE), ("Aframax crude", ob("Aframax Crude"), AQUA), ("LR2", ob("LR2"), YELLOW)]
years = [2026, 2027, 2028, 2029, 2030]; x = np.arange(len(years)); w = 0.2
fig, ax = plt.subplots(figsize=(9, 4.4))
for i, (lab, d, c) in enumerate(series):
    vals = [d.get(y, 0) for y in years]
    ax.bar(x + (i - 1.5) * w, vals, w, color=c, label=lab, zorder=3)
    for xi, v in zip(x, vals):
        if v >= 40: ax.text(xi + (i - 1.5) * w, v + 3, str(v), ha="center", fontsize=7.5, color=INK2)
ax.set_xticks(x, ["2026 (Oct-Dec)", "2027", "2028", "2029", "2030"], fontsize=9)
ax.legend(frameon=False, loc="upper right", fontsize=9, ncol=2)
ax.set_title("Orderbook by Scheduled Delivery Year: the wave peaks in 2027-2028", loc="left", fontweight="bold", fontsize=12)
style(ax, "Ships on order"); ax.set_ylim(0, 200)
finish(fig, "13_delivery_schedule.png", SRC + " Orderbook > Delivery Schedule [L15]. By number of ships; MR includes 1 unit due 2031. Extracted 10 Oct 2026.")

# ---- 14. replacement test: orderbook vs ships aged 20+ ----
age = rd("L16_age_profile_20261010.csv")
fleet = {r[0]: (int(r[1]), int(r[3])) for r in age[1:]}  # total, 20y+
obtot = {"Kamsarmax": sum(ob("Panamax/Kamsarmax").values()), "MR / Handy 25-55k": sum(ob("MR/Handy").values()) + 1,  # +1 unit due 2031 (L15 note)
         "Aframax crude": sum(ob("Aframax Crude").values()), "LR2": sum(ob("LR2").values())}
old = {"Kamsarmax": fleet["Panamax/Kamsarmax Bulker(70-100k)"][1], "MR / Handy 25-55k": fleet["MR/Handy Products Tanker(25-55k)"][1],
       "Aframax crude": fleet["Aframax Crude Tanker(85-125k)"][1], "LR2": fleet["LR2 Products Tanker(85-125k)"][1]}
labs = list(obtot); y = np.arange(len(labs))[::-1]
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.barh(y + 0.19, [obtot[k] for k in labs], 0.36, color=BLUE, label="Ships on order", zorder=3)
ax.barh(y - 0.19, [old[k] for k in labs], 0.36, color=GRAY, label="Ships aged 20+ (built 2006 or earlier)", zorder=3)
for yi, k in zip(y, labs):
    ax.text(obtot[k] + 8, yi + 0.19, f"{obtot[k]}", va="center", fontsize=9, fontweight="bold")
    ax.text(old[k] + 8, yi - 0.19, f"{old[k]}", va="center", fontsize=9, color=INK2)
    ax.text(max(obtot[k], old[k]) + 95, yi, f"cover {obtot[k]/old[k]:.2f}x", va="center", fontsize=9, color=INK)
ax.set_yticks(y, labs, fontsize=9); ax.legend(frameon=False, loc="lower right", fontsize=9)
ax.set_title("Replacement Test: orders vs ships old enough to scrap", loc="left", fontweight="bold", fontsize=12)
style(ax); ax.grid(axis="y", visible=False); ax.grid(axis="x", visible=True); ax.set_xlim(0, 820)
finish(fig, "14_replacement_test.png", SRC + " Orderbook Delivery Schedule [L15] and Fleet Register age profile [L16]. Cover = orderbook / ships aged 20+. Extracted 10 Oct 2026.")
print("deliv", deliv, "demo", demo, "orderbook", obtot, "old", old)
