from config import LOG_GROUP_ID
from Barbie import app
from .database import is_on_off
from pyrogram.enums import ParseMode


async def play_logs(message, streamtype):
    if await is_on_off(2):
        try:
            link = await app.export_chat_invite_link(message.chat.id)
        except:
            return
        logger_text = f"""
<b><u>{app.mention} ᴘʟᴀʏ ʟᴏɢ</u></b>

<b>ᴄʜᴀᴛ ɪᴅ :</b> <code>{message.chat.id}</code>
<b>ᴄʜᴀᴛ ɴᴀᴍᴇ :</b> <code>{message.chat.title}</code>
<b>ᴄʜᴀᴛ ʟɪɴᴋ :</b> <a href={link}>[ᴄʜᴀᴛ ʟɪɴᴋ]</a>
<b>ᴄʜᴀᴛ ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.chat.username}

<b>ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>
<b>ɴᴀᴍᴇ :</b> {message.from_user.mention}
<b>ᴜsᴇʀɴᴀᴍᴇ :</b> @{message.from_user.username}

<b>ǫᴜᴇʀʏ :</b> <code>{message.text.split(None, 1)[1]}</code>
<b>sᴛʀᴇᴀᴍᴛʏᴘᴇ :</b> <code>{streamtype}</code>"""
        if message.chat.id != LOG_GROUP_ID:
            try:
                await app.send_message(
                    chat_id=LOG_GROUP_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return
