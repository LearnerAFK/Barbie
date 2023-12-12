import config
from Barbie.core.mongo import mongodb
from Barbie.utils.database import get_active_video_chats, is_active_video_chat


videodb = mongodb.Javavideocalls

vlimit = []


async def is_video_allowed(chat_idd) -> str:
    chat_id = 123456
    if not vlimit:
        dblimit = await videodb.find_one({"chat_id": chat_id})
        if not dblimit:
            vlimit.clear()
            vlimit.append(config.VIDEO_STREAM_LIMIT)
            limit = config.VIDEO_STREAM_LIMIT
        else:
            limit = dblimit["limit"]
            vlimit.clear()
            vlimit.append(limit)
    else:
        limit = vlimit[0]
    if limit == 0:
        return False
    count = len(await get_active_video_chats())
    if int(count) == int(limit):
        if not await is_active_video_chat(chat_idd):
            return False
    return True


async def get_video_limit() -> str:
    chat_id = 123456
    if not vlimit:
        dblimit = await videodb.find_one({"chat_id": chat_id})
        if not dblimit:
            limit = config.VIDEO_STREAM_LIMIT
        else:
            limit = dblimit["limit"]
    else:
        limit = vlimit[0]
    return limit


async def set_video_limit(limt: int):
    chat_id = 123456
    vlimit.clear()
    vlimit.append(limt)
    return await videodb.update_one(
        {"chat_id": chat_id}, {"$set": {"limit": limt}}, upsert=True
    )
