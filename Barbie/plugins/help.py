import re
from pyrogram import filters
from config import BANNED_USERS, SUPPORT_HEHE, EXTRA_IMG
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
from pyrogram.enums import ChatType
from pyrogram.errors import MessageNotModified
from Barbie import app, HELPABLE
from ..utils import (
    page_load,
    private_panel,
    start_pannel,
    private_help_panel,
    setting_markup,
)


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
async def start_testbot(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    out = start_pannel()
    await message.reply_photo(
        photo=EXTRA_IMG,
        caption=f"**ᴛʜᴀɴᴋs ғᴏʀ ᴀᴅᴅɪɴɢ ᴍᴇ ɪɴ :-**\n\n**ɢʀᴏᴜᴘ** : `{message.chat.title}`\n**ɢʀᴏᴜᴘ ɪᴅ** : `{message.chat.id}`",
        reply_markup=InlineKeyboardMarkup(out),
    )
    return


@app.on_callback_query(filters.regex(r"setting_back_help") & ~BANNED_USERS)
async def settings_back_markup(_, query: CallbackQuery):
    if query.message.chat.type == ChatType.PRIVATE:
        buttons = private_panel()
        await query.message.edit_caption(
            caption="ʜᴇʏ {0} \nᴛʜɪs ɪs {1} ᴀ ᴛᴇʟᴇɢʀᴀᴍ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴀᴡᴇꜱᴏᴍᴇ ꜰᴇᴀᴛᴜʀᴇꜱ.\n\nꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ ʟɪᴋᴇ **ʏᴏᴜᴛᴜʙᴇ**, **ꜱᴘᴏᴛɪꜰʏ** ᴇᴛᴄ.\n\n**ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs.**".format(
                query.from_user.first_name, app.mention
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = setting_markup()
        return await query.edit_message_reply_markup(InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(_, query: CallbackQuery):
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)

    if mod_match:
        try:
            module = mod_match.group(1)
            text = (
                "**{} --{}--** :\n".format("Hᴇʟᴘ Fᴏʀ", HELPABLE[module].__MODULE__)
                + HELPABLE[module].__HELP__
            )
            key = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="ʙᴀᴄᴋ", callback_data="back")]]
            )
            await query.message.edit(text=text, reply_markup=key)
        except MessageNotModified:
            return
    elif prev_match:
        try:
            current_page = int(prev_match.group(1))
            buttons = page_load(current_page - 1, HELPABLE, "help")
            await query.message.edit(
                f"ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{SUPPORT_HEHE}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except MessageNotModified:
            return
    elif next_match:
        try:
            current_page = int(next_match.group(1))
            buttons = page_load(current_page + 1, HELPABLE, "help")
            await query.message.edit(
                f"ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{SUPPORT_HEHE}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except MessageNotModified:
            return


@app.on_callback_query(filters.regex("home_help"))
async def back(_, query: CallbackQuery):
    try:
        buttons = page_load(0, HELPABLE, "help")
        await query.message.edit(
            f"ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{SUPPORT_HEHE}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("back"))
async def back(_, query: CallbackQuery):
    try:
        buttons = page_load(0, HELPABLE, "help")
        await query.message.edit(
            f"ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{SUPPORT_HEHE}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except MessageNotModified:
        return


@app.on_callback_query(filters.regex("semxx"))
async def back(_, query: CallbackQuery):
    try:
        buttons = private_panel()
        await query.message.edit(
            text=f"""ʜᴇʏ {query.from_user.mention}
**ᴛʜɪs ɪs {app.mention} ᴀ ᴛᴇʟᴇɢʀᴀᴍ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴀᴡᴇꜱᴏᴍᴇ ꜰᴇᴀᴛᴜʀᴇꜱ. ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ ʟɪᴋᴇ **ʏᴏᴜᴛᴜʙᴇ**, **ꜱᴘᴏᴛɪꜰʏ** ᴇᴛᴄ ...
ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs :**""",
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except MessageNotModified:
        return


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
async def help_cmd(_, msg: Message):
    try:
        await msg.delete()
    except:
        pass
    key = private_help_panel()
    await msg.reply_text(
        text="ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ɪɴ ᴘᴍ ғᴏʀ ʜᴇʟᴘ !", 
        reply_markup=InlineKeyboardMarkup(key),
    )
