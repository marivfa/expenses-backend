from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from src.routers import users, category, remainders, expenses, dashboard

from src.config import models
from src.config.database import engine
models.Base.metadata.create_all(bind=engine)

from src.auth.JWTBearer import JWTBearer
from src.auth.auth import jwks

app = FastAPI(title="Expenses API")

auth = JWTBearer(jwks)

PROTECTED = [Depends(auth)]

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users", dependencies=PROTECTED)
app.include_router(category.router, prefix="/category", dependencies=PROTECTED)
app.include_router(remainders.router, prefix="/remainders", dependencies=PROTECTED)
app.include_router(expenses.router, prefix="/expenses",  dependencies=PROTECTED)
app.include_router(dashboard.router, prefix="/dashboard", dependencies=PROTECTED)
