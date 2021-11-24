from fastapi import FastAPI
from appORM import models
from appORM.database import engine
from appORM.routers import post, user, auth, vote

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    # "https://google.com/",
    # "https://youtube.com/",
    # "http://localhost",
    # "http://localhost:8000",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "hello wetalik"}

# models.Base.metadata.create_all(bind=engine)
