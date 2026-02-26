from fastapi import FastAPI
from app.api.routes import document

app = FastAPI(title="Doc Automation API")

app.include_router(document.router)