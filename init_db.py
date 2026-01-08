import asyncio
import os
import sys

# Добавляем текущую директорию в пути поиска
sys.path.insert(0, os.path.abspath(os.curdir))

from app.db.session import engine
from app.db.base import Base

async def init_models():
    print("Подключаемся к базе...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Готово! Таблицы созданы.")

if __name__ == "__main__":
    asyncio.run(init_models())