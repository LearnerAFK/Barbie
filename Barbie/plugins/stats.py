import config
import psutil
import asyncio
import platform
from sys import version as pyver
from config import BANNED_USERS
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import InputMediaPhoto, Message
from pytgcalls.__version__ import __version__ as pytgver
from Barbie import app
from ..plugins import ALL_MODULES
from ..core.userbot import assistants
from ..misc import SUDOERS
from ..utils import (
    stats_buttons, overallback_stats_markup, 
    back_stats_buttons, get_served_chats, 
    get_served_users, get_queries, 
    get_stats_markup, get_sudoers)


loop = asyncio.get_running_loop()


__MODULE__ = "Sᴛᴀᴛs"
__HELP__ = """
/stats or /gstats : ɢᴇᴛ ʙᴏᴛ ʀᴇʟᴀᴛᴇᴅ ᴜsᴇʀ ᴏʀ ᴄʜᴀᴛ sᴛᴀᴛs
"""


@app.on_message(filters.command(["stats", "gstats"]) & filters.group & ~BANNED_USERS)
async def stats_global(_, message: Message):
    try:
        await message.delete()
    except:
        pass
    upl = stats_buttons(True if message.from_user.id in SUDOERS else False)
    await message.reply_photo(
        photo=config.EXTRA_IMG,
        caption="**ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs ᴏғ {0}**\nsᴇʟᴇᴄᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ғʀᴏᴍ ʙᴇʟᴏᴡ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴇᴄᴋ ɢʟᴏʙᴀʟ sᴛᴀᴛs ғʀᴏᴍ ʙᴏᴛ's sᴇʀᴠᴇʀs.".format(app.mention),
        reply_markup=upl,
    )


@app.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
async def overall_stats(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    what = callback_data.split(None, 1)[1]
    if what != "s":
        upl = overallback_stats_markup()
    else:
        upl = back_stats_buttons()
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text("ɢᴇᴛᴛɪɴɢ ʙᴏᴛ's ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs ᴀɴᴅ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ...")
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    total_queries = await get_queries()
    blocked = len(BANNED_USERS)
    sudoers = len(SUDOERS)
    mod = len(ALL_MODULES)
    assistant = len(assistants)
    song = config.SONG_DOWNLOAD_DURATION
    play_duration = config.DURATION_LIMIT_MIN
    if config.AUTO_LEAVING_ASSISTANT == str(True):
        ass = "ʏᴇs"
    else:
        ass = "ɴᴏ"
    text = f"""**ʙᴏᴛ's sᴛᴀᴛs ᴀɴᴅ ɪɴғᴏ:**

**ᴍᴏᴅᴜʟᴇs:** `{mod}`
**ᴄʜᴀᴛs:** `{served_chats}`
**ᴜsᴇʀs:** `{served_users}`
**ʙʟᴏᴄᴋᴇᴅ:** `{blocked}`
**sᴜᴅᴏᴇʀs:** `{sudoers}`
    
**ǫᴜᴇʀɪᴇs:** `{total_queries}`
**ᴀssɪsᴛᴀɴᴛs:** `{assistant}`
**ᴀss ᴀᴜᴛᴏ ʟᴇᴀᴠᴇ:** `{ass}`
**Dᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ:** `{play_duration} mins`
**ᴅᴏᴡɴʟᴏᴀᴅ ʟɪᴍɪᴛ:** `{song} mins`
"""
    med = InputMediaPhoto(media=config.EXTRA_IMG, caption=text)
    try:
        await CallbackQuery.edit_message_media(
            media=med, 
            reply_markup=upl,
        )
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(
            photo=config.EXTRA_IMG, 
            caption=text, 
            reply_markup=upl,
        )


@app.on_callback_query(filters.regex("bot_stats_sudo") & ~BANNED_USERS)
async def overall_stats(_, CallbackQuery):
    if CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer("Only for Sudo Users.", show_alert=True)
    callback_data = CallbackQuery.data.strip()
    what = callback_data.split(None, 1)[1]
    if what != "s":
        upl = overallback_stats_markup()
    else:
        upl = back_stats_buttons()
    try:
        await CallbackQuery.answer()
    except:
        pass
    await CallbackQuery.edit_message_text("ɢᴇᴛᴛɪɴɢ ʙᴏᴛ's ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs ᴀɴᴅ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ...")
    sc = platform.system()
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " ɢʙ"
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}ɢʜᴢ"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}ᴍʜᴢ"
    except:
        cpu_freq = "Unable to Fetch"
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    total = str(total)
    used = hdd.used / (1024.0**3)
    used = str(used)
    free = hdd.free / (1024.0**3)
    free = str(free)
    mod = len(ALL_MODULES)

    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    blocked = len(BANNED_USERS)
    sudoers = len(await get_sudoers())
    text = f""" **ʙᴏᴛ's sᴛᴀᴛs ᴀɴᴅ ɪɴғᴏ:**


**ᴍᴏᴅᴜʟᴇs:** `{mod}`
**ᴩʟᴀᴛғᴏʀᴍ:** `{sc}`
**ʀᴀᴍ:** `{ram}`
**ᴩʜʏsɪᴄᴀʟ ᴄᴏʀᴇs:** `{p_core}`
**ᴛᴏᴛᴀʟ ᴄᴏʀᴇs:** `{t_core}`
**ᴄᴩᴜ ғʀᴇǫᴜᴇɴᴄʏ:** `{cpu_freq}`

**ᴩʏᴛʜᴏɴ :** `{pyver.split()[0]}`
**ᴩʏʀᴏɢʀᴀᴍ :** `{pyrover}`
**ᴩʏ-ᴛɢᴄᴀʟʟs :** `{pytgver}`

**ᴀᴠᴀɪʟᴀʙʟᴇ:** `{total[:4]} GiB`
**ᴜsᴇᴅ:** `{used[:4]} GiB`
**ғʀᴇᴇ:** `{free[:4]} GiB`

**ᴄʜᴀᴛs:** `{served_chats}`
**ᴜsᴇʀs:** `{served_users}` 
**ʙʟᴏᴄᴋᴇᴅ:** `{blocked}`
**sᴜᴅᴏᴇʀs:** `{sudoers}` 
"""
    med = InputMediaPhoto(media=config.EXTRA_IMG, caption=text)
    try:
        await CallbackQuery.edit_message_media(
            media=med, 
            reply_markup=upl,
        )
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(
            photo=config.EXTRA_IMG, 
            caption=text, 
            reply_markup=upl,
        )


