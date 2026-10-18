# SIN 数据溯源指南：slide 底部的 Source 怎么查

> 每页 slide 底部的 Source 行写了三类编号：序列号（series）、数据集编号（dataset L6、L11 等）、新闻编号（news #）。下面说明每一类去哪里查、仓库里对应哪个文件，组员可以直接用原始数据自己做图。

## 一、三类编号分别怎么查

| 编号类型 | 例子 | 在 SIN 网站上怎么找 | 仓库里在哪 |
|---|---|---|---|
| 序列号 series | 87302、53070、48989 | 登录 SIN，顶部菜单 TIMESERIES & GRAPHS，点 Search All，在搜索框输入序列号（或英文名称），勾选后点 View Data，右上角 Export 可下载 Excel | `data/raw/` 下的 CSV 和 xlsx；表头方括号里就是序列号，例如 `[SIN 87302]` |
| 数据集 dataset | L6、L11、L13 至 L16 | 不是 SIN 的编号，是我们自己的采集批次编号。每个批次对应哪几个序列号或哪个 SIN 页面，查 `data/catalog.csv` 的"SIN路径"一列 | `data/raw/L6_20260912.csv` 等；截图在 `data/screenshots/` |
| 新闻 news # | #221824、#228241 | 直接打开 `https://sin.clarksons.net/News/Article/文章号`，例如 https://sin.clarksons.net/News/Article/228241 （需先登录） | `data/news/*.md`，每篇有标题、日期、链接、摘要 |

`data/catalog.csv` 是总台账：每一行一个数据项，写明 SIN 菜单路径、序列号、频率、单位、时间范围、提取日期、CSV 文件名和截图文件名。

## 二、第 4 部分（slide 14 至 16）用到的来源逐项对照

| Source 里的写法 | 是什么 | SIN 路径 | 仓库文件 |
|---|---|---|---|
| 87302 | Suezmax 160k dwt 5 年船龄 Eco 二手价，月度，$m | TIMESERIES & GRAPHS > Search All > 87302 > View Data | `data/raw/A3_20260912.csv` |
| 53070 | Suezmax 156-158k dwt 新造船价，月度，$m | 同上，搜 53070 | `data/raw/A6_20260912.csv` 第 4 列 |
| 48989 | Suezmax 150k dwt 一年期租评估，月度，$/day | 同上，搜 48989 | `data/raw/B3_20260912.csv` |
| 49108 | Suezmax 150k dwt 三年期租评估，月度，$/day | 同上，搜 49108 | `data/raw/B6_20260912.csv` 第 3 列 |
| 531088 | Suezmax 2010 年建造船平均收益，周度，$/day | 同上，搜 531088 | `data/raw/C3_20260912.csv` 第 4 列 |
| dataset L6 | 周度过境船数：苏伊士、亚丁湾、霍尔木兹原油轮（序列 11278847、11278869、551286、12792857） | 同上，逐个搜这四个序列号 | `data/raw/L6_20260912.csv` |
| dataset L11 | 被制裁船队时间序列（序列 12116104、12116108、12110866、12110871、12111020） | 同上，逐个搜 | `data/raw/L11_20260912.csv` |
| 17259 | 波罗的海干散货指数 BDI，日度 | 同上，搜 17259 | `data/raw/C1_20260912.csv` |
| 47130 / 71267 | MR 5 年船龄二手价 / MR 新造价 | 同上 | `A1_20260912.csv` / `A6_20260912.csv` 第 2 列 |
| 540721 / 70747 | Kamsarmax 5 年船龄二手价 / 新造价 | 同上 | `A5_20260912.csv` / `A6_20260912.csv` 第 6 列 |
| 38981 / 35905 | Aframax 5 年船龄二手价 / 新造价 | 同上 | `A4_20260912.csv` / `A6_20260912.csv` 第 5 列 |
| news #221824 | Middle East Conflict: Update No.3（2026-03-04） | https://sin.clarksons.net/News/Article/221824 | `data/news/` 里搜 221824 |
| news #227050 | Middle East Update: Disruption Doubling Up?（2026-07-24） | https://sin.clarksons.net/News/Article/227050 | 同上 |
| news #228241 | Sanctioned Vessels Update（2026-08-26） | https://sin.clarksons.net/News/Article/228241 | `data/news/J_Russia_sanctions_tanker_1.md` |
| news #229922 | Ship Recycling: Building Up An "Overhang"（2026-10-09） | https://sin.clarksons.net/News/Article/229922 | 仅在《数据刷新核对_20261015》中记录 |

## 三、9 月数据和 10 月数据的关系

- `data/raw/*_20260912.csv` 是 9 月 12 日的完整历史序列，月度序列的最后一个点是"9 月月中值"。
- 10 月的数值来自 10 月 15 日在 SIN 上的重新拉取，结论写在《数据刷新核对_20261015》，图表用到的 10 月数值单独存成 `data/raw/R_refresh_points_20261015.csv`，每行写明序列号、9 月值、10 月值和日期。仓库里没有 10 月的完整历史 CSV。
- 第 14、15 页的图已改成"9 月对 10 月"：灰色是 9 月 12 日的提取值，深蓝是 10 月值。历史曲线到 8 月为止来自 9 月提取，9 月月末值与 10 月值来自 10 月重新拉取。BDI 日度线到 9 月 10 日，10 月 6 日与 13 日两个读数用虚线点标出，中间日期没有逐日数据。
- 注意 9 月月中提取值和月末终值会不同：Suezmax 5 年船龄 9 月提取时是 1.11 亿，月末修订为 1.2 亿。

## 四、如果组员要用 10 月完整数据重画

1. 在 SIN 按上表搜序列号，View Data 后把时间范围拉到最新，Export 成 Excel。
2. 存进 `data/raw/`，文件名用新的日期，例如 `A3_20261020.csv`。
3. 改 `scripts/make_charts.py` 里 `rd()` 函数读取的日期后缀，运行 `CHART_STYLE=deck python3 scripts/make_charts.py` 生成模板配色版，运行 `python3 scripts/make_charts.py` 生成原配色版。
4. 也可以直接在 Excel 里用导出的数据画图，图下来源行照抄序列号和提取日期即可。
