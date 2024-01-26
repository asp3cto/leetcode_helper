"""Main project file"""

from fastapi import FastAPI

from api_v1.users.views import router as apiv1_users_router

app = FastAPI()
app.include_router(apiv1_users_router)


@app.get("/")
async def root():
    """temp test"""
    return {"message": "Hello World!"}
