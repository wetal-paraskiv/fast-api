from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import session
from .. import models
from .. import oauth2
from ..database import get_db
from ..schemas import Vote


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]  # groupping requests in docs
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: Vote, db: session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="such post does not exists :( :)")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You can not vote twice! or Thrice :)")
        new_vote = models.Vote(
            user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "succesfully added vote!"}
        
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="Vote does not exists :( :)")
        vote_query.delete()
        db.commit()
        return {"message": "unvoted succesfully... urra.."}
