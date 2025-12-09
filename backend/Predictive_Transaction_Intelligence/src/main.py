from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import router

# Create the FastAPI application
app = FastAPI(
    title="Predictive Transaction Intelligence API",
    version="1.0.0",
    description="Backend API for fraud detection project"
)

# CORS configuration (allows frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allow all frontends during development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routes (from your endpoints.py)
app.include_router(router, prefix="/api")

# Example root endpoint (optional)
@app.get("/")
def root():
    return {"message": "Backend API is running!"}



#uvicorn src.main:app --reload