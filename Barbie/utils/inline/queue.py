from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def queue_markup(qek, videoid):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="📑 Qᴜᴇᴜᴇᴅ", callback_data=f"GetQueued {qek}|{videoid}"
                ),
                InlineKeyboardButton(
                    text="ᴄʟᴏsᴇ", callback_data="close"
                ),
            ]
        ]
    )
    return upl


def queue_back_markup(qek):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="ʙᴀᴄᴋ", callback_data=f"queue_back_timer {qek}"
                ),
                InlineKeyboardButton(
                    text="ᴄʟᴏsᴇ", callback_data="close"
                ),
            ]
        ]
    )
    return upl
