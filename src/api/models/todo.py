from typing import Optional
from pydantic import BaseModel, ConfigDict


class Todo(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: Optional[int] = None
    userId: int
    title: str
    completed: Optional[bool] = False


class TodoCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    userId: int
    title: str
    completed: Optional[bool] = False


class TodoUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    userId: Optional[int] = None
    title: Optional[str] = None
    completed: Optional[bool] = None
