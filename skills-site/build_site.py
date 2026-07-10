#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《Agent Skills 从入门到精通》-> 多页静态网站 构建脚本
读取 ../Agent Skills 从入门到精通.md
生成 index.html + ch01..ch11.html + appendix.html + style.css
内容严格对齐书稿。
"""
import os, re

SRC = os.path.join(os.path.dirname(__file__), "..", "Agent Skills 从入门到精通.md")
OUT = os.path.join(os.path.dirname(__file__))
SITE_TITLE = "Agent Skills 从入门到精通"

# ---------------------------------------------------------------------------
# 1. 读取与解析头部
# ---------------------------------------------------------------------------
with open(SRC, encoding="utf-8") as f:
    raw = f.read()
if raw.startswith("﻿"):
    raw = raw[1:]
lines = raw.split("\n")

title = lines[0].lstrip("# ").strip()
si = 1
while si < len(lines) and lines[si].strip() == "":
    si += 1
subtitle = lines[si].strip() if si < len(lines) else ""
meta = {}
i = 2
while i < len(lines):
    ln = lines[i]
    if ln.startswith("## Part"):
        break
    m = re.match(r"\*\*(.+?)\*\*\s*:\s*(.+)", ln)
    if m:
        meta[m.group(1)] = m.group(2).strip()
    i += 1

body = lines[i:]

# ---------------------------------------------------------------------------
# 2. 行内/工具函数
# ---------------------------------------------------------------------------
def split_row(s):
    s = s.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]

def inline(text):
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return text

def linkify(text):
    def repl(m):
        num = m.group(1)
        return '<a class="xref" href="ch%s.html">%s</a>' % (num, m.group(0))
    return re.sub(r"§(\d{2})(?:\.\d+)?", repl, text)

def rich(text):
    return linkify(inline(text))

def parse_table(rows):
    header = split_row(rows[0])
    data = [split_row(r) for r in rows[2:]] if len(rows) > 2 else []
    th = "".join("<th>%s</th>" % inline(c) for c in header)
    trs = ""
    for r in data:
        tds = "".join("<td>%s</td>" % rich(c) for c in r)
        trs += "<tr>%s</tr>" % tds
    return ('<div class="table-wrap"><table><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div>') % (th, trs)

# ---------------------------------------------------------------------------
# 3. 主体解析（索引指针，安全）
# ---------------------------------------------------------------------------
parts = []          # {name, intro:[]}
chapters = []       # {id,label,title,part,is_app,blocks:[]}
cur_part = None
cur_ch = None
para_buf = []
footer_mode = False
footer_lines = []
reading_guide_html = None
rg_pending = False

def flush():
    if not para_buf:
        return
    t = "".join(para_buf)
    para_buf.clear()
    if cur_ch is not None:
        cur_ch["blocks"].append(("p", t))
    elif cur_part is not None:
        cur_part["intro"].append(t)

idx = 0
N = len(body)
while idx < N:
    ln = body[idx]
    stripped = ln.strip()

    if footer_mode:
        if stripped:
            footer_lines.append(stripped)
        idx += 1
        continue

    if stripped.startswith("**标叔出品**"):
        flush()
        footer_mode = True
        footer_lines.append(stripped)
        idx += 1
        continue

    # 代码块
    if ln.startswith("```"):
        flush()
        lang = ln[3:].strip()
        code = []
        j = idx + 1
        while j < N and not body[j].startswith("```"):
            code.append(body[j])
            j += 1
        cur_ch["blocks"].append(("code", lang, "\n".join(code)))
        idx = j + 1
        continue

    # 引用块
    if ln.startswith(">"):
        flush()
        qlines = []
        while idx < N and body[idx].startswith(">"):
            qlines.append(re.sub(r"^>\s?", "", body[idx]))
            idx += 1
        cur_ch["blocks"].append(("quote", qlines))
        continue

    # 表格
    if ln.startswith("|"):
        flush()
        trows = []
        while idx < N and body[idx].startswith("|"):
            trows.append(body[idx])
            idx += 1
        html = parse_table(trows)
        cur_ch["blocks"].append(("table", html))
        if rg_pending:
            reading_guide_html = html
            rg_pending = False
        continue

    # 列表
    if re.match(r"^\s*[-*]\s+", ln) or re.match(r"^\s*\d+\.\s+", ln):
        flush()
        items = []
        ordered = bool(re.match(r"^\s*\d+\.\s+", ln))
        while idx < N and (re.match(r"^\s*[-*]\s+", body[idx]) or
                           re.match(r"^\s*\d+\.\s+", body[idx])):
            items.append(re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", body[idx]))
            idx += 1
        cur_ch["blocks"].append(("list", ordered, items))
        continue

    # 子标题
    if ln.startswith("### ") or ln.startswith("#### "):
        flush()
        lvl = 3 if ln.startswith("### ") else 4
        htxt = ln[lvl + 1:].strip()
        if "阅读指南" in htxt:
            rg_pending = True
        cur_ch["blocks"].append(("h", lvl, htxt))
        idx += 1
        continue

    # 章节 / 部分
    if ln.startswith("## "):
        flush()
        head = ln[3:].strip()
        if head.startswith("Part"):
            cur_part = {"name": head, "intro": []}
            parts.append(cur_part)
            cur_ch = None
        elif head.startswith("§") or head == "附录":
            if head == "附录":
                label, full = "附录", "附录 · 生态速查与阅读指南"
                cid, is_app = "appendix", True
            else:
                m = re.match(r"(§\d{2})\s+(.*)", head)
                label, full = m.group(1), head
                cid, is_app = "ch" + head[1:3], False
            if "阅读指南" in head:
                rg_pending = True
            cur_ch = {"id": cid, "label": label, "title": full,
                       "part": cur_part, "is_app": is_app, "blocks": []}
            chapters.append(cur_ch)
        idx += 1
        continue

    if stripped == "" or stripped == "---":
        flush()
        idx += 1
        continue

    # 普通段落行
    para_buf.append(stripped)
    idx += 1

flush()

# first_in_part 标记（用于部分横幅）
for k, ch in enumerate(chapters):
    prev = chapters[k - 1] if k > 0 else None
    ch["first_in_part"] = (prev is None) or (prev["part"] is not ch["part"])

# ---------------------------------------------------------------------------
# 4. 渲染
# ---------------------------------------------------------------------------
def render_block(b):
    t = b[0]
    if t == "p":
        return "<p>%s</p>" % rich(b[1])
    if t == "h":
        return "<h%d class='sub'>%s</h%d>" % (b[1], inline(b[2]), b[1])
    if t == "code":
        lang = b[1]
        code = b[2].replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        badge = ""
        if lang == "bash":
            badge = "<span class='codelang'>BASH</span>"
        elif lang == "python":
            badge = "<span class='codelang'>PYTHON</span>"
        elif lang == "text":
            badge = "<span class='codelang'>文本</span>"
        elif lang == "markdown":
            badge = "<span class='codelang'>MARKDOWN</span>"
        return "<div class='codewrap'>%s<pre><code>%s</code></pre></div>" % (badge, code)
    if t == "quote":
        paras, buf = [], []
        for line in b[1]:
            if line.strip() == "":
                if buf:
                    paras.append("<p>%s</p>" % rich("".join(buf)))
                    buf = []
            else:
                buf.append(line)
        if buf:
            paras.append("<p>%s</p>" % rich("".join(buf)))
        return "<blockquote>%s</blockquote>" % "".join(paras)
    if t == "table":
        return b[1]
    if t == "list":
        tag = "ol" if b[1] else "ul"
        lis = "".join("<li>%s</li>" % rich(it) for it in b[2])
        return "<%s class='bullets'>%s</%s>" % (tag, lis, tag)
    return ""

def render_body(ch):
    out = []
    if ch.get("first_in_part") and ch["part"] is not None:
        p = ch["part"]
        banner = "<div class='part-banner'><div class='part-name'>%s</div>" % inline(p["name"])
        for intro in p["intro"]:
            banner += "<p class='part-lead'>%s</p>" % rich(intro)
        banner += "</div>"
        out.append(banner)
    for b in ch["blocks"]:
        out.append(render_block(b))
    return "\n".join(out)

footer_html = ""
if footer_lines:
    footer_html = "<footer class='site-footer'><p>%s</p></footer>" % (
        "</p><p>".join(inline(x) for x in footer_lines))

order = ["index.html"] + [c["id"] + ".html" for c in chapters]

# ---------------------------------------------------------------------------
# 5. 模板
# ---------------------------------------------------------------------------
CSS = """\
:root{
  --bg:#fbfaf7; --paper:#ffffff; --ink:#1f2024; --muted:#6b7280;
  --accent:#b45309; --accent-2:#7c2d12; --soft:#fdf3e7;
  --line:#ece7dd; --code-bg:#2a2f37; --code-fg:#e8e6e1; --maxw:780px;
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0;background:var(--bg);color:var(--ink);
  font-family:"PingFang SC","Microsoft YaHei","Hiragino Sans GB",system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  font-size:17px;line-height:1.9;}
