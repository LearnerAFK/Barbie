from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..misc import SUDOERS
from ..utils import set_video_limit


@app.on_message(filters.command(["setlimit"]) & SUDOERS)
async def set_video_limit_kid(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if len(message.command) != 2:
        usage = "**ᴜsᴀɢᴇ:**\n/setlimit [ɴᴜᴍʙᴇʀ ᴏғ ᴄʜᴀᴛs] ᴏʀ [ᴅɪsᴀʙʟᴇ]"
        return await message.reply_text(usage)
    message.chat.id
    state = message.text.split(None, 1)[1].strip()
    if state.lower() == "disable":
        limit = 0
        await set_video_limit(limit)
        return await message.reply_text("ᴠɪᴅᴇᴏ ᴄᴀʟʟs ᴅɪsᴀʙʟᴇᴅ ...")
    if state.isnumeric():
        limit = int(state)
        await set_video_limit(limit)
        if limit == 0:
            return await message.reply_text("ᴠɪᴅᴇᴏ ᴄᴀʟʟs ᴅɪsᴀʙʟᴇᴅ ...")
        await message.reply_text(
            "ᴠɪᴅᴇᴏ ᴄᴀʟʟs ᴍᴀxɪᴍᴜᴍ ʟɪᴍɪᴛ ᴅᴇꜰɪɴᴇᴅ ᴛᴏ {0} ᴄʜᴀᴛs ...".format(limit)
        )
    else:
        return await message.reply_text("ᴘʟᴇᴀsᴇ ᴜsᴇ ɴᴜᴍᴇʀɪᴄ ɴᴜᴍʙᴇʀs ꜰᴏʀ sᴇᴛᴛɪɴɢ ʟɪᴍɪᴛ ...")
