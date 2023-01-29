import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class ShowUser(BaseModel):
    full_name: str
    email: str
    class Config(): 
        orm_mode = True


class User(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class UserForgotPassword(BaseModel):
    email: EmailStr

class UserVerifyAccount(BaseModel):
    email: EmailStr

class UserUpdatePassword(BaseModel):
    email: EmailStr
    password: str

class VerificationCode(BaseModel):
    code: str
    email: EmailStr

class UserOut(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: Optional[str]
    address: Optional[str]
    avatar: Optional[str]
    birth_date: Optional[datetime.date]
    country: Optional[str]
    class Config(): 
        orm_mode = True
    
class UserEdit(BaseModel):
    address: Optional[str]
    avatar: Optional[str]
