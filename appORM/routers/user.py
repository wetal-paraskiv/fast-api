from ..utils import hash_password
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from .. import models
from ..database import get_db
from ..schemas import UserCreate, UserOut


router = APIRouter(
    prefix="/users", 
    tags = ["Users"] # groupping specific requests in docs
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(user: UserCreate, db: session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(
        # title=post.title, content=post.content, published=post.published
        **user.dict()  # unpacking post model
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # kind of postgreSQL RETURNING *
    return new_user


@router.get("/{id}", response_model=UserOut)
async def get_user(id: int,  db: session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id={id} doesn't exists.. :("
        )
    return user