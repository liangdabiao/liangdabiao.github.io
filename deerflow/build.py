# -*- coding: utf-8 -*-
"""把《DeerFlow 2.0 从入门到精通》拆成多页阅读网站。
产物：index.html + 01.html..19.html + style.css + app.js
内容完全来自图书 Markdown，不增删事实。
"""
import re, os
import markdown

SRC = r"D:\真agent小蓝书\do-deepagents-skill\DeerFlow从入门到精通.md"
OUT = r"D:\真agent小蓝书\do-deepagents-skill\deerflow-site"
os.makedirs(OUT, exist_ok=True)

text = open(SRC, encoding="utf-8").read()
lines = text.split("\n")

part_re = re.compile(r"^#\s+Part\s+(\d+)\s*[:：]?\s*(.*)$")
chap_re = re.compile(r"^##\s+§(\d+)\s+(.*)$")

parts = []
cur_part = None
cur_chap = None
preamble_lines = []
state = "preamble"

for ln in lines:
    m_part = part_re.match(ln)
    m_chap = chap_re.match(ln)
    if m_part:
        state = "chapter"
        cur_part = {"num": m_part.group(1), "title": m_part.group(2).strip(), "chapters": []}
        parts.append(cur_part)
        cur_chap = None
        continue
    if m_chap and state != "preamble":
        cur_chap = {"num": int(m_chap.group(1)), "title": m_chap.group(2).strip(),
                    "file": f"{int(m_chap.group(1)):02d}.html", "body": []}
        cur_chap["body"].append(ln)  # 把章节标题行也纳入正文
        cur_part["chapters"].append(cur_chap)
        continue
    if state == "preamble":
        preamble_lines.append(ln)
    else:
        if cur_chap is not None:
            cur_chap["body"].append(ln)

# 前言：截取「# 目录」之前的部分（标题 + 阅读指南）
pre = "\n".join(preamble_lines)
if "# 目录" in pre:
    pre = pre.split("# 目录")[0]
pre = pre.strip()
pre_html = markdown.markdown(pre, extensions=["tables", "fenced_code", "sane_lists"])

# 扁平化章节，便于 prev/next
all_chapters = []
for p in parts:
    for c in p["chapters"]:
        c["part"] = p
        all_chapters.append(c)

def render(md_text):
    return markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])

# ---------- 模板 ----------
PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div class="progress" id="progress"></div>
<header class="topbar">
  <a class="brand" href="index.html">DeerFlow 2.0 · 从入门到精通</a>
  <a class="navlink" href="index.html">目录</a>
</header>
<main class="container">
__CONTENT__
</main>
<footer class="footer">
  <span>DeerFlow 2.0 从入门到精通</span>
  <span class="muted">基于 huashu-bookwriter 风格整理 · 多页阅读版</span>
