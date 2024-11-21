from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .models import User
from .database import get_db
from .utils import hash_password, verify_password, create_access_token
from pydantic import BaseModel

router = APIRouter()

# Pydantic schemas
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Signup route
@router.post("/signup", tags=["Auth"])
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Create a new user
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": {"id": new_user.id, "username": new_user.username}}

# Signin route
@router.post("/signin", tags=["Auth"])
def signin(user: UserLogin, db: Session = Depends(get_db)):
    # Check if the user exists
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Generate JWT token
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
