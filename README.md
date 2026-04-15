# claude-code-skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/yasuhiro112358/claude-code-skills/pulls)

A collection of reusable Claude Code skills and prompts.

**[日本語はこちら / Japanese below](#japanese)**

---

## What is this?

This repository contains [Claude Code](https://claude.ai/code) skills (`SKILL.md` format) and standalone prompts that you can use in your own projects. Each skill is a self-contained prompt file that can be used in two ways:

- **Claude Code users**: Copy a skill folder to `~/.claude/skills/` and invoke it with `/skill-name`
- **Claude.ai / API users**: Copy the prompt content and paste it directly into a conversation

---

## Quick Start

### For Claude Code users

```bash
# Clone the repository
git clone https://github.com/yasuhiro112358/claude-code-skills.git

# Copy a skill to your Claude Code skills directory
cp -r claude-code-skills/skills/smart-commit ~/.claude/skills/

# Now use it in Claude Code
# /smart-commit
```

### For Claude.ai users

Open a skill's `SKILL.md`, copy the prompt content (after the frontmatter `---`), and paste it into a Claude.ai conversation.

---

## Skills

| Name | Category | Description | Dependencies |
|------|----------|-------------|--------------|
| *(coming soon)* | - | - | - |

---

## Agents

| Name | Description | Tools Required |
|------|-------------|----------------|
| *(coming soon)* | - | - |

---

## Prompts

Standalone prompts (no Claude Code required).

| Name | Description | Dependencies |
|------|-------------|--------------|
| [generate-prompt-from-conversation](prompts/generate-prompt-from-conversation.md) | Generate a reusable prompt from a completed AI conversation | None |
| [code-dependency-analysis](prompts/code-dependency-analysis/) | Interactively extract C++/Java/C# dependency graphs (UML class & package diagrams in Mermaid) via chat AI + VS Code preview | Python 3.8+, VS Code + Mermaid Chart extension |

---

## Contributing

Contributions are welcome! Please open an issue or pull request.

When contributing a skill, ensure:
- No personal information or private file paths
- No dependencies on private repositories
- Self-contained and usable in any project

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

<a name="japanese"></a>

# claude-code-skills（日本語）

再利用可能な Claude Code スキル・プロンプトのコレクションです。

---

## このリポジトリについて

[Claude Code](https://claude.ai/code) のスキル（`SKILL.md` 形式）と単体プロンプトを公開しています。スキルは2通りの使い方ができます：

- **Claude Code ユーザー向け**: スキルフォルダを `~/.claude/skills/` にコピーして `/スキル名` で呼び出す
- **Claude.ai / API ユーザー向け**: `SKILL.md` のプロンプト本文をそのまま会話に貼り付けて使う

---

## クイックスタート

### Claude Code で使う場合

```bash
# リポジトリをクローン
git clone https://github.com/yasuhiro112358/claude-code-skills.git

# スキルを Claude Code のスキルディレクトリにコピー
cp -r claude-code-skills/skills/smart-commit ~/.claude/skills/

# Claude Code で呼び出す
# /smart-commit
```

### Claude.ai で使う場合

使いたいスキルの `SKILL.md` を開き、フロントマター（`---` で囲まれた部分）より後のプロンプト本文をコピーして、Claude.ai の会話に貼り付けてください。

---

## スキル一覧

| 名前 | カテゴリ | 概要 | 依存 |
|------|---------|------|------|
| *(準備中)* | - | - | - |

---

## エージェント一覧

| 名前 | 概要 | 必要なツール |
|------|------|------------|
| *(準備中)* | - | - |

---

## プロンプト

Claude Code 不要で使える単体プロンプト。

| 名前 | 概要 | 依存 |
|------|------|------|
| [generate-prompt-from-conversation](prompts/generate-prompt-from-conversation.md) | 完了した AI 作業から再利用可能なプロンプトを生成 | なし |
| [code-dependency-analysis](prompts/code-dependency-analysis/) | 対話型 AI + VS Code プレビューで C++/Java/C# の依存関係を段階抽出し UML クラス図・パッケージ図（Mermaid）を生成 | Python 3.8+、VS Code + Mermaid Chart 拡張 |

---

## コントリビューション

Issue・Pull Request 歓迎です。スキルを追加する際は以下を確認してください：

- 個人情報・プライベートなファイルパスが含まれていないこと
- プライベートリポジトリへの依存がないこと
- 汎用的に使えること（プロジェクト非依存）

---

## ライセンス

MIT License — 詳細は [LICENSE](LICENSE) を参照してください。
