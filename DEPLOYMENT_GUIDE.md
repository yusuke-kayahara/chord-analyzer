# Phase 4: デプロイメントガイド

## 概要
フロントエンド（React）を Vercel、バックエンド（FastAPI）を Railway にデプロイする手順を説明します。

## 🚀 デプロイメント構成

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │───▶│   Backend       │
│   (Vercel)      │    │   (Railway)     │
│                 │    │                 │
│ - React App     │    │ - FastAPI       │
│ - Static Host   │    │ - Python Runtime│
│ - CDN配信       │    │ - Auto Deploy   │
└─────────────────┘    └─────────────────┘
   your-app.vercel.app   your-api.railway.app
```

## 📋 事前準備（ユーザー対応必要）

### 1. アカウント作成
以下のサービスでアカウントを作成してください：

#### Vercel（フロントエンド用）
- **URL**: https://vercel.com
- **推奨**: GitHubアカウントでサインアップ
- **料金**: 個人利用は無料

#### Railway（バックエンド用）  
- **URL**: https://railway.app
- **推奨**: GitHubアカウントでサインアップ
- **料金**: 月$5のスタータープラン（無料枠もあり）

### 2. GitHub連携
両サービスでGitHubリポジトリとの連携を許可してください。

## 🔧 バックエンド（Railway）デプロイ手順

### Step 1: Railway プロジェクト作成
1. Railway にログイン
2. 「New Project」をクリック
3. 「Deploy from GitHub repo」を選択
4. `chord-analyzer` リポジトリを選択

### Step 2: 設定ファイル追加
私がバックエンド用の設定ファイルを作成します：
- `railway.toml` - Railway設定
- `Dockerfile` - Pythonコンテナ設定
- `requirements.txt` - 依存関係（既存）

### Step 3: 環境変数設定（ユーザー対応）
Railway ダッシュボードで以下を設定：
```
PYTHON_VERSION=3.12
PORT=8000
```

### Step 4: デプロイ実行
- GitHubプッシュで自動デプロイされます
- Railway URLが発行されます（例: `your-api.railway.app`）

## 🌐 フロントエンド（Vercel）デプロイ手順

### Step 1: Vercel プロジェクト作成
1. Vercel にログイン
2. 「New Project」をクリック
3. GitHubから `chord-analyzer` を選択
4. **Root Directory**: `frontend` を指定
5. **Framework**: React が自動検出される

### Step 2: 環境変数設定（ユーザー対応）
Vercel ダッシュボードで以下を設定：
```
REACT_APP_API_URL=https://your-api.railway.app
```
※ Railway URLを取得後に設定

### Step 3: ビルド設定
私がフロントエンド用の設定ファイルを作成します：
- `vercel.json` - Vercel設定
- `.env.production` - 本番環境変数

### Step 4: デプロイ実行
- GitHubプッシュで自動デプロイされます
- Vercel URLが発行されます（例: `chord-analyzer.vercel.app`）

## ⚙️ 設定ファイル詳細

### Railway設定（`railway.toml`）
```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/"
healthcheckTimeout = 100
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10

[env]
PYTHON_VERSION = "3.12"
```

### Vercel設定（`vercel.json`）
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": "build",
  "framework": "create-react-app",
  "rewrites": [
    {
      "source": "/(.*)",
      "destination": "/index.html"
    }
  ]
}
```

## 🔗 CORS設定

### バックエンド修正
本番環境用のCORS設定を追加します：
```python
# main.py
origins = [
    "http://localhost:3000",  # 開発環境
    "https://your-app.vercel.app",  # 本番環境
]
```

## 📝 デプロイ手順（実行順序）

### 1. 私が行う作業
- [ ] Railway用Dockerfileと設定ファイル作成
- [ ] Vercel用設定ファイル作成  
- [ ] CORS設定修正
- [ ] 本番環境用の設定追加
- [ ] GitHubにプッシュ

### 2. ユーザーが行う作業
- [ ] Vercel・Railwayアカウント作成
- [ ] Railway プロジェクト作成・GitHub連携
- [ ] Railway 環境変数設定
- [ ] Railway URL取得
- [ ] Vercel プロジェクト作成・GitHub連携
- [ ] Vercel 環境変数設定（Railway URL使用）
- [ ] 本番環境での動作確認

## 🧪 デプロイ後の確認項目

### バックエンドAPI確認
- Railway URLで `/` エンドポイントアクセス
- Swagger UI（`/docs`）動作確認
- `/analyze` エンドポイントのテスト

### フロントエンド確認
- Vercel URLでアプリ表示確認
- API接続状態（緑色インジケーター）
- コード進行分析の動作テスト

### 統合テスト
- `[C][Am][Fm][G]` で借用和音検出
- エラーハンドリング動作
- レスポンス時間確認

## 🛠️ トラブルシューティング

### よくある問題

#### Railway デプロイエラー
```bash
# ログ確認方法
railway logs
```
- **Python依存関係エラー**: requirements.txt 確認
- **ポート設定エラー**: PORT環境変数確認

#### Vercel ビルドエラー
- **API接続エラー**: REACT_APP_API_URL確認
- **Tailwind CSSエラー**: postcss.config.js確認

#### CORS エラー
- Railway URLをmain.pyのoriginsに追加
- ブラウザのネットワークタブでエラー詳細確認

## 💰 料金について

### Vercel（フロントエンド）
- **Hobby**: 無料
- **帯域制限**: 100GB/月
- **独自ドメイン**: 対応

### Railway（バックエンド）
- **Developer**: $5/月
- **リソース**: 512MB RAM, 1GB Storage
- **無料枠**: $5相当（最初の月）

## 🔄 継続的デプロイメント

GitHubにプッシュすると自動デプロイされます：
```bash
# デプロイフロー
git add .
git commit -m "Update: 新機能追加"
git push origin main
# ↓ 自動実行
# Railway: バックエンド再デプロイ
# Vercel: フロントエンド再デプロイ
```

## 📚 参考リンク

- [Railway Docs](https://docs.railway.app)
- [Vercel Docs](https://vercel.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://create-react-app.dev/docs/deployment/)

---

## 🚦 次のステップ

1. **アカウント作成**後にお知らせください
2. **設定ファイル作成**を開始します
3. **段階的デプロイ**で確実に公開します

準備ができましたらお知らせください！ 🚀