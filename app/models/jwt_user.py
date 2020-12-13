from pydantic import BaseModel



class JWTUser(BaseModel):
    username: str
    password: str
    disabled: bool = False
    roles: str = None