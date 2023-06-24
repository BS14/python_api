from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()

# define how should the frontend should be sending data. This is validation. Later we will be refrencing this class to validate. 
# default value for published is True. If used didn't pass the value, it will be set to true
# rating field in options. If user doesn't provide any, default vaule will be null. 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

#Connection to Database. 

while True:
    try:
        conn = psycopg2.connect(host='127.0.0.1', database='python_api', user='python_api', password='password', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection sucessfull!")
        break
    except Exception as error:
        print("Conncting to Database failed!")
        print("Error: ", error)
        time.sleep(5)


# @ section is decorator. get is the method being called, and / is the path. 
@app.get("/")
async def root():
    return {"MSG": "Python FastAPI."}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts  """)
    posts = cursor.fetchall()
    return {"DATA": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# Post is refrencing to the class named Post.
def create_posts(post: Post):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
    RETURNING * """,
                   (post.title, post.content, post.published))
    #Getting the return value from cursor.execture
    new_post = cursor.fetchone()
    #Saving data in the database. 
    conn.commit()
    return {"DATA": new_post}

# Retriving single post 
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")
    return {"DATA": post}


#Deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts where id = %s  RETURNING *""", (str(id)),)
    deleted_post = cursor.fetchone()
    conn.commit()


    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,              
                            detail=f"Post with id: {id} was not found.")    
    return {"UPDATED_POST": updated_post}
