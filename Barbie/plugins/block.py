from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Barbie import app
from ..misc import SUDOERS
from ..utils import add_gban_user, remove_gban_user


__MODULE__ = "Bʟᴏᴄᴋ"
__HELP__ = """
/block [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : sᴛᴀʀᴛs ɪɢɴᴏʀɪɴɢ ᴛʜᴇ ᴜsᴇʀ, sᴏ ᴛʜᴀᴛ ʜᴇ/ꜱʜᴇ ᴄᴀɴ'ᴛ ᴜsᴇ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs.

/unblock [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴜɴʙʟᴏᴄᴋs ᴛʜᴇ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀ.

/blockedusers : sʜᴏᴡs ᴛʜᴇ ʟɪsᴛ ᴏғ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs.
"""


@app.on_message(filters.command(["block"]) & SUDOERS)
async def useradd(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) != 2:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ"
        )
    else:
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)

    if user.id in BANNED_USERS:
        return await message.reply_text(
            "{0} ɪs ᴀʟʀᴇᴀᴅʏ ʙʟᴏᴄᴋᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ʙᴏᴛ".format(
                message.reply_to_message.from_user.mention
            )
        )
    elif user.id in SUDOERS:
        return await message.reply_text("ɴᴏ, ᴛʜɪꜱ ᴜꜱᴇʀ ɪꜱ ᴀ ꜱᴜᴅᴏ ᴜꜱᴇʀ ᴏꜰ ᴛʜɪꜱ ʙᴏᴛ")
    await add_gban_user(user.id)
    BANNED_USERS.add(user.id)
    await message.reply_text(
        "ᴀᴅᴅᴇᴅ **{0}** ᴛᴏ ʙʟᴏᴄᴋ ʟɪsᴛ ᴏꜰ ʙᴏᴛ. ᴜsᴇʀ ᴡᴏɴ'ᴛ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴜsᴇ ʙᴏᴛ ɴᴏᴡ ᴜɴᴅᴇʀ ᴀɴʏ ᴄᴏɴᴅɪᴛɪᴏɴ.\n\nᴄʜᴇᴄᴋ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs: /blockedusers".format(
            user.mention
        )
    )


@app.on_message(filters.command(["unblock"]) & SUDOERS)
async def userdel(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    elif len(message.command) != 2:
        return await message.reply_text(
            "ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ"
        )
    else:
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
    if user.id not in BANNED_USERS:
        return await message.reply_text("ᴜsᴇʀ ɪs ᴀʟʀᴇᴀᴅʏ ꜰʀᴇᴇ.")
    await remove_gban_user(user.id)
    BANNED_USERS.remove(user.id)
    await message.reply_text(
        "ʀᴇᴍᴏᴠᴇᴅ ᴜsᴇʀ ꜰʀᴏᴍ ᴛʜᴇ ʙʟᴏᴄᴋ ʟɪsᴛ. ᴜsᴇʀ ᴡɪʟʟ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴜsᴇ ʙᴏᴛ ɴᴏᴡ."
    )


@app.on_message(filters.command(["blockedusers", "blocked"]) & ~BANNED_USERS)
async def sudoers_list(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    if not BANNED_USERS:
        return await message.reply_text("ɴᴏ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ꜰᴏᴜɴᴅ")
    mystic = await message.reply_text("ɢᴇᴛᴛɪɴɢ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ʟɪsᴛ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ!")
    msg = "**ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs :**\n\n"
    count = 0
    for users in BANNED_USERS:
        try:
            user = await app.get_users(users)
            user = user.mention if user.mention else user.first_name
            msg += f"{count}➤ {user}\n"
            count += 1
        except Exception:
            continue
    if count == 0:
        return await mystic.edit_text("ɴᴏ ʙʟᴏᴄᴋᴇᴅ ᴜsᴇʀs ꜰᴏᴜɴᴅ.")
    else:
        return await mystic.edit_text(msg)
