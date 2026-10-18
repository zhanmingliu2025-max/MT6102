# -*- coding: utf-8 -*-
"""MT6102 chart pack: all data from data/raw/*.csv (Clarksons SIN, 12 Sep 2026)."""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW, OUT = ROOT / "data/raw", ROOT / "charts"
OUT.mkdir(exist_ok=True)

# Validated default palette, light mode, fixed slot order
BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
    "#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#4a3aa7", "#e34948")
GRAY, INK, INK2, GRID = "#b9b8b1", "#1a1a19", "#5f5e58", "#e7e6e2"
import os
DECK = os.environ.get("CHART_STYLE") == "deck"
if DECK:  # template palette for the slide deck (navy, red accent, slate, light blues)
    BLUE, ORANGE, AQUA, YELLOW, MAGENTA, GREEN, VIOLET, RED = (
        "#142B4F", "#C8102E", "#4A6FA5", "#9FB6D9", "#7A8CA8", "#2E5E8C", "#5A6472", "#C8102E")
    GRAY, INK, INK2, GRID = "#C9D6EA", "#1A2433", "#5A6472", "#E3E8EF"
    OUT = ROOT / "charts_deck"; OUT.mkdir(exist_ok=True)

plt.rcParams.update({
    "figure.dpi": 200, "savefig.dpi": 200, "font.size": 10,
    "axes.edgecolor": GRID, "axes.linewidth": 0.8, "axes.grid": True,
    "grid.color": GRID, "grid.linewidth": 0.7, "axes.axisbelow": True,
    "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "axes.labelcolor": INK2, "axes.titlesize": 12,
    "font.family": "DejaVu Sans", "figure.facecolor": "white", "axes.facecolor": "white",
})
if DECK:
    plt.rcParams["font.family"] = "Carlito"

def rd(fid):
    df = pd.read_csv(RAW / f"{fid}_20260912.csv")
    df["Date"] = pd.to_datetime(df.iloc[:, 0])
    return df

def style(ax, ylab=""):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", visible=False)
    if ylab:
        ax.set_ylabel(ylab, fontsize=9)

def finish(fig, name, source):
    fig.text(0.01, 0.012, source, fontsize=7, color=INK2)
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)
    print("saved", name)

SRC = "Source: Clarksons Research, Shipping Intelligence Network"

# ---------- 1. Textbook Peak: Suezmax (12 Sep extract plus 15 Oct re-pull) ----------
a3, a6 = rd("A3"), rd("A6")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1.5, 1]})
h = a3[(a3["Date"] >= "2015-01-01") & (a3["Date"] < "2026-09-01")]
sx = list(h["Date"]) + [pd.Timestamp("2026-09-01"), pd.Timestamp("2026-10-01")]
sy = list(h.iloc[:, 1]) + [120, 130]          # Sep month-end 120, Oct 130 (re-pulled 15 Oct)
nb = a6[a6["Date"] >= "2015-01-01"]
nx = list(nb["Date"]) + [pd.Timestamp("2026-10-01")]
ny = list(nb[a6.columns[3]]) + [90]
ax1.plot(sx, sy, color=BLUE, lw=2, label="5-yr-old secondhand")
ax1.plot(nx, ny, color=ORANGE, lw=2, label="Newbuilding")
ax1.scatter([pd.Timestamp("2026-10-01")], [130], color=BLUE, s=26, zorder=4)
ax1.legend(frameon=False, loc="upper left", fontsize=9)
ax1.annotate("$130m (Oct)", xy=(pd.Timestamp("2026-10-01"), 130), xytext=(-78, 2), textcoords="offset points",
             fontsize=9, fontweight="bold", color=BLUE)
ax1.annotate("$90m", xy=(pd.Timestamp("2026-10-01"), 90), xytext=(5, -4), textcoords="offset points",
             fontsize=9, fontweight="bold", color=ORANGE, annotation_clip=False)
