import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
import app.routes as r
from app.utils.lifespan import lifespan

# Initialize database
Base.metadata.create_all(engine)

# Create FastAPI application with configuration
app = FastAPI(lifespan=lifespan)

# CConfigure CORS and other middleware
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(r.auth_router)
app.include_router(r.user_router)
app.include_router(r.route_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)