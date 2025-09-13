from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from app.db.models import Gender


# Shared properties
class UserBase(BaseModel):
    username: str
    birthDate: Optional[datetime] = None
    gender: Optional[Gender] = None


# Properties to receive on user creation
class UserCreate(UserBase):
    pass


# Properties to receive on user update
class UserUpdate(UserBase):
    username: str


# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class User(UserInDBBase):
    pass


# Properties stored in DB
class UserInDB(UserInDBBase):
    pass
