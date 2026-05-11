#!/usr/bin/env python3
"""
render-flow.py — X Articles + 通常投稿 投稿フロー HTML 生成

x-article-writer skill の Phase 9 で呼ばれる。
入力: article.md + post.txt (Main + Reply 1-N)
出力: flow.html (side TOC + 各セクション コピペボタン付き、X dark theme)

Usage:
    python3 ~/.claude/skills/x-article-writer/scripts/render-flow.py \
        --article apps/<app>/.scratch/<post-folder>/article.md \
        --post    apps/<app>/.scratch/<post-folder>/post.txt \
        --output  apps/<app>/.scratch/<post-folder>/flow.html \
        --cover   branding/sns-bocchi/reference-images/character_desk_focus.png \
        --main-image apps/<app>/.scratch/<post-folder>/main-image.png \
        --title   "X Articles + 通常投稿 投稿フロー" \
        --subtitle "2026-05-08 — 〇〇 記事" \
        --strategy "X Articles 先 → URL 置換 → 通常投稿でセルフリプ末誘導" \
        --goal     "フォロワー獲得 (Premium+ 4倍 + 75x リプ往復 + dwell time max)" \
        --duration "30-40 分"
"""
from __future__ import annotations
import argparse
import html as html_mod
import json
import os
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL_ROOT / "templates" / "flow-template.html"


def x_weight(s: str) -> int:
    """X の weight (ASCII×1 + 全角×2)"""
    return sum(2 if ord(c) > 127 else 1 for c in s)


def chars_no_ws(s: str) -> int:
    """空白/改行除く文字数"""
    return len([c for c in s if c not in "\n\r\t "])


def markdown_to_x_plain(md: str) -> str:
    """article.md を X Articles エディタ (リッチテキスト) に直接貼れるプレーン版に変換。
    Markdown 記号 (## > ** _ ` -) を除去し、--- 区切り線を空行に、リンクは `text URL` 形式に。
    X Articles 上では toolbar で見出し / 引用 / リストを手動適用する前提。
    """
    s = md
    # H1 (記事タイトル) は X Articles の title フィールドが別なので本文からは削除
    s = re.sub(r'^# .+\n', '', s, count=1, flags=re.M)
    # 見出し記号を削除 (X エディタで H2/H3 を手動適用)
    s = re.sub(r'^#{2,6}\s+', '', s, flags=re.M)
    # 太字 / italic
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(r'(?<!\*)\*(?!\*)(.+?)\*(?!\*)', r'\1', s)
    s = re.sub(r'(?<!_)_(?!_)([^_]+?)_(?!_)', r'\1', s)
    # 引用 `>` 行頭マーク削除 (X エディタで引用を手動適用)
    s = re.sub(r'^> ?', '', s, flags=re.M)
    # リンク [text](url) → text URL
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1 \2', s)
    # インラインコード backtick
    s = re.sub(r'`([^`]+)`', r'\1', s)
    # `---` 区切り線を空行に (X エディタには区切り線機能なし)
    s = re.sub(r'^---\s*$', '', s, flags=re.M)
    # 連続改行を最大 2 行に圧縮
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip() + '\n'


def parse_post_sections(post_txt: str) -> list[dict]:
    """post.txt を === N === で切り分け、[{title, body}, ...] を返す"""
    parts = re.split(r"^=== ([^=]+?) ?===\s*\n?", post_txt, flags=re.M)
    items = []
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        items.append({"title": title, "body": body})
    return items


def extract_time(title: str) -> str:
    """タイトルから H:MM を抽出 (例: 'Reply 1 (19:01) — ...' → '19:01')"""
    m = re.search(r"(\d{1,2}:\d{2})", title)
    return m.group(1) if m else ""


