from pyrogram import filters
from Barbie import app
from ..misc import SUDOERS
from ..utils import add_off, add_on


@app.on_message(filters.command(["logger"]) & SUDOERS)
async def logger(_, message):
    try:
        await message.delete()
    except:
        pass
    usage = "**ᴜsᴀɢᴇ:**\n/logger [enable|disable]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "enable":
        await add_on(2)
        await message.reply_text("ᴇɴᴀʙʟᴇᴅ ʟᴏɢɢɪɴɢ ...")
    elif state == "disable":
        await add_off(2)
        await message.reply_text("ᴅɪsᴀʙʟᴇᴅ ʟᴏɢɢɪɴɢ ...")
    else:
        await message.reply_text(usage)
