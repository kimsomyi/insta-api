from fastapi import APIRouter
from deps import SessionDep, PostDep, CurrentUserDep
from models import Post
from sqlalchemy import select
from schemas import PostOut, PostCreate, PostUpdate


# router = APIRouter(prefix='/api/posts')
router = APIRouter(prefix='/api/posts', tags=['posts'])

# @router.get('/posts')
# def post_list():
#     pass

# = 

@router.get('', response_model=list[PostOut])
def post_list(db: SessionDep):
    posts = db.scalars(select(Post).order_by(Post.created_at.desc())).all()

    # for post in posts:
    #     print(post.user.username)

    return posts

# @router.get('/{post_id}', response_model=PostOut)
# def post_detail(post_id: int, db: SessionDep):
#     post = db.get(Post, post_id)
#     return post # json 데이터를 사용자에게 전달

# =

@router.get('/{post_id}', response_model=PostOut)
def post_detail(post: PostDep):
    # post = db.get(Post, post_id)
    return post # json 데이터를 사용자에게 전달

# 게시물 생성 요청 메소드
@router.post('', response_model=PostOut, status_code=201)
def post_create(data: PostCreate, db: SessionDep, user: CurrentUserDep):
    post = Post(content=data.content, user_id=user.id)
    db.add(post)
    db.commit()
    return post


@router.patch('/{post_id}', response_model=PostOut)
def post_update(post: PostDep, data: PostUpdate, db: SessionDep):
    post.content = data.content
    db.commit()
    return post

@router.delete('/{post_id}',status_code=204)
def post_delete(post: PostDep, db: SessionDep):
    db.delete(post)
    db.commit()
    # return을 안 써 놔도 python은 return None으로 보냄