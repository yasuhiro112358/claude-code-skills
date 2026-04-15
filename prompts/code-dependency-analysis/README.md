# 対話型生成AIによるコード依存関係分析ツール

大規模な C++ / Java / C# コードベースの依存関係を、対話型 AI（UI のみ）＋ VS Code ローカルプレビューで段階抽出するツール。API キー・GitHub・外部アカウント不要。詳細は [requirements.md](requirements.md) 参照。

## ファイル構成

| ファイル | 役割 |
|---------|------|
| `requirements.md` | 要件確認書（SRS-lite） |
| `bundle.py` | ソースツリーを MANIFEST 形式に変換する Python スクリプト |
| `prompt.md` | AI に貼り付ける定型プロンプト |
| `class-diagram.md` | **成果物**: UML クラス図（Mermaid `classDiagram`）— AI が累積更新 |
| `package-diagram.md` | **成果物**: UML パッケージ図（Mermaid `graph LR` + `subgraph`）— AI が累積更新 |
| `cyclic-dependencies.md` | **成果物**: 循環依存レポート（検出時のみ AI が生成） |

## 前提環境

- Python 3.8 以上（標準ライブラリのみ使用）
- VS Code + [Mermaid Chart 拡張](https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart) （`MermaidChart.vscode-mermaid-chart`、アカウント登録不要）
- 対話型 AI（Claude.ai / ChatGPT 等の UI）

## 運用フロー

```
【繰り返し】
  1. bundle.py でソースを MANIFEST 形式に変換
  2. prompt.md の本文 + class-diagram.md 全文 + package-diagram.md 全文 + バンドルを AI に貼る
  3. 応答のコピー用コードブロックを各 .md ファイルに上書き保存
  4. VS Code でプレビュー確認
  5. 次のチャンクで 1 に戻る
【完了】
  6. class-diagram.md / package-diagram.md / cyclic-dependencies.md を開発資料として利用
```

## bundle.py の使い方

```bash
# 最小
python bundle.py --root /path/to/src

# 出力先とチャンク分割（値は例。下記「チャンクサイズの決め方」参照）
python bundle.py --root /path/to/src --out bundle.txt --max-chars 60000

# include/exclude
python bundle.py --root /path/to/src \
  --include 'src/auth/*' --include 'src/core/*' \
  --exclude '*/test/*' --exclude '*/generated/*'

# 拡張子を限定
python bundle.py --root /path/to/src --ext .cpp --ext .h
```

### 主なオプション

| オプション | 説明 |
|-----------|------|
| `--root` | 解析対象ルートディレクトリ（必須） |
| `--out` | 出力ファイル（既定: `bundle.txt`） |
| `--include` | 含めるグロブパターン（相対パス、複数可） |
| `--exclude` | 除外グロブパターン（相対パス、複数可） |
| `--max-chars` | 1 チャンクの上限文字数。超えたら `bundle-001.txt, bundle-002.txt, ...` に分割 |
| `--ext` | 対象拡張子を上書き（既定は C++/Java/C# 一式） |

### チャンクサイズの決め方

`--max-chars` に絶対的な正解値はない。以下を目安に運用しながら調整する。

- **大きすぎる弊害**: AI がクラスやエッジを取りこぼす／応答が途切れる／粒度が混在する
- **小さすぎる弊害**: 往復回数が増え、累積更新時の図のドリフトが起きやすい
- **推奨の決め方**:
  1. まずは `--max-chars` 指定なし（または十分大きい値）で小さなサブディレクトリを投入
  2. 応答品質が劣化または途切れる閾値を観測
  3. その **7〜8 割** を本番値に設定
- **初期の目安**: 30,000〜60,000 字（概ね 10〜30 ファイル相当）から試すと扱いやすい
- AI 側の 1 メッセージ入力上限は UI により異なる。制限を超えるとそもそも貼れないため、事実上の上限として作用する

### 出力フォーマット

```
=== MANIFEST ===
File: src/auth/AuthManager.cpp
Classes: AuthManager, AuthToken
File: src/auth/IAuthProvider.h
Classes: IAuthProvider

=== FILE: src/auth/AuthManager.cpp ===
(ファイル全文)

=== FILE: src/auth/IAuthProvider.h ===
(ファイル全文)
```

## AI への投入手順

1. `prompt.md` の `---` に囲まれた本文をコピーして AI に貼る
2. 続けて `class-diagram.md` の全文 → `package-diagram.md` の全文 → `bundle.txt`（または `bundle-001.txt`）をこの順で貼る
3. AI はファイルごとの「コピー用コードブロック」を返す
4. 各ブロック右上のコピーアイコン → 対応する `.md` を上書き保存

## 未確定事項（運用しながら調整）

- Python 実行環境の最終確認（職場 PC で 3.8+ が使えるか）
- `--max-chars` の適切な値（AI の 1 回あたり入力上限に合わせて調整）
- `prompt.md` の定型文の育成（粒度混在や差分返答が発生したら章を追加して塞ぐ）
