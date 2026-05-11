---
name: x-article-writer
description: X Articles (Premium+ 長文記事、最大 25,000 字) を執筆・ブラッシュアップする skill。バズ・見やすさ・ワーディング・平易化・画像戦略・マーケ視点 (Cialdini) を統合し、Hook → 目次 → 章立て → CTA で構造化。post-bocchi と相補 (post-bocchi = 短文 X 投稿、x-article-writer = 長文 X Articles)。Use when ユーザーが「X Articles 書く」「ブログ記事化」「フル版執筆」「note 用記事ブラッシュアップ」等を依頼したとき。
---

# x-article-writer — X Articles 執筆 / ブラッシュアップ

X Premium+ の長文機能 (Articles、最大 25,000 字) で、**個人開発者の 1 次情報をフォロワー獲得 + 検索流入 + 売り切り資産にする** ための執筆 skill。

## いつ使うか

- ユーザーが「X Articles 書く」「ブログ記事化」「フル版執筆」「note 用記事」を依頼
- post-bocchi で書いた短文投稿の続きとして、フル版を書きたい
- 既存記事を「バズ」「見やすさ」「平易化」観点でブラッシュアップしたい

## post-bocchi との相補

| skill | 形式 | 文字数 | 用途 |
|---|---|---|---|
| `post-bocchi` | 短文 X 投稿 + セルフリプ | 280 weight × 8 件 | フロー、フック、拡散 |
| `x-article-writer` ← this | 長文 X Articles | 最大 25,000 字 | ストック、深い解説、フォロワー資産化 |

**ゴールデンルート**: post-bocchi (ティーザー) → x-article-writer (詳細マニュアル) → 通常投稿のセルフリプ末で Articles URL 誘導。

## 連携 skill (Phase 7-D で必要に応じ起動)

| 軸 | skill | 何を強化 |
|---|---|---|
| **説得力 / 心理トリガー** | `influence-principles` | Cialdini 7 原理 (返報性 / 一貫性 / 社会的証明 / 権威 / 好意 / 希少性 / 連合) を本文に |
| **コピーライティング** | `copywriting` | Hook の語感 / リズム / 主張の鮮度を rewrite |
| **ローンチ戦略** | `launch-strategy` | アプリリリース系の angle (PH / 業界フック) |
| **読了 → CTA** | `page-cro` | 末尾 CTA の具体性 / 緊急性 / リスクリバーサル |
| **タイトル + SEO** | `metadata-optimization` | キーワード設計 (Google + AI answer engine) |
| **画像** | `nano-banana` (補助のみ、watermark 注意) | 雰囲気背景。文字 hero は launch-banner template、ブランド visual は既存キャラクターを使う |

---

## X Articles 仕様 (2026)

| 項目 | 値 |
|---|---|
| 文字数上限 | 25,000 字 (Premium+ 加入者) |
| フォーマット | markdown 互換 (見出し / リスト / 強調 / リンク / 画像 / 引用) |
| 画像 | 別途 upload (cover image + 本文挿絵) |
| 目次 | UI が自動生成 (**H1 / H2** から) |
| 見出しサポート | **H1 / H2 のみ**。H3 以下は plain bold 段落にダウングレード |
| タイトル | 本文と別フィールド (markdown の `# Title` をコピペしても自動振り分けされない) |
| 公開後の編集 | 可能 (ただしバージョン履歴あり) |

X 内コンテンツなので、X URL ホワイトリスト問題なし (外部リンク評価ダウンの対象外)。

### 見出し階層の実体 (ハマりポイント、2026-05-09 確認)

X Articles エディタは **本文中の見出しを H1 / H2 の 2 段階しか表示見出しとして扱わない**。markdown 標準の 4 段階 (h1-h4) でソースを書くと、コピペ時に階層が 1 段ズレて「大見出しのつもり」が中見出しに、「中見出し」が plain bold に化ける。

**ソース markdown の書き方 (執筆 / プレビュー用)**:

| Markdown | 役割 | プレビュー (note / GitHub) | X Articles 投稿後 |
|---|---|---|---|
| `# Title` | 記事タイトル | 大見出し | **本文から削除**、X タイトルフィールドへ手動コピペ |
| `## ` | 大見出し (1 章) | 中見出し | **H1 シフト** = X 大見出し |
| `### ` | 中見出し (章内ブロック) | 小見出し | **H2 シフト** = X 中見出し |
| `#### ` | 小見出し | h4 | **plain bold 段落** = `**見出し文**` |

**コピペ前の正規化 (publish 時 1 回実行)**:

```bash
# 1. h1 タイトル削除 → X タイトル欄へ手動コピペ
# 2. 全見出しを 1 段上げ + h4 を bold 段落化
perl -i -pe 's/^## /# /; s/^### /## /; s/^#### (.+)$/**\1**/' article.md
```

**運用ルール**:
- **執筆中は markdown 標準** で書く (h1-h4 ネスト)、note / GitHub / Local プレビューが正しく見える
- **X Articles 公開直前に正規化スクリプト 1 回**走らせる、または手動シフト
- post folder には `article.md` (執筆ソース) と `article-x-shifted.md` (X 投稿用) を分けても良いが、月 1 連載なら 1 ファイルでシフト → 投稿 → ソース戻し戻しは過剰、**シフト後を保存して終了** が運用シンプル
- render-flow.py は `article.md` を読むので、投稿後の `article.md` シフト済でも flow.html は正しく生成される

---

## 構成テンプレ (鉄板の 8 セクション)

