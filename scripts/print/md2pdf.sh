#!/usr/bin/env bash
# 用法: scripts/print/md2pdf.sh <文件名不含.md> <extra_outline|extra_pages>
# 需要: pandoc, 无头 Chromium, 以及与本目录同级的 fonts/NotoSansSC-{400,500,700}.ttf
set -e
name="$1"; extra="$2"; here="$(cd "$(dirname "$0")" && pwd)"; work="${TMPDIR:-/tmp}/md2pdf_$$"; mkdir -p "$work"
cp "$here"/*.css "$work"/
fonts="${FONTS_DIR:-$here/fonts}"; [ -d "$fonts" ] || fonts="/tmp/claude-0/-home-user-MT6102/0b8c27c0-7c61-5386-8dfe-5f85d183f1af/scratchpad/fonts"
ln -s "$fonts" "$work/fonts" 2>/dev/null || true
pandoc "$name.md" -f markdown -t html5 --wrap=none -o "$work/body.html"
python3 -c "import re,sys;p=sys.argv[1];s=open(p,encoding='utf-8').read();open(p,'w',encoding='utf-8').write(re.sub(r'<colgroup>.*?</colgroup>','',s,flags=re.S))" "$work/body.html"
{ echo "<!doctype html><html lang=\"zh\"><head><meta charset=\"utf-8\"><title>$name</title><link rel=\"stylesheet\" href=\"md2pdf.css\"><link rel=\"stylesheet\" href=\"$extra.css\"></head><body>"; cat "$work/body.html"; echo "<div class=\"footer\">MT6102 Maritime Economics · 小组投资方案 · $name</div></body></html>"; } > "$work/$name.html"
chrome="${CHROME:-/opt/pw-browsers/chromium-1194/chrome-linux/chrome}"
(cd "$work" && "$chrome" --headless=new --no-sandbox --disable-gpu --print-to-pdf="$PWD/../$name.pdf" --no-pdf-header-footer --virtual-time-budget=15000 "file://$work/$name.html" >/dev/null 2>&1) || true
mv "$work/../$name.pdf" "./$name.pdf" 2>/dev/null || true
echo "wrote $name.pdf"
