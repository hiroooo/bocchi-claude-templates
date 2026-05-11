# skills/ — Skill の代表例

Claude Code の **skill** は `~/.claude/skills/<name>/SKILL.md` 配置で、Claude が「このタスクならこの skill が使える」と自動判定して呼び出してくれる機能。

## ファイル配置

```
~/.claude/skills/<skill-name>/
├── SKILL.md                  # YAML front-matter (name, description) + 本文
├── templates/                # 任意。HTML / CSS テンプレ等
└── scripts/                  # 任意。Python / shell スクリプト等
```

## YAML front-matter (必須)

```yaml
---
name: skill-name
description: Use when ユーザーが「○○」「△△」を依頼したとき。<具体的な用途を 2-3 行>
---
```

`description` の `Use when ...` が Claude のトリガー条件になる。曖昧だと呼び出されない。

## 本リポに含む代表 skill

| skill | 役割 |
|---|---|
| `x-article-writer/` | X Articles (Premium+ 長文記事、最大 25,000 字) を Phase 1-9 で執筆 |

## 使い方 (Claude Code に取り込む)

ターミナルで Claude Code を起動して、以下のように依頼:

> 「このリポジトリの `skills/x-article-writer/` ディレクトリを `~/.claude/skills/x-article-writer/` にコピーして。SKILL.md の path 参照 (`~/project/<app-factory>/`, `apps/<app-name>/`, `branding/<asset>/...`) を私の環境に合わせて置換して。scripts/ で使われている Python ライブラリ (`playwright`, `markdown` など) を pip install して、Claude Code 再起動して `X Articles 書きたい` と話しかけたら呼び出されるか確認して」

手作業でやるなら:

1. ディレクトリごと `~/.claude/skills/<name>/` にコピー
2. `SKILL.md` の Path 参照を自分の環境に合わせて置換
3. `scripts/` 依存ライブラリを別途インストール
4. Claude Code を再起動 → 自然文で「X Articles 書く」等を依頼

## 設計指針

- **trigger を厳密に**: `Use when` で曖昧な範囲を書くと Claude が呼び出さない (or 呼び出しすぎる)
- **Phase 構造**: 6-9 段階で「ヒアリング → 構成 → 執筆 → 検証ゲート → 出力」型にすると再利用性 + 自動化が両立する
- **検証ゲート (Phase 7)**: スコアリング + REGEN ループを組み込むと「自分で書いたものを自分で甘く採点」を防げる
- **scripts と templates の分離**: 実行ロジックは `scripts/`、文字列フォーマットは `templates/` に。SKILL.md は呼び出し方の説明だけ

## skills ↔ commands の使い分け

| 用途 | skills/ | commands/ |
|---|---|---|
| 自然文トリガー | ○ (`description` の `Use when ...`) | △ (slash 必須) |
| 実行手順固定 | △ (Phase 自由度高) | ○ (dispatcher) |
| 引数 | △ (本文中で柔軟に解釈) | ○ (`$ARGUMENTS`) |
| Token コスト | 大 (本文全部読まれる) | 小 (呼ばれた時だけ) |

→ 「考えさせる」「複合判断」は skills、「特定手順を機械化」は commands、というのが現状の使い分け。