</footer>
<script src="app.js"></script>
</body>
</html>"""

def write_page(fname, title, content_inner):
    html = PAGE.replace("__TITLE__", title).replace("__CONTENT__", content_inner)
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)

# ---------- 章节页 ----------
for i, c in enumerate(all_chapters):
    prev_c = all_chapters[i - 1] if i > 0 else None
    next_c = all_chapters[i + 1] if i < len(all_chapters) - 1 else None
    prev_href = prev_c["file"] if prev_c else "index.html"
    next_href = next_c["file"] if next_c else "index.html"
    prev_label = f"§{prev_c['num']:02d} {prev_c['title']}" if prev_c else "返回目录"
    next_label = f"§{next_c['num']:02d} {next_c['title']}" if next_c else "返回目录"

    body_md = "\n".join(c["body"]).strip()
    chap_html = render(body_md)
    inner = f'''<article class="chapter">
{chap_html}
</article>
<nav class="pager">
  <a class="pager-btn" href="{prev_href}">← {prev_label}</a>
  <a class="pager-btn" href="{next_href}">{next_label} →</a>
</nav>'''
    write_page(c["file"], f"§{c['num']:02d} {c['title']} · DeerFlow 2.0", inner)

# ---------- 目录（index） ----------
toc_parts = []
for p in parts:
    items = []
    for c in p["chapters"]:
        items.append(
            f'    <li><a href="{c["file"]}"><span class="ch-no">§{c["num"]:02d}</span>'
            f'<span class="ch-title">{c["title"]}</span></a></li>')
    toc_parts.append(
        f'<div class="part">\n  <h2>Part {p["num"]} · {p["title"]}</h2>\n'
        f'  <ol class="ch-list">\n' + "\n".join(items) + "\n  </ol>\n</div>")
toc_html = "\n".join(toc_parts)

index_inner = f'''<section class="hero">
  <h1>DeerFlow 2.0<br><span class="hero-sub">从入门到精通</span></h1>
  <p class="tagline">一本写给「想用起来、想看懂、想改得动」的人的书。<br>不是官方文档的翻译，是看过源码与规格后的白话拆解。</p>
  <a class="cta" href="01.html">开始阅读 →</a>
  <p class="meta">共 3 大部分 · 19 章 · 按 Part / 章节分页阅读</p>
</section>

<section class="intro">
{pre_html}
</section>

<section class="toc">
  <h2 class="toc-h">目录</h2>
{toc_html}
</section>'''
write_page("index.html", "DeerFlow 2.0 从入门到精通 · 阅读导航", index_inner)

# ---------- 样式 ----------
CSS = """*:not(code,pre){box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:#fbfaf8;color:#20201e;
  font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei","Noto Sans SC",system-ui,sans-serif;
  font-size:17px;line-height:1.85;-webkit-font-smoothing:antialiased}