ax1.set_xlim(right=pd.Timestamp("2028-01-01")); ax1.set_ylim(35, 140)
ax1.set_title("Suezmax: secondhand 1.44x newbuild in Oct (1.23x on 12 Sep)", loc="left", fontweight="bold")
style(ax1, "$ million")
cats = ["Spot earnings", "1-yr TC", "3-yr TC"]
sep = [335.9, 90.3, 46.3]; octv = [718.2, 140.3, 64.4]
x = np.arange(3); w = 0.36
ax2.bar(x - w / 2, sep, w, color=GRAY, label="September", zorder=3)
ax2.bar(x + w / 2, octv, w, color=BLUE, label="October", zorder=3)
for i in range(3):
    ax2.text(x[i] - w / 2, sep[i] + 12, f"{sep[i]:.0f}k", ha="center", fontsize=8.5, color=INK2)
    ax2.text(x[i] + w / 2, octv[i] + 12, f"{octv[i]:.0f}k", ha="center", fontsize=8.5, fontweight="bold")
ax2.set_xticks(x, cats)
ax2.legend(frameon=False, loc="upper right", fontsize=9)
ax2.set_title("Backwardation steeper in October:\nspot far above 1-yr and 3-yr rates", loc="left", fontweight="bold")
style(ax2, "$'000 per day"); ax2.set_ylim(0, 800)
fig.suptitle("Textbook Peak Signals: Suezmax, September vs October", x=0.01, y=1.03, ha="left", fontsize=14, fontweight="bold")
finish(fig, "01_peak_signals_suezmax.png", SRC + " [87302, 53070, 48989, 49108, 531088]. History to Aug from 12 Sep extract; Sep (month-end) and Oct re-pulled 15 Oct 2026. Earnings: weeks of 11 Sep and 9 Oct.")

