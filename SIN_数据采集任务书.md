# SIN 数据采集任务书（供本地 Claude Code 执行）

> 执行者：运行在用户本地、带 Playwright 浏览器控制的 Claude Code。
> 目标网站：Clarksons Shipping Intelligence Network（https://sin.clarksons.net，用户已在浏览器中登录）。
> 总目标：为 MT6102 小组作业（2.5 亿美元航运投资提案）采集**可追溯、细粒度**的市场数据。
> 数据用途见 `MT6102_Group_Project_投资方案.md`。

---

## 0. 执行规则（先读完再动手）

1. **只做数据读取与导出**，不修改任何账户设置，不进行登录以外需要凭据的操作。登录/MFA 出现时暂停并请用户手动完成。
2. SIN 的菜单命名可能与本任务书略有出入。**以任务书给出的"序列关键词"在 SIN 全局搜索框搜索为准**，找到后把实际路径记录进 catalog。
3. 每完成一个指标，立即做三件事：
   - 数据存 `data/raw/<指标ID>_<YYYYMMDD>.csv`（优先用页面的 Export/Excel 下载再转 CSV；下载不可用则读取页面表格手工整理，并在 catalog 备注 "manual-extract"）；
   - 全页截图存 `data/screenshots/<指标ID>_<YYYYMMDD>.png`（截图必须包含**序列全名与日期轴**）；
   - 在 `data/catalog.csv` 追加一行。
4. `data/catalog.csv` 表头（首次创建时写入）：
   ```
   指标ID,指标名称,SIN实际路径,序列全名,频率,单位,数据区间,提取日期,原始文件,截图文件,优先级,状态,备注
   ```
5. 时间区间默认 **2015-01 至今**（月度）；日度指数取 **2023-01 至今**。区间不足时取全量并备注。
6. 按优先级顺序执行：P0 → P1 → P2。每完成一组（A/B/C…）向用户汇报一次进度。
7. 遇到付费墙/权限不足的序列：截图记录提示信息，状态标 "no-access"，继续下一项，**不要**尝试绕过。

## 目录结构

```
data/
  raw/           # CSV 数据
  screenshots/   # 截图证据
  news/          # 新闻全文/截图
  catalog.csv    # 总台账
```

---

## A. 二手船价格（P0）—— 用于组合定价与周期定位

SIN 模块参考：Prices & Values → Secondhand Prices（或搜索关键词）。

| 指标ID | 序列关键词 | 频率 | 单位 |
|---|---|---|---|
| A1 | MR Product Tanker 51k dwt 5 Year Old Secondhand Price | 月 | $m |
| A2 | Ultramax Bulkcarrier 63.5k dwt 5 Year Old Secondhand Price | 月 | $m |
| A3 | Suezmax Tanker 160k dwt 5 Year Old Secondhand Price | 月 | $m |
| A4 | Aframax Tanker 115k dwt 5 Year Old Secondhand Price | 月 | $m |
| A5 | Kamsarmax/Panamax Bulkcarrier 82k dwt 5 Year Old Secondhand Price | 月 | $m |
| A6 | 同型号 Newbuilding Price（A1–A5 各取对应新造价） | 月 | $m |

> A6 用于展示"二手价 vs 新造价"比值——判断是否接近 peak（Week 3：peak 时二手价超过重置成本）。

## B. 期租租金（P0）—— 收益预测的基准

SIN 模块参考：Timecharter Rates。

| 指标ID | 序列关键词 | 频率 |
|---|---|---|
| B1 | MR Product Tanker 1 Year Timecharter Rate | 周/月 |
| B2 | Ultramax 63.5k dwt 1 Year Timecharter Rate | 周/月 |
| B3 | Suezmax 1 Year Timecharter Rate | 周/月 |
| B4 | Aframax 1 Year Timecharter Rate | 周/月 |
| B5 | Kamsarmax 82k dwt 1 Year Timecharter Rate | 周/月 |
| B6 | 上述船型 3 Year Timecharter Rate（可得则取） | 周/月 |

## C. 现货运价与收益指数（P0）

| 指标ID | 序列关键词 | 频率 |
|---|---|---|
| C1 | Baltic Dry Index (BDI) | 日 |
| C2 | Baltic Supramax/Ultramax Index (BSI) 或 Ultramax Average Earnings | 日/周 |
| C3 | Clarksons Average Tanker Earnings / Suezmax Average Earnings | 周 |
| C4 | MR Clean Products Average Earnings | 周 |
| C5 | Aframax Average Earnings | 周 |
| C6 | ClarkSea Index（全行业收益指数，用于周期总图） | 周 |
| C7 | 关键航线运价：TD3C (MEG-China VLCC), TD20 (WAF-Cont Suezmax), TC7 或 TC17 (MR 航线), 以及 Worldscale 形式的对应报价 | 周 |

## D. 船队与订单簿（P0）—— "选油运/干散、弃集运/LNG"的核心证据

