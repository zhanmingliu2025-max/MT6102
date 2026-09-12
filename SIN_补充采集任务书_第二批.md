# SIN 补充采集任务书（第二批 L 组）—— 供本地 Claude Code 执行

> 执行规则、目录结构、留痕规范与第一批《SIN_数据采集任务书.md》完全相同：
> CSV 存 `data/raw/`、截图存 `data/screenshots/`、逐项登记 `data/catalog.csv`、no-access 如实标注。
> 命名沿用 `<指标ID>_<YYYYMMDD>` 格式。全部完成后 commit 并推送 `claude/confident-rubin-lpa9y8`。

## P0（硬缺口，优先）

| 指标ID | 内容 | SIN 检索关键词/位置 | 备注 |
|---|---|---|---|
| L1 | 各船型营运成本 OPEX（$/day） | 搜索 "Operating Costs" / "OPEX" / "Ship Operating Expenses"；船型：MR、Aframax、Panamax/Kamsarmax Bulker | 若 SIN 时间序列无此口径，截图记录后标 no-access，并在备注写"改用 Drewry/Moore 行业基准"；不要硬凑 |
| L2 | 燃油价格 | "Singapore VLSFO 0.5% Bunker Price"、"Singapore MGO"、"Rotterdam VLSFO"；月度 2019 至今 | 一个 CSV 多列合并即可（L2_YYYYMMDD.csv） |
| L3 | 10 年船龄二手价 | "10 Year Old Secondhand Price"：MR 产品油轮、Ultramax/Handymax 63.5k、Kamsarmax 82k、Aframax 115k | 与 A 组同源模块；用于"5yo vs 10yo"资产选择论证 |
| L4 | 分尺寸段船队/订单簿绝对量与交付排期 | Fleet & Orderbook 模块："Aframax Fleet No/DWT"、"Suezmax Fleet"、"MR Fleet"、"Panamax Bulker Fleet"、"Handymax Fleet"；对应 "Orderbook No/DWT"；2026-2028 delivery schedule | 每段两个数：现役（艘数+dwt）、在手订单（艘数+dwt）；截图 Fleet Register 汇总页即可 |
| L8 | 即期航次 fixture（last done 运价） | FIXTURES > Voyage/Spot：①一笔 Kamsarmax/Ultramax 粮食或煤炭航次（$/t）②一笔 Suezmax TD20 类原油航次（WS）③一笔 MR 清洁油品航次（WS 或 $/t） | **题目第 3 条硬性要求 freight rate last transacted**；每笔记录：日期/船名/货量/装卸港/运价/租家/出处，存 L8_spot_fixtures_YYYYMMDD.csv |

## P1（增强 Q&A 防守）

| 指标ID | 内容 | SIN 检索关键词/位置 | 备注 |
|---|---|---|---|
| L5 | 干散与 MR 即期收益（$/day） | "Kamsarmax 82k Bulkcarrier Spot Earnings"、"Ultramax 63k Earnings"、"BSI TCE"、"MR Pacific Basket Earnings" 或 Baltic TCE assessments | 用于 WS→$/day 换算示例与即期腿情景 |
| L6 | 苏伊士/亚丁湾通行量 | "Suez Canal Transits"、"Gulf of Aden Arrivals"（周/月度） | 量化绕行冲击；若有 "Hormuz" 相关序列一并取 |
| L7 | 铁矿石与小宗散货贸易 | "World Seaborne Iron Ore Trade Mt / Tonne-Miles"、"Minor Bulk Trade"（含 2027 预测） | Simandou 溢出效应 + Ultramax 货种基础 |
| L10 | 美中港口费费率明细 | SIN News 搜索 "USTR port fee" / "Section 301 fee schedule" / "China special port dues"，取 2-3 篇含具体费率的 | 存 data/news/，记录 $/净吨费率数字 |
| L11 | 被制裁油轮时间序列 | 搜索 "Sanctioned Tanker Fleet"（若为序列）；否则收集 2025-2026 各期 Sanctioned Vessels Update 新闻中的艘数/dwt，手工整成 CSV 标 manual-extract | 画"制裁运力占比走势"用 |

## P2（锦上添花）

| 指标ID | 内容 | 位置 | 备注 |
|---|---|---|---|
| L9 | 拆解成交 last done | SALES > Demolition Sales，取最近 2-3 笔油轮/散货拆解成交（$/ldt、LDT、拆解地） | 四大市场 last done 闭环 |
| L12 | FFA 远期报价 | SIN 已确认无 → 若可访问 Baltic Exchange 公开页面则截图记录，否则跳过 | 仅作补充，非 SIN 来源须明确标注 |

## 完工动作
1. catalog.csv 与文件数核对一致；
2. `git add data/ && git commit -m "Add SIN data batch 2 (L-series)" && git push`；
3. 汇报：完成/缺失清单 + L1 OPEX 与 L3 10yo 价的具体数值（回程分析最需要这两个）。
