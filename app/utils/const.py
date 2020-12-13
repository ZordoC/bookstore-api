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


REDIS_URL = f"redis://{DB_HOST}"

TESTING = False
IS_LOAD_TEST = False

TESTING_DB_HOST = "ec2-18-209-224-77.compute-1.amazonaws.com"
TESTING_DB_USER = "test"
TESTING_DB_PASSWORD = "test"
TESTING_DB_NAME = "test"
TESTING_DB_URL = f"postgresql://{TESTING_DB_USER}:{TESTING_DB_PASSWORD}@{TESTING_DB_HOST}/{TESTING_DB_NAME}"

TESTING_REDIS_URL = f"redis://{TESTING_DB_HOST}"