# ---------- 2. Supply shock: earnings vs volumes ----------
c3, f1 = rd("C3"), rd("F1")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1.6, 1]})
m = c3["Date"] >= "2023-01-01"
ax1.plot(c3.loc[m, "Date"], c3.loc[m, c3.columns[2]] / 1000, color=BLUE, lw=2)
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax1.set_title("Weighted crude tanker earnings ($'000/day)", loc="left", fontweight="bold")
ax1.annotate("Hormuz transits\ncollapse (Mar 26)", xy=(pd.Timestamp("2026-03-06"), 120),
             xytext=(-110, 60), textcoords="offset points", fontsize=8, color=INK2,
             arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax1.annotate("Red Sea attacks\nresume (Jul 26)", xy=(pd.Timestamp("2026-07-24"), 230),
             xytext=(-120, 30), textcoords="offset points", fontsize=8, color=INK2,
             arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax1.annotate("$329k/day", xy=(c3["Date"].iloc[-1], 328.6), xytext=(-70, -2),
             textcoords="offset points", fontsize=9, fontweight="bold", color=BLUE)
style(ax1)
yrs = f1[f1["Date"] >= "2023-01-01"]
yoy = yrs.iloc[:, 1].pct_change() * 100
lbl = [str(d.year) + ("F" if d.year >= 2027 else "") for d in yrs["Date"]]
colors = [BLUE if v >= 0 else ORANGE for v in yoy.fillna(0)]
ax2.bar(lbl[1:], yoy.iloc[1:], color=colors[1:], width=0.6, zorder=3)
for i, v in enumerate(yoy.iloc[1:]):
    ax2.text(i, v + 0.35 if v >= 0 else v - 1.0, f"{v:+.1f}%", ha="center", fontsize=9, fontweight="bold")
ax2.axhline(0, color=GRAY, lw=0.8)
ax2.set_ylim(-9.6, 8.8)
ax2.set_title("Seaborne crude volumes (% y/y)", loc="left", fontweight="bold")
style(ax2)
fig.suptitle("A Supply Shock, Not a Demand Boom: volumes fell 7.3% while earnings quintupled",
             x=0.01, y=1.03, ha="left", fontsize=14, fontweight="bold")
finish(fig, "02_supply_shock.png", SRC + " [546177, 98801]. Extracted 12 Sep 2026.")

# ---------- 3. Orderbook % fleet by segment ----------
segs = [("Crude Aframax", 8.4, True), ("Handymax/Ultramax", 13.6, True), ("Panamax/Kamsarmax", 13.7, True),
        ("All Bulkers", 14.5, False), ("MR Product (40-55k)", 18.0, True), ("Product Tankers 10k+", 21.5, False),
        ("All Crude Tankers", 28.1, False), ("Suezmax", 29.1, False), ("LNG Carriers", 36.9, False),
        ("Containerships", 41.9, False)]
segs = segs[::-1]
fig, ax = plt.subplots(figsize=(9, 4.8))
cols = [BLUE if inport else GRAY for _, _, inport in segs]
ax.barh([s[0] for s in segs], [s[1] for s in segs], color=cols, height=0.62, zorder=3)
for i, (_, v, _) in enumerate(segs):
    ax.text(v + 0.5, i, f"{v:.1f}%", va="center", fontsize=9, fontweight="bold")
ax.set_title("Orderbook as % of Fleet, Sep 2026: our segments (blue) carry the least supply risk",
             loc="left", fontweight="bold", fontsize=12)
style(ax)
ax.grid(axis="y", visible=False)
ax.grid(axis="x", visible=True)
ax.set_xlim(0, 47)
finish(fig, "03_orderbook_by_segment.png", SRC + " [534436-534665 series; MR = L4 340/1,906 ships]. Extracted 12 Sep 2026.")

# ---------- 4. Fleet growth with forecast ----------
d6 = rd("D6")
fig, ax = plt.subplots(figsize=(9, 4.4))
m = d6["Date"] >= "2015-01-01"
for col, c, lab in [(1, BLUE, "Crude tankers"), (2, ORANGE, "Product tankers"), (3, AQUA, "Bulkcarriers")]:
    ax.plot(d6.loc[m, "Date"], d6.loc[m].iloc[:, col], color=c, lw=2, label=lab)
ax.axvspan(pd.Timestamp("2026-06-01"), pd.Timestamp("2028-06-01"), color=GRID, alpha=0.5, zorder=0)
ax.text(pd.Timestamp("2027-05-01"), ax.get_ylim()[1] * 0.93, "Forecast", fontsize=9, color=INK2, ha="center")
ax.annotate("7.7%", xy=(pd.Timestamp("2028-01-01"), 7.717), xytext=(-46, -6), textcoords="offset points",
            fontsize=10, fontweight="bold", color=BLUE)
ax.set_ylim(top=8.6)
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.axhline(0, color=GRAY, lw=0.8)
ax.set_title("Crude Tanker Fleet Growth Accelerates into 2028: the delivery wave meets any ceasefire",
             loc="left", fontweight="bold", fontsize=12)
style(ax, "% per year")
finish(fig, "04_fleet_growth.png", SRC + " [534497, 534499, 534495]. Extracted 12 Sep 2026.")

# ---------- 5. Dry bulk recovery (12 Sep extract plus 15 Oct re-pull) ----------
c1 = rd("C1")
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), gridspec_kw={"width_ratios": [1.35, 1]})
c = c1[c1["Date"] >= "2024-01-01"]
ax1.plot(c["Date"], c.iloc[:, 1], color=BLUE, lw=1.5, label="BDI daily, to 10 Sep")
ox = [c["Date"].iloc[-1], pd.Timestamp("2026-10-06"), pd.Timestamp("2026-10-13")]
oy = [c.iloc[-1, 1], 3002, 2801]
ax1.plot(ox, oy, color=ORANGE, lw=1.4, ls=":", label="October readings")
ax1.scatter(ox[1:], oy[1:], color=ORANGE, s=24, zorder=4)
ax1.annotate("3,521\n10 Sep", xy=(ox[0], 3521), xytext=(-62, 4), textcoords="offset points", fontsize=8.5, fontweight="bold", color=BLUE)
ax1.annotate("2,801\n13 Oct", xy=(ox[2], 2801), xytext=(6, -22), textcoords="offset points", fontsize=8.5, fontweight="bold", color=ORANGE, annotation_clip=False)
ax1.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 7]))
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
ax1.set_xlim(pd.Timestamp("2024-01-01"), pd.Timestamp("2026-12-15")); ax1.set_ylim(500, 4000)
ax1.legend(frameon=False, loc="upper left", fontsize=9)
ax1.set_title("Baltic Dry Index: strong, but 20% off the September high", loc="left", fontweight="bold")
style(ax1, "Index points")
segs = ["MR", "Kamsarmax", "Aframax", "Suezmax"]
sep = [50 / 52, 42 / 38.5, 85 / 75.5, 111 / 90]; octv = [52 / 52.5, 42 / 38.5, 85 / 76, 130 / 90]
x = np.arange(4); w = 0.36
ax2.bar(x - w / 2, sep, w, color=GRAY, label="September", zorder=3)
ax2.bar(x + w / 2, octv, w, color=BLUE, label="October", zorder=3)
for i in range(4):
    ax2.text(x[i] - w / 2, sep[i] + 0.012, f"{sep[i]:.2f}", ha="center", fontsize=8.5, color=INK2)
    ax2.text(x[i] + w / 2, octv[i] + 0.012, f"{octv[i]:.2f}", ha="center", fontsize=8.5, fontweight="bold")
