#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
烛龙大数据平台 · GitHub Pages 站点组装脚本

把仓库里的业务原型与业务截图组装成可直接托管的静态站点：

    _site/
      index.html              原型首页（自动取自「配置管理目录功能优化/」下最新的 .html）
      screenshots/
        index.html            业务截图画廊
        *.png                 业务截图原图

用法：
    python publish/build_site.py              # 输出到仓库根目录 _site/
    python publish/build_site.py --out dist   # 输出到指定目录

本脚本只依赖 Python 标准库，可在本地与 GitHub Actions 中直接复用。
"""

from __future__ import annotations

import argparse
import html
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# 原型目录：自动发现其中的 HTML 作为站点首页（换原型 / 改文件名都不必动脚本）
PROTOTYPE_DIR = REPO_ROOT / "配置管理目录功能优化"
# 业务截图目录
SCREENSHOT_SRC = REPO_ROOT / "平台业务截图"


def find_prototype() -> Path | None:
    """在原型目录中定位首页 HTML。存在多个时取最近修改的一个。"""
    if not PROTOTYPE_DIR.is_dir():
        return None
    candidates = sorted(
        (
            p
            for p in PROTOTYPE_DIR.iterdir()
            if p.is_file() and p.suffix.lower() in {".html", ".htm"}
        ),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        return None
    if len(candidates) > 1:
        print(f"[提示] 原型目录内有 {len(candidates)} 个 HTML，取最近修改的：{candidates[0].name}")
        for extra in candidates[1:]:
            print(f"       已忽略：{extra.name}")
    return candidates[0]

# 画廊页配色，与原型主色（#1877f2）保持一致
PAGE_BG = "#f2f6fb"
CARD_BG = "#ffffff"
LINE = "#e3e9f2"
TEXT = "#222b36"
MUTED = "#7a8699"
BLUE = "#1877f2"

# 内联 SVG 图标（目录 / 图层意象），免去额外的图标文件请求
FAVICON = (
    '<link rel="icon" href="data:image/svg+xml,'
    "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E"
    "%3Crect width='32' height='32' rx='7' fill='%231877f2'/%3E"
    "%3Cg fill='none' stroke='white' stroke-width='2' "
    "stroke-linecap='round' stroke-linejoin='round'%3E"
    "%3Cpath d='M16 7.5l8.5 4.3-8.5 4.3-8.5-4.3L16 7.5z'/%3E"
    "%3Cpath d='M8 16.4l8 4.1 8-4.1'/%3E"
    "%3Cpath d='M8 20.6l8 4.1 8-4.1'/%3E"
    "%3C/g%3E%3C/svg%3E\">"
)


def inject_favicon(html_text: str) -> str:
    """在 <head> 后注入站点图标，不改动原型源码本身。"""
    if 'rel="icon"' in html_text:
        return html_text
    idx = html_text.lower().find("<head>")
    if idx == -1:
        return html_text
    at = idx + len("<head>")
    return html_text[:at] + "\n" + FAVICON + html_text[at:]


def write_lf(path: Path, text: str) -> None:
    """统一以 LF 写出，避免 Windows 下生成 CRLF 造成的 diff 噪声。"""
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def build_gallery(titles: list[tuple[str, str]]) -> str:
    """生成业务截图画廊页。titles 为 (文件名, 展示标题) 列表。"""
    cards = []
    for filename, title in titles:
        safe = html.escape(filename)
        cards.append(
            f"""    <figure class="card">
      <a href="{safe}" target="_blank" rel="noopener">
        <img src="{safe}" alt="{html.escape(title)}" loading="lazy">
      </a>
      <figcaption>{html.escape(title)}</figcaption>
    </figure>"""
        )

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="烛龙大数据平台业务截图集。">
{FAVICON}
<title>业务截图 · 烛龙大数据平台</title>
<style>
:root{{--blue:{BLUE};--bg:{PAGE_BG};--card:{CARD_BG};--line:{LINE};--text:{TEXT};--muted:{MUTED}}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--text);font-family:"Microsoft YaHei","PingFang SC",Arial,sans-serif;font-size:14px}}
a{{color:var(--blue);text-decoration:none}}
a:hover{{text-decoration:underline}}
.wrap{{max-width:1280px;margin:0 auto;padding:34px 26px 60px}}
.head{{display:flex;align-items:flex-end;justify-content:space-between;gap:20px;flex-wrap:wrap;margin-bottom:24px}}
h1{{font-size:22px;margin:0 0 8px;letter-spacing:.5px}}
.sub{{color:var(--muted);margin:0;line-height:1.7}}
.back{{font-size:13px;white-space:nowrap}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}}
.card{{margin:0;background:var(--card);border:1px solid var(--line);border-radius:10px;overflow:hidden;box-shadow:0 2px 10px rgba(20,41,67,.05);transition:box-shadow .18s ease,transform .18s ease}}
.card:hover{{box-shadow:0 8px 22px rgba(20,41,67,.12);transform:translateY(-2px)}}
.card img{{display:block;width:100%;height:196px;object-fit:cover;object-position:top center;background:#eef2f7}}
figcaption{{padding:11px 14px;font-size:13px;color:var(--text);border-top:1px solid var(--line)}}
footer{{margin-top:30px;color:var(--muted);font-size:12px;text-align:center}}
</style>
</head>
<body>
<div class="wrap">
  <div class="head">
    <div>
      <h1>烛龙大数据平台 · 业务截图</h1>
      <p class="sub">数据汇聚 / 数据开发 / 数据应用 / 数据资源 / 资产管理 / 系统管理 共 {len(titles)} 张业务界面截图，点击可查看原图。</p>
    </div>
    <a class="back" href="../index.html">← 返回交互原型</a>
  </div>
  <div class="grid">
{chr(10).join(cards)}
  </div>
  <footer>烛龙大数据平台 · 目录配置功能优化原型</footer>
</div>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="组装 GitHub Pages 静态站点")
    parser.add_argument(
        "--out",
        default=str(REPO_ROOT / "_site"),
        help="站点输出目录，默认 _site/",
    )
    args = parser.parse_args()

    out_dir = Path(args.out).resolve()
    shots_dir = out_dir / "screenshots"

    # ---- 1. 原型首页 ----
    prototype_src = find_prototype()
    if prototype_src is None:
        print(f"[错误] 在 {PROTOTYPE_DIR} 下找不到任何 .html 原型文件", file=sys.stderr)
        return 1
    out_dir.mkdir(parents=True, exist_ok=True)
    prototype_html = inject_favicon(prototype_src.read_text(encoding="utf-8"))
    write_lf(out_dir / "index.html", prototype_html)
    print(f"[完成] 原型首页  -> {out_dir / 'index.html'}（源：{prototype_src.name}）")

    # ---- 2. 业务截图 ----
    if not SCREENSHOT_SRC.is_dir():
        print(f"[警告] 业务截图目录不存在，跳过：{SCREENSHOT_SRC}")
        return 0

    shots_dir.mkdir(parents=True, exist_ok=True)
    titles: list[tuple[str, str]] = []
    for src in sorted(SCREENSHOT_SRC.iterdir()):
        if not src.is_file() or src.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
            continue
        shutil.copy2(src, shots_dir / src.name)
        titles.append((src.name, src.stem.replace("_", " ")))

    if titles:
        write_lf(shots_dir / "index.html", build_gallery(titles))
        print(f"[完成] 业务截图  -> {shots_dir}（{len(titles)} 张）")

    print(f"\n站点已组装完毕：{out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
