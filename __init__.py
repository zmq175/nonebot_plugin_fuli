import json

import nonebot
from sqlalchemy import func

from .config import Config

from nonebot.plugin.on import on_regex, on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    MessageSegment,
    Message, ActionFailed
)
from nonebot.typing import T_State
from nonebot.params import CommandArg, Arg

from .model import ImageGallery
from .mysql import session
import random
import aiohttp

global_config = nonebot.get_driver().config
config = Config.parse_obj(global_config)

print(config)

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
    galleries = session.query(ImageGallery).filter(ImageGallery.gallery_title.like('%' + word + '%')).order_by(func.rand())\
        .limit(count)
    if galleries.count() > 0:
        img_msgs = Message()
        async with aiohttp.ClientSession() as client_session:
            for gallery in galleries:
                img_list = gallery.img_list
                img_list = json.loads(img_list)
                img_len = len(img_list)
                img_cnt = 1
                img_msgs.append(gallery.gallery_title)
                for img in img_list:
                    # 构造图片消息
                    async with client_session.get(img) as resp:
                        img_bytes = await resp.read()
                        img_msg = MessageSegment.image(img_bytes)
                    img_msgs.append(img_msg)
                    img_cnt += 1
                forward_msg = Message(img_msgs)
                try:
                    await bot.send(event=event, message=forward_msg, quote=event.message_id)
                except ActionFailed:
                    await bot.send(event=event, message="消息可能被风控，尝试逐条发送，可能会造成刷屏")
                    bot.send(event=event, message=gallery.gallery_title)
                    img_len = len(img_list)
                    img_cnt = 1
                    for img in img_list:
                        async with client_session.get(img) as resp:
                            img_bytes = await resp.read()
                            try:
                                await bot.send(
                                    message=Message([MessageSegment.image(img_bytes), f"这是你要的福利图（{img_cnt} / {img_len}）"]),
                                    event=event)
                            except ActionFailed:
                                await bot.send(event=event, message="逐条发送依旧失败，请尝试其他内容")
                        img_cnt = img_cnt + 1
            # 不需要清空缓存字典
        await bot.send(event=event, message="欢迎图包投稿：http://imgup.chengzhi.info/ 不会前端凑活用吧，上传会有点慢，等着显示success再关了。")
    else:
        await bot.send(event=event, message="这个真没有，图包投稿：http://imgup.chengzhi.info/ 不会前端凑活用吧，上传会有点慢，等着显示success再关了。")
    session.commit()


@on_regex("^看(.*)?张福利$", priority=5).handle()
async def handleRandomSetu(bot: Bot, event: MessageEvent, state: T_State):
    count = state["_matched_groups"][0]
    galleries = session.query(ImageGallery).order_by(func.rand()).limit(count)
    if galleries.count() > 0:
        img_msgs = Message()
        for gallery in galleries:
            img_list = gallery.img_list
            img_list = json.loads(img_list)
            img_len = len(img_list)
            img_cnt = 1
            img_msgs.append(gallery.gallery_title)
            for img in img_list:
                # 构造图片消息
                img_msg = MessageSegment.image(file=img, timeout=5*60*1000)
                img_msgs.append(img_msg)
                img_cnt += 1
                # 构造转发消息
            forward_msg = Message(img_msgs)
            # 发送转发消息
            try:
                await bot.send(event=event, message=forward_msg, quote=event.message_id)
            except ActionFailed:
                
                await bot.send(event=event, message="消息可能被风控，尝试逐条发送，可能会造成刷屏")
                bot.send(event=event, message=gallery.gallery_title)
                img_len = len(img_list)
                img_cnt = 1
                for img in img_list:
                    try:
                        await bot.send(
                            message=Message([MessageSegment.image(file=img, timeout=5*60*1000), f"这是你要的福利图（{img_cnt} / {img_len}）"]),
                            event=event)
                    except ActionFailed:
                        await bot.send(event=event, message="逐条发送依旧失败，请尝试其他内容")
                    img_cnt = img_cnt + 1
        await bot.send(event=event,
                       message="欢迎图包投稿：http://imgup.chengzhi.info/ 不会前端凑活用吧，上传会有点慢，等着显示success再关了。")
    else:
        await bot.send(message="这个真没有，图包投稿：http://imgup.chengzhi.info/ 不会前端凑活用吧，上传会有点慢，等着显示success再关了。", event=event)
    session.commit()
