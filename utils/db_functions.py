from utils.db import execute, fetch
from models.jwt_user import JWTUser


async def db_check_token_user(user: JWTUser):
    query = """ select * from users where username=:username"""
    values = {"username": user.username}
    result = await fetch(query, False, values)
    if result is None:
        return False
    else:
        return result


async def db_check_jwt_username(username):
    query = """ select * from users where username=:username"""
    values = {"username": username}
    result = await fetch(query, True, values)
    if result is None:
        return False
    else:
        return True


async def db_insert_personel(user):
    query = """insert into personel(username, password, mail, role)
            values(:name, :password, :mail, :role)"""
    values = dict(user)
    await execute(query, False, values)


async def db_check_personel(username, password):
    query = """ select * from personel where username=:username
                                          and password=:password"""
    values = {"username": username, "password": password}
    results = await fetch(query, True, values)
    if results is None:
        return False
    else:
        return True


async def db_get_book_with_isbn(isbn):
    query = """select * from books where isbn=:isbn"""
    values = {"isbn": isbn}
    book = await fetch(query, True, values)
    if book is None:
        return False
    else:
        return book


async def db_get_author_name(name):
    query = """select * from author where name=:name"""
    values = {"name": name}
    author = await fetch(query, True, values)
    if author is None:
        return False
    else:
        return author


async def db_get_author_from_id(id):
    query = """select * from author where id =:id"""
    values = {"id": id}
    author = await fetch(query, True, values)
    return author


async def db_patch_author_name(id, name):
    query = """update author set name=:name where id=:id"""
    values = {"id": id, "name": name}
    await execute(query, False, values)
