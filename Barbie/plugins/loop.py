from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..utils import AdminRightsCheck, set_loop


@app.on_message(filters.command(["loop", "cloop"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def admins(_, message: Message, chat_id):
    if len(message.command) != 2:
        return await message.reply_text(
            "**ᴜsᴀɢᴇ:**\n/loop [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] or [ɴᴜᴍʙᴇʀ ʙᴇᴛᴡᴇᴇɴ 1-10]\n\n**ᴇxᴀᴍᴘʟᴇ:** /loop 5"
        )
    state = message.text.split(None, 1)[1].strip()

    if state.isnumeric():
        state = int(state)
        if 1 <= state <= 10:
            await set_loop(chat_id, state)
            return await message.reply_text(
                "ʟᴏᴏᴘ ᴇɴᴀʙʟᴇᴅ ʙʏ {0} ​ ꜰᴏʀ **{1}** ᴛɪᴍᴇs.\n\nʙᴏᴛ ᴡɪʟʟ ɴᴏᴡ ʀᴇᴘᴇᴀᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ꜰᴏʀ **{1}** ᴛɪᴍᴇs ​".format(
                    message.from_user.mention, state
                )
            )
        else:
            return await message.reply_text("ᴘʟᴇᴀsᴇ ᴜsᴇ ɴᴜᴍʙᴇʀs ʙᴇᴛᴡᴇᴇɴ 1-10 ꜰᴏʀ ʟᴏᴏᴘ ᴘʟᴀʏ ...​")
    elif state.lower() == "enable":
        await set_loop(chat_id, 10)
        return await message.reply_text(
            "ʟᴏᴏᴘ ᴇɴᴀʙʟᴇᴅ ʙʏ {0} ​ ꜰᴏʀ **{1}** ᴛɪᴍᴇs.\n\nʙᴏᴛ ᴡɪʟʟ ɴᴏᴡ ʀᴇᴘᴇᴀᴛ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴘʟᴀʏɪɴɢ ᴍᴜsɪᴄ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ꜰᴏʀ **{1}** ᴛɪᴍᴇs ​".format(
                message.from_user.mention, 10
            )
        )
    elif state.lower() == "disable":
        await set_loop(chat_id, 0)
        return await message.reply_text("ʟᴏᴏᴘ ᴘʟᴀʏ ʜᴀs ʙᴇᴇɴ ᴅɪsᴀʙʟᴇᴅ ...​")

    else:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n/loop [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] or [ɴᴜᴍʙᴇʀ ʙᴇᴛᴡᴇᴇɴ 1-10]\n\n**ᴇxᴀᴍᴘʟᴇ:** /loop 5")