def render_review_block(review: dict | None) -> tuple[str, str]:
    """review.json から レビューカード HTML + TOC li を生成。
    なければ ('', '') を返す。

    review.json schema:
    {
      "axes": [
        {"id": "A", "name": "整合性", "max": 4, "score": 4,
         "checks": [{"item": "...", "result": "PASS|FAIL|NEEDS|WARN", "note": "..."}],
         "observations": "..."},
        ...
      ],
      "regen_rounds": 0,
      "regen_log": ["round 1: ..."],
      "summary": "..."  (任意)
    }
    """
    if not review or not review.get("axes"):
        return "", ""

    axes = review["axes"]
    total_score = sum(a.get("score", 0) for a in axes)
    total_max = sum(a.get("max", 0) for a in axes)
    regen_rounds = review.get("regen_rounds", 0)

    # TOC item
    toc_li = f'      <li><a href="#review-step"><span class="step-num-mini">📊</span>レビュー <span style="color:var(--accent);font-family:monospace;">{total_score}/{total_max}</span></a></li>\n'

    # Tab buttons
    tab_btns = []
    tab_contents = []
    for i, ax in enumerate(axes):
        ax_id = ax.get("id", chr(65 + i))
        ax_name = ax.get("name", ax_id)
        score = ax.get("score", 0)
        max_ = ax.get("max", 0)
        active = "active" if i == 0 else ""
        rtab_id = f"rev-{ax_id}"
        tab_btns.append(
            f'<button class="rtab-btn {active}" data-rtab="{rtab_id}">{html_mod.escape(ax_id)}. {html_mod.escape(ax_name)}'
            f'<span class="rscore">{score}/{max_}</span></button>'
        )

        # check rows
        check_rows = []
        for ch in ax.get("checks", []):
            judge = ch.get("result", "?")
            check_rows.append(
                f'<tr><td>{html_mod.escape(ch.get("item", ""))}</td>'
                f'<td class="judge {html_mod.escape(judge)}">{html_mod.escape(judge)}</td>'
                f'<td>{html_mod.escape(ch.get("note", ""))}</td></tr>'
            )
        observations = ax.get("observations", "")
        obs_html = ""
        if observations:
            obs_html = f'<div class="observations"><span class="label">観点 / コメント</span>{html_mod.escape(observations)}</div>'

        tab_contents.append(
            f'<div class="rtab-content {active}" id="{rtab_id}">\n'
            f'  <table class="review-table"><thead><tr><th style="width:30%">チェック項目</th><th style="width:80px">判定</th><th>観点</th></tr></thead>\n'
            f'  <tbody>{"".join(check_rows)}</tbody></table>\n'
            f'  {obs_html}\n'
            f'</div>'
        )

    # External reviews (Phase 7-E)
    for ext in review.get("external_reviews", []):
        skill_name = ext.get("skill", "?")
        rtab_id = f"rev-ext-{skill_name.replace('/', '-').replace(' ', '-')}"
        verdict = ext.get("verdict", "?")
        score = ext.get("score", "")
        focus = ext.get("focus", "")
        tab_btns.append(
            f'<button class="rtab-btn" data-rtab="{rtab_id}">🛠 {html_mod.escape(skill_name)}'
            f'<span class="rscore">{html_mod.escape(verdict)}</span></button>'
        )
        finding_rows = []
        for f in ext.get("findings", []):
            judge = f.get("result", "?")
            finding_rows.append(
                f'<tr><td>{html_mod.escape(f.get("item", ""))}</td>'
                f'<td class="judge {html_mod.escape(judge)}">{html_mod.escape(judge)}</td>'
                f'<td>{html_mod.escape(f.get("note", ""))}</td></tr>'
            )
        observations = ext.get("observations", "")
        obs_html = f'<div class="observations"><span class="label">観点 / コメント</span>{html_mod.escape(observations)}</div>' if observations else ""
        actions = ext.get("actions_taken", [])
        actions_html = ""
        if actions:
            li_html = "".join(f'<li>{html_mod.escape(a)}</li>' for a in actions)
            actions_html = f'<div style="margin-top:10px;"><span class="label" style="display:block;color:var(--muted);font-size:11px;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:4px;">この skill の指摘で取った対策</span><ol class="regen-log">{li_html}</ol></div>'

        score_html = f'<span class="pill">{html_mod.escape(score)}</span>' if score else ""
        verdict_class = "ok" if verdict == "PASS" else ("warn" if verdict in ("FAIL", "NEEDS") else "")
        head_html = (
            f'<div class="review-summary" style="margin-bottom:12px;">'
            f'<span class="pill {verdict_class}">{html_mod.escape(verdict)}</span>'
            f'{score_html}'
            f'<span class="pill">📋 観点: {html_mod.escape(focus)}</span>'
            f'</div>'
        )
        tab_contents.append(
            f'<div class="rtab-content" id="{rtab_id}">\n  {head_html}\n'
            f'  <table class="review-table"><thead><tr><th style="width:30%">観点</th><th style="width:80px">判定</th><th>所見</th></tr></thead>\n'
            f'  <tbody>{"".join(finding_rows)}</tbody></table>\n'
            f'  {obs_html}\n'
            f'  {actions_html}\n'
            f'</div>'
        )

    # Summary tab
    regen_li = "".join(f'<li>{html_mod.escape(s)}</li>' for s in review.get("regen_log", []))
    summary_text = review.get("summary", "")
    summary_html = f'<p>{html_mod.escape(summary_text)}</p>' if summary_text else ""
    regen_html = f'<p style="font-size:13px;color:var(--muted);margin:8px 0 4px;">REGEN ループ: <b style="color:var(--text);">{regen_rounds}</b> 周</p>'
    if regen_li:
        regen_html += f'<ol class="regen-log">{regen_li}</ol>'
    tab_btns.append(
        f'<button class="rtab-btn" data-rtab="rev-summary">📋 総合<span class="rscore">{total_score}/{total_max}</span></button>'
    )
    tab_contents.append(
        f'<div class="rtab-content" id="rev-summary">\n  {summary_html}\n  {regen_html}\n</div>'
    )

    # Pills
    overall_class = "ok" if total_score == total_max else ("warn" if total_score < total_max * 0.75 else "")
    pills_html = (
        f'<span class="pill {overall_class}">合計 {total_score}/{total_max}</span>'
        f'<span class="pill">REGEN {regen_rounds} 周</span>'
    )
    for ax in axes:
        ax_class = "ok" if ax.get("score", 0) == ax.get("max", 0) else ""
        pills_html += f'<span class="pill {ax_class}">{html_mod.escape(ax.get("id", ""))}. {html_mod.escape(ax.get("name", ""))} {ax.get("score", 0)}/{ax.get("max", 0)}</span>'

    block = f"""<div class="step review-step" id="review-step">
      <div class="step-head">
        <span class="step-num">📊</span>
        <h2>レビュー (4 軸スコアリング)</h2>
        <span class="time">{total_score}/{total_max}</span>
      </div>
      <div class="review-summary">{pills_html}</div>
      <div class="review-tabs">{"".join(tab_btns)}</div>
      {"".join(tab_contents)}
    </div>"""

    return block, toc_li


