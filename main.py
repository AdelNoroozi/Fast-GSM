from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import database
from resources import api_router

app = FastAPI()
origins = [
    "http://localhost:3000",
]

app.include_router(api_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()
