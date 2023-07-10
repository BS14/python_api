from pydantic import BaseModel

# define how should the frontend should be sending data. This is validation. Later we will be refrencing this class to validate. 
# default value for published is True. If used didn't pass the value, it will be set to true
# rating field in options. If user doesn't provide any, default vaule will be null. 

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatPost(BaseModel):
    title: str
    contenet: str
    published: bool = True

class UpdatePost(BaseModel):
    title: str
    contenet: str
    published: bool

class AWS(BaseModel):
    project_name: str
    aws_secret_id: str
    aws_secret_key: str

