from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
import time
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

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

# Fetching all Posts without ORM (SQL ALCHEMY)
#@app.get("/posts")
#def get_posts():
#    cursor.execute(""" SELECT * FROM posts  """)
#    posts = cursor.fetchall()
#    return {"DATA": posts}

#Fetching all Posts with ORM 
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"DATA": posts}

@app.get("/aws/accounts", tags=["AWS"])
def get_accounts(db: Session = Depends(get_db)):
    accounts = db.query(models.aws).all()
    for account in accounts:
        account_dict = account.__dict__
        account_dict['aws_secret_key'] = account_dict['aws_secret_key'][:5] + '*' * (len(account_dict['aws_secret_key']) - 5)
    return {"DATA": accounts}

# Creating a post without ORM
#@app.post("/posts", status_code=status.HTTP_201_CREATED)
# Post is refrencing to the class named Post.
#def create_posts(post: Post):
#    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) 
#    RETURNING * """,
#                   (post.title, post.content, post.published))
#    #Getting the return value from cursor.execture
#    new_post = cursor.fetchone()
#    #Saving data in the database. 
#    conn.commit()
#    return {"DATA": new_post}

# Creating a post with ORM ( SQL ALCHEMY)

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.Post, db:Session = Depends(get_db)):
    # This could be hassle to match the each field with each objects in the model. Rather we can use dictonary. 
    #new_post = models.Post(
    #    title=post.title, 
    #    content=post.content, 
    #    published=post.published
    #    )
    new_post = models.Post(
        **post.dict()
    )
    #Adding the post to the database
    db.add(new_post)
    # Commiting the changes to the database. 
    db.commit()
    # Retriving the change to the database. 
    db.refresh(new_post)
    return {"DATA": new_post}

@app.post("/aws/register", status_code=status.HTTP_201_CREATED, tags=["AWS"])
def aws_register(post: schemas.AWS, db:Session = Depends(get_db)):
    new_account = models.aws(
        **post.dict()
    )
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    #Returning only 5 character of the secret leaving other same. 
    response_data = {
        **post.dict(), 
        "aws_secret_key": new_account.aws_secret_key[:5] + '*' * 10
    }
    return {"DATA": response_data}
# Retriving single post without ORM. 
#@app.get("/posts/{id}")
#def get_post(id: int):
#    cursor.execute(""" SELECT * FROM posts where id = %s """, (str(id)))
#    post = cursor.fetchone()
#    if not post:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"Post with id: {id} was not found.")
#    return {"DATA": post}

# Retriving single post with ORM. 
@app.get("/posts/{id}")
def get_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")
    return {"DATA": post}

# Retriving single aws account details 
@app.get("/aws/accounts/{id}", tags=["AWS"])
def get_account(id: int, db:Session = Depends(get_db)):
    account = db.query(models.aws).filter(models.aws.id == id).first()
    if not account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            details=f"Account with id: {id} was not found.")
    account_dict = account.__dict__
    account_dict['aws_secret_key'] = account_dict['aws_secret_key'][:5] + '*' * (len(account_dict['aws_secret_key']) - 5)
    return {"DATA": account_dict}

#Deleting a post without ORM
#@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
#def delete_post(id: int):
#    cursor.execute(""" DELETE FROM posts where id = %s  RETURNING *""", (str(id)),)
#    deleted_post = cursor.fetchone()
#    conn.commit()
#    if deleted_post == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                            detail=f"Post with id: {id} was not found.")
#    return Response(status_code=status.HTTP_204_NO_CONTENT)

#Deleting a post with ORM
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db:Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id) 
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post without ORM
#@app.put("/posts/{id}")
#def update_post(id: int, post: Post):
#    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", 
#                   (post.title, post.content, post.published, str(id)))
#    updated_post = cursor.fetchone()
#    conn.commit()
#    if updated_post == None:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,              
#                            detail=f"Post with id: {id} was not found.")    
#    return {"UPDATED_POST": updated_post}

#Deleting a post with ORM
@app.put("/posts/{id}")
def update_post(id: int, updated_post: schemas.Post, db:Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id )
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,              
                            detail=f"Post with id: {id} was not found.")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return {"UPDATED_POST": post_query.first()}


