# <example-app> — Claude Code コンテキスト

> **配置先**: `~/project/<app-factory>/apps/<example-app>/CLAUDE.md`
> **役割**: 個別アプリのコンテキスト。技術選定の理由 / docs/specs への links / ブランチ戦略 / デザイン路線 / 仕様の補足。

## このアプリについて
- Xcode 16 / iOS 17+ ターゲット、SwiftUI ベース
- 主機能: <example-app の差別化軸 を 1-2 行で>
- 課金: RevenueCat
- 計測: Sentry（クラッシュ + カスタムイベント）。**indie アプリは初期は Sentry なしでも OK** (DAU 増加後に検討)
- 広告: Google AdMob（Free 層のみ、Pro 非表示）

## 関連リファレンス
- `memory/reference-ios-indie-patterns.md` — Widget / hasProAccess / 空状態 / 実機 QA
- `memory/reference-revenuecat-paywall-wiring.md` — SDK 接続パターン
- `memory/reference-ios-testing-runbook.md` — DI ROI / XcodeGen test target / Swift Testing skip

## コマンド

### Slash commands（`.claude/commands/` に配置）
- `/build` — シミュレータ向け Debug ビルド
- `/run` — install + terminate + launch + screenshot
- `/run-device` — 実機に build + uninstall + install
- `/test` — Swift Testing 実行（Xcode 経由）

### 直接実行（scaffold 後に有効化）
- ビルド: `xcodebuild -workspace <example-app>.xcworkspace -scheme <example-app> -destination 'platform=iOS Simulator,name=iPhone 17 Pro' -configuration Debug -skipPackagePluginValidation build`
- 起動: `xcrun simctl launch "iPhone 17 Pro" <your.bundle.prefix>.<example-app>`
- スクショ: `xcrun simctl io "iPhone 17 Pro" screenshot /tmp/shot.png`

### 開発時の MCP
- `xcode` (xcrun mcpbridge) — Apple 純正、SwiftUI Preview 取得
- `xcodebuild` (XcodeBuildMCP) — シミュレータ + 実機
- `sentry` — クラッシュ解析（後日接続）

## 仕様書

詳細仕様は `docs/specs/` 配下を参照:
- 00 overview / 01 onboarding / 02 ... / 99 glossary

実装着手時は該当 spec を必ず読み込む。

## 禁止事項（親の `~/.claude/CLAUDE.md` 踏襲）
- commit/push はユーザー指示待ち
- `git push origin main` 直接プッシュ禁止（PR 経由）
- `.env.local` / `*.p8` / `*.mobileprovision` を絶対コミットしない

## ブランチ戦略（indie weekly ship 簡略版）

```
main        ← App Store 配信版のみ。直 push 禁止、PR 経由でのみ更新
 ↑ PR（/release）
develop     ← 日常の開発統合ブランチ。通常の作業先
 ↑ merge（solo indie のため PR 必須ではない）
feature/*   ← 複数日かかる機能（ex: feature/<topic>）
hotfix/*    ← App Store 版の緊急修正（main 起点 → main + develop にマージ戻す）
```

- 日常作業は `develop` に直 commit / push
- 1 日以上かかる機能は `feature/*` を切る
- TestFlight 配信は `develop` or `release/*` から
- App Store 提出直前のみ `main` にマージ

## デザイン路線（アプリごとに独立）
- 路線方針を 1-2 行で書く（例: 黒×余白ミニマル / グラデ Immersive / モノクロ枯山水 等）
- モック方向性は `design/mocks/` に 3 案並べる予定
- シリーズ感は「コンセプト」で揃え、UI トーンは各アプリ独立

## 収益モデル
- Free: <制限内容> + 広告あり
- Pro: 買切 ¥<XXX>（LAUNCH 特価 ¥<YYY>）
- **Pro 主訴求**: 広告なし > <主機能> > Widget 全開放 の順

## 現状（YYYY-MM-DD）
- 実装: <現状フェーズを 1-3 行で>
- TestFlight: <build N 配信済 / 未配信>
- ASC: <Age Rating / App Privacy / IAP 登録状況>
- 残: <優先 3 件>