```
1. Hook + サブタイトル (200-400 字)
   ├ 数字 hammer + 文脈明示
   └ シリーズなら「<シリーズ名> #N — <キャッチ>」型

2. 目次 (UI 自動 + 念のため手動でも書く)

3. どんな人向け (100-200 字、必須) ★
   ├ ペルソナを bullet で簡潔に列挙 (補足説明は冗長になりがちなので不要)
   └ 「拾い読み OK」明示 (各セクション独立性を保証)

4. なぜ書いたか / 動機 (300-500 字、シリーズ初回または特別回のみ)
   ├ 共感入口 (中途半端あるある型 Hook #9 等)
   ├ 動機を 2-4 個に分けて H3 で並列展開
   └ 動機ごとに 100-200 字、長文化したら H3 で分ける

5. 概要 / 数字 (300-500 字)
   └ 表 or 箇条書きで「全体像 + 数字」を先出し

6. 本論 — N 章 (各 500-1500 字)
   ├ 各章: 症状 → 原因 → 復旧 → 学び の 4 ブロック
   ├ コード片 / スクショ / 表
   ├ H2 が 500 字超なら H3 で分ける (3 個以上の並列なら必ず)
   └ 章末で「次の章への引き」(なめらかな遷移)

7. 結論 / 教訓 (300-500 字)
   └ 全体の貫く法則を 3-5 個

8. CTA + 著者紹介 (200-300 字)
   ├ X / プロフィール / アプリ
   └ 「書いた人 = 〇〇 (実績)」で権威付け
```

★ 「どんな人向け」は省略しがちだが**必須**。執筆者の自己満足を読者の Outcome 視点に強制変換するアンカーになる。

## シリーズ化対応 (月 1 / 不定期連載)

同テーマで連載する場合の使い回しテンプレ:

| 要素 | テンプレ |
|---|---|
| **タイトル** | 「**<Hook + 数字 hammer + キャッチ>** — <シリーズ名> #NN」**Hook 先頭、シリーズ番号は後置** (Karpathy パターン)。例: 「10 日で iOS アプリ 3 本、作り方ぜんぶ公開 — 100 本ノック #01」 |
| **cover image crest** | 「<SERIES> · #NN · <サブテーマ>」(例: 「100 BANG NOCK · #01 · 開発スタイル全公開」) |
| **cover image footer** | 「#NN · YYYY-MM-DD · X% PROGRESS」 (進捗率も併記) |
| **冒頭サブタイトル** | 「シリーズ #NN — <更新頻度>」 + 過去回への戻るリンク |
| **末尾 CTA** | 「Vol.NN+1 以降は X で告知」+ シリーズ index |

Vol.2 以降は **タイトルキャッチ + 数字 + 進捗率だけ更新** で同フォーマット使い回し可。新規執筆コストを 30-50% 削減できる。

### タイトル設計ルール (シリーズ問わず共通)

- **Hook (数字 hammer + キャッチ) を先頭**、シリーズ番号やジャンル名は後置 — 初見読者は数字で目を止める、リピーター/フォロワーはシリーズ名で識別、両取り
- **キャッチワード**は「**作り方ぜんぶ公開**」「**手法 + 経済学**」「**やったこと全部**」「**全工程公開**」等の日本特化バズワード型。「全部さらす」は自虐強だが、教える系より検索流入弱め
- **文字数は 28-35 字**を目安 (X タイムラインで切れない範囲)、長文タイトルは記事ページで読まれるが SNS 流入で不利
- **Hook + 数字 + キャッチ**の 3 要素を必ず含める (例: 「10 日 (Hook) で iOS アプリ 3 本 (数字)、作り方ぜんぶ公開 (キャッチ)」)

合計 4,000-8,000 字が読了率 / 共有率の最適レンジ (実用 how-to 系)。25,000 字フル使うのは「保存版完全マニュアル」「N 選 30 連発」等の特殊ケース。

---

## Hook 9 パターン (1-2 行目で読者の指を止める)

| # | Hook | 向いてるネタ |
|---|------|---|
| 1 | 「N 日で M 件、内訳晒す」+ サブで「全部 X で復旧した手順」 | failure / numbers 系 (実証済、個人開発に最強) |
| 2 | 「結論: ◯◯ は△△ ではなく □□」 | 通説をひっくり返す |
| 3 | 「これ知らないと {半日 / N 万円} 溶ける」 | 技術ハマり / 罠系 |
| 4 | 「N 分で読める / 保存必須」 | 短尺保証で読了率 UP |
| 5 | 「実は〜ほど〜ない理由」 | ギャップ提示 |
| 6 | 「過去のぼくに教えたい」 | 経験談、共感誘導 |
| 7 | 「{失敗} → {学び} → {解決}」 | ストーリー型 |
| 8 | 「アプリ N 本作って分かった、◯◯」 | 実績ベースの権威付け |
| **9** | **「中途半端だった自分が、◯◯ で動けるようになった」型** | **エンジニアあるある共感入口 (アイディアだけ / モックで止まる / リリースまで届かない型に直撃)** |

post-bocchi の Hook 11 パターンを Articles 用に圧縮。最も強いのは **Hook #1** (数字 + 自虐 + 内訳予告) と **Hook #9** (共感入口 + 動機の自然な展開)。

---

## 章立て / 見出しルール (chunk 化)

> **重要**: 以下のルールは **執筆ソースの markdown 標準階層** (h1-h4) を前提に書く。X Articles 投稿時に「見出しレベルの実体」セクションの正規化ステップで 1 段上げシフトされる。執筆中は note / GitHub と同じ標準で書いて OK。

### H2 = 1 章 = 1 テーマ (X では H1)
- 「ベタ流し」を避け、500-1500 字ごとに H2 で区切る
- H2 は **数字 + 名詞 + 短いベネフィット**: `類型 1: IAP プロモ画像 (4 件、復旧 30 分)`
- 抽象タイトル NG: `IAP プロモ画像について` ← 弱い

### H3 = 章内のブロック分け (X では H2)
- 症状 / 原因 / 復旧 / 学び の 4 ブロックは H3 で区切る
- 短く、見出しだけで内容予想可
- **同レベルで性質の違うものを混ぜない**: 「視点 1 / 視点 2 / 視点 3 / アイディアが湧いたら / 視点を磨く習慣」のように並列分類と補足を同 H3 で並べると、レベル不揃いに見える。並列分類は H3、補足は別 H2 か bold 段落に降ろす

### H4 = 小見出し (X では plain bold 段落)
- markdown ソースで `#### 小見出し` と書いても、X 投稿時に `**小見出し**` に変換されるので **目次に出ない**
- 「目次に載せたい」階層なら H3 までに収める。H4 は「読み流し時の視覚アンカー」用途

