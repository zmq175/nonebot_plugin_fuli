import json

from nonebot import get_driver

from .config import Config

from nonebot.plugin.on import on_regex, on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    MessageSegment,
    Message
)
from nonebot.typing import T_State
from nonebot.params import CommandArg, Arg

from .model import ImageGallery
from .mysql import session

global_config = get_driver().config
config = Config.parse_obj(global_config)

Bot_NICKNAME = list(global_config.nickname)

Bot_NICKNAME = Bot_NICKNAME[0] if Bot_NICKNAME else "福利姬bot"

hello = on_command("烧鸡", aliases={"福利"}, rule=to_me(), priority=50, block=True)


@hello.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = (
        "发送【看看xx福利图】可获得一张随机福利图。"
        "图片取自：\n"
        "wnacg.com"
    )
    await hello.finish(msg)


@on_regex("^看(.*)?张(.+)福利$", priority=5).handle()
async def handleRandomSetu(bot: Bot, event: MessageEvent, state: T_State):
    word = state["_matched_groups"][1]
    count = state["_matched_groups"][0]
    galleries = session.query(ImageGallery).filter(ImageGallery.gallery_title.like('%' + word + '%')).limit(count)
    if galleries.count() > 0:
        for gallery in galleries:
            img_list = gallery.img_list
            img_list = json.loads(img_list)
            for img in img_list:
                await bot.send([MessageSegment.image(img), f"这是你要的{word}福利图"])
    else:
        await bot.send("这个真没有")


@on_regex("^看(.*)?张福利$", priority=5).handle()
async def handleRandomSetu(bot: Bot, event: MessageEvent, state: T_State):
    count = state["_matched_groups"][0]
    galleries = session.query(ImageGallery).limit(count)
    if galleries.count() > 0:
        for gallery in galleries:
            img_list = gallery.img_list
            img_list = json.loads(img_list)
            for img in img_list:
                await bot.send([MessageSegment.image(img), f"这是你要的福利图"])
    else:
        await bot.send("这个真没有")