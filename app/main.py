import psycopg2
import time
from psycopg2.extras import RealDictCursor
from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel


'''
CRUD with postgreSQL generated table
'''

app = FastAPI()

class Post(BaseModel):
    ''' set the schema to validate post requests, 
        to ensure that frontend sends the exact data that backend expects 
    '''
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



# setting connection to database
while True:
    try:
        connection = psycopg2.connect(
            host='localhost', database='fastapi', user='postgres', password='postgrespass', cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("connected to database succesfully..")
        break
    except Exception as error:
        print("failed to connect to database..")
        print("Error", error)
        time.sleep(2)


@app.get("/")
async def root():
    return {"message": "Hello FASTAPI"}


@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts;""")
    posts = cursor.fetchall()
    return posts


@app.get("/posts/{id}")
async def get_post_detail(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id=%s;""", (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id={id} doesn't exists.. :(")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_post(post: Post):
    # making staged changes
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""",
                   (post.title, post.content, post.published))  # prevents...SQL atack (if a value is like SELECT, INSERT...)
    post = cursor.fetchone()

    # push staged changes to db, saving..
    connection.commit()
    return post


@app.put("/posts/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_post(id: int, post: Post):
    ''' put method: must specify all fields no matter what you are changing
        patch method: must specify only the field to change 
    '''
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s, rating=%s WHERE id=%s RETURNING *;""",
                   (post.title, post.content, post.published, post.rating, str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id={id} doesn't exists.. :(")
    connection.commit()
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id=%s RETURNING *;""", (str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id={id} doesn't exists.. :(")
    connection.commit()
    return {"message": f"post with id={id} was successfully deleted.. :("}
