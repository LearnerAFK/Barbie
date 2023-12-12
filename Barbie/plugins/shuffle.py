from random import shuffle
from pyrogram import filters
from pyrogram.types import Message
from config import BANNED_USERS
from Barbie import app
from ..misc import db
from ..utils.decorators import AdminRightsCheck


@app.on_message(filters.command(["shuffle"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def admins(_, message: Message, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("ᴇʀʀᴏʀ ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏғ ᴄᴏᴍᴍᴀɴᴅ ...")
    check = db.get(chat_id)
    if not check:
        return await message.reply_text("ɴᴏᴛʜɪɴɢ ɪɴsɪᴅᴇ ǫᴜᴇᴜᴇ ᴛᴏ sʜᴜꜰꜰʟᴇ ...​")
    try:
        popped = check.pop(0)
    except:
        return await message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ sʜᴜꜰꜰʟᴇ ​...")
    check = db.get(chat_id)
    if not check:
        check.insert(0, popped)
        return await message.reply_text("ꜰᴀɪʟᴇᴅ ᴛᴏ sʜᴜꜰꜰʟᴇ ​...")
    shuffle(check)
    check.insert(0, popped)
    await message.reply_text("**ǫᴜᴇᴜᴇ sʜᴜꜰꜰʟᴇᴅ ʙʏ {0} ...​**".format(
            message.from_user.mention
        )
    )
