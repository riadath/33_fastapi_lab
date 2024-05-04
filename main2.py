from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, EmailStr
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import re

# Database Connection
client = MongoClient("mongodb+srv://pauruti100:Y7RednfpR6dTOooJ@cluster0.cmnj1io.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['user_registration']
collection = db['users']

# Ensure unique fields
collection.create_index("username", unique=True)
collection.create_index("email", unique=True)
collection.create_index("phone_number", unique=True)

app = FastAPI()

# CORS policy
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class User(BaseModel):
    username: str = Field(..., min_length=6)
    password: str = Field(..., min_length=7)
    confirm_password: str
    email: EmailStr
    phone_number: str = Field(..., min_length=11, max_length=11)

# Registration Endpoint
@app.post("/register")
async def register_user(user: User = Body(...)):
    print(User)
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match.")
    
    if not re.fullmatch(r'\d{11}', user.phone_number):
        raise HTTPException(status_code=400, detail="Phone number must have exactly 11 digits.")
    
    try:
        user_dict = user.dict()
        del user_dict['confirm_password']  # Remove confirm_password before saving
        collection.insert_one(user_dict)
        return {"message": "User registered successfully."}
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Username, email, or phone number already exists.")

