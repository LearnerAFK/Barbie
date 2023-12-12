from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def botplaylist_markup():
    buttons = [
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ],
    ]
    return buttons


def stream_markup(videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="sᴋɪᴘ ᴄᴜʀʀᴇɴᴛ sᴏɴɢ", callback_data=f"ADMIN Skip|{chat_id}")
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ],
    ]
    return buttons


def telegram_markup(chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
        ],
    ]
    return buttons


def track_markup(videoid, user_id, fplay):
    buttons = [
        [
            InlineKeyboardButton(text="ᴀᴜᴅɪᴏ", callback_data=f"MusicStream {videoid}|{user_id}|a|{fplay}"),
        ],
        [
            InlineKeyboardButton(text="ᴠɪᴅᴇᴏ", callback_data=f"MusicStream {videoid}|{user_id}|v|{fplay}"),
        ],
    ]
    return buttons


def livestream_markup(videoid, user_id, mode, fplay):
    buttons = [
        [
            InlineKeyboardButton(text="ʟɪᴠᴇ sᴛʀᴇᴀᴍ", callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{fplay}"),
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"forceclose {videoid}|{user_id}"),
        ],
    ]
    return buttons


def slider_markup(videoid, user_id, query, query_type, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(text="ᴀᴜᴅɪᴏ", callback_data=f"MusicStream {videoid}|{user_id}|a|{fplay}"),
        ],
        [
            InlineKeyboardButton(text="ᴠɪᴅᴇᴏ", callback_data=f"MusicStream {videoid}|{user_id}|v|{fplay}")
        ],
        [
            InlineKeyboardButton(text="◁", callback_data=f"slider B|{query_type}|{query}|{user_id}|{fplay}"),
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data=f"forceclose {query}|{user_id}"),
            InlineKeyboardButton(text="▷", callback_data=f"slider F|{query_type}|{query}|{user_id}|{fplay}")
        ],
    ]
    return buttons


close_keyboard = InlineKeyboardMarkup( 
            [
                [
                    InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close")
                ]    
            ]
        )

