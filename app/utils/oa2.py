from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer


from app.models import models
from app.utils.token import verify_access_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "bearer"}
    )
    email = verify_access_token(token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.email == email).first()
    return user