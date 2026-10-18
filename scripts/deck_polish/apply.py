# Applies the 18 Oct 2026 polish to slides 1 to 9 of the group's working deck (XML edits only; slides 10 to 35 untouched).
# Usage: python3 apply.py <unpacked pptx dir> <dir holding lib.py> <notes_slides_1_9.json>
import sys, json
sys.path.insert(0, sys.argv[2])
from lib import *
D=sys.argv[1]  # unpacked ppt dir
S=lambda n: Slide(f'{D}/ppt/slides/slide{n}.xml')
HEAD=dict(sz=1800, font='Cambria', color='C8102E', base_b=True)
BODY=dict(sz=1200, color='1A2433')
TITLE=dict()  # keep title style
out={}

# ---------- slide 1
s=S(1)
sub=s.edit('Skip the peak, buy value, lock income: five secondhand ships, three fixed charters, two spot ships and a cash reserve',
           'Skip the peak, buy value, lock income: five secondhand ships, three fixed, two spot, USD 5m cash')
subsp=s.shape_of(sub); s.set_xfrm(subsp, h=0.35)
s.clone_sp(subsp,'Result line','Base case **19.9%** on USD 250m over 12 months, before OPEX; bear case **17.9%**',
           x=0.90,y=4.20,w=11.0,h=0.35, sz=1500, color='C9D6EA', bold_color='FFFFFF')
s.edit('Every purchase price, charter rate and freight rate in this deck is the last transacted sale or fixture on the Clarksons Shipping Intelligence Network (SIN). Price series extracted 12 Sep 2026 and re-checked 15 Oct 2026; supply data extracted 10 Oct 2026.',
       'Purchase prices and base-case charter and freight rates are last transacted sales and fixtures on the Clarksons Shipping Intelligence Network (SIN), except the MR price: no recent 5-year-old MR sale had a disclosed price, so it is the SIN assessment. Price series extracted 12 Sep 2026 and re-checked 15 Oct 2026; supply data extracted 10 Oct 2026.')
s.save(); out[1]=s.log

# ---------- slide 2
s=S(2)
s.edit('How the proposal is built','Seven parts, in the order of the brief')
descs=['How the USD 250m is allocated, why each line is sized that way, and which data supports it. Five ships, four trades, one cash line.',
 'Every purchase price, charter rate and freight rate is a last transacted sale or fixture on Clarksons SIN.',
 'Three demand engines, deliveries against demolition, the 2027 to 2028 delivery wave, and a replacement test against the ageing fleet.',
 'Peak signals in large crude tankers, recovery in dry bulk, what changed since 12 September, and our freight-rate call.',
 'One formula, the base case by vessel, three scenarios with an expected value, and sensitivity.',
 'Five shocks, charter expiry timed against the delivery wave, and the triggers we watch.',
 'The same three questions in the same order: how we allocate, why, and what data says so.']
newd={1:'Purchase prices, charter rates and freight rates from last-done SIN sales and fixtures; the MR price from the SIN assessment.',
      3:'Suezmax peak signals, dry bulk off the high, MR at replacement cost, changes since 12 September, our rate call.'}
for k,d in enumerate(descs):
    s.edit(d, newd.get(k), sz=1250, color='1A2433')
tags={'The decision':'Brief 1 and 2','Pricing basis':'Brief 3','Demand and supply':'Brief 4','Market data and news':'Brief 4','Earnings':'Brief 5','Shocks and mitigation':'Brief 6'}
for h,tag in tags.items():
    p=s.find(h); sp=s.shape_of(p)
    y=int(sp.find('.//a:off',NS).get('y'))/E
    s.clone_sp(sp,'Brief tag',tag,x=10.75,y=y,w=2.00,h=0.36,algn='r',sz=1100,color='5A6472',base_b=False)
s.save(); out[2]=s.log

# ---------- slide 3
s=S(3)
s.edit('Where the USD 250m goes, why, and the data behind it','USD 250m: 70% tankers, 28% dry bulk, 2% cash, 60% of days fixed')
for c in range(4):
    for p in s.cell_paras(0,c): set_para(p, sz=1050)
