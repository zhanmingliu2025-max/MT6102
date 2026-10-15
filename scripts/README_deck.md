# 如何重新生成 PPT

1. 重新生成模板配色的图表：`CHART_STYLE=deck python3 scripts/make_charts.py && CHART_STYLE=deck python3 scripts/make_supply_charts.py`（输出到 `charts_deck/`）。
2. 在有 `pptxgenjs` 与 `jszip` 的目录里运行 `node scripts/make_deck.js`（需要 `npm install pptxgenjs jszip`，并设置 `NODE_PATH` 指向该 `node_modules`）。脚本顶部的 `CH` 常量指向 `charts_deck/` 的绝对路径，换机器时改这一行；`applyTheme` 的路径来自 Claude 的 pptx 技能目录，若不可用可删掉该调用（仅影响主题色记录，不影响页面外观）。
3. 输出 `MT6102_Investment_Proposal.pptx`，复制为仓库根目录的 `MT6102_Group_Presentation.pptx`。

页面与图表、讲稿的对应关系见《PPT页面清单》；每页的 speaker notes 已写入 pptx 备注栏。
