# Swift native app scaffold テンプレ

iOS native アプリ (Xcode 16 + SwiftUI + Swift 6.1) を **30 分で動く Hello World** まで持っていく scaffold テンプレ。

## このテンプレで賄える範囲

| ファイル | 役割 |
|---|---|
| `project.yml` | XcodeGen の入力 (target / scheme / 依存関係 / 署名設定) |
| `Config/Shared.xcconfig` | バージョン / Bundle ID / Swift 設定 / Signing |
| `Config/Debug.xcconfig` | Debug 専用 override (現状ほぼ空) |
| `Package.swift` | SPM ローカル package (RevenueCat / Sentry / GMobileAds / SwiftLint 等) |
| `fastlane/Fastfile` | `register` (Bundle ID + Capabilities + AppGroup + ASC App 自動登録) / `beta` (TestFlight upload) / `attach_build` / `submit_for_review` |
| `fastlane/Appfile` | app_identifier / apple_id / team_id |

## 30 分セットアップ手順

### 1. ディレクトリコピー + 名前置換

```bash
# テンプレを <example-app> としてコピー
cp -R templates/swift-native-app apps/<example-app>
cd apps/<example-app>

# プレースホルダ一覧を確認
grep -rn "<example-app>\|<your\.bundle\.prefix>\|<YOUR_TEAM_ID>\|<your-apple-id-email>" .

# 一括置換 (例)
APP=<example-app>
PREFIX=jp.example
TEAM=ABCDE12345
EMAIL=you@example.com

find . -type f \( -name "*.yml" -o -name "*.swift" -o -name "*.xcconfig" -o -name "Fastfile" -o -name "Appfile" -o -name "*.md" \) \
  -exec sed -i.bak \
    -e "s|<example-app>|$APP|g" \
    -e "s|<your\.bundle\.prefix>|$PREFIX|g" \
    -e "s|<YOUR_TEAM_ID>|$TEAM|g" \
    -e "s|<your-apple-id-email@example.com>|$EMAIL|g" \
    {} \;
find . -name "*.bak" -delete
```

### 2. テンプレ内のフォルダ名 → 自分のアプリ名にリネーム

`project.yml` 内の sources path や package products も実際のディレクトリ名に揃える:

```yaml
# 例: ディレクトリ構成は実装側に合わせて自由
targets:
  <ExampleApp>:
    sources:
      - path: <ExampleApp>
        excludes: ["*.plist"]
```

### 3. XcodeGen 実行

```bash
brew install xcodegen   # 未導入なら
xcodegen generate
```

`<ExampleApp>.xcodeproj` が生成される。GUI で開いて Sim 起動を試す。

### 4. ASC API Key 配置 + 環境変数

```bash
mkdir -p ~/.appstoreconnect
# ASC で発行した .p8 を保存
cp ~/Downloads/AuthKey_<YOUR_KEY_ID>.p8 ~/.appstoreconnect/

# fastlane/.env (gitignored) に書く
cat > fastlane/.env <<EOF
ASC_KEY_ID=<YOUR_KEY_ID>
ASC_ISSUER_ID=<YOUR_ISSUER_ID>
ASC_KEY_PATH=~/.appstoreconnect/AuthKey_<YOUR_KEY_ID>.p8
EOF
```

### 5. Bundle ID + ASC App 自動登録

```bash
fastlane register
```

これで Apple Developer Portal に Bundle ID + Capabilities + App Group が、ASC に App entry が自動で作られる。

> **CloudKit Container だけは ConnectAPI 非対応** — Portal GUI で別途登録が必要。

### 6. Hello World ビルド

```bash
xcodebuild -project <ExampleApp>.xcodeproj -scheme <ExampleApp> \
  -destination 'platform=iOS Simulator,name=iPhone 17 Pro' \
  -configuration Debug -skipPackagePluginValidation build
```

または XcodeBuildMCP 経由:

```
mcp__xcodebuild__session_set_defaults --project ./<ExampleApp>.xcodeproj --scheme <ExampleApp>
mcp__xcodebuild__build_run_sim
```

## 置換ルールまとめ

| placeholder | 置換例 | 影響範囲 |
|---|---|---|
| `<example-app>` | `myapp` (slug) | Fastfile / Appfile / project.yml app_identifier 末尾 |
| `<ExampleApp>` | `MyApp` (PascalCase) | project.yml target 名 / scheme 名 / Package.swift product 名 |
| `<your.bundle.prefix>` | `jp.example` | Bundle ID prefix 全箇所 |
| `<YOUR_TEAM_ID>` | `ABCDE12345` (10 桁) | DEVELOPMENT_TEAM (Shared.xcconfig + Appfile) |
| `<your-apple-id-email@example.com>` | `you@example.com` | Appfile apple_id |

## 既知の罠 (scaffold 後にハマるやつ)

- **SwiftLint がエラー化するルール** (`// TODO:` 禁止 / 行 120 / ファイル 500 / Large tuple 禁止) — 実装前に SwiftLint config を先に揃える
- **Xcode 16 + App Extension は `ENABLE_DEBUG_DYLIB=NO`** が必須 — 設定漏れで Widget 新コードが反映されない
- **空ディレクトリの `resources: [.process("Resources")]`** は sim CodeSign 失敗 — ファイルを置いてから指定
- **App Group / iCloud Container は Capability 登録完了まで entitlements でコメントアウト** — 起動クラッシュ防止
- **`fastlane register` は ASC `apps` リソース CREATE が Admin role 必須** — App Manager role なら GUI で手動登録
- **`fastlane build_app` の Apple Distribution signing** — keychain に Distribution cert がなくても `xcargs: "-allowProvisioningUpdates"` + ASC API Key で bypass 可

## 関連 reference (memory に置く想定)

- `reference-fastlane-patterns.md` — produce 代替 / rescue / Internal Beta Group 手動作成
- `reference-asc-fastlane-metadata-lanes.md` — IAP / Availability / Categories / Build attach / Age Rating
- `reference-export-compliance-info-plist.md` — `ITSAppUsesNonExemptEncryption=false` で恒久 bypass
- `reference-widget-appgroup-setup.md` — JSON pipe / target 分離 / ENABLE_DEBUG_DYLIB
- `reference-revenuecat-paywall-wiring.md` — PurchaseService 薄ラッパー
- `xcode16-extension-debug-dylib-trap.md` — App Extension 反映されない罠

## License

このテンプレ自体は MIT。RevenueCat / Sentry / GoogleMobileAds / SwiftLint Plugins は各自のライセンスに従う。
