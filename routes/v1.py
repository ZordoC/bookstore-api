from fastapi import FastAPI, Body, Header, File, Depends, APIRouter
from models.user import User
from models.author import Author
from models.book import Book
from models.jwt_user import JWTUser
from starlette.status import HTTP_201_CREATED, HTTP_401_UNAUTHORIZED
from starlette.responses import Response
from utils.security import authenticate_user, create_jwt_token
from utils.db_functions import (db_insert_personel, db_check_personel, db_get_book_with_isbn, db_get_author_name,
                                db_get_author_from_id,db_patch_author_name)

app_v1 = APIRouter()


@app_v1.post("/user/", status_code=HTTP_201_CREATED, tags=["User"])
async def post_user(user: User):
    await db_insert_personel(user)
    return {"result": "personel has been created"}


@app_v1.get("/login", tags=["User"])
async def get_user_validation(username: str = Body(...), password: str = Body(...)):
    result = await db_check_personel(username, password)
    return {"is_valid": result}


@app_v1.get("/useless", tags=["User"])
async def useless():
    return {"hello": "hello"}


@app_v1.get("/book/{isbn}", response_model=Book, response_model_exclude=["author"],
            tags=["Book"])  # response_model_include=["author"]
async def get_book_with_isbn(isbn: str):
    book = await db_get_book_with_isbn(isbn)
    author = await db_get_author_name(book['author'])
    author_obj = Author(**author)
    book["author"] = author_obj
    result_book = Book(**book)
    return result_book


@app_v1.get("/author/{id}/book", tags=["Book"])
async def get_author_books(id: int, order: str = 'asc'):
    author = await db_get_author_from_id(id)
    if author is None:
        return {"result": "There's no such author in the database"}
    else:
        books = author["books"]
        if order == 'asc':
            books = sorted(books)
        else:
            books = sorted(books, reverse=True)
        return {"books": books}


@app_v1.patch("/author/{id}/name", tags=["Author"])
async def patch_author_name(id: int, name: str = Body(..., embed=True)):
    await db_patch_author_name(id, name)
    return {"result": "name is updated "}


@app_v1.post("/user/author", tags=["Author"])
async def post_user_and_body(user: User, author: Author, bookstore_name: str = Body(..., embed=True)):
    return {"user": user, "author": author, "bookstore_name": bookstore_name}


@app_v1.post("/user/photo")
async def upload_user_photo(response: Response, profile_photo: bytes = File(...)):
    response.headers['x-file-size'] = str(len(profile_photo))  # custom headers
    response.set_cookie(key="cookie-api", value="test")
    return {"file_size": len(profile_photo)}
