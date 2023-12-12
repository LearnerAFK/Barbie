"""CREDIT : MUKESH DIDI @NOOB-MUKESH"""

import requests
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Barbie import app


@app.on_message(filters.command(["write", "writetool"]) & ~BANNED_USERS)
async def handwrite(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    replied = message.reply_to_message
    msg = f"**Hey {message.from_user.mention} Please Reply To A Text Or Give Some Lines To Write !**"
    if replied:
        if replied.text or replied.caption:
            text = replied.text or replied.caption
        else:
            return await message.reply_text(msg)
    else:
        if len(message.command) > 1:
            text = message.text.split(None, 1)[1]
        else:
            return await message.reply_text(msg)
    m = await message.reply_text("**Please Wait...**")
    write = requests.get(f"https://apis.xditya.me/write?text={text}").url

    caption = f"""
**--sᴜᴄᴇssғᴜʟʟʏ ᴡʀɪᴛᴛᴇɴ ᴛᴇxᴛ :--**

**ᴡʀɪᴛᴛᴇɴ ʙʏ :** {app.mention}
**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ :** {message.from_user.mention}
"""
    await m.delete()
    await message.reply_photo(photo=write, caption=caption)


__MODULE__ = "WʀɪᴛᴇTᴏᴏʟ"
__HELP__ = """
 ᴡʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ ᴏɴ ᴡʜɪᴛᴇ ᴘᴀɢᴇ ᴡɪᴛʜ ᴀ ᴘᴇɴ

/write <ᴛᴇxᴛ> *:* ᴡʀɪᴛᴇs ᴛʜᴇ ɢɪᴠᴇɴ ᴛᴇxᴛ.
 """
