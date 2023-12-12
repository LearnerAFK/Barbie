import asyncio
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pyrogram.types import CallbackQuery, Message
from config import BANNED_USERS, lyrical, adminlist
from Barbie import app
from ..misc import db
from ..core.call import CallMusic
from ..utils import (
    get_authuser_names,
    ActualAdminCB,
    AdminRightsCheck,
    alpha_to_int,
)


@app.on_message(filters.group , group=45)
async def reload_admin_cache(_, message: Message):
    try:
        chat_id = message.chat.id
        admins = []
        async for m in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            admins.append(m)
        authusers = await get_authuser_names(chat_id)
        adminlist[chat_id] = []
        for user in admins:
            if user.privileges.can_manage_video_chats:
                adminlist[chat_id].append(user.user.id)
        for user in authusers:
            user_id = await alpha_to_int(user)
            adminlist[chat_id].append(user_id)
    except Exception as e:
        print(f"[ERROR] : {e}")


@app.on_message(filters.command(["restart"]) & filters.group & ~BANNED_USERS)
@AdminRightsCheck
async def restartbot(_, message: Message):
    chat_id = message.chat.id
    mystic = await message.reply_text(
        f"ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ ʀᴇʙᴏᴏᴛɪɴɢ {app.mention} ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ ..."
    )
    await asyncio.sleep(1)
    try:
        db[chat_id] = []
        await CallMusic.stop_stream(chat_id)
    except:
        pass
    return await mystic.edit_text(
        f"sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇʙᴏᴏᴛᴇᴅ {app.mention} ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ ɴᴏᴡ ʏᴏᴜ ᴄᴀɴ sᴛᴀʀᴛ ᴩʟᴀʏɪɴɢ ᴀɢᴀɪɴ ..."
    )


@app.on_callback_query(filters.regex("stop_downloading") & ~BANNED_USERS)
@ActualAdminCB
async def stop_download(_, CallbackQuery: CallbackQuery):
    message_id = CallbackQuery.message.id
    task = lyrical.get(message_id)

    if not task:
        return await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ...", show_alert=True)
    
    if task.done() or task.cancelled():
        return await CallbackQuery.answer(
            "ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴀʟʀᴇᴀᴅʏ ᴄᴏᴍᴩʟᴇᴛᴇᴅ ᴏʀ ᴄᴀɴᴄᴇʟʟᴇᴅ ...", 
            show_alert=True,
        )

    if not task.done():
        try:
            task.cancel()
            try:
                lyrical.pop(message_id)
            except:
                pass
            await CallbackQuery.answer("ᴅᴏᴡɴʟᴏᴀᴅɪɢ ᴄᴀɴᴄᴇʟʟᴇᴅ ...", show_alert=True)
            return await CallbackQuery.edit_message_text(
                f"ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ᴩʀᴏᴄᴇss ᴄᴀɴᴄᴇʟʟᴇᴅ ʙʏ {CallbackQuery.from_user.mention}"
            )
        except:
            return await CallbackQuery.answer("ғᴀɪʟᴇᴅ ᴛᴏ ᴄᴀɴᴄᴇʟ ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ...", show_alert=True)
    await CallbackQuery.answer("ғᴀɪʟᴇᴅ ᴛᴏ ʀᴇᴄᴏɢɴɪᴢᴇ ᴛʜᴇ ᴏɴɢᴏɪɴɢ ᴛᴀsᴋ ...", show_alert=True)
