from fastapi import FastAPI, APIRouter
from src.database import Base, engine
from src.routes import auth,leaves
from src import models
## To Check and learn about Get fetch command
app=FastAPI()

@app.on_event("startup")  # Connecting db before import
def on_startup():
  models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router,prefix="/auth")
app.include_router(leaves.router, prefix="/leaves")