@app.on_callback_query(filters.regex(pattern=r"^(GETSTATS|GlobalStats)$") & ~BANNED_USERS)
async def back_buttons(_, CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass
    command = CallbackQuery.matches[0].group(1)
    if command == "GlobalStats":
        upl = get_stats_markup(True if CallbackQuery.from_user.id in SUDOERS else False)
        med = InputMediaPhoto(
            media=config.EXTRA_IMG,
            caption="**ɢʟᴏʙᴀʟ sᴛᴀᴛs ᴏғ {0}**\n\nsᴇʟᴇᴄᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ғʀᴏᴍ ʙᴇʟᴏᴡ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴇᴄᴋ ɢʟᴏʙᴀʟ sᴛᴀᴛs ғʀᴏᴍ ʙᴏᴛ's sᴇʀᴠᴇʀs.".format(app.mention),
        )
        try:
            await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await CallbackQuery.message.reply_photo(
                photo=config.EXTRA_IMG,
                caption="**ɢʟᴏʙᴀʟ sᴛᴀᴛs ᴏғ {0}**\n\nsᴇʟᴇᴄᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ғʀᴏᴍ ʙᴇʟᴏᴡ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴇᴄᴋ ɢʟᴏʙᴀʟ sᴛᴀᴛs ғʀᴏᴍ ʙᴏᴛ's sᴇʀᴠᴇʀs.".format(app.mention),
                reply_markup=upl,
            )
    if command == "GETSTATS":
        upl = stats_buttons(True if CallbackQuery.from_user.id in SUDOERS else False)
        med = InputMediaPhoto(
            media=config.EXTRA_IMG,
            caption="**ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs ᴏғ {0}**\nsᴇʟᴇᴄᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ғʀᴏᴍ ʙᴇʟᴏᴡ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴇᴄᴋ ɢʟᴏʙᴀʟ sᴛᴀᴛs ғʀᴏᴍ ʙᴏᴛ's sᴇʀᴠᴇʀs.".format(app.mention),
        )
        try:
            await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
        except MessageIdInvalid:
            await CallbackQuery.message.reply_photo(
                photo=config.EXTRA_IMG,
                caption="**ɢᴇɴᴇʀᴀʟ sᴛᴀᴛs ᴏғ {0}**\nsᴇʟᴇᴄᴛ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ғʀᴏᴍ ʙᴇʟᴏᴡ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʜᴇᴄᴋ ɢʟᴏʙᴀʟ sᴛᴀᴛs ғʀᴏᴍ ʙᴏᴛ's sᴇʀᴠᴇʀs.".format(app.mention),
                reply_markup=upl,
            )
