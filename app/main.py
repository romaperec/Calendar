from fastapi import FastAPI

from routes.calendar import router
from database import init_db

app = FastAPI()
app.include_router(router)

@app.post("/init_db", tags=["Database"])
async def create_db():
    await init_db()
    return {"message": "success"}