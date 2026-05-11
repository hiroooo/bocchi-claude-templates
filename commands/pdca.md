---
description: セッション振り返り — 進捗を docs に保存、学びを memory に抽出、再開用 command を作成
---

# /pdca

このセッションを Plan-Do-Check-Act で振り返り、**次回セッションが途中から再開できる状態**に整える。人の記憶に頼らず、ファイルに全部落とす。

## 実行ステップ

### 1. Plan — 当初の目標を確認

- 会話ログの冒頭からセッション目標を抽出
- ユーザーの要求を要約（1-3 行）

### 2. Do — やったことを棚卸し

- TaskList / TaskGet で今セッション内に触れた task の一覧を取得
- 作ったファイル・書き換えたファイルをまとめる
- 実際に走らせたコマンド・API 呼び出しの履歴を整理

### 3. Check — 評価

- **達成**: Plan で立てた目標のうち、Done になったもの
- **未達**: 残タスク、ブロッカー、ハマった罠
- **意外な発見**: 想定外の挙動、仕様、データなど

### 4. Act — 学びを永続化

以下を**このセッション用プロジェクトの対応する場所**に書き出す:

- **セッションノート** `docs/session-<YYYY-MM-DD>-<topic>.md`
  - Plan / Do / Check / Act を短く
  - 次回の再開方法を具体的に（何を読めばいい、最初に打つコマンド）
  - 成果物のファイルパスを全列挙

- **memory/reference-*.md** — 再利用可能な事実（API 仕様、フォーマット、ファイルパスなど）
  - front-matter: `name`, `description`, `type: reference`

- **memory/feedback-*.md** — 次回以降のルール / 踏み抜いた罠
  - front-matter: `type: feedback`
  - 本文: ルール + `**Why:**` + `**How to apply:**`

- **memory/<project>-*-status.md** — 途中経過 (type: project)
  - 現在のタスク状態 / 推定パラメータ / 未達事項

- **MEMORY.md** — 上記を index に 1 行追加（既存メモリとの重複 / 置換は慎重に）

- **.claude/commands/<topic>-resume.md** (任意) — 続きから再開する slash command
  - 必要な事前チェック（サーバー起動・ファイル存在など）
  - 次の 1 手がすぐ打てるよう手順化

### 5. タスクリスト整理

- Done のタスクは `completed` へ
- 途中で止めた `in_progress` は `pending` に戻す（次回の頭で誰かが `in_progress` に戻す前提）
- 不要タスク (subsumed / obsolete) は `deleted`
- 新規発見の TODO は TaskCreate

### 6. コミットしない

- ユーザー指示がない限り commit / push はしない
- `git status` で変更の山を確認して、ユーザーに「この内容で /save しますか？」と提示して終わる

## 出力テンプレート（サマリ）

振り返り結果をユーザーに返す際は以下の粒度で:

```
## PDCA サマリ

**Plan**: <当初の目標>
**Do**: <実際にやったこと箇条書き 3-5 件>
**Check**:
- ✅ <達成>
- ⚠️ <未達、ブロッカー>
- 💡 <意外な発見>
**Act**:
- 書き出し: docs/session-*.md, memory/* N 件, .claude/commands/*
- 次回再開方法: /<resume command> を打つ or `memory/<project>-*-status.md` を読む
```

## 注意

- **冗長な「全記録」は書かない**。後から誰かが再開するのに必要な情報だけ。
- **日付は絶対日付で書く**（「昨日」「来週」ではなく `YYYY-MM-DD`）
- **コードの重複を避ける**: 同じ snippet を docs と memory に重複させず、どちらかに寄せてリンクで参照
- **プロジェクトと無関係な学び** は `~/.claude/projects/*/memory/` ではなく、より広いスコープ (ユーザーグローバル / アプリファクトリ親) に置く
