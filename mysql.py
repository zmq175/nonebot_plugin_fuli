import nonebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Config

global_config = nonebot.get_driver().config
config = Config.parse_obj(global_config)
engine = create_engine(
    f"mysql+pymysql://{config.MYSQL_USER}:{config.MYSQL_PASSWORD}@{config.MYSQL_HOST}:{config.MYSQL_PORT}/{config.MYSQL_DB}?charset={config.MYSQL_CHARSET}",
    pool_pre_ping=True, pool_recycle=3600, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
