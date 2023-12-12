from pyrogram.types import InlineKeyboardButton
from Barbie import app


def private_help_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="ʜᴇʟᴘ ᴍᴇɴᴜ", url=f"https://t.me/{app.username}?start=help"
            )
        ]
    ]
    return buttons


def served_panel():
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴠᴇʀɪғʏ ʏᴏᴜʀsᴇʟғ", url=f"https://t.me/{app.username}?start"
            )
        ]
    ]
    return buttons
