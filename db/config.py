import environ
from dotenv import load_dotenv

load_dotenv()


@environ.config(prefix="SQLITE")
class SQLiteConfig:
    path: str = environ.var(default='.')
    db_name: str = environ.var(default='test')

sqlite_config: SQLiteConfig = SQLiteConfig.from_environ()