for r in range(1,5):
    ps=s.cell_paras(r,0)
    if len(ps)>1: set_para(ps[1], sz=1050, color='1A2433', base_b=False)
s.edit('Closest to replacement cost of the five segments: 5-year-old $50m against newbuild $52m in September (0.96), $52m against $52.5m in October (0.99). Products trade +6.3% in 2027F. Spot earnings $53,741/day in the week of 9 Oct sit above the 1-year TC, so one ship stays open.',
 'Closest to replacement cost: 5-yr-old $50m vs newbuild $52m in Sep (**0.96x**), **0.99x** in Oct. Products trade **+6.3%** in 2027F. Spot sits above the 1-yr rate, which already prices the expected fall, so the open ship costs little, keeps the upside and fixes if spot stays below **$20,000** for 8 weeks.', sz=1100)
s.edit('Series 47130 / 71267 (prices), 98802 / 534403 (products trade), 543759 (MR Eco earnings). Fixtures PS Imabari to SUNCOR $30,000 and Challenge Pollux to ExxonMobil $27,000, 17 Aug 2026.',
 'Series 47130 / 71267 (prices), 98802 / 534403 (products trade), 541552 (1-yr TC), 543759 (MR Eco spot). Fixtures PS Imabari to SUNCOR $30,000 and Challenge Pollux to ExxonMobil $27,000, 17 Aug 2026.', sz=1050)
s.edit('Lowest orderbook of any segment: 8.4% of dwt, 62 ships on order against 223 over 20 years old. A 3-year fixture at $40,000 exists (Torm Genesis to AET, 31 Aug), so income is certain through the 2027 to 2028 delivery wave. No Suezmax: 5-year-old $130m against newbuild $90m in October, 1-year TC $140,250 against 3-year $64,375.',
 'Lowest orderbook of our five segments: crude Aframax **8.4%** of dwt, **62** ships on order vs **223** over 20 years old. A 3-yr TC at the last-done **$40,000** (Torm Genesis to AET, 31 Aug) keeps income contracted through the 2027 to 2028 wave. No Suezmax: **1.44x** newbuild vs **1.12x** for Aframax.', sz=1100)
s.edit('Series 534456 (orderbook), 531168 (earnings), 87302 / 53070 and 48989 / 49108 (Suezmax signals), datasets L13 to L16. Sales Southern Reverence and Pusaka Borneo at $75.0m.',
 'Series 534456 (orderbook), 531168 (earnings), 38981 / 35905 and 87302 / 53070 (prices), 48989 / 49108 (Suezmax TC), datasets L13 to L16. Sales Southern Reverence and Pusaka Borneo at $75.0m.', sz=1050)
s.edit('Recovery, not peak: BDI 3,521 on 10 Sep and 2,801 on 13 Oct; 5-year-old price 9% above newbuild, against 23% to 44% for Suezmax. Orderbook 13.5%; 2025 deliveries 143 against demolition 14; 2027 deliveries 171 against 618 ships over 20 years old. Guinea bauxite +29% y/y, Simandou iron ore ramping up.',
 'Strong but off the high: BDI **2,801** on 13 Oct, **20%** below 10 Sep; 5-yr-old **9%** above newbuild vs **44%** for Suezmax. Orderbook **13.5%** of ships; 2027 deliveries **171** vs **618** over 20 years old. Guinea bauxite **+29%** y/y (Jan to Apr).', sz=1100)
s.edit('Series 17259 (BDI), 534450, 540721, 557125, 534400 / 547349, 533288. Sales Aquavita Aim $38.0m and Medi Positano $32.0m. Fixtures Intensity to CNR $22,000, XH Hope to Cargill $23,000, coal DBCT to Vizag $25.60/t (SAIL).',
 'Series 17259 (BDI), 540721 / 70747 (prices), 557125, 534400 / 547349, 533288; datasets L15, L16; news #224049. Sales Aquavita Aim $38.0m and Medi Positano $32.0m. Fixtures Intensity $22,000 (charterer not reported), XH Hope to Cargill $23,000.', sz=1050)
