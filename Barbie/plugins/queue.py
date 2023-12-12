from config import BANNED_USERS, STREAM_IMG
from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..misc import db
from ..utils import seconds_to_min, is_active_chat, gen_thumb, queue_markup


basic = {}


def get_duration(playing):
    file_path = playing[0]["file"]
    if "index_" in file_path or "live_" in file_path:
        return "ᴜɴᴋɴᴏᴡɴ"
    duration_seconds = int(playing[0]["seconds"])
    if duration_seconds == 0:
        return "ᴜɴᴋɴᴏᴡɴ"
    else:
        return seconds_to_min(duration_seconds)


@app.on_message(filters.command(["queue", "player"]) & filters.group & ~BANNED_USERS)
async def queue_com(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    chat_id = message.chat.id
    if not await is_active_chat(chat_id):
        return await message.reply_text("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ...")
    got = db.get(chat_id)
    if not got:
        return await message.reply_text("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ ...")
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)

    if ("live_" in file) or ("vid_" in file):
        IMAGE = await gen_thumb(videoid)
    elif "index_" in file:
        IMAGE = STREAM_IMG
    else:
        if videoid == "telegram":
            IMAGE = STREAM_IMG if typo == "Audio" else STREAM_IMG
        else:
            IMAGE = await gen_thumb(videoid)

    cap = f"""**{app.mention} ᴩʟᴀʏᴇʀ**

**Tɪᴛʟᴇ:** {title[:27]}
**Dᴜʀᴀᴛɪᴏɴ:** {DUR}
**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {user}

ᴄʟɪᴄᴋ ᴏɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ᴡʜᴏʟᴇ ǫᴜᴇᴜᴇᴅ ʟɪsᴛ :"""
    upl = queue_markup("g", videoid)
    basic[videoid] = True
    await message.reply_photo(photo=IMAGE, caption=cap, reply_markup=upl)
