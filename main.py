import os
from fastapi import FastAPI, HTTPException
from supabase import create_client, Client
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()

# 1. Подключение к Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

# Модель данных для добавления лайка
class LikeAction(BaseModel):
    user_id: int
    beat_id: int

# Эндпоинт для добавления лайка
@app.post("/api/likes")
async def add_like(like: LikeAction):
    try:
        data = {"user_id": like.user_id, "beat_id": like.beat_id}
        result = supabase.table("likes").insert(data).execute()
        return {"status": "success", "data": result.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Эндпоинт для получения лайков пользователя
@app.get("/api/users/{user_id}/likes")
async def get_user_likes(user_id: int):
    result = supabase.table("likes").select("beat_id").eq("user_id", user_id).execute()
    return {"likes": [item["beat_id"] for item in result.data]}

# Эндпоинт для получения всех битов
@app.get("/api/beats")
async def get_beats():
    result = supabase.table("beats").select("*").execute()
    return {"beats": result.data}
