from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, EmailStr
from .database import UserModel, get_db
from sqlalchemy.orm import Session
from .hashing import get_password_hash, verify_password
from .jwt_utils import create_access_token, decode_access_token

auth_router = APIRouter()

# Pydantic models
class User(BaseModel):
    email: EmailStr
    password: str
    is_admin: bool = False

class Token(BaseModel):
    access_token: str
    token_type: str
    
class Login(BaseModel):
    email: EmailStr
    password: str

@auth_router.post("/register")
def register(user: User, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = UserModel(
        email=user.email,
        password=get_password_hash(user.password),
        is_admin=user.is_admin,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User registered successfully"}

@auth_router.post("/login", response_model=Token)
def login(user: Login, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": user.email, "is_admin": existing_user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Extract and validate the user from the Bearer token in the Authorization header.
    """
    # Extract the token from the Authorization header
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header format")
    token = authorization.split(" ")[1]

    # Decode and validate the token
    payload = decode_access_token(token)
    email = payload.get("sub")
    if email is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # Fetch the user from the database
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return {"email": email, "is_admin": payload.get("is_admin", False)}