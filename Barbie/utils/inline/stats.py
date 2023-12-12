from Barbie import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def overallback_stats_markup():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="GlobalStats"),
            ]
        ]
    )
    return upl


def get_stats_markup(status):
    not_sudo = [InlineKeyboardButton(text="ᴄʟᴏsᴇ ᴍᴇɴᴜ", callback_data="close")]
    sudo = [
        InlineKeyboardButton(text="ʙᴏᴛ sᴛᴀᴛs", callback_data="bot_stats_sudo g"),
        InlineKeyboardButton(text="ᴄʟᴏsᴇ ᴍᴇɴᴜ", callback_data="close"),
    ]
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ᴜsᴇʀ sᴛᴀᴛs",
                    url=f"https://t.me/{app.username}?start=stats",
                )
            ],
            [
                InlineKeyboardButton(
                    text="ᴏᴠᴇʀᴀʟʟ sᴛᴀᴛs", 
                    callback_data="TopOverall g",
                )
            ],
            sudo if status else not_sudo,
        ]
    )
    return upl


def stats_buttons(status):
    not_sudo = [
        InlineKeyboardButton(text="ᴏᴠᴇʀᴀʟʟ sᴛᴀᴛs", callback_data="TopOverall s")
    ]
    sudo = [
        InlineKeyboardButton(text="ʙᴏᴛ sᴛᴀᴛs", callback_data="bot_stats_sudo s"),
        InlineKeyboardButton(text="ᴏᴠᴇʀᴀʟʟ sᴛᴀᴛs", callback_data="TopOverall s"),
    ]
    upl = InlineKeyboardMarkup(
        [
            sudo if status else not_sudo,
            [InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")],
        ]
    )
    return upl


def back_stats_buttons():
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="GETSTATS"),
                InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close"),
            ]
        ]
    )
    return upl
