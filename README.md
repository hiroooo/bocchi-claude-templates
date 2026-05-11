# bocchi-claude-templates

Claude Code (Anthropic 公式 CLI) を使って iOS/Web アプリを個人開発する人向けの、CLAUDE.md / Slash commands / Skills / scaffold テンプレ集。

[「10 日で iOS アプリ 3 本、作り方ぜんぶ公開 — 100 本ノック #01」](https://x.com/bocchistay/status/2052929860784529778) で言及した内容の実装が一式入ってます。

## 構成

- `claude-md/` — CLAUDE.md の 3 階層 (グローバル / Factory / アプリ別) サンプル
- `commands/` — Slash command の代表例 (`/pdca` `/asc-iap-attach` `/post-bocchi` `/x-article-writer`)
- `skills/` — Skill の代表例 (`x-article-writer` = X Articles 執筆 skill)
- `templates/swift-native-app/` — Swift native アプリ scaffold 用テンプレ (project.yml + xcconfig + Package.swift + fastlane)

## 使い方 (Claude Code に取り込む)

### A. 自分の `~/.claude/` に丸ごとコピーしたい時

ターミナルで Claude Code を起動して、以下のように依頼:

> 「このリポジトリ (`https://github.com/hiroooo/bocchi-claude-templates`) を `/tmp/` に clone して、`commands/` の中身を `~/.claude/commands/` に、`skills/` の中身を `~/.claude/skills/` にコピーして。コピー後、各ファイル内の `<placeholder>` を自分の値で置換して。具体的には `<your-github-username>` (Package.swift の自分の app-version-gate 等の参照先) `<your-username>` (macOS user 名) `<your.bundle.prefix>` `<your-apple-id-email@example.com>` `<YOUR_TEAM_ID>` `<your-x-handle>` `<app-factory>` (factory ディレクトリ名) `<your-project-slug>` `<example-app>` (アプリ slug) を、自分の実際の値に書き換えて。」

### B. 個別ファイルだけ取り込みたい時

> 「このリポジトリの `commands/pdca.md` だけを `~/.claude/commands/pdca.md` にコピーして、ファイル内の placeholder を自分の環境に合わせて置換して」

### C. CLAUDE.md 3 階層を自分のプロジェクトに導入したい時

> 「`claude-md/` の 3 階層テンプレ (`global-CLAUDE.md` / `factory-CLAUDE.md` / `app-CLAUDE.md`) を参考にして、自分のプロジェクト用 CLAUDE.md を作って。グローバル (`~/.claude/CLAUDE.md`) は `<your-username>` や Docker 前提などを自分用にカスタマイズ、Factory レベル (`~/project/<my-factory>/CLAUDE.md`) は週次リズムや Bundle ID prefix を書き換え、アプリ別 (`apps/<my-app>/CLAUDE.md`) は実装ガイドを書く」

### D. Swift native scaffold だけ使いたい時

> 「`templates/swift-native-app/` の中身を `apps/<myapp>/` にコピーして、README に書いてある placeholder (`<example-app>` `<ExampleApp>` `<your.bundle.prefix>` `<YOUR_TEAM_ID>` `<your-apple-id-email@example.com>`) を自分の値で sed 置換して、`xcodegen generate` で .xcodeproj を作って」

詳細は各ディレクトリの README.md を参照。

## 注意

- キャラクター画像 (`character_*.png` 等のアバター素材) は個人ブランド資産のため含まれていません。自分用の画像 (`<your-character-image>.png`) を別途用意して差し替えて使ってください
- Apple Developer Team ID / RevenueCat key 等の機密情報は全て `<placeholder>` 化済みです、自分の値で置換してください
- `commands/post-bocchi.md` および `skills/x-article-writer/` の一部は「キャラクターを軸にした SNS 運用」を前提にしています。汎用 X 運用に使う場合は本文中の「自分のキャラ」関連表現や `--bocchi-avatar` などのフラグを、自分の運用スタイルに合わせて読み替え / 削除してください

## License

MIT (Claude/Anthropic は商標、個別管理)