s.edit('Counter-cyclical fund and working capital','Working capital and counter-cyclical fund')
s.edit('Dry powder for when tanker secondhand prices fall back below newbuild. Equals five months of fleet OPEX ($36,560/day). Fixed charters add about $2.7m a month.',
 'Working capital first: nearly five months of fleet OPEX (**$36,560/day**). Fixed hire adds about **$2.7m** a month, which builds a fund to buy tankers once secondhand prices fall below newbuild.', sz=1100)
s.edit('OPEX series 540687 / 540689 / 540683; scrap price series 542047.','OPEX series 540687 / 540689 / 540683; fixed hire from the Part 2 fixtures.', sz=1050)
s.edit('Tankers 70%, dry bulk 28%, cash 2%. 60% of ship-days fixed, 65% of base income. Earnings before OPEX: Bear 17.9%, Base 19.9%, Bull 23.7%.',
 'Tankers **70%**, dry bulk **28%**, cash **2%**. Three of five ships fixed (**60%** of ship-days): the fewest that keep returns above **15%** before OPEX in a stress test on spot data since 2010. Bear **17.9%**, base **19.9%**, bull **23.7%**, expected **20.0%**.', sz=1100)
s.edit('MT6102_Earnings_Model.xlsx','MT6102_Earnings_Model.xlsx; stress test on SIN weekly spot earnings 545055 / 533288, 2010 to 2026', sz=1050)
s.save(); out[3]=s.log

# ---------- slide 4
s=S(4)
s.edit('Capital allocation: five ships and one cash line, exactly USD 250m','Capital allocation: USD 245m in five ships, USD 5m in cash')
for r in (1,2):
    set_para(s.cell_paras(r,1)[0], '50k dwt, 5-yr-old Eco, Korea or Japan')
s.edit('Southern Reverence and Pusaka Borneo, both $75.0m (May and Apr 2026)','Southern Reverence, Pusaka Borneo: $75.0m each (May, Apr 2026)')
shipfill=s.cell(1,0).find(q('tcPr')).find(q('solidFill')).find(q('srgbClr')).get('val')
for c in range(5): set_cell_fill(s.cell(7,c), shipfill)
set_para(s.cell_paras(7,0)[0], color='1A2433', base_b=False)
set_para(s.cell_paras(7,1)[0], 'Working capital and reserve', color='1A2433', base_b=False)
set_para(s.cell_paras(7,4)[0], 'Reserve for tankers below newbuild', color='1A2433', base_b=False)
for r in range(1,6): set_para(s.cell_paras(r,2)[0], color='C8102E', base_b=True)
for r,txt in ((1,'1-year TC at **$30,000/day**'),(3,'3-year TC at **$40,000/day**'),(4,'12-month TC at **$22,000/day**')):
    set_para(s.cell_paras(r,4)[0], txt, color='1A2433')
s.edit('Financing in one line','All equity: no debt to service', **HEAD)
s.edit('The USD 250m is treated as equity, so there is no interest and no repayment schedule to meet in a weak year. Banks lend 60 to 80 percent against 5-year-old tonnage if the board later wants leverage; the Aframax with its 3-year charter is the natural first asset to mortgage or to sell and lease back.',
 'No interest and no repayment schedule in a weak year. Banks lend **60 to 80%** against 5-yr-old tonnage if the board later wants leverage; the Aframax on its **3-year** charter is the first asset to mortgage or to sell and lease back.', **BODY)
s.edit('All five ships are Japan or Korea built','Japan or Korea built: no Section 301 fees', **HEAD)
s.edit('They sit outside the US Section 301 port-fee regime whose suspension expires around 10 November 2026. The market already prices this: a 2015 Japan-built Kamsarmax sold for $32.0m against $29.25m for a China-built sister (Presinge), a $2.75m premium for the same insurance.',
 'With a non-Chinese owner they fall outside the US Section 301 port fees, whose suspension ends around **10 Nov 2026**; this matters for Kamsarmax #2 in US Gulf grain. A Japan-built Kamsarmax sold **$2.75m** above its China-built sister, a gap that includes port-fee risk.', **BODY)
