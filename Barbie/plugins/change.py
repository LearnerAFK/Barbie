import os
from config import BANNED_USERS
from pyrogram import filters
from Barbie import app
from ..utils import adminsOnly


__MODULE__ = "Cʜᴀɴɢᴇ"
__HELP__ = """
/settitle - ᴄʜᴀɴɢᴇ ᴛʜᴇ ɴᴀᴍᴇ ᴏғ ᴀ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ

/setphoto - ᴄʜᴀɴɢᴇ ᴛʜᴇ ᴘғᴘ ᴏғ ᴀ ɢʀᴏᴜᴘ/ᴄʜᴀɴɴᴇʟ

/title - ᴄʜᴀɴɢᴇ ᴛʜᴇ ᴀᴅᴍɪɴ ᴛɪᴛʟᴇ
"""


@app.on_message(filters.command("settitle") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def set_chat_title(_, message):
    try:
        await message.delete()
    except:
        pass
    if len(message.command) < 2:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n/settitle NEW NAME")
    old_title = message.chat.title
    new_title = message.text.split(None, 1)[1]
    await message.chat.set_title(new_title)
    await message.reply_text(
        f"Successfully Changed Group Title From `{old_title}` To `{new_title}`"
    )


@app.on_message(filters.command("title") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def set_user_title(_, message):
    try:
        await message.delete()
    except:
        pass
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to user's message to set his admin title"
        )
    if not message.reply_to_message.from_user:
        return await message.reply_text(
            "I can't change admin title of an unknown entity"
        )
    chat_id = message.chat.id
    from_user = message.reply_to_message.from_user
    if len(message.command) < 2:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n/title NEW ADMIN")
    title = message.text.split(None, 1)[1]
    await app.set_administrator_title(chat_id, from_user.id, title)
    await message.reply_text(
        f"Successfully Changed {from_user.mention}'s Admin Title To `{title}`"
    )


@app.on_message(filters.command("setphoto") & ~filters.private & ~BANNED_USERS)
@adminsOnly("can_change_info")
async def set_chat_photo(_, message):
    try:
        await message.delete()
    except:
        pass
    reply = message.reply_to_message
    if not reply:
        return await message.reply_text("Reply to a photo to set it as chat_photo")
    file = reply.document or reply.photo
    if not file:
        return await message.reply_text(
            "Reply to a photo or document to set it as chat_photo"
        )
    if file.file_size > 5000000:
        return await message.reply("File size too large.")
    photo = await reply.download()
    await message.chat.set_photo(photo)
    await message.reply_text("Successfully Changed Group Photo ...")
    os.remove(photo)
