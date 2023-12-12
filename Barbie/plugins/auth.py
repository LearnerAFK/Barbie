from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..utils import (
    extract_user,
    int_to_alpha,
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
    AdminActual,
    close_keyboard,
)
from config import BANNED_USERS, adminlist


__MODULE__ = "Aᴜᴛʜ"
__HELP__ = """
/auth [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴀᴅᴅ ᴀᴜᴛʜ ᴜsᴇʀ

/unauth [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ʀᴇᴍᴏᴠᴇ ᴀᴜᴛʜ ᴜsᴇʀ

/authlist : sʜᴏᴡs ᴛʜᴇ ᴀᴜᴛʜ ʟɪsᴛ ᴏғ ᴛʜᴇ ɢʀᴏᴜᴘ
"""


@app.on_message(filters.command(["auth", "addauth"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def auth(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ !"
            )
    user = await extract_user(message)
    token = await int_to_alpha(user.id)
    _check = await get_authuser_names(message.chat.id)
    count = len(_check)
    if int(count) == 25:
        return await message.reply_text(
            "» ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ʜᴀᴠᴇ 25 ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !"
        )
    if token not in _check:
        assis = {
            "auth_user_id": user.id,
            "auth_name": user.first_name,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.first_name,
        }
        get = adminlist.get(message.chat.id)
        if get:
            if user.id not in get:
                get.append(user.id)
        await save_authuser(message.chat.id, token, assis)
        return await message.reply_text(
            "» ᴀᴅᴅᴇᴅ {0} ᴛᴏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ʟɪsᴛ !".format(user.mention)
        )
    else:
        return await message.reply_text(
            "{0} ɪs ᴀʟʀᴇᴀᴅʏ ɪɴ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ʟɪsᴛ !".format(user.mention)
        )


@app.on_message(filters.command(["unauth", "delauth"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def unauthusers(_, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "» ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ ɪᴅ !"
            )
    user = await extract_user(message)
    token = await int_to_alpha(user.id)
    deleted = await delete_authuser(message.chat.id, token)
    get = adminlist.get(message.chat.id)
    if get:
        if user.id in get:
            get.remove(user.id)
    if deleted:
        return await message.reply_text(
            "» ʀᴇᴍᴏᴠᴇᴅ {0} ғʀᴏᴍ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ʟɪsᴛ !".format(user.mention)
        )
    else:
        return await message.reply_text(
            "{0} ɪs ɴᴏᴛ ɪɴ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ʟɪsᴛ !".format(user.mention)
        )


@app.on_message(filters.command(["authlist", "authusers"]) & filters.group & ~BANNED_USERS)
async def authusers(_, message: Message):
    wtf = await get_authuser_names(message.chat.id)
    if not wtf:
        return await message.reply_text("» ɴᴏ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ꜰᴏᴜɴᴅ !")
    else:
        j = 0
        mystic = await message.reply_text("ғᴇᴛᴄʜɪɴɢ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ʟɪsᴛ ...")
        text = "» ʟɪsᴛ ᴏғ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴜsᴇʀs ɪɴ {0} :\n\n".format(message.chat.title)
        for umm in wtf:
            _umm = await get_authuser(message.chat.id, umm)
            user_id = _umm["auth_user_id"]
            admin_id = _umm["admin_id"]
            admin_name = _umm["admin_name"]
            try:
                user = (await app.get_users(user_id)).first_name
                j += 1
            except:
                continue
            text += f"{j}➤ {user}[<code>{user_id}</code>]\n"
            text += f"   <b>↬ ᴀᴅᴅᴇᴅ ʙʏ :</b> {admin_name}[<code>{admin_id}</code>]\n\n"
        await mystic.edit_text(text, reply_markup=close_keyboard())
