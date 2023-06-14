from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()

# define how should the frontend should be sending data. This is validation. Later we will be refrencing this class to validate. 
# default value for published is True. If used didn't pass the value, it will be set to true
# rating field in options. If user doesn't provide any, default vaule will be null. 
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "Country", "content": "Nepal", "id":1}, {"title": "District", "content": "Chitwan", "id":2} ]

# @ section is decorator. get is the method being called, and / is the path. 
@app.get("/")
async def root():
    return {"MSG": "Python FastAPI."}

@app.get("/posts")
def get_posts():
    return {"DATA": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# Post is refrencing to the class named Post.
def create_posts(post: Post):
    print(post)
    #printing the output in dictionary format 
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"DATA": post_dict}

# Getting the post of the specific id
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
# Finding index of the post for deleting and updating post. 
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i 
        

# Retriving single post 
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")
    return {"DATA": post}


#Deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found.")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update a post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,              
                            detail=f"Post with id: {id} was not found.")    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index]=post_dict
    return {"MSG": "Post Updated."}
