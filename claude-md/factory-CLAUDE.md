# App Factory — 個人開発アプリ量産拠点

> **配置先**: `~/project/<app-factory>/CLAUDE.md`
> **役割**: アプリを量産する親ディレクトリの方針。週次リリース / スタック選定 / 命名規約 / 提出フロー。

## ミッション
**週1本** のペースで iOS/Android/Web アプリをリリースし、収益化・販促まで回す個人開発ファクトリ。

## ディレクトリ方針
- `apps/<name>/` — 各アプリは **独立 GitHub リポを git submodule で配置**（親は管理ハブ）
- `branding/` — SNS / マーケ用ブランド資産（マスコットキャラ画像 + 投稿用プロンプト）
- `ai-tips-db/` — AI 最新 Tips の SQLite DB + fetch スクリプト
- `templates/` — スタック別スキャフォールド（swift-native-app / flutter-app / expo-app / next-web-app）
- `docs/` — 週次リリース SOP / 収益化メニュー / ASO / 販促プレイブック
- `ROADMAP.md` — Now / Next / Later / Ideas の4レーン

## スタック選定基準
| 用途 | スタック |
|---|---|
| Screen Time / ネイティブ AI / 高品質UX | **Swift native** (Xcode 16 + SwiftUI) |
| 軽量クロスプラット（タイマー/習慣/瞑想） | Flutter |
| Web中心 + モバイル補完 | Expo (React Native + Web) |
| LP / 課金管理 / ダッシュボード | Next.js 15 |

## 週次リズム（月〜金）
- **月火**: 開発（コア機能実装）
- **水**: QA（E2E + 実機確認 + ストア用スクショ）
- **木**: ストア提出（TestFlight / Internal Testing → 本番審査）
- **金**: 販促（X / Product Hunt / TikTok 原稿、次週アプリのアイデア vet）

## Claude Code 運用
- 公式プラグイン: `frontend-design` / `swift-lsp`
- プロジェクト commands: `/new-app` / `/weekly-ship` / `/app-status` / `/idea-vet` / `/pre-ship-check` / `/submit-review`
- memory: `~/.claude/projects/<project-slug>/memory/` に蓄積（`MEMORY.md` が index）
- iOS 固有の reference は `memory/reference-*.md` 参照

## スラッシュコマンド
- `/new-app <name> <stack>` — 新アプリ scaffold + gh repo create + submodule add
- `/weekly-ship <app>` — 週次リリースチェック
- `/app-status` — 全アプリ横断ステータス
- `/idea-vet <idea>` — 市場調査・実現性評価
- `/pre-ship-check <app>` — ビルド前の lint / XcodeGen / device-qa 検証 + ASC reject 6 類型 regex check + IAP 初回 attach フック
- `/submit-review <app>` — ASC 審査提出直前チェック (24h 前必須 15 項、過去 reject 経験から逆算)
- `/review-reject-fix <app> [reject-email]` — リジェクト対応の 6 類型別 playbook (2.3.2 IAP / 2.3.7 スクショ / 2.1(b) IAP attach / 5.1.1(iv) Permission UX / 2.1 ATT / 提出 blocker)
- `/asc-iap-attach <app>` — IAP 初回提出時 7 step 機械化 (2.1(b) reject 防止 / 既 reject 復旧)
- `/post-bocchi <type>` — キャラクターアカウント (`<your-x-handle>`) 用 X 投稿文を 6 type × 3 案で生成

## マーケ/ASO skill ツールキット（`~/.claude/skills/` 配下）
週次 ship フロー前後で呼ぶ。
- **ASO 4 連** (ASC 提出時): `keyword-research` → `metadata-optimization` → `app-description-writer` → `aso-appstore-localize`（多言語）
- **画像生成** (素材生成時): `iap-promo-image` — IAP プロモ画像 1024×1024 を価格ゼロ独自ポスター HTML テンプレで生成
- **マーケ/コピー** (ローンチ前後): `launch-strategy` / `copywriting` / `page-cro` / `email-sequence` / `cold-email` / `paywall-upgrade-cro`
- **リリース文** (next build): `release-app-store-changelog`（git log → What's New 草案）
- **デザイン audit**: `design-review` — Web/iOS/Android UI を 9 軸スコア + 5 シグナルで audit
- **安全弁** (常時 hook): `git-guardrails-claude-code` — `git push` / `reset --hard` 等を物理 block

## ASC 提出 / リジェクト対応（体系化）
過去の reject 経験から 6 類型を抽出。提出フロー全体を skill/command/memory で再現可能化:

- **memory 核 2 ファイル** (`~/.claude/projects/<project-slug>/memory/`):
  - `reference-asc-rejection-patterns.md` — reject 6 類型 + 提出 24h 前必須チェック 15 項
  - `reference-asc-playwright-master.md` — ASC Playwright 操作の罠 6 件 (dirty flag / file_chooser 二重 PUT / React natural click / Capability 紐付け)
- **command 3 強化** (`/submit-review` / `/review-reject-fix` / `/pre-ship-check`): 上記 memory への dispatcher として機能
- **command 1 新設**: `/asc-iap-attach`
- **scaffold ガイド**: `templates/swift-native-app/design/SCAFFOLD-NOTES.md` — 新アプリ素材作成時の禁則事項 5 か条 + 推奨 skill/command + 関連 memory

## グローバルルール踏襲
- 親の `~/.claude/CLAUDE.md` の禁止事項（`docker system prune` 禁止・`git push origin main` 禁止・commit/push はユーザー指示待ち）を本プロジェクトでも遵守
- **例外**: Swift native アプリは Docker 化せず Xcode / macOS 上で直接ビルドする（他プロジェクトは Docker 前提ルールが適用）

## Bundle ID prefix 固定ルール（Swift native アプリ）
- **Bundle ID prefix は `<your.bundle.prefix>` で固定**。過去事故で別の prefix を使ったことがあるが、必ず 1 つに統一する
- 関連識別子も全部 同 prefix で揃える: Bundle ID / Widget Bundle ID / App Group (`group.<your.bundle.prefix>.<slug>.shared`) / iCloud Container (`iCloud.<your.bundle.prefix>.<slug>`)
- 対象: `project.yml` bundleIdPrefix / `Config/*.xcconfig` PRODUCT_BUNDLE_IDENTIFIER / `*.entitlements` / `fastlane/Fastfile` / `fastlane/Appfile` app_identifier / アプリコード内 `containerURL(...)` / `cloudKitDatabase: .private(...)`
- ただし `Appfile` の `apple_id("<your-apple-id-email@example.com>")` は **Apple ID ログインメールなので例外**、Bundle ID prefix と別物
- `fastlane register` を叩く前に必ず `grep -rn "<old.prefix>" apps/<new>/` で 0 件確認

## 一時ファイルの置き場所

- **プロジェクトルート (`~/project/<app-factory>/`) に一時ファイルを生成しない**
- Playwright MCP の `browser_snapshot` / `browser_take_screenshot`、Xcodebuild MCP の `screenshot`、ASC 操作キャプチャ、検証用の中間 md/png 等は **必ず `apps/<name>/.scratch/` 配下に出力する**
- 各アプリ submodule の `.gitignore` に `.scratch/*` が登録済み（commit 混入防止）
- セッションまたぎで残したいなら `apps/<name>/docs/` 配下の適切なサブディレクトリへ移す
- ルート直下に新しい `.md` / `.png` を書く前に「これはどのアプリに属するか」を必ず自問する
