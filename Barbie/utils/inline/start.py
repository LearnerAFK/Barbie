from config import SUPPORT_CHANNEL
from Barbie import app
from pyrogram.types import InlineKeyboardButton


def start_pannel():
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕", url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users"
            )
        ],
        [
            InlineKeyboardButton(
                text="sᴇᴛᴛɪɴɢ", callback_data="settings_helper"
            )
        ],
        [
            InlineKeyboardButton(
                text="ʜᴇʟᴘ ᴍᴇɴᴜ", url=f"https://t.me/{app.username}?start=help"
            )
        ],
    ]
    return buttons


def private_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ➕",
                url=f"https://t.me/{app.username}?startgroup=s&admin=delete_messages+manage_video_chats+pin_messages+invite_users",
            )
        ],
        [
            InlineKeyboardButton(text="ʜᴇʟᴘ ᴍᴇɴᴜ", callback_data="home_help"),
        ],
        [
            InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇꜱ", url=f"{SUPPORT_CHANNEL}"),
        ],
    ]
    return buttons
