from config import BANNED_USERS, START_IMG
from Barbie import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message


def post_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕",
                url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users",
            )
        ]
    ]
    return buttons


@app.on_message(filters.command(["p", "post"]) & (filters.channel | filters.group) & ~BANNED_USERS)
async def help_cmd(_, msg: Message):
    try:
        await msg.delete()
    except:
        pass
    key = post_panel()
    await msg.reply_photo(
        photo=START_IMG,
        caption=f"""
ᴍᴏsᴛ ᴀᴅᴠᴀɴᴄᴇᴅ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ᴀɴᴅ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ ғᴏʀ ᴛᴇʟᴇɢʀᴀᴍ ɢʀᴏᴜᴘ ᴀɴᴅ ᴄʜᴀɴɴᴇʟ ᴠɪᴅᴇᴏᴄʜᴀᴛs... ✨

‣ 𝟸𝟺x𝟽 ᴜᴘᴛɪᴍᴇ 
‣ ᴍᴜsɪᴄ ʙᴏᴛ ғᴇᴀᴛᴜʀᴇs
‣ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ ғᴇᴀᴛᴜʀᴇs
‣ ɪᴛ's sᴇᴄᴜʀᴇ ᴀɴᴅ sᴀғᴇ

ᴀᴅᴅ ᴍᴇ » **{app.mention}**""",
        reply_markup=InlineKeyboardMarkup(key),
    )
