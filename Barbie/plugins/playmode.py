from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup
from Barbie import app
from ..utils import playmode_users_markup, get_playmode, get_playtype, is_nonadmin_chat


@app.on_message(filters.command(["playmode", "mode"]) & filters.group & ~BANNED_USERS)
async def bot_play_mode(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    playmode = await get_playmode(message.chat.id)
    Direct = True if playmode == "Direct" else None

    is_non_admin = await is_nonadmin_chat(message.chat.id)
    Group = None if is_non_admin else True

    playty = await get_playtype(message.chat.id)
    Playtype = None if playty == "Everyone" else True
    buttons = playmode_users_markup(Direct, Group, Playtype)
    await message.reply_text(
        text="sᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴏᴅᴇ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ ᴛʜᴇ ǫᴜᴇʀɪᴇs ɪɴsɪᴅᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ [{0}] :".format(
            message.chat.title
        ),
        reply_markup=InlineKeyboardMarkup(buttons),
    )