def render_copy_block(
    idx: str,
    label: str,
    body: str,
    weight: int | None = None,
    display_name: str = "ボッチ社長エンジニア",
    handle: str = "@bocchistay",
    avatar_rel: str = "",
) -> str:
    w = weight if weight is not None else x_weight(body)
    body_esc = html_mod.escape(body)
    tweet_time = extract_time(label)
    time_html = f'<span class="tw-time">· {html_mod.escape(tweet_time)}</span>' if tweet_time else ""
    avatar_style = f"background-image: url('{html_mod.escape(avatar_rel)}');" if avatar_rel else ""
    return f"""<div class="copy-block" id="reply-{idx}-block">
      <div class="copy-head">
        <span class="label">{html_mod.escape(label)}</span>
        <span class="weight">{w} weight</span>
        <button class="copy-btn" data-target="reply-{idx}">📋 コピー</button>
      </div>
      <div class="tabs">
        <button class="tab-btn active" data-tab="reply-{idx}-text">プレーン</button>
        <button class="tab-btn" data-tab="reply-{idx}-tweet">👁 ツイート</button>
      </div>
      <div class="tab-content active" id="reply-{idx}-text">
        <pre id="reply-{idx}">{body_esc}</pre>
      </div>
      <div class="tab-content" id="reply-{idx}-tweet">
        <div class="tweet-preview">
          <div class="tw-avatar" style="{avatar_style}"></div>
          <div>
            <div class="tw-head">
              <span class="tw-name">{html_mod.escape(display_name)}</span>
              <span class="tw-handle">{html_mod.escape(handle)}</span>
              {time_html}
            </div>
            <div class="tw-content">{body_esc}</div>
            <div class="tw-actions">
              <span>💬</span><span>🔁</span><span>♡</span><span>📊</span><span>⤴</span>
            </div>
          </div>
        </div>
      </div>
    </div>"""


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--article", default="", help="article.md path (任意。未指定なら X Articles step は省略され、通常投稿のみのフローになる)")
    p.add_argument("--post", required=True, help="post.txt path (Main + Reply 1-N)")
    p.add_argument("--output", required=True, help="flow.html output path")
    p.add_argument("--cover", default="", help="Cover image path (Articles 用)")
    p.add_argument("--main-image", dest="main_image", default="main-image.png", help="メイン投稿の添付画像 path (flow.html からの相対 path も可)")
    p.add_argument("--bocchi-avatar", dest="bocchi_avatar", default="", help="ヘッダーに飾るボッチアイコン画像 path。未指定なら branding/sns-bocchi/reference-images/character_100knock_header.png を自動採用")
    p.add_argument("--review", default="", help="review.json path (Phase 7 の 4 軸スコアを記録した JSON、未指定ならレビューカード非表示)")
    p.add_argument("--title", default="X Articles + 通常投稿 投稿フロー", help="HTML タイトル")
    p.add_argument("--subtitle", default="", help="HTML サブタイトル (日付 + 記事名)")
    p.add_argument("--strategy", default="X Articles 先 → URL 置換 → 通常投稿でセルフリプ末誘導", help="戦略短文")
    p.add_argument("--goal", default="フォロワー獲得 (Premium+ 4倍 + 75x リプ往復 + dwell time max)", help="狙い短文")
    p.add_argument("--duration", default="30-40 分", help="所要時間")
    args = p.parse_args()

    post_path = Path(args.post).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()

    if not post_path.exists():
        sys.exit(f"post.txt not found: {post_path}")
    if not TEMPLATE.exists():
        sys.exit(f"template not found: {TEMPLATE}")

    has_article = bool(args.article)
    article = ""
    article_title = ""
    article_body = ""
    article_x_plain = ""
    if has_article:
        article_path = Path(args.article).expanduser().resolve()
        if not article_path.exists():
            sys.exit(f"article not found: {article_path}")
        article = article_path.read_text()
        m = re.search(r"^# (.+)$", article, re.M)
        article_title = m.group(1) if m else "(no title)"
        article_body = article[m.end():].lstrip() if m else article
        # X Articles 用プレーン版 (Markdown 記号除去) を自動生成
        article_x_plain = markdown_to_x_plain(article)

    post_txt = post_path.read_text()
    template = TEMPLATE.read_text()

    # post.txt sections
    sections = parse_post_sections(post_txt)
    main_idx = next((i for i, it in enumerate(sections) if it["title"].startswith("Main")), 0)

    # Bocchi avatar: --bocchi-avatar 指定があればそれ、なければ branding 既定アイコン
    bocchi_default = Path.home() / "project/<app-factory>/branding/sns-bocchi/reference-images/character_100knock_header.png"
    bocchi_src = Path(args.bocchi_avatar).expanduser().resolve() if args.bocchi_avatar else bocchi_default
    bocchi_avatar_rel = ""
    if bocchi_src.exists():
        bocchi_avatar_rel = os.path.relpath(bocchi_src, output_path.parent)

    main_block = render_copy_block(str(main_idx), sections[main_idx]["title"], sections[main_idx]["body"], avatar_rel=bocchi_avatar_rel)
    reply_blocks_html = "".join(
        render_copy_block(str(i), s["title"], s["body"], avatar_rel=bocchi_avatar_rel) for i, s in enumerate(sections) if i != main_idx
    )

    # TOC reply items
    toc_reply_items = "".join(
        f'          <li><a href="#reply-{i}-block">{html_mod.escape(s["title"])}</a></li>\n'
        for i, s in enumerate(sections) if i != main_idx
    )

    # Cover image: 出力 HTML からの相対 path に変換 (なければそのまま、無効でも壊れない)
    cover_rel = ""
    if args.cover:
        cover_abs = Path(args.cover).expanduser().resolve()
        if cover_abs.exists():
            cover_rel = os.path.relpath(cover_abs, output_path.parent)

    # Main image: cover と同じく cwd 起点 / 絶対 path を resolve、flow.html 同ディレクトリ起点もフォールバック対応
    main_image_rel = ""
    if args.main_image:
        main_image_abs = Path(args.main_image).expanduser().resolve()
        if not main_image_abs.exists():
            fallback = (output_path.parent / args.main_image).resolve()
            if fallback.exists():
                main_image_abs = fallback
        if main_image_abs.exists():
            main_image_rel = os.path.relpath(main_image_abs, output_path.parent)

    # ARTICLE_STEPS / TOC: article 有無で出し分け
    article_steps_html = ""
    article_toc_items = ""
    main_step_num = "1"
    tail_step_num = "2"
    if has_article:
        cover_block = ""
        if cover_rel:
            cover_block = f"""<div class="image-card">
        <div class="thumb" style="background-image: url('{html_mod.escape(cover_rel)}');"></div>
        <div class="info">
          <div class="label">📷 Cover image (Articles 用)</div>
          <code>{html_mod.escape(args.cover or '(なし)')}</code>
        </div>
        <div class="actions">
          <a class="download-btn" href="{html_mod.escape(cover_rel)}" download>⬇ DL</a>
        </div>
      </div>"""
        article_steps_html = f"""<div class="step" id="step1">
      <div class="step-head">
        <span class="step-num">1</span>
        <h2>X Articles を投稿</h2>
        <span class="time">~10 分</span>
      </div>
      <p class="note">X.com のホームから投稿エディタを開いて「Article」モードに切り替え。Premium+ 加入者なら使える。</p>

      <div class="copy-block" id="article-title-block">
        <div class="copy-head">
          <span class="label">📝 Article タイトル</span>
          <span class="weight">{x_weight(article_title)} weight / {len(article_title)} 文字</span>
          <button class="copy-btn" data-target="article-title">📋 コピー</button>
        </div>
        <pre id="article-title">{html_mod.escape(article_title)}</pre>
      </div>

      <div class="copy-block" id="article-body-block">
        <div class="copy-head">
          <span class="label">📄 Article 本文</span>
          <span class="weight">{x_weight(article)} weight / {chars_no_ws(article)} 文字</span>
          <button class="copy-btn rich-html" data-html-target="article-body-rich-source" data-plain-target="article-x-plain">✨ HTML リッチコピー</button>
        </div>
        <div class="tabs">
          <button class="tab-btn active" data-tab="article-body-rich">✨ HTML リッチペースト (推奨)</button>
          <button class="tab-btn" data-tab="article-body-x-plain">📋 X 用プレーン</button>
          <button class="tab-btn" data-tab="article-body-md">Markdown (参考)</button>
        </div>
        <div class="tab-content active" id="article-body-rich">
          <p class="note" style="margin: 0; border-radius: 0;">✨ X Articles エディタは Draft.js ベースで <b>HTML を貼ると見出し / 引用 / リスト / 太字を自動展開</b>する。上の「✨ HTML リッチコピー」ボタンで <b>text/html を含めてクリップボードに書き込み</b>、X 下書きに貼るとフォーマット込みで入る。失敗したら 📋 X 用プレーン タブにフォールバック</p>
          <div class="md-preview" id="article-body-rich-source" data-md-source="article-body"></div>
        </div>
        <div class="tab-content" id="article-body-x-plain">
          <p class="note warn" style="margin: 0; border-radius: 0;">⚠️ HTML リッチコピーが失敗した時のフォールバック。X 下書きに貼って toolbar で見出し / 引用 / リストを手動適用</p>
          <pre id="article-x-plain" class="tall">{html_mod.escape(article_x_plain)}</pre>
        </div>
        <div class="tab-content" id="article-body-md">
          <pre id="article-body" class="tall">{html_mod.escape(article_body)}</pre>
        </div>
      </div>

      {cover_block}
      <p class="note warn">⚠️ 公開後に <b>Articles URL をコピー</b> して Step 2 で使う</p>
    </div>

    <div class="step" id="step2">
      <div class="step-head">
        <span class="step-num">2</span>
        <h2>post.txt の URL プレースホルダを置換</h2>
        <span class="time">1 分</span>
      </div>
      <p>Step 1 でコピーした Articles URL で <code>&lt;&lt;&lt;X_ARTICLES_URL_HERE&gt;&gt;&gt;</code> を置換。</p>
      <p class="note">手動置換が手間なら、Step 3 のセルフリプ末を X 上で直接編集して URL を貼り付けても OK。</p>
    </div>"""
        article_toc_items = (
            '      <li><a href="#step1"><span class="step-num-mini">1</span>X Articles 投稿</a>\n'
            '        <ol class="sub">\n'
            '          <li><a href="#article-title-block">タイトル</a></li>\n'
            '          <li><a href="#article-body-block">本文</a></li>\n'
            '        </ol>\n'
            '      </li>\n'
            '      <li><a href="#step2"><span class="step-num-mini">2</span>URL 置換</a></li>\n'
        )
        main_step_num = "3"
        tail_step_num = "4"

    # Main image card (添付画像があるときだけ)
    main_image_card = ""
    if main_image_rel:
        main_image_card = f"""<div class="image-card">
        <div class="thumb" style="background-image: url('{html_mod.escape(main_image_rel)}');"></div>
        <div class="info">
          <div class="label">📷 メイン投稿 添付画像</div>
          <code>{html_mod.escape(args.main_image)}</code>
        </div>
        <div class="actions">
          <a class="download-btn" href="{html_mod.escape(main_image_rel)}" download>⬇ DL</a>
        </div>
      </div>"""

    # Review JSON 読み込み (任意)
    review_data = None
    if args.review:
        review_path = Path(args.review).expanduser().resolve()
        if review_path.exists():
            try:
                review_data = json.loads(review_path.read_text())
            except json.JSONDecodeError as e:
                print(f"⚠️  review.json parse error: {e}", file=sys.stderr)
    review_block, review_toc_item = render_review_block(review_data)

    # 置換
    replacements = {
        "{{TITLE}}": html_mod.escape(args.title),
        "{{SUBTITLE}}": html_mod.escape(args.subtitle),
        "{{STRATEGY}}": html_mod.escape(args.strategy),
        "{{GOAL}}": html_mod.escape(args.goal),
        "{{DURATION}}": html_mod.escape(args.duration),
        "{{ARTICLE_STEPS}}": article_steps_html,
        "{{ARTICLE_TOC_ITEMS}}": article_toc_items,
        "{{MAIN_STEP_NUM}}": main_step_num,
        "{{TAIL_STEP_NUM}}": tail_step_num,
        "{{MAIN_IMAGE_CARD}}": main_image_card,
        "{{MAIN_BLOCK}}": main_block,
        "{{REPLY_BLOCKS}}": reply_blocks_html,
        "{{TOC_REPLY_ITEMS}}": toc_reply_items,
        "{{BOCCHI_AVATAR_REL}}": html_mod.escape(bocchi_avatar_rel),
        "{{REVIEW_BLOCK}}": review_block,
        "{{REVIEW_TOC_ITEM}}": review_toc_item,
    }
    out = template
    for k, v in replacements.items():
        out = out.replace(k, v)

    output_path.write_text(out)
    # X Articles 用プレーン版を post folder に書き出し (article ありの場合のみ)
    if has_article and article_x_plain:
        x_plain_path = output_path.parent / "article-x-plain.txt"
        x_plain_path.write_text(article_x_plain)
        print(f"   article-x-plain.txt: {x_plain_path} ({len(article_x_plain)} chars)")
    print(f"✅ flow.html generated: {output_path}")
    print(f"   Sections: Main + {len(sections) - 1} replies")
    print(f"   Article: {x_weight(article)} weight ({chars_no_ws(article)} 文字)")


if __name__ == "__main__":
    main()