### 太字は「目で読み取る要点」
- 1 段落に 1 箇所まで。多用すると効果ゼロ
- 「**動詞 + 数字**」が最強: `**全部 24-48h で復旧した**`

### リスト / 表
- 比較は表
- 手順は番号付きリスト
- 並列要素は箇条書き

---

## ワーディング / 平易化 (X 投稿のメインと同じ二段構造)

### 二段構造ルール

| 層 | 想定読者 | 用語 |
|---|---|---|
| **Hook + サブタイトル + 目次 + はじめに** | 一般層含む | カタカナ化 + 文脈明示 (`indie` → `個人開発`、`reject` → `リジェクト`、`App Store 審査` 等) |
| **本論 + 詳細手順** | ターゲット読者 (技術者) | 技術用語 OK、ただし初出は補足括弧 (`MCP (外部ツール接続規格)` 等) |

### 専門用語の補足ルール

```
ガイドライン番号: 2.3.2 = アプリ内課金の宣伝画像ルール違反
RevenueCat: 課金管理 SDK
ATT: App Tracking Transparency = 広告トラッキング許可ダイアログ
```

初出時に括弧で補足、2 回目以降は補足なしで OK。

### NG ワーディング

- 業界カタカナ語の文脈ナシ多用 (Hook で `indie 開発 reject 12 件` ← 一般層に伝わらない)
- AI っぽい接続詞 (「重要なのは」「〜することで」)
- 一人称「ぼく」3 連発以上 (memory `feedback-bocchi-no-pronoun-spam`)
- Apple メール本文の直接引用 (DPLA §10 リスク、memory `feedback-apple-reject-share-safety`)

---

## SEO ワーディング (検索流入 + AI answer engine)

### Google 検索狙い (古典 SEO)
- タイトルに **検索キーワード 2-3 個**: `App Store 審査リジェクト` `個人開発 iOS` `対処手順`
- H2 に semantic キーワード: `IAP プロモ画像 (2.3.2)` のようなガイドライン番号
- meta description (X Articles では subtitle): 100-150 字、結論先出し

### AI answer engine 狙い (Claude / Perplexity / ChatGPT Answers)
- **質問形式の H2 / H3 を 1-2 個入れる**: `App Store のリジェクト 2.3.2 はどう直す？`
- **結論を本文先頭に置く** (AI が summary に使う)
- **数字 / 表 / 箇条書き** を活用 (AI がパースしやすい)

### 関連キーワード ロングテール
- 「個人開発」「iOS アプリ」「審査リジェクト」「ASC」「IAP」「RevenueCat」「ATT」 等を本文に自然分散

---

## 画像戦略 (watermark 回避必須)

memory `feedback-gemini-image-watermark.md` 通り、画像はサポート、メイン visual に AI 生成画像を使わない。

| 用途 | 推奨 | 例 |
|---|---|---|
| **Cover image (記事冒頭)** | 既存キャラクター画像 1 枚 or `cover-banner.html` テンプレ (1500×600 dark theme + crest + footer + brand) | tips 系 → `character_desk_focus.png`、シリーズ系 → cover-banner template |
| **table 画像 (本文 markdown table 代替)** | `templates/table-styles.css` + plain `<table>` → `scripts/render-tables.py` で PNG 量産 | 一覧 / 比較 / 数字 summary / 月次費用 / 改善課題 |
| **数字 hero 画像 (記事冒頭バナー)** | `templates/launch-banner/` の HTML テンプレ + Chrome headless | アプリリリース連動時 |
| **章ごとの挿絵 (任意)** | 既存スクショ (ASC GUI / 実装画面) or コード片 (markdown code block で十分、画像化不要) | — |
| **NG (使わない)** | nano-banana / Gemini watermark あり画像、ストック写真 | — |

### table 画像化が必要な理由

X Articles エディタは markdown table を解釈しない (`|` 文字列がプレーンテキストで横並びになるだけ)。本文中の比較表 / 一覧 / 数字 summary はすべて **PNG 化して画像 block として挿入する** のが必須。

### table 画像の標準デザイン (実装事例で実証)

X Articles 本文と「島浮き感ゼロ」で馴染ませるため、**light theme 統一**:

| 要素 | 値 | 理由 |
|---|---|---|
| **背景** | `#ffffff` | X Articles 本文 (light) と一致 |
| **text primary** | `#0f1419` | X UI primary text |
| **text secondary** | `#536471` | X UI secondary text (mono / muted 列) |
| **border** | `#eff3f4` | X UI 標準罫線 |
| **font** | `-apple-system, BlinkMacSystemFont, "SF Pro Text", "Hiragino Kaku Gothic ProN"` | X system font 一致 |
| **mono** | `ui-monospace, SFMono-Regular, "SF Mono", Menlo` | code/数字/日付 列 |
| **accent (yellow brand)** | `#b8941f` (濃いめ) | brand 統一、ただし number / KPI / highlight 行に最小限 |
| **左右 padding** | **0** (`body { padding: 24px 0; }`) | 縮小表示時に table 本体が画像端まで広がる |
| **font-size** | **28px** (本文) / 22px (header) | 縮小表示後でも 14-16px 確保 |

**画像 1 枚に含める要素 (本体のみ)**:
- ✅ table のみ (header + tbody + 必要なら highlight 行)
- ❌ crest「DATA · #NN · ラベル」(章見出しと重複)
- ❌ title「N 本の内訳」(章見出しと重複)
- ❌ footer「#NN · YYYY-MM-DD · <your-x-handle>」(brand 過剰)

→ `_styles.css` の `.crest, .title, .subtitle, .footer { display: none; }` で全部隠す。

### compare card / KPI grid は使わない (NG パターン、2026-05-09 学び)

「Swift vs Flutter 2 列対比カード」「KPI 4×2 グリッド」などビジュアル豊かなレイアウトは AI 感満載で記事の信頼性を落とす。**plain `<table>` 形式で統一する**:

- ❌ 2 col compare card (左赤右緑、badge 付き) — 商業 LP 風で記事と違和感
- ❌ KPI grid (4 列 × 2 行 数字カード) — Stripe / Notion 風で indie 記事と違和感
- ❌ VS バッジ + ロゴアイコン + 装飾 — AI 生成丸出し
- ✅ シンプルな plain `<table>` を 1 つの画像に 1〜2 個並べ、必要なら間に控えめな `.section-label` で区切る

