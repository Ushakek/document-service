import fastapi

from app.urls import router


app = fastapi.FastAPI()

app.include_router(router, prefix='', tags=['Название для группы'])
