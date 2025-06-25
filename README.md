# Chord Analyzer - コード進行分析ツール

音楽理論に基づき、コード進行からキー（調性）を推定し、借用和音（ボロウド・コード）を検出・分析するためのWebアプリケーションです。

[アプリケーションを試す](https://chord-analyzer.up.railway.app/)  <!-- TODO: 正しいデプロイ先のURLに更新 -->

![アプリケーションのスクリーンショット](https://example.com/screenshot.png) <!-- TODO: スクリーンショット画像へのリンクを挿入 -->

## 主な機能

- **高精度なキー推定:**
  - Krumhansl & Kesslerの調性プロファイル、借用和音の最小化、トライアド構成比率など、複数のアルゴリズムを組み合わせたハイブリッド分析により、複雑なコード進行からも最適なキーを推定します。
- **詳細な借用和音分析:**
  - 非ダイアトニックコードを自動検出し、その借用元として考えられるキーを音楽理論的な関係性（同主調、平行調、属調など）に基づいて複数提示します。
  - テンションノート (`Cmaj7(9, #11)`など) を含む複雑なコードにも対応しています。
- **インタラクティブなUI:**
  - 分析結果を分かりやすく表示し、コード進行と借用関係を視覚的に確認できます。
  - 分析アルゴリズムの重み付けを調整できる詳細設定機能。
  - 分析履歴の保存・再生や、URLによる分析結果の共有が可能です。

## 技術スタック

- **バックエンド:**
  - **フレームワーク:** [FastAPI](https://fastapi.tiangolo.com/) (Python 3.12)
  - **主要ライブラリ:**
    - `pychord`: コード解析
    - `numpy`, `scikit-learn`: ピッチクラスベクトルの計算と類似度分析
- **フロントエンド:**
  - **フレームワーク:** [React](https://reactjs.org/) (TypeScript)
  - **UI:** [Tailwind CSS](https://tailwindcss.com/)
  - **API通信:** [Axios](https://axios-http.com/)
- **デプロイ:**
  - [Docker](https://www.docker.com/)
  - [Railway](https://railway.app/)

## セットアップと実行方法

### 1. 前提条件

- [Node.js](https://nodejs.org/) (v16以上)
- [Python](https://www.python.org/) (v3.12)
- [pip](https://pip.pypa.io/en/stable/)

### 2. リポジトリのクローン

```bash
git clone https://github.com/yusuke-kayahara/chord-analyzer.git
cd chord-analyzer
```

### 3. バックエンドのセットアップと起動

```bash
# 依存関係のインストール
pip install -r requirements.txt

# サーバーの起動
uvicorn main:app --reload
```

APIサーバーが `http://127.0.0.1:8000` で起動します。

### 4. フロントエンドのセットアップと起動

```bash
# フロントエンドディレクトリに移動
cd frontend

# 依存関係のインストール
npm install

# 開発サーバーの起動
npm start
```

アプリケーションが `http://localhost:3000` で開きます。

## APIエンドポイント

- `POST /analyze`: コード進行の文字列を受け取り、分析結果（推定キー、借用和音など）をJSON形式で返します。
- `GET /keys`: 分析に使用可能なキーのリストを返します。

詳細なリクエスト/レスポンスの仕様については、`http://127.0.0.1:8000/docs` のSwagger UIで確認できます。

## 今後の展望

- セカンダリドミナントの明示的な表示
- モーダルインターチェンジ以外の借用和音（例: ネアポリの和音）への対応
- 分析結果のMIDIファイルでのエクスポート機能

## 貢献

バグ報告や機能提案は、GitHubのIssuesまでお気軽にどうぞ。プルリクエストも歓迎します。

