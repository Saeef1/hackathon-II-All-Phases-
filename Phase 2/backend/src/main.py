from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
import os

from .database.session import engine
from .models.auth import User
from .models.todo import Todo


# Create database tables on startup
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (nothing to do)


app = FastAPI(title="Todo API", version="1.0.0", lifespan=lifespan)

# CORS middleware - in production, restrict origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include API routers
from .api.auth import router as auth_router
from .api.todos import router as todos_router

app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(todos_router, prefix="/api/v1/todos", tags=["todos"])

@app.get("/")
def read_root():
    return {"message": "Todo API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )