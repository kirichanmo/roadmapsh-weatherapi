# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

神奈川県（都市コード140010）の天気予報を取得・表示するFastAPI製のWebアプリケーション。Upstash Redisを使用したキャッシュ機能とレートリミッター（30リクエスト/分）を実装。

## 開発コマンド

```bash
# 依存関係のインストール（uvを使用）
uv sync

# 開発サーバー起動
uv run uvicorn api.main:app --reload

# または直接
uvicorn api.main:app --reload
```

## 環境変数

`.env`ファイルに以下を設定：
- `REDIS_URL` - Redis接続URL（FastAPILimiter用、redis://...形式）
- `UPSTASH_REDIS_REST_URL` - Upstash REST API URL（キャッシュ用）
- `UPSTASH_REDIS_REST_TOKEN` - Upstash認証トークン

## アーキテクチャ

- `api/main.py` - FastAPIアプリケーション本体。エンドポイント、キャッシュ処理、レートリミッター設定を含む
- `templates/index.html` - Jinja2テンプレート。天気表示UI

### APIエンドポイント
- `GET /` - 天気表示UI（HTML）
- `GET /api/weather` - 天気データJSON。`no_cache=1`でキャッシュバイパス

### キャッシュ戦略
Upstash Redis REST APIを使用。TTLは1時間。レスポンスに`from_cache`フラグで取得元を表示。