「同じ table デザインで 10 枚並ぶ」方が、読み手は「この人の記事フォーマット」と認識して記事全体に統一感を感じる。

### 画像配置の鉄則
- **冒頭 + 各章の最初**にだけ。間に挟みすぎは読了率ダウン
- 画像枚数: 5,000 字記事で 3-5 枚 (cover + 主要 table 2-4 枚)、10,000 字超で 8-12 枚 OK
- 画像下に 1 行キャプション (画像だけだと素人感)
- table 画像は alt text で必ずタイトル + 数値要旨 (アクセシビリティ + SEO)

### table 画像化フロー (Phase 9 と連動)

1. article.md の markdown table を `tables/table-NN-<slug>.html` として書き出す (各 HTML は `<link rel="stylesheet" href="_styles.css">` のみ、共通 CSS 参照)
2. `templates/table-styles.css` を `tables/_styles.css` にコピー (or symlink)
3. `python3 ~/.claude/skills/x-article-writer/scripts/render-tables.py <tables_dir>` で 全 PNG 量産 (body 自然高さで余白なし clip)
4. article.md の table を `![alt text](tables/table-NN-<slug>.png)` に置換
5. flow.html 再生成 (`render-flow.py`)
6. X Articles エディタで 本文ペースト → 各画像位置で Finder の PNG を Cmd+C → Cmd+V で挿入

---

## マーケ視点 (Cialdini 7 原理を本文に埋める)

memory `influence-principles` skill を任意で起動して強化可能。最低限以下 3 つは Articles に入れる:

| 原理 | 配置 | 例 |
|---|---|---|
| **社会的証明** | Hook + 概要 + 結論 | 「アプリ 4 本 / 16 日 / 12 件」(数字 = 第三者検証可能) |
| **権威 (実績)** | はじめに + 著者紹介 | 「個人開発 iOS で〇〇本リリース」「100 本ノック中」 |
| **返報性 (Tips の出し惜しみなし)** | 本論全体 | 「URL 踏まなくても本文だけで復旧できる」レベルの完結性 |

### 売り切りオファー (将来の note / プロダクト誘導)

X Articles は無料が定番だが、本文中に「もっと深い実装は別記事 / プロダクトで」という導線を 1 箇所だけ仕込んでおくと、後から有料 note へのリンクを追加しやすい。

---

## Phase 構造

### Phase 1: ヒアリング + ネタ確認
- 引数 (タイトル or テーマ) を受け取る
- 既存 markdown / scratch があれば「ブラッシュアップモード」、なければ「新規執筆モード」
- ターゲット読者 (一般 / 技術者 / 両方) を確認

### Phase 2: 構成案 (3 パターン提示)

3 案出す:
- A. **N 選型** (12 リジェクト / 7 つの罠 等): 保存ブクマ最強
- B. **失敗ストーリー型**: 共感 + 学びで読了率 max
- C. **完全ガイド型** (How to X): SEO 流入狙い

ユーザーに 1 つ選んでもらう or 内部判断で 1 つに絞る。

### Phase 3: タイトル + サブタイトル設計
- Hook 8 パターンから選択
- 検索キーワード 2-3 個を入れる
- 30-60 字 (X Articles のタイトルは長くても OK)
- サブタイトル (X Articles の description フィールド) 100-150 字、結論先出し

### Phase 4: 章立て (H2 / H3) 設計
- 4-7 章
- 各章は 500-1500 字を目安
- H2 タイトルで「数字 + 名詞 + ベネフィット」

### Phase 5: 本文執筆
- 章ごとに執筆 (順次 or 並列)
- 各章の構成: 症状 → 原因 → 復旧 → 学び (この型を全章で揃える、読みやすさ激増)
- コード片 / 表 / 番号リストを章ごとに 1-2 個

### Phase 6: 画像戦略 + 配置
- Cover image: キャラクターから 1 枚選定
- 各章 H2 の下に挿絵 (任意、schema diagram or 既存スクショ)
- watermark 警告 (Gemini 系 NG)

### Phase 7: 検証ゲート (4 軸スコアリング)

| 軸 | 構成項目 | 満点 | REGEN 基準 |
|---|---|---|---|
| **A. 整合性** | 数字正確 / 引用正確 / Apple メール直接引用なし / URL 公式性 | 4/4 | 1 つでも FAIL |
| **B. バズ性 / 見やすさ** | Hook 強度 / 数字 hammer / 章立て chunk 化 / **lede 段落 + callout 引用ブロック** (list 過多回避) | 4/4 | 2/4 以下 |
| **C. 平易化** | 1 行目文脈明示 / 専門用語補足 / カタカナ化 / 一人称コントロール / **平易化辞書 grep** (`feedback-bocchi-wording-dictionary.md` 参照、`indie` `reject` `scaffold` `submodule` 等の業界カタカナ語と Claude 内部ジャーゴン (`hammer` `hero` `sim` `chunk 化` 等) がゼロ) | 4/4 | 2/4 以下 |
| **D. マーケ** | 社会的証明 / 権威 / 返報性 (Tips 完結性) / CTA 具体性 | 4/4 | 1/4 以下 |

**REGEN ループ最大 3 周**。それでも改善しなければ Phase 2 (構成) からやり直し。

#### `review.json` を必ず出力する (Phase 9 で flow.html に反映)

Phase 7 のスコアリング結果を `apps/<app>/.scratch/<post-folder>/review.json` に保存。flow.html のレビュータブにそのまま反映され、「本当に 4 軸でレビューしたか」がユーザーから可視化できる。

スキーマ:

