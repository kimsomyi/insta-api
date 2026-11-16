from fastapi import Depends, HTTPException
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from typing import Annotated
from database import engine
from models import Post



password_hash = PasswordHash.recommended()

def get_db():
  with Session(engine) as db:
    yield db

SessionDep = Annotated[Session, Depends(get_db)]


def get_post_or_404(post_id: int, db: SessionDep):
  post = db.get(Post, post_id)
  if post is None:
    raise HTTPException(status_code=404, detail='해당 게시물이 없습니다.')
  return post

PostDep = Annotated[Post, Depends(get_post_or_404)]