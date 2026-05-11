# commands/ — Slash command の代表例

Claude Code は `.claude/commands/<name>.md` を slash command として認識する。配置先は 2 つ:

| 配置先 | スコープ |
|---|---|
| `~/.claude/commands/<name>.md` | 全プロジェクト共通の slash command |
| `~/project/<repo>/.claude/commands/<name>.md` | そのプロジェクト固有の slash command |

## ファイルフォーマット

```markdown
---
description: 1 行説明（slash command 一覧に出る）
argument-hint: <arg1> [arg2]   # 任意
model: opus                     # 任意 (opus / sonnet / haiku)
---

# /command-name

本文 (markdown)。`$ARGUMENTS` で引数にアクセス可能。
```

## 4 つの代表例

| ファイル | 役割 | 配置先 |
|---|---|---|
| `pdca.md` | セッション振り返り (Plan / Do / Check / Act) | `~/.claude/commands/` |
| `asc-iap-attach.md` | App Store Connect 新規アプリ初回 IAP attach 7 step 機械化 | `~/project/<app-factory>/.claude/commands/` |
| `post-bocchi.md` | X 投稿文を 6 type × 3 案で生成 (キャラ前提) | `~/.claude/commands/` |
| `x-article-writer.md` | X Articles (長文) 執筆 (skill 概要から command 化) | `~/.claude/commands/` |

## キャラクター前提 commands

`/post-bocchi` は「キャラクターベース X アカウント」キャラ前提で書かれている。テンプレとして使う場合は:

1. キャラ名 / 口調 / 一人称ルールを自分用に置換
2. 投稿アカウント (`<your-x-handle>`) を自分のハンドルに置換
3. キャラ設定 (`~/.claude/skills/post-bocchi/SKILL.md` 相当) を自分のキャラに作り直す

## 使い方 (Claude Code に取り込む)

ターミナルで Claude Code を起動して、以下のように依頼:

> 「このリポジトリの `commands/pdca.md` `commands/asc-iap-attach.md` を `~/.claude/commands/` にコピーして、placeholder を自分の値で置換して。Claude Code 再起動して `/pdca` `/asc-iap-attach` が認識されるか確認して」

`asc-iap-attach` のようなプロジェクト固有 command を取り込む場合:

> 「`commands/asc-iap-attach.md` を `~/project/<my-factory>/.claude/commands/` に置いて、ファイル内の `<your-revenuecat-public-key>` `<your-team-id>` `<example-app>` を私の値で置換して」

手作業でやるなら:

1. ファイルを配置先にコピー
2. `<placeholder>` を自分の値に置換
3. Claude Code を再起動 (or 新セッション)
4. `/<command-name>` で呼び出し

## 設計指針

- **slash command は dispatcher** — 詳細な手順を memory (`~/.claude/projects/<slug>/memory/reference-*.md`) に書き、command はそこへの誘導 + 引数受け渡しに専念
- **冪等にする** — 同じ command を何度叩いても壊れないように
- **次の 1 手を提示する** — command の最後に「次にやるべきこと」を出力