```json
{
  "axes": [
    {
      "id": "A",
      "name": "整合性",
      "max": 4,
      "score": 4,
      "checks": [
        {"item": "数字正確", "result": "PASS", "note": "16/12/4 を git log と照合済"},
        {"item": "Apple メール直接引用なし", "result": "PASS", "note": "..."},
        {"item": "Submission ID / Reviewer 個人情報", "result": "PASS", "note": "..."},
        {"item": "URL 公式性", "result": "PASS", "note": "..."}
      ],
      "observations": "軸全体の所感 / 判断根拠 (なぜこの判定にしたか)"
    },
    { "id": "B", "name": "バズ性",  "max": 4, "score": 4, "checks": [...], "observations": "..." },
    { "id": "C", "name": "平易化",  "max": 4, "score": 4, "checks": [...], "observations": "..." },
    { "id": "D", "name": "マーケ",  "max": 4, "score": 4, "checks": [...], "observations": "..." }
  ],
  "regen_rounds": 1,
  "regen_log": [
    "Round 1: A-2 で Apple メール直接引用 → 自分の言葉に書き換え",
    "Round 1: C-3 でカタカナ語 (indie/reject) を一般語化"
  ],
  "summary": "4 軸 16/16 PASS。... (総合所感)"
}
```

- `result` は `PASS` / `FAIL` / `NEEDS` / `WARN` のいずれか (CSS 配色がそれぞれ用意されている)
- `checks[].note` はその判定根拠を 1-2 文で。「なぜ PASS / FAIL か」を残す
- `observations` は軸全体の俯瞰。「なぜそのスコアになったか」「なぜ改善できたか」を 2-3 文で
- `regen_log` で REGEN ループの履歴を 1 行ずつ。レビューの実在証拠になる
- 仮にスコアが満点でも、checks / observations / regen_log は省略禁止 (「ちゃんと観点を持って見た」記録が消えるため)

### Phase 7-E (必須): 外部 skill による独立レビュー

自前 4 軸採点だけだと「自分で書いたものを自分で甘く採点」リスクがある。外部 skill の独立観点を**必ず通過**させ、結果を `review.json` の `external_reviews[]` に記録する。

| skill | 観点 | 通過基準 |
|---|---|---|
| **`copywriting`** (必須) | Hook 強度 / 明快さ / Outcome 訴求 / リズム・語感 | verdict = PASS |
| **`influence-principles`** (必須) | Cialdini 7 原理 (返報性 / 権威 / 社会的証明 / 一貫性 / 好意 / 希少性 / 連合) のうち最低 4 原理を物理配置 | 4 原理以上 = PASS |
| **`page-cro`** (必須) | 末尾 CTA 具体性 / 読了 → 行動の摩擦 / 信頼シグナル | verdict = PASS |
| `metadata-optimization` (任意) | タイトル文字数 / 検索キーワード密度 / SEO 観点 | 任意通過 |
| `launch-strategy` (任意、launch / app-launch 系のみ) | ローンチ起点の物語 / waitlist 設計 | 任意通過 |

各 skill の評価結果は **`external_reviews[]` の 1 entry** として保存:

```json
{
  "skill": "copywriting",
  "focus": "Hook 強度 / 明快さ / Outcome 訴求",
  "verdict": "PASS",
  "score": "8/10",
  "findings": [
    {"item": "Hook 強度", "result": "PASS", "note": "..."},
    {"item": "明快さ", "result": "PASS", "note": "..."}
  ],
  "observations": "...",
  "actions_taken": ["この skill の指摘で C-2 を rewrite", "..."]
}
```

`verdict` のいずれかが `FAIL` / `NEEDS` なら REGEN ループ対象。3 周回しても通らないなら Phase 2 から構成見直し。

### Phase 7-F (必須): 影響力 + コピー力 self-check

外部 skill の独立レビュー (Phase 7-E) とは別に、Cialdini 7 原理 + Caples 「ザ・コピーライティング」テクニックを **記事に物理配置できているか** を自分で 1 周点検する。スコアリングではなく「配置漏れの有無」だけ確認。

#### Cialdini 7 原理 配置チェック

| 原理 | 配置箇所 | 例 |
|---|---|---|
| **返報性** | 章 0 lede / 本論全体 | 「URL 踏まなくても本文だけで全部直せます」「再現コード / 復旧手順をすべて公開」 |
| **希少性** | 章 0 hero pull-quote / 数字 hammer | 「16 日で 12 件は indie でも稀な密度」「最終更新: YYYY-MM-DD」(時限性) |
| **社会的証明** | 末尾 CTA / 著者紹介 | 公開済アプリへのリンク + ストア URL、第三者検証可能な数字 (アプリ N 本 / フォロワー N) |
| **権威** | はじめに / ガイドライン番号 | 公式ガイドライン番号正確 + 復旧時間の具体数字 + 「100 本ノック中 N 本目」 |
| **一貫性** | 章 0 / 末尾 | 「100 本ノック」のような継続コミット可視化、追記前提宣言 |
| **好意** | 全体トーン / 自分のキャラのトーン | 失敗共有 + 自虐 + 一人称コントロール (省略 + 体言止め混合) |
| **統一性** | 共同体ワード | 「個人開発仲間が同じ罠を踏んだら」「indie の役に立てば」 |

**REGEN 基準**: 「返報性」「希少性」「社会的証明」「権威」の 4 原理は**必ず物理配置**。1 つでも欠落 → REGEN。残り 3 (一貫性 / 好意 / 統一性) は 2 つ以上配置で OK。

#### Caples「ザ・コピーライティング」 4U + ベネフィット先出し

| 観点 | チェック | REGEN 基準 |
|---|---|---|
| **タイトル 4U** | Useful (役に立つ) / Urgent (急ぎ感) / Unique (独自) / Ultra-specific (具体的) | 3/4 以上 PASS、2/4 以下 → タイトル REGEN |
| **ベネフィット先出し** | lede 段落 (50-100 字) で「読者が何を持ち帰れるか」を先頭で明示 | 不在 → 章 0 REGEN |
| **数字 hammer** | タイトル + Hook + 章タイトル + 各章末 callout に具体数字 | 数字なしの章が 2 章以上 → REGEN |
| **章末 callout の How-to 型統一** | `> 鉄則: <症状> なら <一手> で <時間>` 型で全章統一 | 1 章でも崩れる → 揃え直し |
| **17 ヘッドライン型の活用** | "How to" / "Why" / 数字型 / 体験談型 のうち 1 個以上を章タイトルで使う | 不在 → 章タイトル見直し |

#### Phase 7-F の出力

