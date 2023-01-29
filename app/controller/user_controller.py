from sqlalchemy.orm import Session
from ..schema import schemas
from ..models import models
from fastapi import BackgroundTasks, HTTPException, status
from ..utils import email_handler, hash, token
import time

PASSWORD_RESET_INTERVAL = 2 * 60 * 60 # 2 hours
VERIFICATION_EXPIRATION_INTERVAL = 5 * 60 # 5 minutes

def create(user: schemas.User, db: Session):
    hashed_password = hash.hash_password(user.password)
    new_user = models.User(full_name=user.full_name, email=user.email, 
    password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get(id: int, db:Session):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
        detail=f"User with id: {id} not found")
    return user


def get_all(db:Session):
    return db.query(models.User).all()


def reset_can_update_password(user_object: models.User, seconds: float, db:Session):
    time.sleep(seconds)
    user_object.can_update_password = False
    db.add(user_object)
    db.commit()


def forgot_password(email_to:str, background_tasks: BackgroundTasks, db:Session):

    user_query = db.query(models.User).filter(models.User.email == email_to)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    user.can_update_password = True
    email_handler.send_email(
        background_tasks, 
        'Forgotten Password: Reset your password', 
        email_to, {'title': 'Welcome'}, 
        "forgot_password.html")
    background_tasks.add_task(reset_can_update_password, user, PASSWORD_RESET_INTERVAL, db)
    
    db.add(user)
    db.commit()

def update_user_information(user_email: str, user_fields: schemas.UserEdit, db: Session):
    user_query = db.query(models.User).filter(models.User.email == user_email)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user_fields.address:
        user.address = user_fields.address
    if user_fields.avatar:
        user.avatar = user_fields.avatar
        
    db.add(user)
    db.commit()

def hash_update_password(user_info: schemas.UserUpdatePassword, db:Session):
    user_query = db.query(models.User).filter(models.User.email == user_info.email)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user.can_update_password == False:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,detail="Passord Update not Allowed or Expired")
    
    user.password = hash.hash_password(user_info.password)
    user.can_update_password = False
    db.add(user)
    db.commit()


def verification_expired(user_object: models.User, seconds: float, db:Session):
    time.sleep(seconds)
    user_object.verification_code = ""
    db.add(user_object)
    db.commit()


def verify_user_account(email_to:str, background_tasks: BackgroundTasks, db:Session):

    user_query = db.query(models.User).filter(models.User.email == email_to)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="User already verified")

    verification_code = token.generate_user_verification_code()
    user.verification_code = verification_code
    print(verification_code)
    email_handler.send_email(background_tasks, "Account Verification: Let's make sure it is you", email_to, {'verification_code': verification_code}, "account_verification.html")
    background_tasks.add_task(verification_expired, user, VERIFICATION_EXPIRATION_INTERVAL, db)
    
    db.add(user)
    db.commit()


def confirm_verification(verification_code: str, user_email: str, db: Session):
    
    user_query = db.query(models.User).filter(models.User.email == user_email)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    if user.is_verified:
        raise HTTPException(status_code=status.HTTP_202_ACCEPTED, detail="User already verified")
    if user.verification_code == "":
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Verification code expired")
    if user.verification_code != verification_code:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect code")
    
    user.is_verified = True
    db.add(user)
    db.commit()


def validate_passport_text(current_user: schemas.User, passport_text):
    lower_case_text = passport_text.lower()
    user_name_list = current_user.full_name.lower().split(" ")
    for name in user_name_list:
        if not name in lower_case_text:
            return False
    return "passport" in lower_case_text