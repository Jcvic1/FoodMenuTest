from app import models, menus
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(menus.router, tags=['Menu'], prefix='/api/v1')





