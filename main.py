from fastapi import FastAPI, Depends,HTTPException
from routes.v1 import app_v1
from routes.v2 import app_v2
from starlette.requests import Request
from starlette.responses import Response
from utils.security import check_jwt_token, authenticate_user, create_jwt_token
from starlette.status import HTTP_401_UNAUTHORIZED
from datetime import datetime
from fastapi.security import OAuth2PasswordRequestForm
from models.jwt_user import JWTUser
from utils.const import TOKEN_DESCRIPTION, TOKEN_SUMMARY
import uvicorn
from utils.db_objects import  db

app = FastAPI(title="Book-store API documentation", description="API used for books", version="1.0.0")

app.include_router(app_v1, prefix='/v1',dependencies=[Depends(check_jwt_token)])
app.include_router(app_v2, prefix='/v2',dependencies=[Depends(check_jwt_token)])

@app.on_event("startup")
async def connect_db():
    await db.connect()
@app.on_event("shutdown")
async def disconect_db():
    await db.disconnect()
@app.post("/token", description=TOKEN_DESCRIPTION, summary=TOKEN_SUMMARY)
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    jwt_user_dict = {"username": form_data.username,
                     "password": form_data.password}
    jwt_user = JWTUser(**jwt_user_dict)
    user = await authenticate_user(jwt_user)
    if user is None:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED)
    jwt_token = create_jwt_token(user)
    return {"access_token": jwt_token}


@app.middleware("http")
async def middleware(request: Request, call_next):
    start_time = datetime.utcnow()
    # modify request
    # if not any(word in str(request.url) for word in ["/token", "/docs", "/openapi.json"]):
    #     try:
    #         jwt_token = request.headers["Authorization"].split("Bearer ")[1]
    #         #print(jwt_token)
    #         is_valid = await check_jwt_token(jwt_token)
    #         print(is_valid,"hello")
    #     except Exception as e:
    #         is_valid = False
    #     if not is_valid:
    #         return Response("Unauthorized", status_code=HTTP_401_UNAUTHORIZED)
    response = await call_next(request)
    # modify response
    execution_time = (datetime.utcnow() - start_time).microseconds
    response.headers["x-execution-time"] = str(execution_time)
    return response

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)