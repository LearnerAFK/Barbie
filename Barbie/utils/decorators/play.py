from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import adminlist, EXTRA_IMG
from Barbie import YouTube
from ...misc import SUDOERS
from ..inline.play import botplaylist_markup
from ..database import (
    get_playmode,
    get_playtype,
    is_active_chat,
    is_commanddelete_on,
)


def PlayWrapper(command):
    async def wrapper(client, message):
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass

        audio_telegram = (
            (message.reply_to_message.audio or message.reply_to_message.voice)
            if message.reply_to_message
            else None
        )
        video_telegram = (
            (message.reply_to_message.video or message.reply_to_message.document)
            if message.reply_to_message
            else None
        )
        url = await YouTube.url(message)

        if audio_telegram is None and video_telegram is None and url is None:
            if len(message.command) < 2:
                if "stream" in message.command:
                    return await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴍ𝟹ᴜ𝟾 ʟɪɴᴋs ᴏʀ ɪɴᴅᴇx ʟɪɴᴋs ...")
                buttons = botplaylist_markup()
                return await message.reply_photo(
                    photo=EXTRA_IMG,
                    caption="**ᴜsᴀɢᴇ:** /play [ᴍᴜsɪᴄ ɴᴀᴍᴇ ᴏʀ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀᴜᴅɪᴏ]",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )

        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ",
                            callback_data="AnonymousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(
                "ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ ɪɴ ᴛʜɪs ᴄʜᴀᴛ ɢʀᴏᴜᴘ !", 
                reply_markup=upl
            )

        chat_id = message.chat.id

        playmode = await get_playmode(message.chat.id)
        playty = await get_playtype(message.chat.id)
        if playty != "Everyone":
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return 
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text(
                            "**ᴀᴅᴍɪɴs ᴏɴʟʏ ᴘʟᴀʏ**\n\nᴏɴʟʏ ᴀᴅᴍɪɴs ᴀɴᴅ ᴀᴜᴛʜ ᴜsᴇʀs ᴄᴀɴ ᴘʟᴀʏ ᴍᴜsɪᴄ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ ...\n\nᴄʜᴀɴɢᴇ ᴍᴏᴅᴇ ᴠɪᴀ /playmode "
                        )

        if message.command[0][0] == "v":
            video = True
        else:
            if "-v" in message.text:
                video = True
            else:
                video = True if message.command[0][1] == "v" else None

        if message.command[0][-1] == "e":
            if not await is_active_chat(chat_id):
                return await message.reply_text(
                    "**ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ғᴏᴜɴᴅ**\n\nᴛᴏ ᴜsᴇ ғᴏʀᴄᴇ ᴘʟᴀʏ, ᴛʜᴇʀᴇ ᴍᴜsᴛ ʙᴇ ᴀɴ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ..."
                )
            fplay = True
        else:
            fplay = None
        return await command(
            client,
            message,
            chat_id,
            video,
            playmode,
            url,
            fplay,
        )

    return wrapper
