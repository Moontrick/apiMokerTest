from typing import Optional
from pydantic import BaseModel, Field, EmailStr, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    id: Optional[int] = None
    name: str
    username: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    company: Optional[dict] = None
    address: Optional[dict] = None


class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: str
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    company: Optional[dict] = None
    address: Optional[dict] = None


class UserUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None
    company: Optional[dict] = None
    address: Optional[dict] = None
