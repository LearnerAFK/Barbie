from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..misc import SUDOERS
from ..utils import add_off, add_on


@app.on_message(filters.command(["videomode"]) & SUDOERS)
async def videoloaymode(client, message: Message):
    try:
        await message.delete()
    except:
        pass
    usage = "**ᴜsᴀɢᴇ:**\n/videomode [ᴅᴏᴡɴʟᴏᴀᴅ|ᴍ𝟹ᴜ𝟾]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "download":
        await add_on(1)
        await message.reply_text(
            "ᴠɪᴅᴇᴏ ᴘʟᴀʏ ᴍᴏᴅᴇ sᴇᴛ ᴀs ᴅᴏᴡɴʟᴏᴀᴅᴇʀ. ʙᴏᴛ ᴡɪʟʟ ʙᴇ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴛʀᴀᴄᴋs ɴᴏᴡ."
        )
    elif state == "m3u8":
        await add_off(1)
        await message.reply_text(
            "ᴠɪᴅᴇᴏ ᴘʟᴀʏ ᴍᴏᴅᴇ sᴇᴛ ᴀs ᴍ3ᴜ8. ʙᴏᴛ ᴡɪʟʟ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴘʟᴀʏ ᴛʀᴀᴄᴋs ʟɪᴠᴇ ɴᴏᴡ."
        )
    else:
        await message.reply_text(usage)