s.save(); out[4]=s.log

# ---------- slide 5
s=S(5)
s.edit('Buy secondhand, not charter-in, not newbuild','Buy secondhand: charter-in earns little, newbuild arrives too late')
s.edit('Charter-in rejected','Charter-in: a thin spread, no asset', **HEAD)
s.edit('Period rates sit at cycle highs, so chartering in locks a cost at the top. A chartered-in MR costs $30,000/day and earns $27,000 in the base case and $22,950 in the bear case. Only the bull case pays, and there is no asset to resell.',
 'A charterer keeps only the spread over hire. Kamsarmax: hire **$22,000** vs **$23,000** base, **+$0.35m** a year, or a **$3.2m** loss at 2025 earnings ($12,880). MR: hire **$30,000** vs **$27,000** base, a **$1.05m** loss. Chartering in also leaves most of the $250m idle and no asset at the end.', **BODY)
s.edit('Newbuild rejected','Newbuild: nothing earned in our window', **HEAD)
s.edit('Building a ship takes 1.5 to 3 years from contract, whichever yard builds it, so a newbuild earns nothing in our 12-month window and arrives after the 2027 to 2028 delivery wave. Newbuild prices are also at decade highs.',
 'Delivery takes **1.5 to 3 years** from contract, so a newbuild earns nothing in our 12 months while stage payments fall due. A 5-yr-old Eco MR costs about the same and earns from delivery.', **BODY)
s.edit('5-year-old Eco chosen over 10-year-old','Secondhand at or near replacement cost', **HEAD)
s.edit('Cost per remaining service year is lower (MR $2.50m against $2.67m a year), the ships are Eco specification for EU ETS and FuelEU, and 5-year-old prices sit at or just above newbuild in our segments, while Suezmax trades at 1.44 times newbuild.',
 'In September, 5-yr-old prices ran **0.96x** to **1.13x** newbuild in our segments (chart) against **1.23x** for Suezmax, **1.44x** by October. A 5-yr-old MR costs **$2.50m** per remaining year vs **$2.67m** at 10 years. All five ships are Eco for EU ETS and FuelEU.', **BODY)
s.edit('Source: SIN series 47130 / 542021 / 540721 / 38981 / 87302 (5-year-old prices) and 71267 / 23357 / 70747 / 35905 / 53070 (newbuild prices), September 2026; 10-year-old prices dataset L3.',
 'Source: SIN series 47130 / 542021 / 540721 / 38981 / 87302 (5-year-old prices) and 71267 / 23357 / 70747 / 35905 / 53070 (newbuild prices), September 2026, October re-pull 15 Oct 2026; 10-year-old prices dataset L3.')
s.save(); out[5]=s.log

# ---------- slide 6
s=S(6)
CB=dict(sz=1400, color='1A2433')
RT=dict(color='5A6472')
s.edit('Which trades our ships go into','Four trades, each backed by demand growth or a fixed charter')
s.edit('2× MR product tankers','2× MR: product trade grows in 2027', **HEAD)
s.edit('Clean products: Middle East and India refineries to East Africa and South East Asia','Clean products: Indian and Middle East refineries to Africa and Asia, plus Atlantic voyages', **RT)
s.edit('Refining capacity is moving east, so each tonne travels further. Products trade +6.3% in 2027F and tonne-miles +6.5%. One ship fixed to SUNCOR for a year, one trading spot where earnings are $53,741/day.',
 'Products trade **+6.3%** in 2027F after a dip in 2026; tonne-miles **+6.5%**. The average haul rose **19%** from 2019 to 2024 as refining moved east. MR #1 on a 1-yr TC at **$30,000**; MR #2 spot, fixed for a year if spot stays below **$20,000** for 8 weeks.', **CB)
