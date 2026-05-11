# claude-md/ — CLAUDE.md の 3 階層

Claude Code は起動時に **3 階層の CLAUDE.md** を順番に読み込んで context を構築する。階層化することで「全プロジェクト共通ルール」「ファクトリ全体の方針」「個別アプリの仕様」を独立に管理できる。

## 階層

| ファイル | 配置先 | 役割 |
|---|---|---|
| `global-CLAUDE.md` | `~/.claude/CLAUDE.md` | 全プロジェクト共通ルール (Docker 前提 / 禁止事項 / モデル使い分け / 単価) |
| `factory-CLAUDE.md` | `~/project/<app-factory>/CLAUDE.md` | アプリ量産拠点の方針 (週次リリース / スタック選定 / Bundle ID prefix / scaffold ルール) |
| `app-CLAUDE.md` | `~/project/<app-factory>/apps/<app-name>/CLAUDE.md` | 個別アプリのコンテキスト (技術選定 / 仕様書場所 / ブランチ戦略 / デザイン路線) |

## 読み込み順

Claude Code は起動時に CWD から親ディレクトリへ向かって `CLAUDE.md` を探索する。アプリ → factory → global の順に重ね合わさる。

## 使い方 (Claude Code に取り込む)

ターミナルで Claude Code を起動して、以下のように依頼:

> 「このリポジトリの `claude-md/global-CLAUDE.md` を `~/.claude/CLAUDE.md` にコピーして、`<your-username>` `<your-monthly-rate>` `<your-hourly-rate>` などの placeholder を自分の値で置換して。あと自分のプロジェクト用に `~/project/<my-factory>/CLAUDE.md` を `factory-CLAUDE.md` 雛形ベースで作って」

> 「`app-CLAUDE.md` を雛形に、`apps/<my-new-app>/CLAUDE.md` を作って。技術選定 (Swift native / Flutter / Next.js)・docs 配置・ブランチ戦略・デザイン路線 を私のアプリ用に書いて」

手作業でやるなら:

1. 各テンプレを上記の配置先にコピー
2. `<placeholder>` を自分の値に置換
3. プロジェクト固有のルールを追加 / 削除

## 設計指針

- **global** — 「全部のプロジェクトで Claude にやってほしくない / やってほしい」を集約。短く、絶対ルールだけ
- **factory** — 「このディレクトリ群全体で守る」事項。スタック選定 / 命名規約 / 提出フローのテンプレ
- **app** — 「このアプリだけの」仕様。docs/specs への links、設計判断の経緯、デザインの一貫性ルール

3 階層に分けないと、グローバルルールがアプリ別 CLAUDE.md にコピペで散らばり、メンテで死ぬ。
