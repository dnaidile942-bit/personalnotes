from fastapi import FastAPI , HTTPException , Header , Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel , Field
import functions

app = FastAPI(title="Personal Notes Manager API", description="Manage personal notes securely")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"]
)


def authorize(token):
    payload = functions.verify_token(token=token, token_type="access")
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or Expired access token")
    return payload


class NoteCreate(BaseModel):
    title: str = Field(min_length=1)
    content: str = Field(min_length=1)


# A2
@app.post("/login")
def login(email=Body(), password=Body()):
    token = functions.verify_login(email=email, password=password)
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


# E2
@app.post("/notes")
def add_note(note: NoteCreate, token=Header(None)):
    payload = authorize(token)
    return functions.add_note(user_id=payload["user_id"],title=note.title,content=note.content)