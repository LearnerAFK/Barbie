from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..misc import SUDOERS
from ..utils import blacklist_chat, blacklisted_chats, whitelist_chat


__MODULE__ = "Bʟ-ᴄʜᴀᴛ"
__HELP__ = """
/blacklistchat [ᴄʜᴀᴛ ɪᴅ] : ʙʟᴀᴄᴋʟɪsᴛ ᴀ ᴄʜᴀᴛ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.

/whitelistchat [ᴄʜᴀᴛ ɪᴅ] : ᴡʜɪᴛᴇʟɪsᴛ ᴛʜᴇ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ.

/blacklistedchat : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs.
"""


@app.on_message(filters.command(["blacklistchat", "blchat"]) & SUDOERS)
async def blacklist_chat_func(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if len(message.command) != 2:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n/blacklistchat [ᴄʜᴀᴛ-ɪᴅ]")
    chat_id = int(message.text.strip().split()[1])
    if chat_id in await blacklisted_chats():
        return await message.reply_text("ᴄʜᴀᴛ ɪs ᴀʟʀᴇᴀᴅʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ.")
    blacklisted = await blacklist_chat(chat_id)
    if blacklisted:
        await message.reply_text("ᴄʜᴀᴛ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssꜰᴜʟʟʏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ")
    else:
        await message.reply_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ !")
    try:
        await app.leave_chat(chat_id)
    except:
        pass


@app.on_message(filters.command(["whitelistchat", "unblchat", "wlchat"]) & SUDOERS)
async def white_funciton(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if len(message.command) != 2:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n/whitelistchat [ᴄʜᴀᴛ-ɪᴅ]")
    chat_id = int(message.text.strip().split()[1])
    if chat_id not in await blacklisted_chats():
        return await message.reply_text("ᴄʜᴀᴛ ɪs ᴀʟʀᴇᴀᴅʏ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ.")
    whitelisted = await whitelist_chat(chat_id)
    if whitelisted:
        return await message.reply_text("ᴄʜᴀᴛ ʜᴀs ʙᴇᴇɴ sᴜᴄᴄᴇssꜰᴜʟʟʏ ᴡʜɪᴛᴇʟɪsᴛᴇᴅ ")
    await message.reply_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ !")


@app.on_message(filters.command(["blacklistedchat", "blchats"]) & ~BANNED_USERS)
async def all_chats(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    text = "**ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs :**\n\n"
    j = 0
    for count, chat_id in enumerate(await blacklisted_chats(), 1):
        try:
            title = (await app.get_chat(chat_id)).title
        except:
            title = "ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        j = 1
        text += f"**{count}. {title}** [`{chat_id}`]\n"
    if j == 0:
        await message.reply_text("ɴᴏ ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛs.")
    else:
        await message.reply_text(text)
