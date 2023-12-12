from pyrogram import filters
from pyrogram.types import Message
from config import MONGO_DB, OWNER_ID, BANNED_USERS
from Barbie import app
from ..misc import SUDOERS
from ..utils import add_sudo, remove_sudo


__MODULE__ = "Sᴜᴅᴏ"
__HELP__ = """
/addsudo [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ᴀᴅᴅ sᴜᴅᴏ ᴜsᴇʀ

/delsudo [ᴜsᴇʀɴᴀᴍᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴜsᴇʀ] : ʀᴇᴍᴏᴠᴇ sᴜᴅᴏ ᴜsᴇʀ

/sudolist : sʜᴏᴡs ᴛʜᴇ sᴜᴅᴏ ᴜsᴇʀs ᴏғ ᴍᴜsɪᴄ ʙᴏᴛ
"""


@app.on_message(filters.command(["addsudo", "sudo"]) & filters.user(OWNER_ID) & ~filters.forwarded)
async def userr_add(_, message: Message):
    if MONGO_DB is None:
        return await message.reply_text(
            f"**ᴩʟᴇᴀsᴇ ᴀᴅᴅ ʏᴏᴜʀ ᴍᴏɴɢᴏ ᴅᴀᴛᴀʙᴀsᴇ ɪɴ ᴠᴀʀs ᴛᴏ ᴜsᴇ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ...**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ ...**"
            )
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id in SUDOERS:
            return await message.reply_text(
                "{0} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ ...".format(user.mention)
            )
        added = await add_sudo(user.id)
        if added:
            SUDOERS.add(user.id)
            await message.reply_text("ᴀᴅᴅᴇᴅ **{0}** ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs ...".format(user.mention))
        else:
            await message.reply_text("ғᴀɪʟᴇᴅ ...")
        return
    if message.reply_to_message.from_user.id in SUDOERS:
        return await message.reply_text(
            "{0} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ ...".format(
                message.reply_to_message.from_user.mention
            )
        )
    added = await add_sudo(message.reply_to_message.from_user.id)
    if added:
        SUDOERS.add(message.reply_to_message.from_user.id)
        await message.reply_text(
            "ᴀᴅᴅᴇᴅ **{0}** ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs ...".format(
                message.reply_to_message.from_user.mention
            )
        )
    else:
        await message.reply_text("ғᴀɪʟᴇᴅ ...")
    return


@app.on_message(filters.command(["delsudo", "rmsudo"]) & filters.user(OWNER_ID) & ~filters.forwarded)
async def userr_del(_, message: Message):
    if MONGO_DB is None:
        return await message.reply_text(
            f"**ᴩʟᴇᴀsᴇ ᴀᴅᴅ ʏᴏᴜʀ ᴍᴏɴɢᴏ ᴅᴀᴛᴀʙᴀsᴇ ɪɴ ᴠᴀʀs ᴛᴏ ᴜsᴇ ᴛʜɪs ғᴇᴀᴛᴜʀᴇ ...**"
        )
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(
                "**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴜsᴇʀ's ᴍᴇssᴀɢᴇ ᴏʀ ɢɪᴠᴇ ᴜsᴇʀɴᴀᴍᴇ/ᴜsᴇʀ_ɪᴅ ...**"
            )
        user = message.text.split(None, 1)[1]
        if "@" in user:
            user = user.replace("@", "")
        user = await app.get_users(user)
        if user.id not in SUDOERS:
            return await message.reply_text("ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ʙᴏᴛ's sᴜᴅᴏ ...")
        removed = await remove_sudo(user.id)
        if removed:
            SUDOERS.remove(user.id)
            await message.reply_text("ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ʙᴏᴛ's sᴜᴅᴏ ᴜsᴇʀ ...")
            return
        await message.reply_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ...")
        return
    user_id = message.reply_to_message.from_user.id
    if user_id not in SUDOERS:
        return await message.reply_text("ɴᴏᴛ ᴀ ᴘᴀʀᴛ ᴏꜰ ʙᴏᴛ's sᴜᴅᴏ ...")
    removed = await remove_sudo(user_id)
    if removed:
        SUDOERS.remove(user_id)
        await message.reply_text("ʀᴇᴍᴏᴠᴇᴅ ꜰʀᴏᴍ ʙᴏᴛ's sᴜᴅᴏ ᴜsᴇʀ ...")
        return
    await message.reply_text("sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ ...")


@app.on_message(filters.command(["sudolist", "owner", "slist"]) & ~BANNED_USERS)
async def sudoers_list(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    text = "⭐️<u> **Oᴡɴᴇʀ :**</u>\n"
    count = 0
    for x in OWNER_ID:
        try:
            user = await app.get_users(x)
            user = user.first_name if not user.mention else user.mention
            count += 1
        except Exception:
            continue
        text += f"{count}➤ {user}\n"
    smex = 0
    for user_id in SUDOERS:
        if user_id not in OWNER_ID:
            try:
                user = await app.get_users(user_id)
                user = user.first_name if not user.mention else user.mention
                if smex == 0:
                    smex += 1
                    text += "\n❤<u> **Sᴜᴅᴏ Usᴇʀs :**</u>\n"
                count += 1
                text += f"{count}➤ {user}\n"
            except Exception:
                continue
    if text:
        await message.reply_text(text)
    else:
        await message.reply_text("ɴᴏ sᴜᴅᴏ ᴜsᴇʀs ғᴏᴜɴᴅ ...")
