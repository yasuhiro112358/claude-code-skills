# 対話型生成AIによるコード依存関係分析ツール

大規模な C++ / Java / C# コードベースの依存関係を、対話型 AI（UI のみ）＋ VS Code ローカルプレビューで段階抽出するツール。API キー・GitHub・外部アカウント不要。詳細は [requirements.md](requirements.md) 参照。

## アーキテクチャ

2フェーズ・メタデータ中心構成を採用。コードの再読み込みを避けるため、Phase 1 で構造化メタデータ（JSON）を蓄積し、Phase 2 でメタデータから任意の図をオンデマンド生成する。metadata.json の管理は CRUD 操作に対応する 3 つのプロンプトで構成する。

```
Phase 1 Upsert (C+U): コードチャンク + metadata.json → AI → metadata.json（蓄積・更新）
Phase 1 Delete  (D) : 削除指示 + metadata.json     → AI → metadata.json（削除）
Phase 2 Read    (R) : 図の指示 + metadata.json      → AI → Mermaid .md ファイル
```

## ファイル構成

| ファイル | 役割 |
|---------|------|
| `requirements.md` | 要件確認書（SRS-lite） |
| `bundle.py` | ソースツリーを MANIFEST 形式に変換する Python スクリプト |
| `metadata.json` | **状態ストア**: コード解析メタデータ（Phase 1 の出力、Phase 2 の入力） |
| `prompt-phase1-upsert.md` | Phase 1 Upsert: メタデータの蓄積・更新（新規追加もソース変更も同一プロンプト） |
| `prompt-phase1-delete.md` | Phase 1 Delete: メタデータの削除 |
| `prompt-phase2.md` | Phase 2 Read: メタデータから図を生成（全 6 種のテンプレート埋め込み） |
| `prompt-legacy.md` | 旧プロンプト（単一フェーズ構成、後方互換用に保持） |

### 生成される成果物（Phase 2 出力）

| ファイル | 図の種類 | Tier |
|---------|---------|------|
| `class-diagram.md` | UML クラス図 | Tier 1 |
| `package-diagram.md` | UML パッケージ図 | Tier 1 |
| `sequence-diagram.md` | UML シーケンス図 | Tier 1 |
| `state-diagram.md` | UML 状態機械図 | Tier 2（条件付き） |
| `component-diagram.md` | UML コンポーネント図 | Tier 2（条件付き） |
| `er-diagram.md` | ER 図 | Tier 2（条件付き） |
| `cyclic-dependencies.md` | 循環依存レポート | 検出時のみ |

## 前提環境

- Python 3.8 以上（標準ライブラリのみ使用）
- VS Code + [Mermaid Chart 拡張](https://marketplace.visualstudio.com/items?itemName=MermaidChart.vscode-mermaid-chart)（`MermaidChart.vscode-mermaid-chart`、アカウント登録不要）
- 対話型 AI（Claude.ai / ChatGPT 等の UI）

## 運用フロー

### Phase 1 Upsert: メタデータ蓄積・更新（繰り返し）

```
1. bundle.py でソースを MANIFEST 形式に変換
2. prompt-phase1-upsert.md の本文 + metadata.json + バンドルを AI に貼る
3. 応答の metadata.json コードブロックをコピーして上書き保存
4. 次のチャンクで 1 に戻る
```

ソースが更新された場合も同じ手順。変更されたファイルを `bundle.py` で再変換して投入すれば、該当ファイルのメタデータがコードの現状で上書きされる。

### Phase 1 Delete: メタデータ削除（必要に応じて）

```
5. prompt-phase1-delete.md の本文 + metadata.json を AI に貼る
6. 削除対象のファイルパス・クラス名・パッケージ名を自然言語で指示
7. 応答の metadata.json コードブロックをコピーして上書き保存
```

### Phase 2 Read: 図の生成（オンデマンド）

```
8. prompt-phase2.md の本文 + metadata.json を AI に貼る
9. 生成したい図の種類・範囲・条件を自然言語で指示する
   例: 「Tier 1 全て」「auth パッケージのクラス図」「authenticate の呼び出しチェーンのシーケンス図」
10. 応答のコピー用コードブロックを各 .md ファイルに保存
11. VS Code でプレビュー確認
```

### Tier 2 図の追加生成（必要に応じて）

```
12. metadata.json の予約セクション（components / entities / states）に
    追加データを AI に投入して埋めてもらう（Upsert プロンプトで指示）
13. Phase 2 と同様に図を生成
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

- **大きすぎる弊害**: AI がクラスやエッジを取りこぼす／応答が途切れる
- **小さすぎる弊害**: 往復回数が増え、メタデータの更新ミスが起きやすい
- **推奨の決め方**:
  1. まずは `--max-chars` 指定なし（または十分大きい値）で小さなサブディレクトリを投入
  2. 応答品質が劣化または途切れる閾値を観測
  3. その **7〜8 割** を本番値に設定
- **初期の目安**: 30,000〜60,000 字（概ね 10〜30 ファイル相当）から試すと扱いやすい

### metadata.json のサイズ上限

```
Phase 1: JSON上限 = AIコンテキスト上限 − プロンプト定型文 − コードチャンクサイズ
Phase 2: JSON上限 = AIコンテキスト上限 − プロンプト定型文 − 図生成指示（短い）
```

JSON が上限を超えた場合はパッケージ単位で分割する（例: `metadata-auth.json`、`metadata-infra.json`）。Phase 2 では必要なパッケージの JSON のみを送信すればよい。

## 未確定事項（運用しながら調整）

- Python 実行環境の最終確認（職場 PC で 3.8+ が使えるか）
- `--max-chars` の適切な値（AI の 1 回あたり入力上限に合わせて調整）
- プロンプトの育成（粒度混在や差分返答が発生したら制約を追加して塞ぐ）
- `metadata.json` のスキーマ最終確定（運用で不足が見つかった場合に拡張）
