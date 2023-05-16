import nonebot
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import Config

global_config = nonebot.get_driver().config
config = Config.parse_obj(global_config)
engine = create_engine(
    f"mysql+pymysql://{config.mysql_user}:{config.mysql_password}@{config.mysql_host}:{config.mysql_port}/{config.mysql_db}?charset={config.mysql_charset}",
    pool_pre_ping=True, pool_recycle=3600, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
