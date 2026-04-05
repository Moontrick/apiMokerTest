from typing import Optional
from pydantic import BaseModel, ConfigDict


class Post(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: Optional[int] = None
    userId: int
    title: str
    body: str


class PostCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    userId: int
    title: str
    body: str


class PostUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    userId: Optional[int] = None
    title: Optional[str] = None
    body: Optional[str] = None


class Like(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: Optional[int] = None
    postId: int
    userId: Optional[int] = None
    createdAt: Optional[str] = None
