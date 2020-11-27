JWT_SECRET_KEY = "37b7867c5f6687a5682f105673a9c22ea0b2a627f0ea43dc370f02bcb4a1f096"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5

TOKEN_DESCRIPTION = "Checks username and password, if true it returns JWT token"
TOKEN_SUMMARY = "It returns JWT token"

ISBN_DESCRIPTION = "It is unique identifier for books"

DB_HOST = "ec2-18-207-230-232.compute-1.amazonaws.com"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_NAME = "bookstore"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
