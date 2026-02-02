from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.core.security import hash_password, verify_password, create_access_token
from app.db.session import get_db  # Import from our new file
from app.models.user import User
from app.models.address import Address  # Clean import

router = APIRouter()

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user with optional addresses"""

    # 🔹 Check if user already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 🔹 Create user
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=hash_password(user_data.password),
        contact=user_data.contact,
        whatsapp=user_data.whatsapp,
        collage=user_data.collage,
        expertise=user_data.expertise,
        role=user_data.role
    )

    db.add(new_user)
    db.flush()  # ✅ get user.id without commit

    # 🔹 Create addresses (if provided)
    access_token = create_access_token(
        data={
            "sub": str(new_user.id),
            "role": user_data.role   # admin / instructor / student
        }
    )
    print("Access Token:", access_token)
    if user_data.addresses:
        primary_found = False

        for addr in user_data.addresses:
            if addr.is_primary:
                if primary_found:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Only one primary address is allowed"
                    )
                primary_found = True

            address = Address(
                user_id=new_user.id,
                address_line_1=addr.address_line_1,
                address_line_2=addr.address_line_2,
                city=addr.city,
                state=addr.state,
                country=addr.country,
                postal_code=addr.postal_code,
                address_type=addr.address_type,
                is_primary=addr.is_primary
            )
            print( address)
            db.add(address)

    db.commit()
    db.refresh(new_user)


    return {"access_token":access_token, **new_user.__dict__}

@router.post("/login")
async def login_user(
    login_data:UserLogin ,
    db: Session = Depends(get_db)
):
    """Authenticate user and return token"""
    email = login_data.email
    password = login_data.password
    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 🔐 CREATE TOKEN
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role   # admin / instructor / student
        }
    )

    return {
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.full_name,
            "role": user.role
        }
    }