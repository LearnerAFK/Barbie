from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..core.call import CallMusic
from ..utils import close_keyboard, AdminRightsCheck, is_music_playing, music_on


@app.on_message(filters.command(["resume"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def resume_com(_, message: Message, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("ᴇʀʀᴏʀ ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏғ ᴄᴏᴍᴍᴀɴᴅ ...")
    if await is_music_playing(chat_id):
        return await message.reply_text("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ ...")
    await music_on(chat_id)
    await CallMusic.resume_stream(chat_id)
    await message.reply_text(
        "**sᴛʀᴇᴀᴍ ʀᴇsᴜᴍᴇᴅ** ʙʏ : {} ...".format(message.from_user.mention),
        reply_markup=close_keyboard,
    )