ax2.axhline(1.0, color=INK2, lw=1.1, ls="--", label="Replacement cost = 1.0")
ax2.set_xticks(x, segs); ax2.set_ylim(0.8, 1.55)
ax2.legend(frameon=False, loc="upper left", fontsize=9)
ax2.set_title("5-yr-old price ÷ newbuild price", loc="left", fontweight="bold")
style(ax2, "ratio")
fig.suptitle("Buy Value: Dry Bulk Recovering, MR at Replacement Cost (September vs October)", x=0.01, y=1.03, ha="left", fontsize=14, fontweight="bold")
finish(fig, "05_drybulk_recovery.png", SRC + " [17259; 47130/71267, 540721/70747, 38981/35905, 87302/53070]. BDI daily to 10 Sep from 12 Sep extract; 6 and 13 Oct readings and October prices re-pulled 15 Oct 2026.")

# ---------- 6. Guinea bauxite ----------
f5 = rd("F5")
gm = f5[f5.iloc[:, 2].notna()].copy()
gm = gm[gm["Date"] >= "2021-01-01"]
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.bar(gm["Date"], gm.iloc[:, 2], width=24, color="#9ec5f4", zorder=3)
roll = gm.iloc[:, 2].rolling(12).mean()
ax.plot(gm["Date"], roll, color=BLUE, lw=2.2, label="12-month average")
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.set_title("Guinea Bauxite Exports (Mt/month): +29% y/y Jan-Apr 2026, plus Simandou iron ore ramp-up",
             loc="left", fontweight="bold", fontsize=12)
style(ax, "Mt per month")
finish(fig, "06_bauxite_guinea.png", SRC + " [557125]; Clarksons SIN News Article 224049. Extracted 12 Sep 2026. Sep-26 partial month.")

# ---------- 7. Price vs replacement cost ----------
ratios = [("MR 51k", 50 / 52), ("Kamsarmax 82k", 42 / 38.5), ("Ultramax 63.5k", 39 / 35.5),
          ("Aframax 115k", 85 / 75.5), ("Suezmax 160k", 111 / 90)]
fig, ax = plt.subplots(figsize=(9, 4.2))
cols = [BLUE if r < 1 else ("#86b6ef" if r < 1.15 else ORANGE) for _, r in ratios]
ax.bar([n for n, _ in ratios], [r for _, r in ratios], color=cols, width=0.58, zorder=3)
ax.axhline(1.0, color=INK2, lw=1.2, ls="--")
ax.text(-0.45, 1.012, "Replacement cost (newbuild parity)", fontsize=8, color=INK2, ha="left")
for i, (_, r) in enumerate(ratios):
    ax.text(i, r + 0.015, f"{r:.2f}x", ha="center", fontsize=10, fontweight="bold")
ax.set_ylim(0.8, 1.32)
ax.set_title("5-yr-old Price ÷ Newbuild Price, Sep 2026: MR is the only segment at or below replacement cost (0.99x in Oct)",
             loc="left", fontweight="bold", fontsize=12)
style(ax)
ax.grid(axis="x", visible=False)
finish(fig, "07_replacement_cost.png", SRC + " [A1-A6 series: 47130/542021/540721/38981/87302 vs 71267/23357/70747/35905/53070]. Extracted 12 Sep 2026.")

# ---------- 8. Average haul divergence (indexed) ----------
f1x = rd("F1")
m = (f1x["Date"] >= "2019-01-01") & (f1x["Date"] <= "2027-12-31")
sub = f1x.loc[m].copy()
base_t, base_tm = sub.iloc[0, 1], sub.iloc[0, 2]
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.plot(sub["Date"], sub.iloc[:, 1] / base_t * 100, color=ORANGE, lw=2, label="Tonnes")
ax.plot(sub["Date"], sub.iloc[:, 2] / base_tm * 100, color=BLUE, lw=2, label="Tonne-miles")
ax.axvspan(pd.Timestamp("2026-06-01"), pd.Timestamp("2027-06-01"), color=GRID, alpha=0.5, zorder=0)
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.annotate("2026: volumes -7.3%,\naverage haul +3.3% to 5,643 miles", xy=(pd.Timestamp("2026-01-01"), 96),
            xytext=(-160, -42), textcoords="offset points", fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="-", color=INK2, lw=0.8))