s.edit('1× Aframax crude tanker','1× Aframax: 3 years fixed through the wave', **HEAD)
s.edit('Crude oil worldwide, routed by an oil-major-class charterer under a 3-year charter','Crude oil worldwide, trades set by the charterer under a 3-year TC', **RT)
s.edit('The lowest orderbook of any segment (8.4% of dwt). We sell certainty rather than spot exposure: $40,000/day for three years, through the delivery wave and past any ceasefire.',
 'Lowest orderbook of our five segments: **8.4%** of dwt for crude Aframax (**20.8%** with LR2s, which can switch to crude). We give up spot upside for **$40,000/day** over **3 years**, through the 2027 to 2028 delivery wave, whether or not a ceasefire comes.', **CB)
s.edit('1× Kamsarmax (fixed)','Kamsarmax #1: 12 months fixed at $22,000', **HEAD)
s.edit('Bauxite Guinea to China and Pacific coal, on a 12-month charter to CNR','Guinea bauxite or Pacific coal, as the charterer directs', **RT)
s.edit('Guinea exports +29% y/y; the Guinea to China run is the longest haul in dry bulk, so volume growth counts twice. Kamsarmax is the largest ship Port Kamsar can take.',
 'Guinea bauxite exports **+29%** y/y (Jan to Apr) on one of the longest hauls in dry bulk, which ties up more ships per tonne. Kamsarmax is the largest ship Port Kamsar can take.', **CB)
s.edit('1× Kamsarmax (spot)','Kamsarmax #2: Q4 grain season on spot', **HEAD)
s.edit('Grain US Gulf and Black Sea to Asia in the Q4 season, then bauxite and coal', **RT)
s.edit('Harvest seasonality lifts US Gulf exports from September; 2026 is a bumper grain year. If the Black Sea stays closed the ship shifts to bauxite and coal, where two recent coal fixtures confirm the cargo.',
 'Harvest lifts US Gulf grain exports from September; 2026 is a bumper grain year. If Black Sea attacks cut grain cargoes, the ship moves to bauxite and coal, where two September coal fixtures confirm the cargo. Fixed for 12 months if BDI stays below **2,000** for 8 weeks.', **CB)
s.edit('Source: SIN series 98802 / 534403 (products trade), 534456 (crude Aframax orderbook), 557125 (Guinea bauxite), 534400 / 547349 (grain); SIN news #224049, #227870, #191021.',
 'Source: SIN series 98802 / 534403 (products trade), 534456 (crude Aframax orderbook), dataset L4 (incl. LR2), 557125 (Guinea bauxite), 534400 / 547349 (grain); SIN news #224049, #227870, #191021; voyage fixtures dataset L8.')
s.save(); out[6]=s.log

# ---------- slide 7
s=S(7)
s.edit('Pricing basis I: secondhand prices from last transacted sales','Pricing basis I: last transacted sales, plus one SIN assessment')
for c in range(5):
    if c==3: continue
    for p in s.cell_paras(5,c): set_para(p, color='5A6472')
s.edit('Control: the $2.75m discount for China-built tonnage prices the port-fee risk','Comparison: China-built sister, $2.75m lower; the gap includes port-fee risk', color='5A6472')
s.edit('Our two MRs','Our two MRs; no recent 5-yr-old MR sale with a disclosed price')
p=s.find('Two same-type, same-age Aframax sales at an identical $75.0m make that price firm. The two Kamsarmaxes are benchmarked to two Japan-built sales on the same day. The Presinge control shows what the market charges for the port-fee insurance we are buying.')
body=s.shape_of(p)
s.clone_sp(body,'Panel title','Sales price three ships; the SIN assessment prices the two MRs', x=0.75,y=5.55,w=11.80,h=0.32, sz=1600, font='Cambria', color='C8102E', base_b=True)
set_para(p, 'Two 2018 Tsuneishi Aframaxes sold at about **$75m** in Apr and May. Medi Positano sold **$2.75m** above its China-built sister, a gap that also reflects its scrubber. No recent 5-yr-old MR sale had a disclosed price, so the MRs use the SIN assessment (**$50m** Sep, **$52m** Oct).', **BODY)
s.set_xfrm(body, y=5.90, h=0.55)
s.save(); out[7]=s.log

