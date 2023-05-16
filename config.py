import nonebot
from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    """Plugin Config Here"""
    mysql_host = ""
    mysql_user = ""
    mysql_password = ""
    mysql_db = "nonebot"
    mysql_port = 3306
    mysql_charset = "utf8mb4"


global_config = nonebot.get_driver().config
config = Config(**global_config.dict())
