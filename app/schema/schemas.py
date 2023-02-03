from enum import Enum
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


class SlotTypeEnum(str, Enum):
    LAB = "LAB"
    TUT = "TUT"
    LEC = "LEC"


class Slot(BaseModel):
    instructor_name: Optional[str]
    room_number:    Optional[str]
    start_time:   datetime.datetime
    end_time:  datetime.datetime
    course_name: Optional[str]
    type:       Optional[SlotTypeEnum]
    course_id: str
    group_id:     str

    class Config():
        orm_mode = True


class SlotUpdate(BaseModel):
    instructor_name: Optional[str]
    room_number:    Optional[str]
    start_time:    Optional[datetime.datetime]
    end_time:   Optional[datetime.datetime]
    course_name: Optional[str]
    type:       Optional[SlotTypeEnum]
    course_id:  Optional[str]
    group_id:      Optional[str]

    class Config():
        orm_mode = True


class SlotRange(BaseModel):
    start_date: datetime.date
    end_date: datetime.date

    class Config():
        orm_mode = True
