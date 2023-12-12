from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..misc import SUDOERS
from ..utils.database import (
    get_active_chats,
    get_active_video_chats,
    remove_active_chat,
    remove_active_video_chat,
)


__MODULE__ = "Aᴄᴛɪᴠᴇ"
__HELP__ = """
/activevoice : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇᴄʜᴀᴛs ᴏɴ ᴛʜᴇ ʙᴏᴛ.

/activevideo : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏᴄʜᴀᴛs ᴏɴ ᴛʜᴇ ʙᴏᴛ.

/activechats : ɢᴇᴛ ꜱᴛᴀᴛꜱ ᴏꜰ ᴀᴄᴛɪᴠᴇ ᴄʜᴀᴛꜱ.

/autoend [ᴇɴᴀʙʟᴇ|ᴅɪsᴀʙʟᴇ] : ᴇɴᴀʙʟᴇ sᴛʀᴇᴀᴍ ᴀᴜᴛᴏ ᴇɴᴅ ɪғ ɴᴏ ᴏɴᴇ ɪs ʟɪsᴛᴇɴɪɴɢ.
"""


@app.on_message(filters.command(["aa", "activevoice"]) & SUDOERS)
async def activevc(bot: app, message: Message):
    try:
        await message.delete()
    except:
        pass
    mystic = await message.reply_text("» ɢᴇᴛᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ʟɪsᴛ...")
    served_chats = await get_active_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await bot.get_chat(x)).title
        except:
            await remove_active_chat(x)
            continue
        try:
            if (await bot.get_chat(x)).username:
                user = (await bot.get_chat(x)).username
                text += f"<b>{j + 1}.</b> <a href=https://t.me/{user}>{title}</a> [<code>{x}</code>]\n"
            else:
                text += f"<b>{j + 1}.</b> {title} [<code>{x}</code>]\n"
            j += 1
        except:
            continue
    if not text:
        await mystic.edit_text(f"» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs ᴏɴ {bot.mention} !")
    else:
        await mystic.edit_text(
            f"<b>» ʟɪsᴛ ᴏғ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛs :</b>\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["av", "activevideo"]) & SUDOERS)
async def activevi_(bot: app, message: Message):
    try:
        await message.delete()
    except:
        pass
    mystic = await message.reply_text("» ɢᴇᴛᴛɪɴɢ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs ʟɪsᴛ...")
    served_chats = await get_active_video_chats()
    text = ""
    j = 0
    for x in served_chats:
        try:
            title = (await bot.get_chat(x)).title
        except:
            await remove_active_video_chat(x)
            continue
        try:
            if (await bot.get_chat(x)).username:
                user = (await bot.get_chat(x)).username
                text += f"<b>{j + 1}.</b> <a href=https://t.me/{user}>{title}</a> [<code>{x}</code>]\n"
            else:
                text += f"<b>{j + 1}.</b> {title} [<code>{x}</code>]\n"
            j += 1
        except:
            continue
    if not text:
        await mystic.edit_text(f"» ɴᴏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs ᴏɴ {bot.mention} !")
    else:
        await mystic.edit_text(
            f"<b>» ʟɪsᴛ ᴏғ ᴄᴜʀʀᴇɴᴛʟʏ ᴀᴄᴛɪᴠᴇ ᴠɪᴅᴇᴏ ᴄʜᴀᴛs :</b>\n\n{text}",
            disable_web_page_preview=True,
        )


@app.on_message(filters.command(["activechats", "ac"]) & SUDOERS)
async def littleac(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    ac_audio = str(len(await get_active_chats()))
    ac_video = str(len(await get_active_video_chats()))
    await message.reply_text(
        """
• ʙᴏᴛ ᴀᴄᴛɪᴠᴇ ᴄʜᴀᴛs ɪɴғᴏ •
•━━━━━━━━━━━━━━━━━━•
🎧 ᴀᴜᴅɪᴏ 🎧 » {0} ᴀᴄᴛɪᴠᴇ
•───────•
🎥 ᴠɪᴅᴇᴏ 🎥 » {1} ᴀᴄᴛɪᴠᴇ
•──────•
""".format(ac_audio, ac_video), quote=True)
