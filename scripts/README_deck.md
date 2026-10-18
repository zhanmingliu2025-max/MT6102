# 如何重新生成 PPT

1. 重新生成模板配色的图表：`CHART_STYLE=deck python3 scripts/make_charts.py && CHART_STYLE=deck python3 scripts/make_supply_charts.py`（输出到 `charts_deck/`）。
2. 在有 `pptxgenjs` 与 `jszip` 的目录里运行 `node scripts/make_deck.js`（需要 `npm install pptxgenjs jszip`，并设置 `NODE_PATH` 指向该 `node_modules`）。脚本顶部的 `CH` 常量指向 `charts_deck/` 的绝对路径，换机器时改这一行；`applyTheme` 的路径来自 Claude 的 pptx 技能目录，若不可用可删掉该调用（仅影响主题色记录，不影响页面外观）。
3. 输出 `MT6102_Investment_Proposal.pptx`，复制为仓库根目录的 `MT6102_Group_Presentation.pptx`。

页面与图表、讲稿的对应关系见《PPT页面清单》；每页的 speaker notes 已写入 pptx 备注栏。

## 2026-10-18 起的工作版本

仓库根目录的 `MT6102_Group_Presentation.pptx` 现在是小组的工作版本（组员已改第 14 至 16 页），不再由 `make_deck.js` 直接生成。重新跑 `make_deck.js` 会丢掉组员的修改，所以以后只在 pptx 上小改。

第 1 至 9 页的优化用 `scripts/deck_polish/` 完成：解压 pptx，运行
`python3 -I scripts/deck_polish/apply.py <解压目录> scripts/deck_polish scripts/deck_polish/notes_slides_1_9.json`，
再从解压目录内部 `zip -Xr` 打包。脚本按原文逐字匹配，原文对不上就报错，不会悄悄改错页；第 10 至 35 页不动。
