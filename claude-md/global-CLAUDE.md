# グローバルルール（全プロジェクト共通）

> **配置先**: `~/.claude/CLAUDE.md`
> **役割**: 全プロジェクトで Claude Code に適用したいルール。短く、絶対ルールだけ書く。

## 基本原則

- **Docker 前提開発**: 全プロジェクトで Docker コンテナ内開発。ローカルに直接 `npm install` や `pip install` しない
- **他プロジェクト保護**: `docker system prune` 禁止。コンテナ停止時は対象プロジェクトのみ
- **確認URL必須**: 修正完了時は必ず確認用URLを提示する（例: `http://localhost:3001/path`）
- **実動確認してから報告**: 「できた」と言う前にビルド成功・サーバー起動・ブラウザ確認を行う
- **commit/push はユーザー指示を待つ**: 明示的な指示（`/save`, `ok。commit` 等）なしにコミット・プッシュしない

## モデル使い分け

| モデル | 用途 |
|--------|------|
| Opus | 重要判断（台本執筆、構成レビュー、複雑なロジック実装） |
| Sonnet | 軽作業（フォーマット、体裁レビュー、commit/push 委任） |
| Haiku | 調査・確認（ログ確認、ステータスチェック） |

## 自分の単価（開発見積もり / 工数試算で使う標準値）

| 項目 | 値 |
|---|---|
| 人月 | <YOUR_MONTHLY_RATE> |
| 時給換算 | <YOUR_HOURLY_RATE> |
| 1 人月の換算 | 160h（20 営業日 × 8h） |

- 議論の主軸は **時間 (h) と人月**、金額は社内稟議 / 客先提示用の参考値
- 見積もりは `/dev-estimation` skill が default でこの単価を使う（`--rate` `--monthly-rate` で上書き可）

## ポート一覧（プロジェクト別）

| ポート | サービス | プロジェクト |
|--------|---------|-------------|
| 3000-3099 | Web フロントエンド | example-web |
| 3306-3399 | MySQL | example-api |
| 8000-8099 | API (FastAPI / Hono 等) | example-api |

ワークツリーポート = ベースポート + (Issue番号 % 100)

## 技術スタック概要

| 領域 | 技術 |
|------|------|
| Mobile | Swift native (iOS) / Flutter (cross) |
| Frontend | Next.js 15 / React 19 + Vite |
| Backend | FastAPI + SQLAlchemy Async / Hono on Cloudflare Workers |
| インフラ | AWS (ECS Fargate, Lambda, S3, RDS), Terraform, Docker Compose |

## セッションの儀式

### 開始時（SessionStart フックで自動表示）
- ブランチ名、未コミット変更数、Docker 状態が自動表示される
- 未コミット変更がある場合は前回の作業を確認

### 終了時（Stop フックで自動警告）
- 未コミット変更があれば警告が表示される
- `/save` でコミット+プッシュしてからセッション終了

### 共有コマンド（全プロジェクト共通）
| コマンド | 説明 |
|---------|------|
| `/save` | commit + push 一括 |
| `/ship` | commit + push + develop→main マージ |
| `/check` | Docker内 lint/型チェック |
| `/code-review` | コードレビュー |
| `/pr-ship` | worktree→PR→マージ→片付け |
| `/kill-zombies` | ゾンビプロセス停止 |
| `/pdca` | セッション振り返り |
| `/diagnose` | エラー自動診断 |
| `/sync` | 全リポ pull + 状態レポート |
| `/dev-up` / `/dev-down` | Docker 環境起動/停止 |

## iOS 開発（Swift native アプリ、`apps/*` 配下）

> Docker 前提の例外領域。Xcode/macOS で直接ビルド。

### ツール前提
- **Xcode 16+ / iOS 17+ / Swift 6.1 / SPM package 中心 / MV パターン（ViewModel 不使用）**
- **XcodeGen**: `project.yml` → `xcodegen generate` で `.xcodeproj` 自動生成。GUI 作成より優先
- **Fastlane + ASC API Key**: `~/.appstoreconnect/AuthKey_<YOUR_KEY_ID>.p8` を全 iOS アプリで流用
- **XcodeBuildMCP**: `mcp__xcodebuild__build_sim` / `build_run_sim` / `session_set_defaults`（profile 切替で複数アプリ管理）

