from typing import Optional
from pydantic import BaseModel, ConfigDict


class Comment(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: Optional[int] = None
    postId: int
    name: str
    email: Optional[str] = None
    body: str


class CommentCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    postId: int
    name: str
    email: Optional[str] = None
    body: str


class CommentUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    postId: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    body: Optional[str] = None
