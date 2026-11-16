from fastapi import APIRouter, HTTPException, Depends
from schemas import UserCreate, UserOut, Token
from deps import SessionDep, password_hash, create_access_token, CurrentUserDep
from models import User
from sqlalchemy import select
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

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



@router.post('/login', response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends(OAuth2PasswordRequestForm)], db: SessionDep):
    # 사용자 찾기
    user = db.scalar(select(User).where(User.username == form.username))

    # 유저가 없거나 비밀번호가 일치하지 않는다면
    if user is None or not password_hash.verify(form.password, user.password_hash):
        raise HTTPException(status_code=401, detail='아이디 또는 비밀번호가 틀렸습니다.')

    # 신분증 발행
    token = create_access_token(user.id)
    # database에 기록하지 않음 싸인 된 신분증을 사용자에게 넘겨 주기만 함g

    # acess token 리턴
    return {'access_token': 'token', 'token_type': 'bearer'}

@router.get('/me', response_model=UserOut)
def me(user: CurrentUserDep):
    return user