# ---------- slide 8
s=S(8)
s.edit('Torm Genesis (Aframax, 119,456 dwt)','Torm Genesis (Aframax, 119,456 dwt, 2011)')
s.edit('CNR','Not reported (CNR)')
s.edit('MR #1 fixed rate','MR #1 rate benchmark')
s.edit('Our Aframax 3-year charter','Benchmark for our Aframax 3-year TC')
s.edit('Kamsarmax #1 fixed rate','Kamsarmax #1 rate benchmark')
s.edit('Why these charterers','Benchmark rates, first-class charterers', **HEAD)
s.edit('Oil majors, a Canadian integrated producer and the largest grain house. Counterparty risk on the fixed 60% of ship-days is as low as the market offers, and a long charter is itself bankable security.',
 "Base-case rates are benchmarks from other owners' fixtures: **SUNCOR** (Canadian integrated oil), **AET** (MISC, Petronas group) and a Kamsarmax charterer SIN does not name (**CNR**). We will fix only with first-class names; a long charter is itself bankable security.", **BODY)
s.edit('What the October refresh adds','October: our MR rates look conservative', **HEAD)
s.edit('The SIN 1-year MR Eco assessment rose from $29,000 in September to $43,000 in October, and MR spot earnings reached $53,741/day. The $30,000 fixture is kept as the last transacted rate; the final data cut will replace it with the October fixture, which only raises the fixed leg.',
 'SIN 1-yr MR Eco rose from **$29,000** (Sep) to **$43,000** (Oct); MR spot **$53,741/day**. Our base keeps the last-done **$30,000** for MR #1, as the brief asks, so the MR base case is conservative. Kamsarmax 1-yr (**$19,750**) and Aframax 3-yr (**$37,500**) sit below our benchmarks.', **BODY)
s.edit('Source: SIN Fixtures Register (Timecharter), extracted 12 Sep 2026; SIN 1-year MR Eco TC assessment series 541552, October 2026 value $43,000/day.',
 'Source: SIN Fixtures Register (Timecharter), extracted 12 Sep 2026; SIN 1-year MR Eco TC assessment series 541552, October 2026 value $43,000/day; Kamsarmax 1-year TC 540614 ($19,750) and Aframax 3-year TC 49138 ($37,500), October 2026.')
s.save(); out[8]=s.log

# ---------- slide 9
s=S(9)
s.edit('Kamsarmax spot leg; converts to about $27,400/day TCE at September bunker prices, above the $23,000 base assumption',
 'Kamsarmax spot leg: about **$27,400/day** TCE at $875/t VLSFO (Sep), above our **$23,000** base')
p=s.find('Three price families, 17 transactions, all last done: purchase prices, charter rates and freight rates. Our spot exposure sits in coal and clean products, outside the war-premium crude market.')
body=s.shape_of(p)
s.clone_sp(body,'Panel title','Three price families, no crude on spot', x=0.75,y=5.68,w=11.80,h=0.30, sz=1600, font='Cambria', color='C8102E', base_b=True)
set_para(p, '**16** last-done transactions plus **1** SIN assessment (MR price). Spot ships carry grain, coal and clean products; MR spot holds some war premium, so the bear case uses 2025 averages and MR #2 fixes if spot stays below **$20,000** for 8 weeks.', **BODY)
s.set_xfrm(body, y=6.00, h=0.48)
s.save(); out[9]=s.log

# ---------- notes
notes=json.load(open(sys.argv[3],encoding='utf-8'))
for k,v in notes.items():
    set_notes(f"{D}/ppt/notesSlides/notesSlide{k}.xml", v)

for k,v in out.items():
    print('== slide',k, len(v),'edits')