a{color:var(--accent);text-decoration:none;}
a:hover{text-decoration:underline;}
.wrap{max-width:var(--maxw);margin:0 auto;padding:32px 22px 80px;}
#progress{position:fixed;top:0;left:0;height:3px;width:0;background:var(--accent);z-index:50;transition:width .1s;}
.topbar{position:sticky;top:0;z-index:40;display:flex;align-items:center;justify-content:space-between;
  gap:12px;padding:11px 18px;background:rgba(251,250,247,.86);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line);font-size:14px;}
.topbar .nav-home{font-weight:600;color:var(--accent);white-space:nowrap;}
.topbar .nav-cur{color:var(--muted);font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.topbar .nav-pn{display:flex;gap:6px;white-space:nowrap;}
.topbar .nav-pn a{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;
  border:1px solid var(--line);border-radius:8px;background:var(--paper);color:var(--ink);font-size:16px;}
.topbar .nav-pn a:hover{text-decoration:none;border-color:var(--accent);color:var(--accent);}
.topbar .nav-pn span.disabled{display:inline-flex;align-items:center;justify-content:center;width:30px;height:30px;
  border:1px solid var(--line);border-radius:8px;color:#cbd0d6;}
h1.chapter-title{font-size:30px;line-height:1.3;margin:8px 0 4px;letter-spacing:.01em;}
.chapter-kicker{color:var(--accent);font-weight:700;letter-spacing:.06em;font-size:14px;}
.part-banner{background:var(--soft);border:1px solid var(--line);border-left:4px solid var(--accent);
  border-radius:12px;padding:18px 22px;margin:8px 0 30px;}
.part-banner .part-name{font-weight:700;color:var(--accent-2);letter-spacing:.04em;}
.part-lead{color:#5b4632;margin:8px 0 0;font-size:15.5px;}
h3.sub{font-size:21px;margin:38px 0 10px;padding-bottom:6px;border-bottom:1px solid var(--line);}
h4.sub{font-size:18px;margin:26px 0 8px;color:var(--accent-2);}
p{margin:16px 0;}
strong{color:#111;font-weight:700;}
.xref{font-weight:600;border-bottom:1px dotted var(--accent);}
blockquote{background:var(--soft);border-left:4px solid var(--accent);border-radius:0 10px 10px 0;
  padding:14px 20px;margin:22px 0;}
blockquote p{margin:8px 0;}
.bullets{margin:16px 0;padding-left:24px;}
.bullets li{margin:7px 0;}
.codewrap{position:relative;margin:20px 0;}
.codelang{position:absolute;top:-10px;right:12px;background:var(--accent);color:#fff;
  font-size:11px;font-weight:700;letter-spacing:.06em;padding:2px 8px;border-radius:6px;}
pre{background:var(--code-bg);color:var(--code-fg);border-radius:10px;padding:18px 18px;
  overflow-x:auto;font-size:14px;line-height:1.65;margin:0;}
pre code{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;}
code{background:#f1ede4;color:#7c2d12;padding:1px 6px;border-radius:5px;font-size:.92em;
  font-family:"SFMono-Regular",Consolas,Menlo,monospace;}
.codewrap pre code{background:none;color:inherit;padding:0;border-radius:0;}
.table-wrap{overflow-x:auto;margin:22px 0;}
table{border-collapse:collapse;width:100%;font-size:15px;background:var(--paper);}
th,td{border:1px solid var(--line);padding:9px 12px;text-align:left;vertical-align:top;}
th{background:var(--soft);color:var(--accent-2);font-weight:700;}
tbody tr:nth-child(even){background:#fcfbf8;}
.nav-foot{display:flex;justify-content:space-between;gap:12px;margin-top:48px;
  padding-top:22px;border-top:1px solid var(--line);}
.nav-foot a{display:inline-flex;align-items:center;gap:6px;font-weight:600;
  border:1px solid var(--line);border-radius:10px;padding:10px 16px;background:var(--paper);color:var(--ink);}
.nav-foot a:hover{text-decoration:none;border-color:var(--accent);color:var(--accent);}
.nav-foot .grow{flex:1;}
.site-footer{text-align:center;color:var(--muted);font-size:13px;line-height:1.8;
  max-width:var(--maxw);margin:60px auto 0;padding:24px 22px;border-top:1px solid var(--line);}
.hero{background:linear-gradient(180deg,#ffffff 0%,#fbfaf7 100%);border-bottom:1px solid var(--line);
  padding:66px 22px 46px;text-align:center;}
.hero .kicker{color:var(--accent);font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:13px;}
.hero h1{font-size:42px;line-height:1.22;margin:12px auto 8px;max-width:760px;}
.hero .sub{color:var(--muted);font-size:19px;max-width:620px;margin:0 auto;}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-top:22px;}
.chip{background:var(--soft);border:1px solid var(--line);border-radius:999px;padding:5px 13px;font-size:13px;color:#5b4632;}
.intro{max-width:var(--maxw);margin:0 auto;padding:30px 22px 0;text-align:center;color:#374151;font-size:16.5px;}
.toc{max-width:var(--maxw);margin:0 auto;padding:26px 22px 0;}
.part{margin-top:34px;}
.part h2{font-size:14px;letter-spacing:.1em;color:var(--accent);text-transform:uppercase;
  border-bottom:2px solid var(--line);padding-bottom:9px;margin:0 0 6px;}
.part .lead{color:var(--muted);font-size:14.5px;margin:10px 0 16px;}
.clink{display:flex;gap:14px;align-items:baseline;padding:13px 16px;border:1px solid var(--line);
  border-radius:12px;margin-bottom:11px;background:var(--paper);transition:.15s;}
.clink:hover{transform:translateY(-1px);box-shadow:0 8px 20px rgba(0,0,0,.06);text-decoration:none;}
.clink .num{font-weight:800;color:var(--accent);min-width:48px;font-variant-numeric:tabular-nums;}
.clink .ttl{color:var(--ink);}
.guide{max-width:var(--maxw);margin:0 auto;padding:34px 22px 0;}
.guide h2{font-size:22px;margin:0 0 12px;}
@media(max-width:600px){.hero h1{font-size:32px;}.wrap{padding-top:24px;}}
"""

PAGE = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__TITLE__</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div id="progress"></div>
<div class="topbar">
  <a class="nav-home" href="index.html">← 目录</a>
  <span class="nav-cur">__LABEL__</span>
  <span class="nav-pn">__PN__</span>
</div>
<main class="wrap">
<div class="chapter-kicker">__KICKER__</div>
<h1 class="chapter-title">__TITLEBODY__</h1>
__BANNER__
__BODY__
<div class="nav-foot">__FOOTNAV__</div>
</main>
__FOOTER__
<script>
var bar=document.getElementById('progress');
addEventListener('scroll',function(){var h=document.documentElement;var sc=h.scrollTop/(h.scrollHeight-h.clientHeight||1);bar.style.width=(sc*100)+'%';});
</script>
</body>
</html>"""

def nav_pn(cur_id):
    ix = order.index(cur_id)
    prev = order[ix - 1] if ix > 0 else None
    nxt = order[ix + 1] if ix + 1 < len(order) else None
    s = ""
    s += '<a href="%s" title="上一页">←</a>' % prev if prev else '<span class="disabled">←</span>'
    s += '<a href="%s" title="下一页">→</a>' % nxt if nxt else '<span class="disabled">→</span>'
    return s

def foot_nav(cur_id):
    ix = order.index(cur_id)
    prev = order[ix - 1] if ix > 0 else None
    nxt = order[ix + 1] if ix + 1 < len(order) else None
    left = '<a href="%s">← 上一页</a>' % prev if prev else '<span class="grow"></span>'
    right = '<a href="%s">下一页 →</a>' % nxt if nxt else '<span class="grow"></span>'
    return left + right

# ---------------------------------------------------------------------------
# 6. 生成各章
# ---------------------------------------------------------------------------
for ch in chapters:
    cid = ch["id"]
    kicker = ("第 %s 章" % ch["label"].replace("§", "")) if not ch["is_app"] else "附录"
    body_html = render_body(ch)
    html = (PAGE
             .replace("__TITLE__", "%s | %s" % (ch["title"], SITE_TITLE))
             .replace("__LABEL__", ch["label"])
             .replace("__TITLEBODY__", ch["title"])
             .replace("__KICKER__", kicker)
             .replace("__BANNER__", "")
             .replace("__BODY__", body_html)
             .replace("__PN__", nav_pn(cid + ".html"))
             .replace("__FOOTNAV__", foot_nav(cid + ".html"))
             .replace("__FOOTER__", footer_html))
    with open(os.path.join(OUT, cid + ".html"), "w", encoding="utf-8") as f:
        f.write(html)

# ---------------------------------------------------------------------------
# 7. 生成 index.html
# ---------------------------------------------------------------------------
chips = ""
for k in ("创建者", "为谁创建", "最后更新"):
    if k in meta:
        chips += "<span class='chip'>%s：%s</span>" % (k, meta[k])
if "基于" in meta:
    chips += "<span class='chip'>基于：%s</span>" % meta["基于"]

toc = ""
for p in parts:
    toc += "<div class='part'><h2>%s</h2>" % inline(p["name"])
    if p["intro"]:
        toc += "<p class='lead'>%s</p>" % rich("".join(p["intro"]))
    for ch in [c for c in chapters if c["part"] is p]:
        ttl = ch["title"]
        if ttl.startswith(ch["label"]):
            ttl = ttl[len(ch["label"]):].strip()
        toc += ("<a class='clink' href='%s.html'><span class='num'>%s</span>"
                "<span class='ttl'>%s</span></a>") % (ch["id"], ch["label"], ttl)
    toc += "</div>"

guide = ""
if reading_guide_html:
    guide = "<div class='guide'><h2>四天阅读指南</h2>%s</div>" % reading_guide_html

index_html = """<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>__SITETITLE__</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<div id="progress"></div>
<header class="hero">
  <div class="kicker">AI Native Coder · 标叔</div>
  <h1>__TITLE__</h1>
  <div class="sub">__SUBTITLE__</div>
  <div class="chips">__CHIPS__</div>
</header>
<p class="intro">这是一本写给普通开发者、产品经理、业务专家与创业者的 Agent Skills 通俗指南。读完你能自己造、自己串、自己沉淀技能——从“人学界面”切换到“Agent 直接拿结果”。</p>
<section class="toc">
  <h2 style="font-size:14px;letter-spacing:.1em;color:var(--accent);text-transform:uppercase;border-bottom:2px solid var(--line);padding-bottom:9px;">总目录</h2>
  __TOC__
</section>
__GUIDE__
__FOOTER__
<script>
var bar=document.getElementById('progress');
addEventListener('scroll',function(){var h=document.documentElement;var sc=h.scrollTop/(h.scrollHeight-h.clientHeight||1);bar.style.width=(sc*100)+'%';});
</script>
</body>
</html>"""
index_html = (index_html
    .replace("__SITETITLE__", SITE_TITLE)
    .replace("__TITLE__", title)
    .replace("__SUBTITLE__", subtitle)
    .replace("__CHIPS__", chips)
    .replace("__TOC__", toc)
    .replace("__GUIDE__", guide)
    .replace("__FOOTER__", footer_html))

with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

with open(os.path.join(OUT, "style.css"), "w", encoding="utf-8") as f:
    f.write(CSS)

print("DONE. chapters=%d parts=%d footer=%d reading_guide=%s" % (
    len(chapters), len(parts), len(footer_lines), reading_guide_html is not None))
