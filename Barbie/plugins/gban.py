import asyncio
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from Barbie import app
from ..misc import SUDOERS
from ..utils import (
    get_readable_time,
    add_banned_user,
    get_banned_count,
    get_banned_users,
    get_served_chats,
    is_banned_user,
    remove_banned_user,
)


__MODULE__ = "G-ʙᴀɴ"
__HELP__ = """
/gban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ʙᴀɴs ᴛʜᴇ ᴜsᴇʀ ғʀᴏᴍ ᴀʟʟ ᴛʜᴇ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴀɴᴅ ʙʟᴀᴄᴋʟɪsᴛ ʜɪᴍ/ʜᴇʀ ғʀᴏᴍ ᴜsɪɴɢ ᴛʜᴇ ʙᴏᴛ.

/ungban [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ɢʟᴏʙᴀʟʟʏ ᴜɴʙᴀɴs ᴛʜᴇ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇᴅ ᴜsᴇʀ.

/gbanlist : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ɢʟᴏʙᴀʟʟʏ ʙᴀɴɴᴇʀ ᴜsᴇʀs.
"""


@app.on_message(filters.command(["gban"]) & SUDOERS)
async def gbannuser(_, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.mention
    else:
        if len(message.command) != 2:
            return await message.reply_text(
                "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ"
            )
        user = message.text.split(None, 1)[1]
        user = await app.get_users(user)
        user_id = user.id
        mention = user.mention

    if user_id == message.from_user.id:
        return await message.reply_text("ʏᴏᴜ ᴄᴀɴ'ᴛ ɢʙᴀɴ ʏᴏᴜʀsᴇʟғ !")
    elif user_id == app.id:
        return await message.reply_text("ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ɢʙᴀɴ ᴍʏsᴇʟғ ? ʟᴏʟ.")
    elif user_id in SUDOERS:
        return await message.reply_text("ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢʙᴀɴ ᴍʏ ꜱᴜᴅᴏ ᴜꜱᴇʀ ?")
    is_gbanned = await is_banned_user(user_id)
    if is_gbanned:
        return await message.reply_text(
            "{0} ɪs ᴀʟʀᴇᴀᴅʏ **ɢʙᴀɴɴᴇᴅ** ғʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.".format(mention)
        )
    if user_id not in BANNED_USERS:
        BANNED_USERS.add(user_id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = len(served_chats)
    time_expected = get_readable_time(time_expected)
    mystic = await message.reply_text(
        "**ɢʟᴏʙᴀʟ ʙᴀɴɴɪɴɢ {0}**\n\nᴇxᴩᴇᴄᴛᴇᴅ ᴛɪᴍᴇ : {1}.".format(mention, time_expected)
    )
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.ban_chat_member(chat_id, user_id)
            number_of_chats += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    await add_banned_user(user_id)
    await message.reply_text(
        "**ɢʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ**\n\nʙᴀɴɴᴇᴅ **{0}** ғʀᴏᴍ **{1}** ᴄʜᴀᴛs.".format(
            mention, number_of_chats
        )
    )
    await mystic.delete()


@app.on_message(filters.command(["ungban"]) & SUDOERS)
async def ungbannuser(_, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        mention = message.reply_to_message.from_user.mention
    else:
        if len(message.command) != 2:
            return await message.reply_text(
                "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ"
            )
        user = message.text.split(None, 1)[1]
        user = await app.get_users(user)
        user_id = user.id
        mention = user.mention
    is_gbanned = await is_banned_user(user_id)
    if not is_gbanned:
        return await message.reply_text(
            "{0} ɪꜱ ɴᴏᴛ **ɢʙᴀɴɴᴇᴅ** ʏᴇᴛ ꜰʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.".format(mention)
        )
    if user_id in BANNED_USERS:
        BANNED_USERS.remove(user_id)
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = len(served_chats)
    time_expected = get_readable_time(time_expected)
    mystic = await message.reply_text(
        "**ᴜɴɢʙᴀɴɴɪɴɢ {0}**\n\nᴇxᴩᴇᴄᴛᴇᴅ ᴛɪᴍᴇ : {1}.".format(mention, time_expected)
    )
    number_of_chats = 0
    for chat_id in served_chats:
        try:
            await app.unban_chat_member(chat_id, user_id)
            number_of_chats += 1
        except FloodWait as e:
            await asyncio.sleep(int(e.value))
        except Exception:
            pass
    await remove_banned_user(user_id)
    await message.reply_text(
        "**ᴜɴɢʙᴀɴɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ**\n\nᴜɴʙᴀɴɴᴇᴅ **{0}** ɪɴ **{1}** ᴄʜᴀᴛs.".format(
            mention, number_of_chats
        )
    )
    await mystic.delete()


@app.on_message(filters.command(["gbanlist"]) & SUDOERS)
async def gbanned_list(_, message: Message):
    counts = await get_banned_count()
    if counts == 0:
        return await message.reply_text("ɴᴏ ᴏɴᴇ ɪs ɢʙᴀɴɴᴇᴅ.")
    mystic = await message.reply_text("ɴᴏ ᴏɴᴇ ɪs ɢʙᴀɴɴᴇᴅ.")
    msg = "ɢʙᴀɴɴᴇᴅ ᴜsᴇʀs :\n\n"
    count = 0
    users = await get_banned_users()
    for user_id in users:
        count += 1
        try:
            user = await app.get_users(user_id)
            user = user.first_name if not user.mention else user.mention
            msg += f"{count}➤ {user}\n"
        except Exception:
            msg += f"{count}➤ [ᴜɴᴋɴᴏᴡɴ ᴜsᴇʀ]{user_id}\n"
            continue
    if count == 0:
        return await mystic.edit_text("ɴᴏ ᴏɴᴇ ɪs ɢʙᴀɴɴᴇᴅ.")
    else:
        return await mystic.edit_text(msg)
