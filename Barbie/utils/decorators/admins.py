from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import adminlist
from ..formatters import int_to_alpha
from Barbie import app
from ...misc import SUDOERS
from ..database import (
    get_authuser_names,
    is_active_chat,
    is_commanddelete_on,
    is_nonadmin_chat,
)


def AdminRightsCheck(mystic):
    async def wrapper(client, message):
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass

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
            
        if not await is_active_chat(message.chat.id):
            return await message.reply_text("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ...")

        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin:
            if message.from_user.id not in SUDOERS:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    print("Admin List Not Found ...")
                else:
                    if message.from_user.id not in admins:
                        return await message.reply_text("ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ...")
        return await mystic(client, message, message.chat.id)
    return wrapper


def AdminActual(mystic):
    async def wrapper(client, message):
        if await is_commanddelete_on(message.chat.id):
            try:
                await message.delete()
            except:
                pass

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

        if message.from_user.id not in SUDOERS:
            try:
                member = await app.get_chat_member(
                    message.chat.id, message.from_user.id
                )
                if not member.status == ChatMemberStatus.ADMINISTRATOR:
                    return await message.reply(
                        "ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ ..."
                    )
            except Exception as e:
                return await message.reply(f"ERROR : {str(e)}")
        return await mystic(client, message)
    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery)

        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            try:
                a = await app.get_chat_member(
                    CallbackQuery.message.chat.id,
                    CallbackQuery.from_user.id,
                )
                if not a.status == ChatMemberStatus.ADMINISTRATOR:
                    if CallbackQuery.from_user.id not in SUDOERS:
                        token = await int_to_alpha(CallbackQuery.from_user.id)
                        _check = await get_authuser_names(CallbackQuery.from_user.id)
                        if token not in _check:
                            return await CallbackQuery.answer(
                                "ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴍᴀɴᴀɢᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ʀɪɢʜᴛs ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ ...",
                                show_alert=True,
                            )
                elif a is None:
                    return await CallbackQuery.answer("ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴀ ᴍᴇᴍʙᴇʀ ᴏғ ᴛʜɪs ᴄʜᴀᴛ ...")
            except Exception as e:
                return await CallbackQuery.answer(f"ERROR : {str(e)}")
        return await mystic(client, CallbackQuery)
    return wrapper
