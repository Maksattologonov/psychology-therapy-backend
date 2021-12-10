import uvicorn

from core.settings import settings


uvicorn.run(
    'app:app',
    host=settings.server_host,
    port=settings.server_port,
    reload=True,
)
