
from fastapi import FastAPI,Header,HTTPException
from passlib.context import CryptContext
from models.jwt_user import JWTUser
from datetime import datetime, timedelta
from utils.const import JWT_EXPIRATION_TIME_MINUTES, JWT_SECRET_KEY, JWT_ALGORITHM
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import time
from utils.db_functions import db_check_token_user, db_check_jwt_username
from starlette.status import HTTP_401_UNAUTHORIZED

oauth_schema = OAuth2PasswordBearer(tokenUrl="/token")
pwd_context = CryptContext(schemes=['bcrypt'])


def get_hashed_password(password):
    return pwd_context.hash(password)

def verify_password(plain_password,hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        return False

# hashed="$2b$12$5mFPY2oC3MMF83yFU.ZWOecGT.B0DpVD3b3llpLLWKW16urzvG2zu"
# print(get_hashed_password("mysecret"))
# print(verify_password("mysecret",hashed))


# Authenticate username and password to give JWT token
async def authenticate_user(user:JWTUser):
    potential_users = await db_check_token_user(user)
    is_valid = False
    for db_user in potential_users:
        if verify_password(user.password, db_user["password"]):
            is_valid = True
    if is_valid:
        user.roles = "admin"
        return user
    return None



# Creates access JWT token
def create_jwt_token(user):
    expiration = datetime.utcnow() + timedelta(minutes=JWT_EXPIRATION_TIME_MINUTES)
    jwt_payload = {"sub": user.username,
                   "role": user.roles,
                   "exp":expiration}

    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return jwt_token


# Checks wether JWT token is correct
async def check_jwt_token(token: str = Depends(oauth_schema)):
    try:
        jwt_payload = jwt.decode(token,JWT_SECRET_KEY,algorithms=JWT_ALGORITHM)
        username = jwt_payload.get("sub")
        role = jwt_payload.get("role")
        expiration = jwt_payload.get("exp")
        if time.time() < expiration:
            #print("stuff")
            is_valid = True
            if is_valid:
                #print(is_valid)
                return final_checks(role)
    except Exception as e:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)


# Last checking and returning the final result
def final_checks(role: str):
    if role == "admin":
        return True
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)

    


# print(get_hashed_password("secret"))