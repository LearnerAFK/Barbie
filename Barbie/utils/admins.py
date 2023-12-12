from pyrogram.enums import ChatMembersFilter
from Barbie import app
from config import OWNER_ID
from pyrogram.types import Message
from functools import wraps
from traceback import format_exc as err
from pyrogram.errors import ChatWriteForbidden, ChatAdminRequired


admins_in_chat = {}



async def list_admins(chat_id: int):
    global admins_in_chat
    try:
        admins = []
        async for m in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        ):
            admins.append(m)
        admins_in_chat[chat_id] = []
        for user in admins:
            admins_in_chat[chat_id].append(user.user.id)
            return admins_in_chat
    except Exception as e:
        print(f"[ERROR] : {e}")
        
        
@app.on_message(group=19) 
async def admin_cache(_, m: Message):
    chat_id = m.chat.id
    await list_admins(chat_id)


async def member_permissions(chat_id: int, user_id: int):
    try:
        perms = []
        member = (await app.get_chat_member(chat_id, user_id)).privileges
        if not member:
            return []
        if member.can_post_messages:
            perms.append("can_post_messages")
        if member.can_edit_messages:
            perms.append("can_edit_messages")
        if member.can_delete_messages:
            perms.append("can_delete_messages")
        if member.can_restrict_members:
            perms.append("can_restrict_members")
        if member.can_promote_members:
            perms.append("can_promote_members")
        if member.can_change_info:
            perms.append("can_change_info")
        if member.can_invite_users:
            perms.append("can_invite_users")
        if member.can_pin_messages:
            perms.append("can_pin_messages")
        if member.can_manage_video_chats:
            perms.append("can_manage_video_chats")
        return perms
    except AttributeError:
        pass
    except ChatAdminRequired:
        print("[ERROR] : Chat Admin Required !")


async def authorised(func, subFunc2, client, message, *args, **kwargs):
    chatID = message.chat.id
    try:
        await func(client, message, *args, **kwargs)
    except ChatWriteForbidden:
        await app.leave_chat(chatID)
    except Exception as e:
        try:
            await message.reply_text(str(e.MESSAGE))
        except AttributeError:
            await message.reply_text(str(e))
        e = err()
        print(str(e))
    return subFunc2


async def unauthorised(message: Message, permission, subFunc2):
    chatID = message.chat.id
    text = f"ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀᴇǫᴜɪʀᴇᴅ ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ᴘᴇʀғᴏʀᴍ ᴛʜɪs ᴀᴄᴛɪᴏɴ\n**ᴘᴇʀᴍɪssɪᴏɴ :** `{permission}`"
    try:
        await message.reply_text(text)
    except ChatWriteForbidden:
        await app.leave_chat(chatID)
    return subFunc2


def adminsOnly(permission):
    def subFunc(func):
        @wraps(func)
        async def subFunc(client, message: Message, *args, **kwargs):
            chatID = message.chat.id
            if not message.from_user:
                if message.sender_chat and message.sender_chat.id == message.chat.id:
                    return await authorised(
                        func, subFunc, client, message, *args, **kwargs
                    )
                return await unauthorised(message, permission, subFunc)
            userID = message.from_user.id
            permissions = await member_permissions(chatID, userID)
            if userID not in OWNER_ID and permission not in permissions:
                return await unauthorised(message, permission, subFunc)
            return await authorised(func, subFunc, client, message, *args, **kwargs)

        return subFunc

    return subFunc


def ownerOnly(permission):
    def subFun(func):
        @wraps(func)
        async def subFunc2(client, message: Message, *args, **kwargs):
            chatID = message.chat.id
            if not message.from_user:
                if message.sender_chat and message.sender_chat.id == message.chat.id:
                    return await authorised(
                        func, subFunc2, client, message, *args, **kwargs
                    )
                return await unauthorised(message, permission, subFunc2)
            userID = message.from_user.id
            permissions = await member_permissions(chatID, userID)
            if userID not in OWNER_ID and permission not in permissions:
                return await unauthorised(message, permission, subFunc2)
            return await authorised(func, subFunc2, client, message, *args, **kwargs)

        return subFunc2

    return subFun
