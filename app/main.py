from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import v1_router
from app.db.session import create_tables
from app.middleware.authentication import TokenMiddleware
from app.services.cloudinary_config import cloudinary

app = FastAPI(title="My FastAPI Application", version="1.0.0")

# ✅ 1. ADD CORS FIRST (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 2. THEN add your custom middleware
app.add_middleware(TokenMiddleware)

# Create DB tables
create_tables()
print("Database tables created.")


@app.on_event("startup")
async def startup_event():
    print("Cloudinary configured successfully!")
    print(f"Cloud Name: {cloudinary.config().cloud_name}")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# ✅ 3. Include routers AFTER middleware
app.include_router(v1_router, prefix="/api/v1")
