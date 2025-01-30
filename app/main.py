from fastapi import FastAPI
from fastapi.responses import FileResponse

from routes.calendar import router
from database import init_db

app = FastAPI(title="FixWeek", version="beta")
app.include_router(router)


@app.get('/', include_in_schema=False)
async def index():
    return FileResponse("templates/index.html")


@app.post("/init_db", tags=["database ⚙️"])
async def create_db():
    await init_db()
    return {"message": "successfully"}