`review.json` の末尾に以下を追加:

```json
{
  "influence_check": {
    "cialdini_placement": [
      {"principle": "返報性", "placed": true, "location": "章 0 lede + 末尾 CTA", "note": "..."},
      {"principle": "希少性", "placed": true, "location": "章 0 hero pull-quote", "note": "..."}
    ],
    "verdict": "PASS"
  },
  "caples_check": {
    "title_4u": {"useful": true, "urgent": true, "unique": true, "ultra_specific": true, "score": "4/4"},
    "benefit_lede": {"present": true, "location": "章 0 lede 50-100 字目", "note": "..."},
    "number_hammer": {"chapters_without_numbers": [], "verdict": "PASS"},
    "callout_howto_unified": true,
    "verdict": "PASS"
  }
}
```

### Phase 7-G (必須): 法務観点レビュー

DPLA / 個人情報 / 商標 / 不当表示 / 著作権 / アフィリエイト / 業種特化規制 の 7 軸で公開前にリスクを潰す。Articles 公開後に「法的に問題がある投稿だった」と気づくと取り下げが面倒 + 信頼を失う。

#### 7 軸チェック

| 軸 | 観点 | 失敗時の対応 |
|---|---|---|
| **A. Apple confidentiality (DPLA §10)** | リジェクトメール本文の直接引用 / Submission ID / Reviewer 個人情報の漏洩なし | 自分の言葉で要約、ID は伏せる (`feedback-apple-reject-share-safety.md`) |
| **B. 個人情報 / 法人情報** | 本名 / 住所 / 電話 / メアド / 法人名 / Bundle ID prefix / API Key / Team ID / AdMob pub-ID 等の意図しない暴露なし | placeholder 化 (`<your-...>` 形式) |
| **C. 第三者ブランド表現** | 名指し誹謗・虚偽情報なし、比較は事実ベースで公正 (景表法 / 不正競争防止法) | 「優れているが好みの問題」「自分のスタイルでは合わなかった」型に書き換え |
| **D. 比較最上級・誇張** | 「最強」「絶対」「世界初」「必ず」「ベスト」等の不当表示・断言なし、数字は実績ベース | 主観表現 (「自分の場合は」「個人的には」) or 削除 |
| **E. 引用 / 著作権** | 第三者の長文引用は「主従」「明確化」「出典明示」の 3 要件を満たす、画像・文章の無断転載なし | URL 付き引用、要約に変える |
| **F. アフィリエイト / PR / ステマ** | PR / アフィリエイト案件は明示、自社アプリは OK (本人の投稿として明確化) | `[PR]` `[広告]` 表記追加 |
| **G. 業種特化規制** | アプリ別の規制 (金融商品の助言 / 医療助言 / 投資推奨 / 法務助言 / 薬機法 / 特商法) を踏まない | 「情報提供のみ、助言ではない」と明示、薬機法対象なら表現削除 |

#### `review.json` への記録

```json
{
  "legal_check": {
    "axes": [
      {"id": "A", "name": "Apple confidentiality", "result": "PASS", "note": "Apple メール直接引用なし、Submission ID 記載なし"},
      {"id": "B", "name": "個人情報 / 法人情報", "result": "PASS", "note": "メアド / Bundle ID prefix / Team ID / API Key / AdMob pub-ID 全て除去確認"},
      {"id": "C", "name": "第三者ブランド表現", "result": "PASS", "note": "Cursor / Sentry / ChatGPT 等は中立な比較、誹謗なし"},
      {"id": "D", "name": "比較最上級・誇張", "result": "PASS", "note": "「最強」「絶対」「世界初」「必ず」なし、数字は実績ベース"},
      {"id": "E", "name": "引用 / 著作権", "result": "PASS", "note": "第三者の長文引用なし、公式 URL のみ参照"},
      {"id": "F", "name": "アフィリエイト / PR / ステマ", "result": "PASS", "note": "該当なし、自社アプリのみ"},
      {"id": "G", "name": "業種特化規制", "result": "PASS", "note": "投資 / 医療 / 法務 / 金融商品の助言なし"}
    ],
    "verdict": "PASS",
    "score": "7/7",
    "observations": "..."
  }
}
```

verdict が `FAIL` / `NEEDS` なら REGEN ループ対象。法務リスクは特に「公開してから気づく」コストが高いので、グレーゾーンは保守側に倒す。

### Phase 8: 提示 (markdown + プレビュー) + X Articles 見出し正規化
- markdown 全文を提示
- 文字数 + 想定読了時間 + 4 軸スコアを併記
- 改善案 (どこが弱いか + どう直すか)
- **X Articles コピペ前の見出し正規化** (X Articles エディタが markdown 直貼りで見出しを認識する場合に必須):
  ```bash
  # 1. h1 タイトル行を削除 (X Title 欄に手動コピペ)、h2 → h1, h3 → h2, h4 → bold段落
  perl -i -pe 's/^## /# /; s/^### /## /; s/^#### (.+)$/**\1**/' article.md
  # 2. flow.html 再生成
  python3 ~/.claude/skills/x-article-writer/scripts/render-flow.py --article ... --post ...
  ```
- **正規化を飛ばす運用** (article-x-plain.txt 経由): `flow.html` の「X 用プレーンタブ」からコピー → X Articles エディタの toolbar で見出し / 引用 / リストを手動再装飾、の流れなら不要 (見出しレベルがどうあれ全部 plain text 化されてるので)
- **どちらを使うか**: 短い記事 (5,000 字以下) は手動装飾、長い記事 (10,000 字以上 / 複雑な階層) は正規化 + markdown 直貼りが速い

### Phase 9: 出力 folder 自動生成 + flow.html 投稿フロー

`apps/<app>/.scratch/post-<YYYY-MM-DD>-<slug>/` に:
- `article.md` — X Articles 本文 (markdown、執筆 / バックアップ用)
- `article-x-plain.txt` — **X Articles 直接ペースト用プレーン版 (記号除去済、render-flow.py が article.md から自動生成)**
- `post.txt` — 通常投稿 Main + Reply 1-N (`=== Main ... ===` / `=== Reply 1 (19:01) — ... ===` 区切り)
- `main-image.png` — メイン投稿の添付画像 (任意、既存キャラ流用 OK)
- `cover.png` — Articles cover (任意)
- `flow.html` — **投稿実行用ダッシュボード**。`render-flow.py` でテンプレから生成

