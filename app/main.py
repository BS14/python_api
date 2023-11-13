from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db

#Migration

models.Base.metadata.create_all(bind=engine)


app = FastAPI()



# while True:
#     try:
#         conn = psycopg2.connect(
#             host='localhost', 
#             database='python_api', 
#             user='python_api', 
#             password='password',
#             cursor_factory=RealDictCursor)
        
#         cursor = conn.cursor()
#         print("Database Connection successful!!!")
#         break
#     except Exception as e:
#         print(f"Database connection failed. \n Error: \n {e}")
#         time.sleep(5)


# This is used for validation of the body that is being send by the user. 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # True is the default value.
    rating: Optional[int] = None # This is the optional field. If user doesn't provide a value it will be None. 

@app.get("/") #@DECORATOR.METHOD-ALLOWED("PATH")
async def root():  # Path operation Function
    return {"message": "FAST API Learning."}

@app.get("/sql")
def test_posts(db: Session = Depends(get_db)):
    return{"Status": "Sucess"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return{"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # Converting pydantic model post to a dict and appending into to a my_posts array. 
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return{
        "data": new_post
    }

# {id} is the path parameter. int is the validation, id automatically gets converted into a integer and then passed on. If the value cannot be 
# converted into a integer the it throws a validation error. 
@app.get("/posts/{id}")
def get_post(id: str):

    cursor.execute("""SELECT * FROM posts WHERE id = %s """, 
                   (str(id),))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post ID {id} not found.")
    return {
        "data": post
    }

@app.delete("/posts/{id}")
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""",
                   (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post not found.")
    else:
        return{"message": "Post was successfully deleted."}

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    # Logic to Fetch the current post.
    cursor.execute("""SELECT * FROM posts where id = %s""", 
                   (str(id),))
    existing_post = cursor.fetchone()
    
    if not existing_post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, 
                            detail=f"Post Not found!!!")
    
    if (existing_post['title'] == post.title and 
        existing_post['content'] == post.content and
        existing_post['published'] == post.published):

        return{
            "message":
            "No Change Detected. Post Not updated!!!"
        }

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published =  %s WHERE id = %s RETURNING *""", 
                   (post.title, 
                    post.content, 
                    post.published,
                    str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    return{
            "message": "Post Updated Successfully.", 
            "data": updated_post
        }
