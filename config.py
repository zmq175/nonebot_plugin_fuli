from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    MYSQL_HOST = ""
    MYSQL_USER = ""
    MYSQL_PASSWORD = ""
    MYSQL_DB = "nonebot"
    MYSQL_PORT = 3306
    MYSQL_CHARSET = "utf8mb4"
