#!/usr/bin/env python3
"""Single source: curriculum/curriculum.json.
Regenerates (1) the LEVELS block inside index.html and (2) the PDFs in curriculum/ (needs Google Chrome).
Run from the site folder:  python3 scripts/build_curriculum.py
"""
import base64, json, re, subprocess, sys, tempfile
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
data = json.loads((ROOT / "curriculum/curriculum.json").read_text())["levels"]
PHONE = "+91 74830 31638"

# 1) patch index.html
js = "var LEVELS = " + json.dumps(data, ensure_ascii=False, indent=1) + ";"
html = (ROOT / "index.html").read_text()
html, n = re.subn(r"/\*LEVELS-START\*/.*?/\*LEVELS-END\*/", lambda m: "/*LEVELS-START*/\n" + js + "\n/*LEVELS-END*/", html, flags=re.S)
if n != 1:
    sys.exit("LEVELS markers not found in index.html")
(ROOT / "index.html").write_text(html)

# 2) PDFs
logo = base64.b64encode((ROOT / "logo.png").read_bytes()).decode()
CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0}
body{font-family:'Gantari','Avenir Next','Segoe UI',Helvetica,Arial,sans-serif;color:#151b3a;background:#faf5ea;-webkit-print-color-adjust:exact;print-color-adjust:exact;font-size:11.5pt;line-height:1.45}
.page{width:210mm;min-height:297mm;padding:0 14mm 22mm;position:relative;page-break-after:always;background:#faf5ea}
.page:last-child{page-break-after:auto}
.top{margin:0 -14mm 8mm;background:#151b3a;color:#faf5ea;padding:8mm 14mm;display:flex;align-items:center;gap:5mm;border-bottom:2.5mm solid #e9a73b}
.top img{height:16mm}.wm{font-weight:800;font-size:22pt;letter-spacing:-.02em}.wm b{color:#e9a73b}
.top small{display:block;letter-spacing:.18em;font-size:7pt;color:#c4c8de;font-weight:700}
.tagpill{display:inline-block;background:#e9a73b;color:#151b3a;font-weight:800;font-size:8.5pt;letter-spacing:.08em;text-transform:uppercase;border-radius:99px;padding:1mm 4mm}
h1{font-size:30pt;line-height:1.05;margin:3mm 0 2mm;letter-spacing:-.02em}
.sum{color:#4d5578;font-size:13pt;margin-bottom:5mm}
.out{background:#fbecc8;border-left:2mm solid #e9a73b;border-radius:3mm;padding:4mm 5mm;margin-bottom:6mm}
.out b{display:block;font-size:8.5pt;letter-spacing:.1em;text-transform:uppercase;color:#8a5a00;margin-bottom:1mm}
.sec{background:#fff;border:.3mm solid #e2d7bb;border-radius:4mm;padding:4mm 5mm;margin-bottom:4mm;break-inside:avoid}
.sec h3{font-size:11pt;color:#8a5a00;text-transform:uppercase;letter-spacing:.08em;margin-bottom:2mm}
.sec ul{list-style:none;padding:0;columns:2;column-gap:8mm}
.sec li{position:relative;padding:.8mm 0 .8mm 6mm;break-inside:avoid;font-size:10.5pt}
.sec li::before{content:"";position:absolute;left:0;top:2.1mm;width:3mm;height:3mm;border:.4mm solid #151b3a;border-radius:.8mm}
.meta{color:#4d5578;font-size:9.5pt;margin-bottom:4mm}
.foot{position:fixed;left:0;right:0;bottom:0;background:#151b3a;color:#faf5ea;padding:4mm 14mm;font-size:8.5pt;display:flex;justify-content:space-between;gap:6mm}
.foot b{color:#e9a73b}
.cover h1{font-size:40pt;margin-top:10mm}
.lv{display:flex;gap:5mm;align-items:center;background:#fff;border:.3mm solid #e2d7bb;border-radius:4mm;padding:4mm 5mm;margin-bottom:3.5mm}
.lv .n{flex:none;width:12mm;height:12mm;border-radius:3mm;background:#151b3a;color:#e9a73b;font-weight:800;font-size:16pt;display:grid;place-items:center}
.lv strong{font-size:13pt}.lv span{display:block;color:#4d5578;font-size:10pt}
.lv em{margin-left:auto;font-style:normal;font-weight:800;color:#8a5a00;font-size:10pt;white-space:nowrap}
"""
def foot():
    return (f'<div class="foot"><span><b>Chessopia</b> &middot; Learn &middot; Play &middot; Grow together</span>'
            f'<span>Weekend classes in Bangalore &middot; WhatsApp / Call {PHONE}</span></div>')
TOP = (f'<div class="top"><img src="data:image/png;base64,{logo}" alt=""><div><div class="wm">chess<b>opia</b></div>'
       '<small>LEARN &middot; PLAY &middot; GROW TOGETHER</small></div></div>')
def count(L): return sum(len(s["topics"]) for s in L["sec"])
def level_page(L):
    secs = "".join(f'<div class="sec"><h3>{escape(s["title"])}</h3><ul>' + "".join(f"<li>{escape(t)}</li>" for t in s["topics"]) + "</ul></div>" for s in L["sec"])
    return (f'<section class="page">{TOP}<span class="tagpill">Level {L["n"]} &middot; {escape(L["tag"])}</span>'
            f'<h1>{escape(L["name"])}</h1><p class="sum">{escape(L["sum"])}</p>'
            f'<div class="out"><b>By the end of this level</b>{escape(L["out"])}</div>'
            f'<p class="meta">{count(L)} topics across {len(L["sec"])} sections</p>{secs}{foot()}</section>')
def cover():
    rows = "".join(f'<div class="lv"><div class="n">{L["n"]}</div><div><strong>{escape(L["name"])} &middot; {escape(L["tag"])}</strong><span>{escape(L["sum"])}</span></div><em>{count(L)} topics</em></div>' for L in data)
    return (f'<section class="page cover">{TOP}<span class="tagpill">Curriculum</span><h1>From first pawn<br>to master strategy</h1>'
            f'<p class="sum">Five levels. Every child starts at the right level and moves up when the topics are mastered, not when the calendar says so.</p>{rows}'
            f'<p class="meta" style="margin-top:6mm">Weekend batches for ages 6&ndash;9 and 10&ndash;16 &middot; Free demo class &middot; Book on WhatsApp {PHONE}</p>{foot()}</section>')
def pdf(name, body):
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{body}</body></html>'
    with tempfile.TemporaryDirectory() as t:
        f = Path(t) / "x.html"; f.write_text(doc)
        out = ROOT / "curriculum" / name
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out}", f.as_uri()],
                       check=True, capture_output=True, timeout=120)
        print("wrote", out.relative_to(ROOT), out.stat().st_size // 1024, "KB")
pdf("chessopia-curriculum-all-levels.pdf", cover() + "".join(level_page(L) for L in data))
for L in data:
    pdf(f"chessopia-level-{L['n']}.pdf", level_page(L))