| 指标ID | 序列关键词 | 说明 |
|---|---|---|
| D1 | Orderbook as % of Fleet — Product Tankers | 当前值+历史 |
| D2 | Orderbook as % of Fleet — Crude Tankers（或分 Suezmax/Aframax） | 同上 |
| D3 | Orderbook as % of Fleet — Bulkcarriers | 同上 |
| D4 | Orderbook as % of Fleet — Containerships | 对比用 |
| D5 | Orderbook as % of Fleet — LNG Carriers | 对比用 |
| D6 | Fleet Development/Growth（上述各板块船队增速） | 年度 |
| D7 | Fleet Age Profile（油轮/散货 15 岁以上运力占比） | 当前 |

## E. 交付与拆解（P1）

| 指标ID | 序列关键词 |
|---|---|
| E1 | Tanker Deliveries（历史+2026–2028 预测/schedule） |
| E2 | Bulkcarrier Deliveries（同上） |
| E3 | Tanker Demolition（月度/年度量） |
| E4 | Bulkcarrier Demolition（同上） |
| E5 | Demolition Price（$/ldt，判断拆解意愿） |

## F. 海运贸易量与吨海里（P1）—— 需求侧证据

SIN 模块参考：Trade / Seaborne Trade（Shipping Review & Outlook 数据表也可）。

| 指标ID | 序列关键词 |
|---|---|
| F1 | Seaborne Crude Oil Trade（吨 + tonne-miles，含预测） |
| F2 | Seaborne Oil Products Trade（吨 + tonne-miles，含预测） |
| F3 | Seaborne Coal Trade |
| F4 | Seaborne Grain Trade（注意季节性，取月度） |
| F5 | Seaborne Bauxite Trade（几内亚→中国为主的增量证据） |
| F6 | World Seaborne Trade Total vs World GDP Growth（两条序列做相关图） |

## G. Last-done S&P 成交记录（P0）—— 题目第 3 条硬性要求

来源：SIN 的 Sale & Purchase 周报 / S&P transactions 数据库。

对 A1–A5 每种目标船型，抓取**最近 3 笔**二手成交：

- 记录字段：成交日期、船名、船型、DWT、建造年份、建造船厂/建造国、成交价（$m）、买方（如披露）、报告出处（周报名称+日期）。
- 存入 `data/raw/G_SP_lastdone_<YYYYMMDD>.csv`，每笔成交所在报告页面单独截图。
- **建造国必须记录**（用于评估美国对中国建造船舶港口费的风险敞口）。

## H. Last-done 期租 fixtures（P0）

来源：SIN Fixtures 数据库 / 周报。

对 B1–B5 每种船型抓取**最近 3 笔** 1 年期租 fixture：日期、船名、DWT、建造年、租金（$/day）、期限、租家、交船地。存 `data/raw/H_TC_fixtures_<YYYYMMDD>.csv` + 截图。

## I. FFA 远期曲线（P1）

| 指标ID | 内容 |
|---|---|
| I1 | 干散 FFA：Panamax/Supramax 未来 4 个季度合约价 |
| I2 | 油轮 FFA/远期评估（如 SIN 可得；不可得则标 no-access） |

## J. 新闻证据库（P1）—— 每条新闻存标题、日期、来源、要点摘录

在 SIN News（及 Clarksons Research 报告摘要）中逐个搜索以下关键词，各取最近 3–5 条最相关：

```
Red Sea / Suez transits          （运距与风险）
Russia sanctions tanker          （影子船队、制裁出清）
US tariff / Section 301 port fee （中国建造船港口费）
refinery closure Europe          （成品油贸易重构）
refinery Dangote / Middle East   （新炼厂投产）
Guinea bauxite export            （铝土矿长运距增量）
grain harvest export             （季节性）
IMO carbon / EU ETS shipping     （环保法规与老船淘汰）
newbuilding orders tanker bulker （订单动向）
demolition market                （拆解动向）
```

存 `data/news/J_<关键词>_<序号>.md`（含链接与访问日期）+ 截图。

## K. 候选船只核查（P2）—— World Fleet Register

抓完 G 组后，对出现在 last-done 成交里的**同型姊妹船**（5–7 年龄、eco 型），在 World Fleet Register 各筛出 5 条候选：船名、DWT、建造年、船厂、建造国、主机/eco 标识、现船东。存 `data/raw/K_candidates_<船型>.csv`。

---

## 完工自检清单

- [ ] catalog.csv 行数 = raw 文件数 = 截图数（news 除外）
- [ ] 每张截图能看到序列全名和日期
- [ ] G/H 组每笔成交都有出处（报告名+日期）
- [ ] P0 全部完成；no-access 项已备注
- [ ] `git add data/ && git commit && git push` 到 `claude/confident-rubin-lpa9y8`
- [ ] 向用户口头汇报：完成 X 项 / no-access Y 项 / 值得注意的市场信号 3 条