a{color:#b5482e;text-decoration:none}
a:hover{text-decoration:underline}

.progress{position:fixed;top:0;left:0;height:3px;width:0;background:#b5482e;z-index:50;transition:width .08s linear}

.topbar{position:fixed;top:0;left:0;right:0;height:56px;display:flex;align-items:center;
  justify-content:space-between;padding:0 22px;background:rgba(255,255,255,.92);
  backdrop-filter:saturate(160%) blur(8px);border-bottom:1px solid #e7e3dc;z-index:40}
.brand{font-weight:700;color:#20201e;letter-spacing:.2px}
.brand:hover{text-decoration:none;color:#b5482e}
.navlink{color:#6b6b66;font-size:15px}
.navlink:hover{color:#b5482e}

.container{max-width:780px;margin:0 auto;padding:84px 22px 60px}

/* 索引页 */
.hero{text-align:center;padding:34px 0 26px;border-bottom:1px solid #e7e3dc;margin-bottom:34px}
.hero h1{font-size:40px;line-height:1.2;margin:0 0 6px;font-weight:800;letter-spacing:.5px}
.hero-sub{color:#b5482e}
.tagline{color:#4a4a45;margin:14px auto 22px;max-width:560px;font-size:16px}
.cta{display:inline-block;background:#b5482e;color:#fff;padding:11px 26px;border-radius:8px;
  font-weight:600;font-size:16px;transition:.15s}
.cta:hover{background:#9c3b24;text-decoration:none;transform:translateY(-1px)}
.meta{color:#9a968f;font-size:13px;margin-top:16px}

.intro{background:#fff;border:1px solid #ece8e0;border-radius:12px;padding:26px 30px;margin-bottom:38px}
.intro h2{margin-top:0;font-size:20px}

.toc-h{font-size:22px;margin:0 0 18px}
.part{margin-bottom:26px}
.part h2{font-size:17px;color:#b5482e;margin:0 0 10px;font-weight:700}
.ch-list{list-style:none;margin:0;padding:0}
.ch-list li{margin:0}
.ch-list a{display:flex;align-items:baseline;gap:12px;padding:10px 14px;border:1px solid #ece8e0;
  border-radius:9px;margin-bottom:8px;background:#fff;color:#20201e;transition:.12s}
.ch-list a:hover{border-color:#b5482e;text-decoration:none;transform:translateX(3px);background:#fdf6f3}
.ch-no{font-variant-numeric:tabular-nums;font-weight:700;color:#b5482e;min-width:42px}
.ch-title{flex:1}

/* 章节页 */
.chapter h2{font-size:28px;line-height:1.3;margin:0 0 22px;font-weight:800;
  padding-bottom:14px;border-bottom:2px solid #b5482e}
.chapter h3{font-size:20px;margin:30px 0 12px;font-weight:700}
.chapter h4{font-size:17px;margin:22px 0 8px;font-weight:700;color:#33332f}
.chapter p{margin:14px 0}
.chapter ul,.chapter ol{padding-left:24px;margin:14px 0}
.chapter li{margin:6px 0}

.chapter blockquote{margin:18px 0;padding:12px 18px;border-left:4px solid #b5482e;
  background:#f3e9e4;color:#4a4a45;border-radius:0 8px 8px 0}
.chapter blockquote p{margin:6px 0}

.chapter code{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;
  background:#f0ede8;padding:2px 6px;border-radius:4px;font-size:90%;color:#9c3b24}
.chapter pre{background:#f6f4f1;border:1px solid #e7e3dc;border-radius:8px;
  padding:16px 18px;overflow-x:auto;margin:18px 0;line-height:1.6}
.chapter pre code{background:none;padding:0;color:#2b2b28;font-size:14.5px}

.chapter table{border-collapse:collapse;width:100%;margin:20px 0;font-size:15px;
  background:#fff;border:1px solid #e7e3dc;border-radius:8px;overflow:hidden}
.chapter th,.chapter td{border:1px solid #e7e3dc;padding:10px 13px;text-align:left;vertical-align:top}
.chapter th{background:#f3efe9;font-weight:700}
.chapter tr:nth-child(even) td{background:#faf8f5}

.chapter hr{border:none;border-top:1px solid #e7e3dc;margin:30px 0}

.pager{display:flex;justify-content:space-between;gap:14px;margin-top:46px;
  padding-top:22px;border-top:1px solid #e7e3dc}
.pager-btn{flex:1;text-align:center;padding:13px 10px;border:1px solid #e7e3dc;border-radius:9px;
  background:#fff;color:#20201e;font-size:15px;transition:.12s;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.pager-btn:hover{border-color:#b5482e;color:#b5482e;text-decoration:none;background:#fdf6f3}

.footer{max-width:780px;margin:0 auto;padding:26px 22px 50px;color:#9a968f;font-size:13px;
  display:flex;flex-direction:column;gap:4px;border-top:1px solid #ece8e0}
.footer .muted{color:#bdb9b1}

@media (max-width:560px){
  body{font-size:16px}
  .container{padding:74px 16px 50px}
  .hero h1{font-size:32px}
  .chapter h2{font-size:23px}
  .pager-btn{font-size:13px;padding:11px 6px}
}"""

with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as f:
    f.write(CSS)

JS = """function onScroll(){
  var h=document.documentElement, b=document.body;
  var sc=h.scrollTop||b.scrollTop, height=h.scrollHeight-h.clientHeight;
  var pct=height>0?(sc/height*100):0;
  var bar=document.getElementById('progress');
  if(bar) bar.style.width=pct+'%';
}
window.addEventListener('scroll',onScroll,{passive:true});
onScroll();
var prev=document.querySelector('.pager-btn');
var next=document.querySelectorAll('.pager-btn');
var nxt=next.length>1?next[1]:null;
document.addEventListener('keydown',function(e){
  var t=e.target;
  if(t&&/INPUT|TEXTAREA/.test(t.tagName))return;
  if(e.key==='ArrowLeft'&&prev){window.location.href=prev.href;}
  if(e.key==='ArrowRight'&&nxt){window.location.href=nxt.href;}
});"""
with open(os.path.join(OUT, "app.js"), "w", encoding="utf-8") as f:
    f.write(JS)

print("OK ->", OUT)
print("chapters:", len(all_chapters), "| parts:", len(parts))
for c in all_chapters:
    print(" ", c["file"], "§%02d" % c["num"], c["title"])
