from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from redis import Redis
from app.db.session import get_db
from app.core.config import settings

router = APIRouter()

@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    db_status = "connected"
    redis_status = "connected"
    try:
        await db.execute(text("SELECT 1"))
    except Exception:
        db_status = "error"
    try:
        r = Redis.from_url(settings.REDIS_URL)
        r.ping()
    except Exception:
        redis_status = "error"
    return {"status": "ok", "database": db_status, "redis": redis_status}