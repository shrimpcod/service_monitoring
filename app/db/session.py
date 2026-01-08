from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Базовый класс для моделей
Base = declarative_base()

# 2. Создаем асинхронный движок (Engine)
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 3. Настраиваем фабрику сессий (sessionmaker)
# Это "завод", который по нашему запросу будет создавать новые сессии связи с БД
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# 4. Функция-зависимость (Dependency Injection) для FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session