ax.set_title("Crude Trade, Indexed (2019 = 100): distance, not volume, is carrying demand",
             loc="left", fontweight="bold", fontsize=12)
style(ax, "Index, 2019 = 100")
finish(fig, "08_average_haul.png", SRC + " [98801, 534402]; haul = tonne-miles / tonnes (Week 5 method). Extracted 12 Sep 2026.")

# ---------- 9. Chokepoints ----------
l6 = rd("L6")
m = l6["Date"] >= "2025-06-01"
sub = l6.loc[m]
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.plot(sub["Date"], sub.iloc[:, 3], color=BLUE, lw=2, label="Gulf of Aden: all deep sea cargo")
ax.plot(sub["Date"], sub.iloc[:, 4], color=ORANGE, lw=2, label="Strait of Hormuz: crude tankers")
ax.legend(frameon=False, loc="lower left", fontsize=9)
ax.text(pd.Timestamp("2026-03-25"), 40, "2-7 transits/week\n(near-closure)",
        fontsize=9, fontweight="bold", color=ORANGE)
ax.set_title("Chokepoint Transits per Week: the disruption premium, quantified",
             loc="left", fontweight="bold", fontsize=12)
style(ax, "Vessels per week")
finish(fig, "09_chokepoints.png", SRC + " [551286, 12792857]. Extracted 12 Sep 2026.")

# ---------- 10. Sanctioned fleet ----------
l11 = rd("L11")
m = l11["Date"] >= "2022-01-01"
sub = l11.loc[m]
fig, ax = plt.subplots(figsize=(9, 4.2))
ax.plot(sub["Date"], sub.iloc[:, 2] / 1e6, color=BLUE, lw=2, label="All sanctioned vessels")
ax.plot(sub["Date"], sub.iloc[:, 4] / 1e6, color=ORANGE, lw=2, label="Sanctioned crude tankers")
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.annotate("137m dwt", xy=(sub["Date"].iloc[-1], 137), xytext=(-58, 6), textcoords="offset points",
            fontsize=9, fontweight="bold", color=BLUE)
ax.text(pd.Timestamp("2025-05-01"), 44, "97m dwt = 20% of\ncrude tanker fleet",
        fontsize=9, fontweight="bold", color=ORANGE)
ax.set_title("Sanctioned Fleet (million dwt): effective supply withdrawn, and reversible",
             loc="left", fontweight="bold", fontsize=12)
style(ax, "Million dwt")
finish(fig, "10_sanctioned_fleet.png", SRC + " [12116108, 12110871]; SIN News Article 228241. Extracted 12 Sep 2026.")

# ---------- 11. Scenario earnings ----------
import numpy as np
sc = ["Bear: spot legs at 2025 average", "Base: last-done fixtures", "Bull: spot of 9 Oct 2026 holds"]
gross = [44.7, 49.7, 59.2]
net = [31.9, 36.9, 46.4]
x = np.arange(3)
fig, ax = plt.subplots(figsize=(9, 4.4))
ax.bar(x - 0.18, gross, 0.32, color=BLUE, label="Before OPEX (assignment basis)", zorder=3)
ax.bar(x + 0.18, net, 0.32, color="#9ec5f4", label="After OPEX (Q&A reference)", zorder=3)
for i in range(3):
    ax.text(x[i] - 0.18, gross[i] + 0.8, f"${gross[i]:.1f}m\n{gross[i]/2.5:.1f}%", ha="center", fontsize=9, fontweight="bold")
    ax.text(x[i] + 0.18, net[i] + 0.8, f"${net[i]:.1f}m", ha="center", fontsize=9, color=INK2)
ax.set_xticks(x, sc, fontsize=9)
ax.legend(frameon=False, loc="upper left", fontsize=9)
ax.set_ylim(0, 70)
ax.set_title("12-Month Earnings on USD 250m: 60% of days fixed to first-class charterers caps the downside at 17.9%",
             loc="left", fontweight="bold", fontsize=11.5)
style(ax, "$ million")
ax.grid(axis="x", visible=False)
finish(fig, "11_scenarios.png", "Basis: last-done fixtures (SIN Fixtures Register, Aug-Sep 2026); Bull = SIN earnings series week of 9 Oct 2026; OPEX = Clarksons series [540687/540689/540683]; 350 operating days/ship.")

print("ALL CHARTS DONE")
