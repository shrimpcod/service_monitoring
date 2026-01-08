# Импортируем саму основу (Base)
from app.db.session import Base

# Импортируем ВСЕ модели.
# Это заставляет Python прочитать эти файлы, и модели "регистрируются" в Base.
from app.models.service import Service
from app.models.state import ServiceState

# Теперь, когда кто-то импортирует Base из ЭТОГО файла,
# он получит Base, который уже "знает" о существовании Service и ServiceState.