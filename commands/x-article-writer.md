---
description: X Articles (Premium+ 長文記事、最大 25,000 字) を執筆・ブラッシュアップする skill の slash command 風概要。詳細は skills/x-article-writer/SKILL.md
model: opus
---

# /x-article-writer

X Premium+ の長文機能 (Articles、最大 25,000 字) で、**個人開発者の 1 次情報をフォロワー獲得 + 検索流入 + 売り切り資産にする** ための執筆 command。

> **これは skill の slash command 風概要**です。実際は `skills/x-article-writer/SKILL.md` が本体で、Phase 1-9 / 検証ゲート / 画像戦略 / `render-flow.py` 連携まで全部入り。本 command はそこへの dispatcher として使ってください。

## いつ使うか

- ユーザーが「X Articles 書く」「ブログ記事化」「フル版執筆」「note 用記事」を依頼
- post-bocchi で書いた短文投稿の続きとして、フル版を書きたい
- 既存記事を「バズ」「見やすさ」「平易化」観点でブラッシュアップしたい

## post-bocchi との相補

| skill | 形式 | 文字数 | 用途 |
|---|---|---|---|
| `/post-bocchi` | 短文 X 投稿 + セルフリプ | 280 weight × 8 件 | フロー、フック、拡散 |
| `/x-article-writer` ← this | 長文 X Articles | 最大 25,000 字 | ストック、深い解説、フォロワー資産化 |

**ゴールデンルート**: post-bocchi (ティーザー) → x-article-writer (詳細マニュアル) → 通常投稿のセルフリプ末で Articles URL 誘導。

## X Articles 仕様 (2026)

| 項目 | 値 |
|---|---|
| 文字数上限 | 25,000 字 (Premium+ 加入者) |
| 見出しサポート | **H1 / H2 のみ**。H3 以下は plain bold 段落にダウングレード |
| タイトル | 本文と別フィールド |
| 公開後の編集 | 可能 (バージョン履歴あり) |

→ markdown 標準階層 (h1-h4) で執筆 → 公開直前に 1 段シフト (`## → #`, `### → ##`, `#### → **bold**`)

## 構成テンプレ (鉄板の 8 セクション)

```
1. Hook + サブタイトル (200-400 字)
2. 目次 (UI 自動 + 念のため手動でも書く)
3. どんな人向け (100-200 字、必須)
4. なぜ書いたか / 動機 (シリーズ初回または特別回のみ)
5. 概要 / 数字 (300-500 字)
6. 本論 — N 章 (各 500-1500 字、症状 → 原因 → 復旧 → 学び)
7. 結論 / 教訓 (300-500 字)
8. CTA + 著者紹介 (200-300 字)
```

## Phase 構造

| Phase | やること |
|---|---|
| 1 | ヒアリング + ネタ確認 |
| 2 | 構成案 (3 パターン: N 選型 / 失敗ストーリー型 / 完全ガイド型) を提示 |
| 3 | タイトル + サブタイトル設計 (Hook 9 パターン + 検索キーワード 2-3 個) |
| 4 | 章立て (H2 / H3) 設計 |
| 5 | 本文執筆 (各章 症状 → 原因 → 復旧 → 学び) |
| 6 | 画像戦略 + 配置 (cover / table 画像 / 章挿絵) |
| 7 | 検証ゲート (4 軸スコアリング: 整合性 / バズ性 / 平易化 / マーケ) + 外部 skill レビュー + 影響力 self-check + 法務観点 |
| 8 | 提示 (markdown + プレビュー) + X Articles 見出し正規化 |
| 9 | 出力 folder 自動生成 + flow.html 投稿フロー (`render-flow.py`) |

## 連携 skill

| skill | 役割 |
|---|---|
| `copywriting` | Hook 強度 / 明快さ / Outcome 訴求 |
| `influence-principles` | Cialdini 7 原理を本文に物理配置 |
| `page-cro` | 末尾 CTA 具体性 / 信頼シグナル |
| `metadata-optimization` | タイトル文字数 / 検索キーワード密度 |
| `launch-strategy` | ローンチ起点の物語 (任意、launch 系のみ) |

## 共通 NG (出力前チェック)

- markdown のまま X Articles エディタに貼る (記号が raw 表示)
- 見出しレベルを X 仕様に合わせず markdown 標準のまま貼る
- Apple メール本文の直接引用 (DPLA §10 リスク)
- 数字 / 引用の捏造
- 25,000 字超過
- 画像に watermark (Gemini 系)
- 「重要なのは」「〜することで」(AI 翻訳調)
- 章タイトルに絵文字を 2 章以上連続で並べる
- 誇張・最上級 (「最強」「絶対」「世界初」「必ず」)

## 起動例

```bash
# 新規執筆
/x-article-writer リジェクト 12 件の対処法

# 既存 markdown をブラッシュアップ
/x-article-writer apps/<example-app>/.scratch/post-YYYY-MM-DD-<slug>/article.md

# 構成だけ提案
/x-article-writer <topic> --outline-only
```

## 詳細

本 command は要約。Phase 7 検証ゲート / 画像 PNG 化フロー / `render-flow.py` 連携 / `review.json` schema 等の詳細は **`skills/x-article-writer/SKILL.md`** を参照。
