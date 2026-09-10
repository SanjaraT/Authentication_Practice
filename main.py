from fastapi import FastAPI, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from supabase import create_client
from pydantic import BaseModel
import os


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Auth API")

security = HTTPBearer()

def get_current_user(
        credentials : HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    response = supabase.auth.get_user(token)

    return response.user

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

@app.get("/protected")
def protected_route(user=Depends(get_current_user)):
    return {
        "message": "You are authenticated",
        "user": user
    }

print("Server running and connected to Supabase")