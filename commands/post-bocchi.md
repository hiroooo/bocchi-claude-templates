---
description: キャラクターベース X アカウント (<your-x-handle>) 用の X 投稿文を 6 type × 3 案で生成する skill 風 command。キャラ前提なので自分用にキャラ差し替え推奨
argument-hint: <type> [追加情報]
model: opus
---

# /post-bocchi

`<your-x-handle>`（キャラクターベース X アカウント）用の X 投稿を 3 案生成する。**メイン投稿 + セルフリプライ 1-2 段** をセットで提案、Hook 9 パターンから最適な 3 種選択 + 推奨画像 + ハッシュタグ + 自己評価 8 軸まで一気通貫。

> **キャラ前提 command**: テンプレとして使う場合は、キャラ名 / 口調 / 一人称ルール / 投稿アカウントを自分用に置換してください。本格運用するなら `~/.claude/skills/post-bocchi/SKILL.md` 相当を自分のキャラで作り直すのが推奨。

## 使い方 / type 一覧

| type | 用途 | 引数例 |
|---|---|---|
| `tips` | Claude Code / AI Tips の発信 | `/post-bocchi tips Auto Memory` |
| `tips --auto` | ai-tips-db から自動 pick | `/post-bocchi tips --auto` |
| `app-dev` | アプリ開発進捗 | `/post-bocchi app-dev OCR の精度上げてます` |
| `app-launch` | 新アプリ告知 | `/post-bocchi app-launch <app-name> ¥XXX <主機能>` |
| `failure` | 失敗談 (Apple reject 等) | `/post-bocchi failure 審査 4 回 reject` |
| `numbers` | 数字オープン (収益 / DL 内訳) | `/post-bocchi numbers <app> DL 100 / 内訳 X60 ASO30 紹介10` |
| `hotel-link` | ホテル↔開発クロス | `/post-bocchi hotel-link APA 築地で <app> 仕上げました` |
| `bio` | bio 更新 (現状アプリ数等を反映) | `/post-bocchi bio` |
| `roundup` | ◯選 / まとめ型 (メイン + セルフリプ 5 連投) | `/post-bocchi roundup MCP server 5 選` |

## ペルソナ「キャラクターベース X アカウント」 (置換対象)

- **設定**: 東京で開発会社をやってる内向の社長エンジニア。出張先のホテルで泊まりながら、毎週 1 本アプリを作ってる
- **連動**: 自分の他メディア (YouTube / blog 等) と同一人格として運用
- **トーン**: 敬体ベース（です・ます）+ 体言止め混合 / 自虐は短く

### 一人称ルール (最重要)

- **基本: 省略**。日本語の自然な無主語文を活用
- **使う場合: 1 投稿に最大 1-2 回**まで
- **連投スレッド全体**でも一人称総数 3 回以内（メイン + リプ 2 段）

### 避けるワード (個人バレ防止 / トーン違和感)

- 法人名 / 本名 / Bundle ID prefix / 自宅地域の詳細 / 顔写真リンク
- 「〜だぜ」「〜じゃん」「マジで〜」(軽すぎ)
- 「〜である」「〜だ」(硬すぎ)
- 「重要なのは〜」「〜することで」(AI 翻訳調)

## 文字数 (X 公式 weight 仕様)

X の 1 投稿上限は **280 weight**:
- **1 weight**: ASCII (a-z / A-Z / 0-9 / 半角記号)
- **2 weight**: 日本語 / 全角句読点 / 絵文字 等

→ 日本語ベースなら **実質 140 字が上限**。提示前に必ず weight 計算 (ASCII×1 + 全角×2)。

## Hook 9 パターン

| # | Hook |
|---|------|
| 1 | 「N 日で M 件、内訳晒す」+ 全部復旧した手順 |
| 2 | 「結論: ◯◯ は△△ ではなく □□」 |
| 3 | 「これ知らないと {半日 / N 万円} 溶ける」 |
| 4 | 「N 分で読める / 保存必須」 |
| 5 | 「実は〜ほど〜ない理由」 |
| 6 | 「過去のぼくに教えたい」 |
| 7 | 「{失敗} → {学び} → {解決}」 |
| 8 | 「アプリ N 本作って分かった、◯◯」 |
| 9 | 「中途半端だった自分が、◯◯ で動けるようになった」 |

## 出力フォーマット (3 案分)

各案で以下を提示:

1. **メイン投稿** (本文 + weight 数表示)
2. **セルフリプ 1-2 段** (本文 + weight 数表示)
3. **Hook タイプ** (1-9 のどれを使ったか)
4. **推奨画像** (任意 / character_*.png 流用 / 数字バナー / 章末スクショ等)
5. **ハッシュタグ** (1-3 個、X アルゴ的に過剰 NG)
6. **自己評価 8 軸**: バズ性 / 共感 / 一貫性 / 自虐の質 / 数字具体性 / 平易化 / Hook 強度 / CTA

## type 別の注意点

### `failure` (Apple reject 等)
- Apple メール本文の直接引用は **DPLA §10 Confidentiality 違反リスク**。ガイドライン番号 (公開情報) と自分の言葉での解説は OK
- Submission ID / Reviewer 個人情報は NG

### `app-launch` / `hotel-link` (URL を含む)
- URL は **本文に直貼り**ではなく **末尾セルフリプ**へ
- App Store URL は `id<numeric>` だけで開ける、日本語スラッグは削除
- 5MB 超画像は X が拒否、`sips -Z 1600 -s format jpeg -s formatOptions 85` で圧縮

### `tips`
- 16:9 横長 (1200×675 / 1500×600) 画像必須、cover 流用が最速
- AI 生成画像 (Gemini / nano-banana) は **SynthID watermark** でブランド visual に不向き、文字 hero は HTML テンプレ + Chrome headless 一択

## 関連 memory / skill

- `feedback-bocchi-no-pronoun-spam.md` — 一人称ルール
- `feedback-bocchi-image-optional.md` — 画像添付は任意 (節目のみ)
- `feedback-x-character-weight.md` — weight 計算
- `feedback-apple-reject-share-safety.md` — Apple reject 公開時の安全運用
- `reference-x-bocchi-tips-template.md` — Tips 投稿の鉄板テンプレ
- `~/.claude/skills/x-article-writer/SKILL.md` — 長文 X Articles の相補 skill
