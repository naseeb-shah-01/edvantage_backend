from fastapi import APIRouter, Depends, HTTPException
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserResponse,UserResponseWithOutToken



app=APIRouter()

@app.get("/details/{user_id}", response_model= UserResponseWithOutToken,summary="Get user details by ID", description="Retrieve user details for a specific user ID.")
async def read_user(user_id: int, db=Depends(get_db)):
    try:
        user_repo = UserRepository(db)
        user = user_repo.findById(user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