#### `flow.html` の必須機能 (テンプレ化済み、render-flow.py 経由で自動付与)

呼び出すだけで全部入る。手書き禁止 — 必ず `~/.claude/skills/x-article-writer/scripts/render-flow.py` を経由する。

| 機能 | 仕様 |
|---|---|
| **サイド TOC (sticky)** | 260px 左カラム、Step + 各 Reply タイトルへスクロール。Intersection Observer で active 自動ハイライト |
| **キャラクターアイコン hero** | ヘッダー左にアバター (96px circular、yellow border + glow)、`<YOUR-CHARACTER> X FLOW` タグ + グラデ背景。`--character-avatar` 未指定なら `<your-branding>/<your-character>/avatar.png` 自動採用 |
| **コピペボタン** | 各セクションに 📋 コピー (clipboard.writeText、1.5 秒トーストフィードバック) |
| **X 用プレーンタブ (デフォルト active)** | Article 本文ブロックの 1 タブ目。`article-x-plain.txt` を表示、コピーボタンの target はこちら。X Articles エディタにそのまま貼って toolbar で見出し / 引用 / リストを手動適用 |
| **Markdown / プレビュータブ (副)** | 副タブで Markdown raw + marked.js render プレビューも見られる (バックアップ確認用) |
| **ツイートプレビュータブ** | Main + 各 Reply に「プレーン / 👁 ツイート」タブ。X dark theme 風カード (avatar / 名前 / handle / 時刻 / 本文)。時刻は section title `(19:01)` から自動抽出 |
| **画像ダウンロードボタン** | Cover / Main image を image-card 化 (サムネ + path + `⬇ DL`)。HTML5 `download` 属性で右クリック不要 |
| **weight pill** | 各ブロックに X weight (ASCII×1+全角×2) と文字数を表示 |

#### render-flow.py 呼び出し例

```bash
python3 ~/.claude/skills/x-article-writer/scripts/render-flow.py \
  --article apps/<app>/.scratch/<post-folder>/article.md \
  --post    apps/<app>/.scratch/<post-folder>/post.txt \
  --output  apps/<app>/.scratch/<post-folder>/flow.html \
  --cover   branding/sns-bocchi/reference-images/character_desk_focus.png \
  --main-image main-image.png \
  --title   "X Articles + 通常投稿 投稿フロー" \
  --subtitle "2026-MM-DD — 〇〇 記事" \
  --strategy "X Articles 先 → URL 置換 → 通常投稿でセルフリプ末誘導" \
  --goal     "フォロワー獲得 (Premium+ 4倍 + 75x リプ往復 + dwell time max)" \
  --duration "30-40 分"
# --bocchi-avatar は省略可 (デフォで character_100knock_header.png)
```

#### post.txt フォーマット

```
=== Main (推奨投稿時刻: 2026-MM-DD HH:MM) ===
<本文 (280 weight 以下)>

=== Reply 1 (HH:MM) — <短いラベル> ===
<本文>

=== Reply 2 (HH:MM) — <ラベル> ===
...
```

- `=== ... ===` の前後スペース有無は寛容 (regex `^=== ([^=]+?) ?===\s*\n?` で吸収)
- `(HH:MM)` をタイトルに含めるとツイートプレビューの時刻に自動反映

#### 末尾の `open` コマンド

```
open apps/<app>/.scratch/<post-folder>/flow.html
```

主に flow.html 1 枚で完結 (TOC で Article→Main→Reply 全部辿れる)。

---

## 共通 NG (出力前チェック必須)

