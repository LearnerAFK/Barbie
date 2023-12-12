from typing import Union
from pyrogram.types import InlineKeyboardButton


def setting_markup():
    buttons = [
        [
            InlineKeyboardButton(text="ᴘʟᴀʏ ᴍᴏᴅᴇ", callback_data="PM"),
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴇᴀɴ ᴍᴏᴅᴇ", callback_data="CM"),
        ],
        [
            InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close"),
        ],
    ]
    return buttons


def cmd_del_markup(
    dels: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴄᴏᴍᴍᴀɴᴅ ᴄʟᴇᴀɴ", 
                callback_data="COMMANDANSWER",
            ),
            InlineKeyboardButton(
                text="✅ ᴇɴᴀʙʟᴇᴅ" if dels == True else "❌ ᴅɪsᴀʙʟᴇᴅ",
                callback_data="COMMANDELMODE",
            ),
        ],
        [
            InlineKeyboardButton(
                text="ʙᴀᴄᴋ",
                callback_data="settingsback_helper",
            ),
            InlineKeyboardButton(
                text="ᴄʟᴏsᴇ", 
                callback_data="close",
            ),
        ],
    ]
    return buttons


def playmode_users_markup(
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(
                text="sᴇᴀʀᴄʜ ᴍᴏᴅᴇ", 
                callback_data="SEARCHANSWER"),
            InlineKeyboardButton(
                text="✅ ᴅɪʀᴇᴄᴛ" if Direct == True else "✅ ɪɴʟɪɴᴇ",
                callback_data="MODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴘʟᴀʏ ᴍᴏᴅᴇ", 
                callback_data="AUTHANSWER",
            ),
            InlineKeyboardButton(
                text="✅ ᴀᴅᴍɪɴs" if Group == True else "✅ ᴇᴠᴇʀʏᴏɴᴇ",
                callback_data="CHANNELMODECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(
                text="ᴘʟᴀʏ ᴛʏᴘᴇ", 
                callback_data="PLAYTYPEANSWER",
            ),
            InlineKeyboardButton(
                text="✅ ᴀᴅᴍɪɴs" if Playtype == True else "✅ ᴇᴠᴇʀʏᴏɴᴇ",
                callback_data="PLAYTYPECHANGE",
            ),
        ],
        [
            InlineKeyboardButton(
                text="ʙᴀᴄᴋ",
                callback_data="settingsback_helper",
            ),
            InlineKeyboardButton(
                text="ᴄʟᴏsᴇ", 
                callback_data="close",
            ),
        ],
    ]
    return buttons
