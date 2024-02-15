from fastapi import FastAPI

from table import router as table_router

app = FastAPI()
app.include_router(table_router)


@app.get("/")
async def root():
    return {"message": "Hello World!"}
