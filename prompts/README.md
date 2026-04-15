# Prompts

Claude Code 不要で使える単体プロンプトのコレクションです。  
各ファイルはプロンプト本文のみで構成されており、**全選択してそのままAIに貼り付けて使用**できます。

---

## 使い方

1. 目的のプロンプトファイルを開く
2. ファイルの内容を全選択（`Cmd+A` / `Ctrl+A`）してコピー
3. ChatGPT / Claude / Gemini などの会話に貼り付けて送信

---

## プロンプト一覧

### [generate-prompt-from-conversation.md](generate-prompt-from-conversation.md)

**用途**: 会話の作業内容から再現用プロンプトを自動生成する

特定の作業（要約・翻訳・コードレビューなど）を生成AIで行った後、この会話の末尾に貼り付けて実行すると、同じ作業を別の場面でも再現できる汎用プロンプトが生成されます。

**対応ユースケース**: 文章の要約・リライト、翻訳・言い換え、コードのレビュー・デバッグ・生成、データ分析、アイデア構造化、ドキュメント作成

---

### [code-dependency-analysis/](code-dependency-analysis/)

**用途**: 対話型生成AI + VS Codeローカルプレビューで C++/Java/C# コードベースの依存関係を段階的に抽出し、UML クラス図・パッケージ図（Mermaid）として累積生成する

API キー・GitHub・外部アカウント不要。Python 補助スクリプト `bundle.py` でソースを MANIFEST 形式に変換し、`prompt.md` と合わせて AI に貼り付けて運用します。詳細は [code-dependency-analysis/README.md](code-dependency-analysis/README.md) を参照。

**対応ユースケース**: 大規模コードベースのリバースエンジニアリング、オンボーディング資料作成、依存循環検知
