from fastapi import FastAPI , HTTPException , Header , Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel , Field , EmailStr
import functions

app = FastAPI(title="Personal Notes Manager API", description="Manage personal notes securely")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class UserRegister(BaseModel):
    username: str = Field(min_length=1)
    email: EmailStr                      
    password: str = Field(min_length=1)  

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)

def authorize(token):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired access token")
    return payload


class NoteCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)

#A1
@app.post("/register")
def register(username=Body(), password=Body() , email=Body()):
    user = functions.register_user(username=username, email=email, password=password)
    if not user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User registered successfully", "user": user}

# A2
@app.post("/login")
def login(user: UserLogin):
    token = functions.verify_login(email=user.email, password=user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return token


# A3
@app.post("/refresh")
def refresh(refresh_token=Header(None)):
    payload = functions.verify_token(token=refresh_token, token_type="refresh")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired refresh token")

    access_token = functions.create_token(user_id=payload["user_id"],username=payload["username"],token_type="access")
    return {"access_token": access_token}

#E1
@app.get("/notes")
def get_notes(token=Header(None)):
    payload = authorize(token)
    return functions.get_notes(user_id=payload["user_id"])

# E2
@app.post("/notes")
def add_note(note: NoteCreate, token=Header(None)):
    payload = authorize(token)
    return functions.add_note(user_id=payload["user_id"],title=note.title,content=note.content)