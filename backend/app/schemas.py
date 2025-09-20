from pydantic import BaseModel
from typing import Optional, List


STATUSES = [
     "Working",
     "Working Remotely",
     "On Vacation",
     "Business Trip",
]


class Token(BaseModel):
     access_token: str
     token_type: str = "bearer"


class LoginRequest(BaseModel):
     username: str
     password: str


class UserPublic(BaseModel):
     id: int
     username: str
     full_name: str
     status: str
     class Config:
          from_attributes = True


class UsersList(BaseModel):
     items: List[UserPublic]


class UpdateStatus(BaseModel):
     status: str