### SwiftLint が「エラー化」する既知ルール（ビルド失敗）
- **TODO コメント禁止**: `// TODO:` は違反、普通のコメントで書く
- **Large tuple 禁止**: 3 要素超のタプルは struct に
- **Line length 120**: multi-line init で対応
- **File length 500**: ファイル分割

### SourceKit の既知の誤検知（無視）
- 同一 module 内の `Cannot find type 'Xxx' in scope`
- `'View' is only available in macOS 10.15 or newer`（Package iOS only でも macOS と誤判定）
- → 実 build を走らせて確認すれば正体が分かる

### XcodeGen の罠
- `project.yml` の `info:/entitlements:` 指定は既存 plist を**最小化で上書き**。詳細 plist を保ちたいなら節自体を消して xcconfig の `INFOPLIST_FILE` / `CODE_SIGN_ENTITLEMENTS` だけで指定
- `resources: [.process("Resources")]` は空ディレクトリだと sim の CodeSign が失敗。ファイルが入るまで指定しない（`.gitkeep` だけではダメ）

### Fastlane / Apple Developer Portal
- **`produce` action は Apple ID + 2FA が必要**。ASC API Key だけで完結したいなら `Spaceship::ConnectAPI::BundleId.create` を直叩きする lane を書く
- `app_store_connect_api_key(set_spaceship_token: true)` で Spaceship global token 設定 → 後続 ConnectAPI 呼出で使える
- **ASC `apps` リソース CREATE は Admin role 必須**。App Manager role では拒否される → ASC の GUI で手動作成する方が早い
- **Widget Extension も Bundle ID 登録必要**（`<main>.widgets`）。fastlane register lane で同時登録
- **App Group / CloudKit Container の登録は ConnectAPI 非対応** → Xcode Automatic Signing + Portal GUI

### entitlements の扱い
- Portal で Capability 登録完了まで、`iCloud/APS/App Groups` は **コメントアウトで保持**（起動クラッシュ回避）
- App Group 未登録時は `App.init()` 内の `FileManager.containerURL` を fallback（Documents）で保護

### ビルドコマンドの必須フラグ
- `extraArgs: ["-skipPackagePluginValidation"]` — SwiftLintPlugins 承認ダイアログ回避
- **Xcode 16 + App Extension は `ENABLE_DEBUG_DYLIB=NO`** — Extension 新コードが `.debug.dylib` に分離されて反映されない罠

### 人間作業（Claude 不可、時期が来たら案内）
- ASC で App 新規作成 / Privacy Details 入力 / IAP 登録
- RevenueCat ダッシュボードの Product/Entitlement/Offering 作成
- CloudKit Container 登録（Portal GUI）
- Sandbox 課金テスト（実機必須）
- スクショ 8 枚の Figma 合成（Chrome headless の Full page PNG を素材化した状態で渡す）

### 新アプリ scaffold の推奨フロー（30 分）
1. 名前候補 3 つ並列で衝突チェック（App Store + ドメイン + 商標）
2. `apps/<name>/` ディレクトリ作成、`docs/` に planning / features / pricing は最初に書く（specs / aso / legal は提出直前に）
3. リファレンスアプリの `project.yml` / `Config/` / `Package.swift` / `fastlane/` を **コピー → 置換**
4. `xcodegen generate` → `mcp__xcodebuild__build_sim` で Hello World 確認
5. `fastlane register` で Bundle ID 自動登録

## やってはいけないこと

- `docker system prune` — 他プロジェクトの volume を破壊する
- `git push origin main` — 保護ブランチ
- `npm run lint` / `tsc` をローカル直接実行 — worktree では node_modules がない
- `.env` や credentials をコミット
- ユーザー確認なしの破壊的操作（DB削除、ブランチ削除、force push）
