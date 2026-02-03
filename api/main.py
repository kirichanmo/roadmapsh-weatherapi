import json
from fastapi import FastAPI, Query, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import redis.asyncio as redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
import httpx
import os
from dotenv import load_dotenv

load_dotenv() 
templates = Jinja2Templates(directory="templates")

app = FastAPI()

REDIS_URL = os.getenv("REDIS_URL")
REDIS_REST_URL = os.getenv("UPSTASH_REDIS_REST_URL")
REDIS_TOKEN = os.getenv("UPSTASH_REDIS_REST_TOKEN")
CACHE_TTL = 60 * 60  # 1時間

async def cache_get(key: str):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{REDIS_REST_URL}/get/{key}",
            headers={"Authorization": f"Bearer {REDIS_TOKEN}"}
        )
        data = res.json()
        if data.get("result"):
            return json.loads(data["result"])
    return None

async def cache_set(key: str, value: dict):
    async with httpx.AsyncClient() as client:
        await client.get(
            f"{REDIS_REST_URL}/set/{key}/{json.dumps(value)}/ex/{CACHE_TTL}",
            headers={"Authorization": f"Bearer {REDIS_TOKEN}"}
        )


@app.on_event("startup")
async def startup():
    # UpstashのRESTじゃなくて「Redis接続URL(redis://...)」を使う想定
    redis_url = os.getenv("REDIS_URL")
    r = redis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(r)

@app.get("/", response_class=HTMLResponse)
async def ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/weather", dependencies=[Depends(RateLimiter(times=30, seconds=60))])
async def get_weather(no_cache: int = Query(0)):
    cache_key = "weather:140010"
    
    # キャッシュ確認
    cached = await cache_get(cache_key)
    if cached:
        return {**cached, "from_cache": True}

    # APIから天気予報取得
    url = "https://weather.tsukumijima.net/api/forecast/city/140010"

    async with httpx.AsyncClient() as client:
        res = await client.get(url)
        data = res.json()
    
    todayWeather = data["forecasts"][0]["telop"]
    result = {"weather": todayWeather}
    
    # キャッシュ保存
    await cache_set(cache_key, result)
    
    return {**result, "from_cache": False}
