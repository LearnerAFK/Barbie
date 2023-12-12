from config import LOG_GROUP_ID, BANNED_USERS
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from Barbie import app
from ..utils import add_served_chat, blacklisted_chats, get_assistant, start_pannel


@app.on_message(filters.new_chat_members & ~BANNED_USERS, group=13)
async def welcome_Barbie(c, message: Message):
    chat_id = message.chat.id
    await add_served_chat(chat_id)
    if app.id in [user.id for user in message.new_chat_members]:
        if chat_id in await blacklisted_chats():
            await message.reply_text(
                "**ʙʟᴀᴄᴋʟɪsᴛᴇᴅ ᴄʜᴀᴛ**\n\nᴛʜɪs ᴄʜᴀᴛ ɪs ʙʟᴀᴄᴋʟɪsᴛ ғᴏʀ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ. ʀᴇǫᴜᴇsᴛ ᴀ sᴜᴅᴏ ᴜsᴇʀ ᴛᴏ ᴡʜɪᴛᴇʟɪsᴛ ʏᴏᴜʀ ᴄʜᴀᴛ sᴜᴅᴏ ᴜsᴇʀs [ʟɪsᴛ]({0}).".format(
                    f"https://t.me/{app.username}?start=sudolist"
                )
            )
            return await app.leave_chat(chat_id)
        userbot = await get_assistant(message.chat.id)
        out = start_pannel()
        await message.reply_text(
            "Hᴇʏ ᴛʜɪs ɪs {0}\nᴀ ғᴀsᴛ ᴀɴᴅ ᴩᴏᴡᴇʀғᴜʟ ᴍᴜsɪᴄ ᴩʟᴀʏᴇʀ ʙᴏᴛ ᴡɪᴛʜ sᴏᴍᴇ ᴀᴡᴇsᴏᴍᴇ ғᴇᴀᴛᴜʀᴇs ...\n๏ ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀɴᴀᴍᴇ :- @{1}\n๏ ᴀssɪsᴛᴀɴᴛ ɪᴅ :- {2}".format(
                app.mention, userbot.username, userbot.id
            ),
            reply_markup=InlineKeyboardMarkup(out),
        )
        add_m = message.from_user.mention if message.from_user else "ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ"
        add_id = message.from_user.username if message.from_user else "None"
        title = message.chat.title
        uname = f"@{message.chat.username}" if message.chat.username else "ᴩʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ"
        chat_id = message.chat.id
        new = f"**✫** <b><u>ɴᴇᴡ ɢʀᴏᴜᴘ</u></b> **:**\n\n**ᴄʜᴀᴛ ɪᴅ :** {chat_id}\n**ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :** {uname}\n**ᴄʜᴀᴛ Tɪᴛʟᴇ :** {title}\n\n**ᴀᴅᴅᴇᴅ ʙʏ :** {add_m}\n**ᴀᴅᴅᴇᴅ ʙʏ :** @{add_id}"
        chat = await app.get_chat(chat_id)
        try:
            link = chat.invite_link
            if not link:
                link = await app.export_chat_invite_link(chat_id)
        except:
            return
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Group Link", url=f"{link}")
                ]
            ]
        )
        await app.send_message(LOG_GROUP_ID, new, reply_markup=keyboard)
