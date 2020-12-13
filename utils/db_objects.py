from databases import Database
from utils.const import DB_URL, TESTING, TESTING_DB_URL, IS_LOAD_TEST

if TESTING or IS_LOAD_TEST:
    db = Database(TESTING_DB_URL)
else:
    db = Database(DB_URL)
