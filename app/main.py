from fastapi import FastAPI
from app import models, database
from app.routers import books

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Book Review Service")

app.include_router(books.router)
