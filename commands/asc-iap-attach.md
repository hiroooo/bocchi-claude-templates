---
description: 新規アプリ初回 v1.0 提出時の IAP attach 7 step を機械化（2.1(b) reject 防止 / 既 reject 復旧）
argument-hint: <app-name>
---

# /asc-iap-attach

対象アプリ: `$ARGUMENTS` （例: `example-app-1` / `example-app-2`）

ASC 新規アプリの **初回 v1.0 提出** で、IAP を「メタデータが不足」のまま放置すると Apple から **Guideline 2.1(b) Performance: App Completeness** で reject される。経験から 1h 復旧する手順を機械化。**新規 v1.0 提出時必須**、既存アプリの v1.0.x 更新では不要。

## 鉄則

- IAP の状態が「**提出準備完了**」でないと、version 画面の「アプリ内購入とサブスクリプション」セクション自体が出現せず、attach UI が無いまま気づかず提出してしまう
- メタデータ不足の主因は **App Review Screenshot (審査に関する情報 > スクリーンショット)** 未 upload
- dirty flag が立たないと「保存」が disabled (`feedback-asc-dirty-flag-trap.md`) → 1 char 編集で強制 dirty 化
- reject 受信時の復旧は **build 上げ直し必須**、metadata reject 路線は使えない (Apple が "upload a new binary" と明示)

## 7 step フロー

### Step 1: ASC IAP 状態確認

```
mcp__appstore-connect__list_apps                                      # appId 取得
# 別途 ASC GUI で /apps/<appId>/distribution/iaps を開く
```

各 IAP の **状態** 列をチェック:
- 「提出準備完了」 → Step 5 へジャンプ (attach 段階)
- 「メタデータが不足」 → Step 2 へ進む (Review Screenshot upload 必須)

### Step 2: Paywall sheet を Sim で撮影

最低 640×920、最大 1242×2688 (iPhone) の PNG が必要。**MCP `screenshot` tool は optimized JPEG で 368×800 と小さくなる罠**があるため `xcrun simctl` 直叩きで生 PNG を撮る:

```bash
# Sim をブートして Paywall sheet を表示させた状態で
xcrun simctl io booted screenshot apps/$ARGUMENTS/.scratch/iap-review-screenshot.png

# 寸法確認 (1206×2622 等が出るはず)
sips -g pixelWidth -g pixelHeight apps/$ARGUMENTS/.scratch/iap-review-screenshot.png
```

### Step 3: ASC で Review Screenshot upload (Playwright)

```
https://appstoreconnect.apple.com/apps/<appId>/distribution/iaps/<iapId>
```

「**審査に関する情報 > スクリーンショット**」slot に upload。「画像（任意）」slot とは別物 (こちらは IAP プロモ画像、A 類型 reject の対象)。

Playwright 操作の罠は `reference-asc-playwright-master.md` §罠 4 (screenshot upload) を参照。upload 自体は auto-save なので「保存」ボタン不要。

### Step 4: 審査メモ + dirty 化 + 保存

「審査に関する情報」セクションに **審査メモを 1 char 以上** 入れて dirty flag を立てる:

```
Apple Reviewer 向け: Paywall sheet 上で対象 IAP を tap → Sandbox account で購入できることを確認してください。
```

→ page top「保存」が **enable** になることを確認 → click → API 永続化。disabled なら別 field 1 char 変更で dirty 化 (`feedback-asc-dirty-flag-trap.md`)。

**page reload して「審査に関する情報」が残っているか必ず確認**。

### Step 5: 状態遷移確認

IAP 一覧ページで状態が「メタデータが不足」→ **「提出準備完了」** に遷移しているか確認。遷移しない場合は Step 4 の保存が永続化されてない (dirty flag 罠) → 再度保存。

### Step 6: version 画面で attach

```
https://appstoreconnect.apple.com/apps/<appId>/distribution/ios/version/inflight
```

「**アプリ内購入とサブスクリプション**」セクションが新規出現する (IAP が「提出準備完了」状態に遷移して初めて出る)。

1. 「**アプリ内購入またはサブスクリプションを選択**」 click
2. modal で対象 IAP の row checkbox を click (natural click 必須、`feedback-playwright-main-vs-agent`)
3. 「完了」 click
4. version 画面で IAP が表示されているか確認

### Step 7: ConnectAPI で sanity check

```bash
mcp__appstore-connect__list_app_versions appId=<id>           # versionId 取得
# version detail で inAppPurchases relationship を確認
```

submission に attach されているか version 画面で目視 + API でダブルチェック。

## reject から復旧する場合 (1h 復旧パターン)

Apple が "upload a new binary" と明示するので **build 上げ直し必須**。

1. 上記 Step 1-7 を完走 (IAP メタデータ完成 + version attach)
2. `Config/Shared.xcconfig` の `CURRENT_PROJECT_VERSION` を bump
3. `cd apps/$ARGUMENTS && fastlane beta` で新 binary upload (5-10 min)
4. `fastlane attach_build` で新 build を version に紐付け
5. Resolution Center で英語返信 (添付なし、`reference-asc-playwright-master.md` §罠 2 のフロー)
6. version 画面の「**審査内容を更新**」 click
7. submission detail へ遷移 → 「**App Reviewに再提出**」 click → 「審査待ち」復帰

## 出力

各 step の進捗を以下のフォーマットで報告:
- ✅ / ⚠️ / ❌ + 1 行サマリ
- ❌ があれば次の手順を user に提案
- 完走したら最後に user に確認を求める (実機 Sandbox 購入テストの依頼)

## 関連 memory

**核**:
- `feedback-iap-first-submission-attach.md` — 本 command の根拠
- `reference-asc-playwright-master.md` — Playwright 操作 罠 5 件
- `reference-asc-rejection-patterns.md` — C 類型: 2.1(b) IAP 不完全提出

**個別**:
- `feedback-asc-dirty-flag-trap.md` — Step 4 dirty 化
- `reference-asc-fastlane-metadata-lanes.md` — `attach_build` lane の使い方
- `feedback-marketing-url-mandatory.md` — 同じ「初回提出忘れ物」系統
