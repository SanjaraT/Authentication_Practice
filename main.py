from fastapi import FastAPI
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel
import os


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Auth API")
class AuthReq(BaseModel):
    email: str
    password : str

    
@app.post("/signup")
def signup(request: AuthReq):
    response = supabase.auth.sign_up({
        "email": request.email,
        "password": request.password
    })

    return response

@app.post("/login")
def login(request: AuthReq):
    response = supabase.auth.sign_in_with_password({
        "email": request.email,
        "password": request.password
    })

    return response

print("Server running and connected to Supabase")