- ❌ **article.md を Markdown のまま X Articles エディタに貼り付け** (リッチテキストエディタなので `## > ** -` 等の記号が raw 表示される。`article-x-plain.txt` (render-flow.py で自動生成) を貼って toolbar で見出し / 引用 / リストを手動適用するのが正解。`feedback-x-articles-no-markdown`)
- ❌ **見出しレベルを X Articles 仕様に合わせず markdown 標準のまま貼る** (X Articles は **H1 / H2 のみ表示見出し**、`### `以下は plain bold 化される。markdown 直貼りで「大見出しのつもり」が中見出しに化ける。Phase 8 の正規化スクリプト `perl -i -pe 's/^## /# /; s/^### /## /; s/^#### (.+)$/**\\1**/'` をコピペ前に必ず走らせる、または article-x-plain.txt + 手動装飾ルートを使う)
- ❌ Apple メール本文の直接引用 (`failure` / Apple reject 系の必須チェック、`feedback-apple-reject-share-safety`)
- ❌ Hook + サブタイトルの業界カタカナ語連発 (一般層伝わらない)
- ❌ 数字 / 引用の捏造 (整合性 FAIL)
- ❌ 25,000 字超過 (文字数チェック必須)
- ❌ 画像に watermark (Gemini 系)
- ❌ AI っぽい接続詞 (「重要なのは」「〜することで」)
- ❌ **章タイトルに絵文字を 2 章以上連続で並べる** (AI 感が強くなる、indie らしさが消える)。装飾絵文字は最大 1 章まで or 全削除。代わりに「症状名 — 一言エッセンス (ガイドライン番号 / 件数 / 日付)」骨格で揃える
- ❌ **章番号の機械感** (「類型 1: ...」「セクション 3: ...」)。自然な節タイトルに置換 (例: 「類型 1: IAP プロモ画像」→「IAP プロモ画像 — 4 件喰らった最頻出パターン」)
- ❌ **table を markdown のまま貼る** (X Articles エディタは markdown table を解釈せず、`|` 区切りがプレーンテキストの行内文字列に化ける)。**`templates/table-styles.css` + plain `<table>` を `scripts/render-tables.py` で PNG 化**して画像 block として挿入する。bullet list 化は読みづらいので非推奨、画像化が王道
- ❌ **AI 感ある visual レイアウト** (Swift vs Flutter 2 列対比カード / KPI 4×2 グリッド / VS バッジ / icon 装飾)。商業 LP 風で indie 記事の信頼性を落とす。**plain `<table>` のみで 10 枚並べる方が読み手は記事フォーマットとして認識し統一感を感じる** (2026-05-09 学び)
- ❌ **画像内の crest / title / footer 装飾** (「DATA · #01 · ラベル」「N 本の内訳」「<your-x-handle>」等)。章見出しと重複 + brand 過剰で AI 生成感。`.crest, .title, .footer { display: none }` で全部隠し、table 本体のみに
- ❌ **list 過多** (各章で「症状 list / 復旧 list / 学び list」の三段重ね)。short list は流れる文 + 引用ブロック (callout) に置換、本当に箇条性が強い「復旧手順」だけ list キープ
- ❌ **lede 段落の不在** (H2 直下にいきなり list / 表 / 手順)。各章は「導入文 2-3 行 → 詳細 list」の順で書く。冒頭 50 字で章の本質が伝わるか自問
- ❌ **段落が長すぎる** (5 行超は scan 効率↓)。一文 40-60 字、3-4 文で改行、PC 2-4 行 / モバイル 1-2 行でブロック化
- ❌ **章ごとの hero 画像 / stock photo 装飾** (Medium 風で AI 感の元)。indie 記事の画像は **証拠画像** (ASC スクショ / dashboard 画面 / 修正前後比較 / 実装コード抜粋) を 2-3 章にだけ挿入。cover image 1 枚 + 章末 callout で視覚 break は十分
- ❌ **同種列挙が 4 個以上続く** (例: 「ChatGPT / Spotify / Adobe / Notion / Microsoft 365」)。**3 つに絞る**のが見やすさの黄金比。例の代表性で十分伝わる
- ❌ **内輪ジャーゴン / 執筆作業ノートの本文混入** (例: 「機械的な『類型 N:』連番」「章ごとの大きな画像 / stock photo」「sim 操作の手順」等)。これらは執筆者の作業ガイドで、読者には不要。`feedback-bocchi-wording-dictionary.md` の Claude 内部ジャーゴン表参照
- ❌ **誇張・最上級表現** (「最強」「ベスト」「絶対」「世界初」「必ず」)。`Phase 7-G D 軸` で grep して全削除、「自分の場合は」「個人的には」で婉曲化
- ❌ **第三者ブランドへの断言批判** (例: 「劣る」「勝負にならず」)。**「機能としては優れているが、自分の作業スタイルでは合わなかった、好みの問題」**型に書き換え。信者対策 + 景表法 / 不正競争防止法のリスクをゼロ化
- ❌ **執筆セッション内で何度も語ってしまう同じメタ語り** (例: 「100 本ノックの本質は…」「これも『ベストじゃない、日々改善』の一例」)。1 記事につき 1 回まで、繰り返しは削除
- ❌ note URL を X Articles 内に貼る (Articles なら note より自分の X 別 Articles を貼れ)
- ❌ 章立てなし / ベタ流し (chunk 化で読了率が決まる)
- ❌ **Main 投稿画像が 1:1 正方形** (X タイムラインで cropped 表示)。**16:9 横長 (1200×675 / 1500×600) 必須**、cover.png 流用が最速。memory `feedback-x-article-image-strategy.md`
- ❌ **Main 投稿画像が 5MB 超** (X 公式制限で投稿拒否)。提出前に `sips -Z 1600 -s format jpeg -s formatOptions 85` で圧縮、7.5MB → 660KB に収まる
- ❌ **通常投稿で Articles と同じレベルで全 N パターン詳細展開** (記事誘導動機が消える)。**4 段ティーザー型** (Main フック / Reply 1 痛み 1 件 / Reply 2 数字 / Reply 3 URL) で 280 weight × 4 段に絞る。memory `feedback-x-articles-vs-post-length-strategy.md`

---

## 関連 memory / skill

- `~/.claude/projects/<your-project-slug>/memory/reference-x-bocchi-tips-template.md` — X 短文投稿テンプレ (post-bocchi の鉄板)
- `~/.claude/projects/<your-project-slug>/memory/feedback-x-post-html-preview.md` — HTML プレビュー folder 仕様 (Phase 9 で参照)
- `~/.claude/projects/<your-project-slug>/memory/feedback-bocchi-no-pronoun-spam.md` — 一人称ルール
- `~/.claude/projects/<your-project-slug>/memory/feedback-apple-reject-share-safety.md` — Apple reject 公開時の安全運用 (DPLA §10)
- `~/.claude/projects/<your-project-slug>/memory/feedback-gemini-image-watermark.md` — 画像はサポート、watermark 回避
- `~/.claude/skills/post-bocchi/SKILL.md` — 短文投稿 skill、Hook / NG / Phase 構造を流用
- `~/project/<app-factory>/templates/launch-banner/` — 数字 hero バナー (アプリリリース連動時)

## 起動例

```bash
# 新規執筆 (テーマだけ渡す)
/x-article-writer リジェクト 12 件の対処法

# 既存 markdown をブラッシュアップ
/x-article-writer apps/<example-app>/.scratch/post-YYYY-MM-DD-<slug>/article.md

# 構成だけ提案させる
/x-article-writer <topic> ローンチ振り返り --outline-only
```

## Progressive Disclosure (将来の skill 拡張余地)

初版は 1 ファイル (この SKILL.md) に集約。フォロワー数や記事数が増えて再利用パターンが固まったら、以下の references/ に分割予定:

- `references/x-articles-format.md` — フォーマット詳細
- `references/viral-structure.md` — Hook + バズ構造の事例集
- `references/plain-language.md` — 平易化ルール拡張
- `references/image-strategy.md` — 画像戦略 + 過去事例
- `references/seo-keywords.md` — AI answer engine + Google SEO

`examples/` に過去記事を蓄積:
- `examples/2026-05-08-asc-rejection-12-cases.md` (1 本目)
- 以降の Articles を accumulate

---

書いた指針: 個人開発者の 1 次情報を、フォロワー獲得 + 検索流入 + 売り切り資産にする。文章メイン、画像はサポート、watermark 回避、Apple メール直接引用なし、二段構造 (Hook = 一般、本論 = 技術)。
