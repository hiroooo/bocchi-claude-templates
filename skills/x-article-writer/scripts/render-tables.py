#!/usr/bin/env python3
"""
X Articles 用 table 画像 (PNG) 量産スクリプト.

Usage:
    python3 render-tables.py <tables_dir>

<tables_dir> 配下の table-*.html を全て PNG 化する.
- _styles.css は templates/table-styles.css をシンボリックリンク or コピーで配置すること.
- 出力 PNG は body の自然高さで clip され余白なし.
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    if len(sys.argv) < 2:
        print("Usage: render-tables.py <tables_dir>")
        sys.exit(1)
    base = Path(sys.argv[1]).resolve()
    if not base.exists():
        print(f"Directory not found: {base}")
        sys.exit(1)

    htmls = sorted(base.glob("table-*.html"))
    if not htmls:
        print(f"No table-*.html found in {base}")
        sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for html in htmls:
            page = browser.new_page(
                viewport={"width": 1500, "height": 800},
                device_scale_factor=2,
            )
            page.goto(f"file://{html}")
            page.wait_for_load_state("networkidle")
            body_height = page.evaluate("document.body.getBoundingClientRect().height")
            png = html.with_suffix(".png")
            page.screenshot(
                path=str(png),
                full_page=False,
                clip={"x": 0, "y": 0, "width": 1500, "height": int(body_height)},
            )
            print(f"  {html.name} → {png.name} ({int(body_height)}px)")
            page.close()
        browser.close()

    print(f"\nDone: {len(htmls)} PNGs")


if __name__ == "__main__":
    main()
