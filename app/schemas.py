from pydantic import BaseModel, EmailStr

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True



# The Below two classes will inherit the PostBase class and it's properties
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class Post(BaseModel):
    title: str
    content: str
    published: bool

    class Congig:
        orm_model = True


# This is for the compelete response model for the production state
# class PostResponse(BaseModel):
#     status: str
#     data: Post



# USER Schemas

class UserCreate(BaseModel):
    # username: str
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr