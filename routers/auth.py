from fastapi import APIRouter, HTTPException
from schemas import UserCreate, UserOut
from deps import SessionDep, password_hash
from models import User
from sqlalchemy import select

router = APIRouter(prefix='/api/auth', tags=['auth'])

@router.post('/signup', response_model=UserOut)
def signup(data: UserCreate, db: SessionDep):
    user = db.scalar(select(User).where(User.username == data.username))

    if user:
        raise HTTPException(status_code=409, detail='사용 중인 아이디입니다.')

    hashed_pw = password_hash.hash(data.password)
    User(username = data.username, password_hash = hashed_pw)
    db.add(user)
    db.commit()

    return user