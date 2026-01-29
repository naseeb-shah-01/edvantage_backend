from fastapi import FastAPI
from app.api.v1.api import v1_router  # Import from api.py
from app.db.session import create_tables
from app.middleware.authentication import TokenMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="My FastAPI Application", version="1.0.0")

create_tables()
print("Database tables created.")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
# Add middleware
app.add_middleware(TokenMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the v1 router from api.py
app.include_router(v1_router, prefix="/api/v1")
