from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from typing import List

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add CORSMiddleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Your Pydantic models and FastAPI endpoints follow here
class User(BaseModel):
    username: str = Field(..., min_length=6)
    password: str = Field(..., min_length=7)
    email: EmailStr
    phoneNumber: str = Field(..., min_length=11, max_length=11)

# Mock database
users_db: List[User] = []

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: User):
    # User registration logic follows
    if any(u for u in users_db if u.username == user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    if any(u for u in users_db if u.email == user.email):
        raise HTTPException(status_code=400, detail="Email already exists")
    if any(u for u in users_db if u.phoneNumber == user.phoneNumber):
        raise HTTPException(status_code=400, detail="Phone number already exists")

    # If validations pass, add user to 'database'
    users_db.append(user)
    for u in users_db:
        print(u.username, u.email, u.phoneNumber)
    return {"message": "User registered successfully"}

