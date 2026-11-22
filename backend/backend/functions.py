from sqlalchemy import Integer, String, Column, create_engine, ForeignKey
from sqlalchemy.orm import Session, declarative_base
from datetime import datetime,timedelta , timezone
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher()


DB_PATH = "notes.db"
engine = create_engine(f"sqlite:///{DB_PATH}")
Base = declarative_base()


ACCESS_TOKEN_EXPIRY = 15
REFRESH_TOKEN_EXPIRY = 7*24*60
SECRET_KEY ="SECRETCODE"
ALGORITHM = "HS256"


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    created_at = Column(String)


class Notes(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    title = Column(String)
    content = Column(String)
    created_at = Column(String)


Base.metadata.create_all(engine)


# E2
def add_note(user_id, title, content):
    session = Session(engine)
    new_note = Notes(user_id=user_id, title=title, content=content, created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    session.add(new_note)
    session.commit()
    response = {
        "id": new_note.id,
        "user_id": new_note.user_id,
        "title": new_note.title,
        "content": new_note.content,
        "created_at": new_note.created_at
    }
    session.close()
    return response




# A2
def verify_login(email,password):
    session = Session(engine)
    user = session.query(User).filter_by(email=email).first()
    if user is None:
        session.close()
        return False
    try :
        ph.verify(user.hashed_password,password)

    except VerifyMismatchError:
        session.close()
        return False

    access_token = create_token(user_id=user.user_id,username=user.username,token_type="access")
    refresh_token = create_token(user_id=user.user_id,username=user.username,token_type="refresh")

    session.close()
    return {"access_token":access_token,"refresh_token":refresh_token}


# A2 and A3
def create_token(user_id,username,token_type):
    time = ACCESS_TOKEN_EXPIRY
    if token_type == "refresh":
        time = REFRESH_TOKEN_EXPIRY
    payload={
        "user_id":user_id,
        "username":username,
        "token_type":token_type,
        "exp":datetime.now(timezone.utc)+timedelta(minutes=time)
    }
    token =jwt.encode(payload=payload,key=SECRET_KEY,algorithm=ALGORITHM)
    return token


# A3
def verify_token(token,token_type):
    try:
        payload = jwt.decode(jwt=token,key=SECRET_KEY,algorithms=[ALGORITHM])
    except:
        return False

    if payload ["token_type"] == token_type:
        return payload
    return False


