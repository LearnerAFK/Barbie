from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..core.call import CallMusic
from ..utils import set_loop, close_keyboard, AdminRightsCheck


@app.on_message(filters.command(["stop", "end"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def stop_music(_, message: Message, chat_id):
    if not len(message.command) == 1:
        return await message.reply_text("ᴇʀʀᴏʀ ᴡʀᴏɴɢ ᴜsᴀɢᴇ ᴏғ ᴄᴏᴍᴍᴀɴᴅ ...")
    await CallMusic.stop_stream(chat_id)
    await set_loop(chat_id, 0)
    await message.reply_text(
        text="**sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ** ʙʏ : {} ...".format(message.from_user.mention),
        reply_markup=close_keyboard,
    )
