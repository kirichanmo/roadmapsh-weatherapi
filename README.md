# WeatherAPI

神奈川県（都市コード: 140010）の天気予報を取得・表示するFastAPI製Webアプリケーション。

## ProjectURL
本コードは、roadmap.shの青果物です。
https://roadmap.sh/projects/weather-api-wrapper-service

## AppURL
https://roadmapsh-weatherapi.onrender.com/

## 機能

- 天気予報API（[天気予報 API（livedoor 天気互換）](https://weather.tsukumijima.net/)）から神奈川の天気を取得
- Upstash Redisによるキャッシュ（TTL: 1時間）
- レートリミッター（30リクエスト/分）
- シンプルな天気表示UI

## 必要要件

- Python 3.13以上
- [uv](https://docs.astral.sh/uv/)（推奨）またはpip
- Upstash Redisアカウント

## セットアップ

### 1. 依存関係のインストール

```bash
uv sync
```

### 2. 環境変数の設定

`.env`ファイルを作成し、以下を設定:

```env
REDIS_URL=redis://default:xxxxx@xxx.upstash.io:6379
UPSTASH_REDIS_REST_URL=https://xxx.upstash.io
UPSTASH_REDIS_REST_TOKEN=your_token_here
```

| 変数名 | 説明 |
|--------|------|
| `REDIS_URL` | Redis接続URL（FastAPILimiter用、`redis://...`形式） |
| `UPSTASH_REDIS_REST_URL` | Upstash REST API URL（キャッシュ用） |
| `UPSTASH_REDIS_REST_TOKEN` | Upstash認証トークン |

### 3. サーバー起動

```bash
uv run uvicorn api.main:app --reload
```

http://localhost:8000 でアクセス可能。

## APIエンドポイント

| メソッド | パス | 説明 |
|----------|------|------|
| GET | `/` | 天気表示UI（HTML） |
| GET | `/api/weather` | 天気データJSON |
| GET | `/api/weather?no_cache=1` | キャッシュをバイパスして取得 |

### レスポンス例

```json
{
  "weather": "晴れ",
  "from_cache": true
}
```

## プロジェクト構成

```
.
├── api/
│   └── main.py          # FastAPIアプリケーション
├── templates/
│   └── index.html       # 天気表示UI
├── pyproject.toml       # 依存関係定義
└── .env                 # 環境変数（gitignore対象）
```
