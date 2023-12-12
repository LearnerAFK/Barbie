import random
import asyncio
import config
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardMarkup,
    InputMediaPhoto,
)
from config import AUTO_DOWNLOADS_CLEAR, BANNED_USERS, STREAM_IMG
from Barbie import app, YouTube
from Barbie.core.call import CallMusic
from Barbie.misc import db
from ..utils import *
from ..plugins.queue import basic, get_duration
from Barbie.utils import seconds_to_min, ActualAdminCB
from Barbie.utils.inline import stream_markup, telegram_markup
from Barbie.utils.inline.play import close_keyboard
from Barbie.utils.stream.autoclear import auto_clean
from Barbie.utils.thumbnails import gen_thumb


checker = {}


@app.on_callback_query(filters.regex("close") & ~BANNED_USERS)
async def close_menu(_, CallbackQuery):
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        return


@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@ActualAdminCB
async def del_back_playlist(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(
            "ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ᴏɴ ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ...", 
            show_alert=True,
        )

    mention = CallbackQuery.from_user.mention

    if command == "Pause":
        if not await is_music_playing(chat_id):
            return await CallbackQuery.answer("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ᴘᴀᴜsᴇᴅ ...​", show_alert=True)
        await CallbackQuery.answer()
        await music_off(chat_id)
        await CallMusic.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(
            "**sᴛʀᴇᴀᴍ ᴩᴀᴜsᴇᴅ** ʙʏ : {} ".format(mention), 
            reply_markup=close_keyboard,
        )

    elif command == "Resume":
        if await is_music_playing(chat_id):
            return await CallbackQuery.answer("ᴍᴜsɪᴄ ɪs ᴀʟʀᴇᴀᴅʏ ʀᴇsᴜᴍᴇᴅ ...​", show_alert=True)
        await CallbackQuery.answer()
        await music_on(chat_id)
        await CallMusic.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(
            "**sᴛʀᴇᴀᴍ ʀᴇsᴜᴍᴇᴅ** ʙʏ : {} ".format(mention), 
            reply_markup=close_keyboard,
        )

    elif command == "Stop" or command == "End":
        await CallbackQuery.answer()
        await CallMusic.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.delete()
        await CallbackQuery.message.reply_text(
            "**sᴛʀᴇᴀᴍ ᴇɴᴅᴇᴅ/sᴛᴏᴩᴩᴇᴅ** ʙʏ : {} ".format(mention),
            reply_markup=close_keyboard,
        )
        try:
            popped = check.pop(0)
        except:
            return await CallbackQuery.answer(
                "ꜰᴀɪʟᴇᴅ ᴛᴏ sʜᴜꜰꜰʟᴇ ​.\n\nᴄʜᴇᴄᴋ ǫᴜᴇᴜᴇ : /queue", 
                show_alert=True,
            )
        check = db.get(chat_id)
        if not check:
            check.insert(0, popped)
            return await CallbackQuery.answer(
                "ꜰᴀɪʟᴇᴅ ᴛᴏ sʜᴜꜰꜰʟᴇ ​.\n\nᴄʜᴇᴄᴋ ǫᴜᴇᴜᴇ : /queue", 
                show_alert=True,
            )
        await CallbackQuery.answer()
        random.shuffle(check)
        check.insert(0, popped)
        await CallbackQuery.message.reply_text(
            "**ǫᴜᴇᴜᴇ sʜᴜꜰꜰʟᴇᴅ ʙʏ {0} ​**\n\nᴄʜᴇᴄᴋ sʜᴜꜰꜰʟᴇᴅ ǫᴜᴇᴜᴇ : /queue".format(
                mention
            )
        )

    elif command == "Skip":
        check = db.get(chat_id)
        popped = None
        try:
            popped = check.pop(0)
            if popped:
                if AUTO_DOWNLOADS_CLEAR == str(True):
                    await auto_clean(popped)
            if not check:
                ms = await CallbackQuery.edit_message_text(
                    "» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0} ...".format(mention),
                    reply_markup=close_keyboard,
                )
                await CallbackQuery.message.reply_text(
                    "sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ ʙʏ : {0} \n\n**» ɴᴏ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ɪɴ** {1}, **ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏᴄʜᴀᴛ.**".format(
                        mention, CallbackQuery.message.chat.title
                    ),
                    reply_markup=close_keyboard,
                )
                await CallbackQuery.message.delete(ms)
                try:
                    return await CallMusic.stop_stream(chat_id)
                except:
                    return
        except:
            try:
                await CallbackQuery.edit_message_text(
                    "» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention),
                    reply_markup=close_keyboard,
                )
                await CallbackQuery.message.reply_text(
                    "sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ ʙʏ : {0} \n\n**» ɴᴏ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ɪɴ** {1}, **ʟᴇᴀᴠɪɴɢ ᴠɪᴅᴇᴏᴄʜᴀᴛ.**".format(
                        mention, CallbackQuery.message.chat.title
                    ),
                    reply_markup=close_keyboard,
                )
                return await CallMusic.stop_stream(chat_id)
            except:
                return

        await CallbackQuery.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        duration_min = check[0]["dur"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0

        if "live_" in queued:
            n, link = await YouTube.video(videoid, True)
            if n == 0:
                return await CallbackQuery.message.reply_text(
                    "ᴇʀʀᴏʀ ᴡʜɪʟᴇ ᴄʜᴀɴɢɪɴɢ sᴛʀᴇᴀᴍ ᴛᴏ **{0}** ​\n\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴀɢᴀɪɴ.".format(
                        title
                    )
                )
            try:
                await CallMusic.skip_stream(chat_id, link, video=status)
            except Exception:
                return await CallbackQuery.message.reply_text(
                    "**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ."
                )
            await CallbackQuery.edit_message_text("» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention))
            button = telegram_markup(chat_id)
            img = await gen_thumb(videoid)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                    user, f"https://t.me/{app.username}?start=info_{videoid}"
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        elif "vid_" in queued:
            mystic = await CallbackQuery.message.reply_text(
                "ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ɴᴇxᴛ ᴛʀᴀᴄᴋ ꜰʀᴏᴍ ᴘʟᴀʏʟɪsᴛ", 
                disable_web_page_preview=True,
            )
            try:
                file_path, direct = await YouTube.download(
                    videoid, mystic, videoid=True, video=status
                )
            except:
                return await mystic.edit_text(
                    "**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ."
                )
            try:
                await CallMusic.skip_stream(chat_id, file_path, video=status)
            except Exception:
                return await mystic.edit_text(
                    "**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ."
                )
            await CallbackQuery.edit_message_text(
                "» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention)
            )
            button = stream_markup(videoid, chat_id)
            img = await gen_thumb(videoid)
            run = await CallbackQuery.message.reply_photo(
                photo=img,
                caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{videoid}",
                    duration_min,
                    user,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            await mystic.delete()
        elif "index_" in queued:
            try:
                await CallMusic.skip_stream(chat_id, videoid, video=status)
            except Exception:
                return await CallbackQuery.message.reply_text(
                    "**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ."
                )
            await CallbackQuery.edit_message_text(
                "» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention)
            )
            button = telegram_markup(chat_id)
            run = await CallbackQuery.message.reply_photo(
                photo=STREAM_IMG,
                caption="**sᴛʀᴇᴀᴍ ᴛʏᴘᴇ :** ʟɪᴠᴇ sᴛʀᴇᴀᴍ [ᴜʀʟ]\n**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {0}".format(
                    user
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        else:
            try:
                await CallMusic.skip_stream(chat_id, queued, video=status)
            except:
                return await CallbackQuery.message.reply_text(
                    "**ꜰᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ**\nᴘʟᴇᴀsᴇ ᴜsᴇ /skip ᴛᴏ ᴄʜᴀɴɢᴇ ᴛʀᴀᴄᴋ ᴀɢᴀɪɴ."
                )
            await CallbackQuery.edit_message_text(
                "» ꜱᴛʀᴇᴀᴍ ꜱᴋɪᴘᴘᴇᴅ ʙʏ {0}".format(mention)
            )
            if videoid == "telegram":
                button = telegram_markup(chat_id)
                run = await CallbackQuery.message.reply_photo(
                    photo=STREAM_IMG if str(streamtype) == "audio" else STREAM_IMG,
                    caption="**Tɪᴛʟᴇ:** {0}\n**Dᴜʀᴀᴛɪᴏɴ:** {1}\n**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {2} ".format(
                        title, check[0]["dur"], user
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"

            else:
                button = stream_markup(videoid, chat_id)
                img = await gen_thumb(videoid)
                run = await CallbackQuery.message.reply_photo(
                    photo=img,
                    caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** {2} ᴍɪɴᴜᴛᴇs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        duration_min,
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"

    else:
        playing = db.get(chat_id)
        if not playing:
            return await CallbackQuery.answer(
                "ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ. ɴᴏ ᴛʀᴀᴄᴋs ғᴏᴜɴᴅ", 
                show_alert=True,
            )

        duration_seconds = int(playing[0]["seconds"])
        if duration_seconds == 0:
            return await CallbackQuery.answer(
                "sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ.",
                show_alert=True,
            )

        file_path = playing[0]["file"]
        if "index_" in file_path or "live_" in file_path:
            return await CallbackQuery.answer(
                "sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ.",
                show_alert=True,
            )

        duration_played = int(playing[0]["played"])
        if int(command) in [1, 2]:
            duration_to_skip = 10
        else:
            duration_to_skip = 30
        duration = playing[0]["dur"]

        if int(command) in [1, 3]:
            if (duration_played - duration_to_skip) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    "» ʙᴏᴛ ɪs ᴜɴᴀʙʟᴇ ᴛᴏ sᴇᴇᴋ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ Dᴜʀᴀᴛɪᴏɴ ᴇxᴄᴇᴇᴅs.\n\nᴄᴜʀʀᴇɴᴛʟʏ ᴩʟᴀʏᴇᴅ :** {0}** ᴍɪɴᴜᴛᴇs ᴏᴜᴛ ᴏғ **{1}** ᴍɪɴᴜᴛᴇs.".format(
                        bet, duration
                    ),
                    show_alert=True,
                )
            to_seek = duration_played - duration_to_skip + 1
        else:
            if (duration_seconds - (duration_played + duration_to_skip)) <= 10:
                bet = seconds_to_min(duration_played)
                return await CallbackQuery.answer(
                    "» ʙᴏᴛ ɪs ᴜɴᴀʙʟᴇ ᴛᴏ sᴇᴇᴋ ʙᴇᴄᴀᴜsᴇ ᴛʜᴇ Dᴜʀᴀᴛɪᴏɴ ᴇxᴄᴇᴇᴅs.\n\nᴄᴜʀʀᴇɴᴛʟʏ ᴩʟᴀʏᴇᴅ :** {0}** ᴍɪɴᴜᴛᴇs ᴏᴜᴛ ᴏғ **{1}** ᴍɪɴᴜᴛᴇs.".format(
                        bet, duration
                    ),
                    show_alert=True,
                )
            to_seek = duration_played + duration_to_skip + 1

        await CallbackQuery.answer()
        mystic = await CallbackQuery.message.reply_text("sᴇᴇᴋɪɴɢ")
        if "vid_" in file_path:
            n, file_path = await YouTube.video(playing[0]["vidid"], True)
            if n == 0:
                return await mystic.edit_text(
                    "sᴏʀʀʏ ʙᴜᴛ ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇᴇᴋ ᴛʜᴇ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ, ɪᴛ ᴄᴀɴ ᴏɴʟʏ ʙᴇ sᴋɪᴩᴩᴇᴅ ᴏʀ sᴛᴏᴩᴩᴇᴅ."
                )
        try:
            await CallMusic.seek_stream(
                chat_id,
                file_path,
                seconds_to_min(to_seek),
                duration,
                playing[0]["streamtype"],
            )
        except:
            return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ sᴇᴇᴋ")
        if int(command) in [1, 3]:
            db[chat_id][0]["played"] -= duration_to_skip
        else:
            db[chat_id][0]["played"] += duration_to_skip
        string = "sᴇᴇᴋᴇᴅ ᴛᴏ {0} ᴍɪɴs".format(seconds_to_min(to_seek))
        await mystic.edit_text("{0}\n\nᴄʜᴀɴɢᴇs ᴅᴏɴᴇ ʙʏ : {1} !".format(string, mention))


@app.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
async def play_music(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, fplay = callback_request.split("|")
    try:
        chat_id = CallbackQuery.message.chat.id
    except:
        return
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("sᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏᴡɴ sᴏɴɢ ...", show_alert=True)
        except:
            return
    user_name = CallbackQuery.from_user.first_name
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        pass
    mystic = await CallbackQuery.message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ ...")
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ ...")
    if details["duration_min"]:
        duration_sec = time_to_seconds(details["duration_min"])
        if duration_sec > config.DURATION_LIMIT:
            return await mystic.edit_text(
                "**Dᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ**\n\n**ᴀʟʟᴏᴡᴇᴅ Dᴜʀᴀᴛɪᴏɴ:** {0} ᴍɪɴᴜᴛᴇs\n**ʀᴇᴄᴇɪᴠᴇᴅ Dᴜʀᴀᴛɪᴏɴ:** {1} ᴍɪɴᴜᴛᴇs".format(
                    config.DURATION_LIMIT_MIN, details["duration_min"]
                )
            )
    else:
        buttons = livestream_markup(
            track_id,
            CallbackQuery.from_user.id,
            mode,
            "f" if fplay else "d",
        )
        return await mystic.edit_text(
            "**ʟɪᴠᴇ sᴛʀᴇᴀᴍ ᴅᴇᴛᴇᴄᴛᴇᴅ** ...", reply_markup=InlineKeyboardMarkup(buttons)
        )
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    try:
        await stream(
            mystic,
            CallbackQuery.from_user.id,
            details,
            chat_id,
            user_name,
            CallbackQuery.message.chat.id,
            video,
            streamtype="youtube",
            forceplay=ffplay,
        )
    except Exception as e:
        print(f"[ERROR] : {e}")
        ex_type = type(e).__name__
        err = (
            e
            if ex_type == "AssistantErr"
            else "sᴏᴍᴇ **ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ** ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ\n\nᴇxᴄᴇᴘᴛɪᴏɴ ᴛʏᴘᴇ:- `{0}`".format(
                ex_type
            )
        )
        return await mystic.edit_text(err)
    return await mystic.delete()


@app.on_callback_query(filters.regex("LiveStream") & ~BANNED_USERS)
async def play_live_stream(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, fplay = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("sᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏᴡɴ sᴏɴɢ ...", show_alert=True)
        except:
            return
    try:
        chat_id = CallbackQuery.message.chat.id
    except:
        return
    video = True if mode == "v" else None
    user_name = CallbackQuery.from_user.first_name
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        pass
    mystic = await CallbackQuery.message.reply_text("🔄 **ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ** ...")
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception:
        return await mystic.edit_text("ꜰᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ ...")

    ffplay = True if fplay == "f" else None
    if not details["duration_min"]:
        try:
            await stream(
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                CallbackQuery.message.chat.id,
                video,
                streamtype="live",
                forceplay=ffplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = (
                e
                if ex_type == "AssistantErr"
                else "sᴏᴍᴇ **ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ** ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ\n\nᴇxᴄᴇᴘᴛɪᴏɴ ᴛʏᴘᴇ:- `{0}`".format(
                    ex_type
                )
            )
            return await mystic.edit_text(err)
    else:
        return await mystic.edit_text("ɪᴛ's ɴᴏᴛ ᴀ ʟɪᴠᴇ sᴛʀᴇᴀᴍ ...")
    await mystic.delete()


@app.on_callback_query(filters.regex("slider") & ~BANNED_USERS)
async def slider_queries(_, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (
        what,
        rtype,
        query,
        user_id,
        fplay,
    ) = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("sᴇᴀʀᴄʜ ʏᴏᴜʀ ᴏᴡɴ sᴏɴɢ ...", show_alert=True)
        except:
            return
    what = str(what)
    rtype = int(rtype)
    if what == "F":
        if rtype == 9:
            query_type = 0
        else:
            query_type = int(rtype + 1)
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ɴᴇxᴛ ʀᴇsᴜʟᴛ ...")
        except:
            pass
        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(vidid, user_id, query, query_type, fplay)
        med = InputMediaPhoto(
            media=thumbnail,
            caption="**Tɪᴛʟᴇ:** {0}\n\n**Dᴜʀᴀᴛɪᴏɴ:** {1} ᴍɪɴs".format(
                title.title(), duration_min
            ),
        )
        return await CallbackQuery.edit_message_media(
            media=med, 
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    elif what == "B":
        if rtype == 0:
            query_type = 9
        else:
            query_type = int(rtype - 1)
        try:
            await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ɴᴇxᴛ ʀᴇsᴜʟᴛ ...")
        except:
            pass
        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(vidid, user_id, query, query_type, fplay)
        med = InputMediaPhoto(
            media=thumbnail,
            caption="**Tɪᴛʟᴇ:** {0}\n\n**Dᴜʀᴀᴛɪᴏɴ:** {1} ᴍɪɴs".format(
                title.title(), duration_min
            ),
        )
        return await CallbackQuery.edit_message_media(
            media=med, 
            reply_markup=InlineKeyboardMarkup(buttons),
        )



@app.on_callback_query(filters.regex("GetQueued") & ~BANNED_USERS)
async def queued_tracks(_, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    what, videoid = callback_request.split("|")
    try:
        chat_id = CallbackQuery.message.chat.id
    except:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ...", show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ ...", show_alert=True)
    if len(got) == 1:
        return await CallbackQuery.answer(
            "ᴏɴʟʏ ᴏɴᴇ ᴛʀᴀᴄᴋ ɪs ɪɴ ǫᴜᴇᴜᴇ ᴀᴅᴅ sᴏᴍᴇ ᴍᴏʀᴇ ᴛʀᴀᴄᴋs ɪɴ ǫᴜᴇᴜᴇ ᴛᴏ ᴄʜᴇᴄᴋ ᴡʜᴏʟᴇ ǫᴜᴇᴜᴇ",
            show_alert=True,
        )
    await CallbackQuery.answer()
    basic[videoid] = False
    buttons = queue_back_markup(what)
    thumbnail = await YouTube.thumbnail(videoid, True)
    med = InputMediaPhoto(media=thumbnail, caption="» ᴩʟᴇᴀsᴇ ᴡᴀɪᴛ ...")
    await CallbackQuery.edit_message_media(media=med)
    j = 0
    msg = ""
    for x in got:
        j += 1
        if j == 1:
            msg += "{0} Pʟᴀʏᴇʀ :\n\nTɪᴛʟᴇ : {1}\nDᴜʀᴀᴛɪᴏɴ : {2}\nBʏ : {3}\n\n".format(
                app.mention, x["title"], x["dur"], x["by"]
            )
        elif j == 2:
            msg += "Qᴜᴇᴜᴇᴅ :\n\nTɪᴛʟᴇ : {0}\nDᴜʀᴀᴛɪᴏɴ : {1}\nBʏ : {2}\n\n".format(
                x["title"], x["dur"], x["by"]
            )
        else:
            msg += "Tɪᴛʟᴇ : {0}\nDᴜʀᴀᴛɪᴏɴ : {1}\nRᴇǫᴜᴇsᴛᴇᴅ Bʏ : {2}\n\n".format(
                x["title"], x["dur"], x["by"]
            )
    if "Queued" in msg:
        if len(msg) < 700:
            await asyncio.sleep(1)
            return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)
        link = await Pastebin(msg)
        if not link:
            return await CallbackQuery.message.reply_text("ғᴀɪʟᴇᴅ ᴛᴏ ғᴇᴛᴄʜ ǫᴜᴇᴜᴇ ʟɪsᴛ ...")
        med = InputMediaPhoto(
            media=link,
            caption="<u>**ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs :</u>**  [ᴄʜᴇᴄᴋᴏᴜᴛ ᴍᴏʀᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ғʀᴏᴍ ʜᴇʀᴇ]({0})".format(link),
        )
        await CallbackQuery.edit_message_media(media=med, reply_markup=buttons)
    else:
        await asyncio.sleep(1)
        return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)


@app.on_callback_query(filters.regex("queue_back_timer") & ~BANNED_USERS)
async def queue_back(_, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cp = callback_data.split(None, 1)[1]
    try:
        chat_id = CallbackQuery.message.chat.id
    except:
        return
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer("ʙᴏᴛ ɪsɴ'ᴛ sᴛʀᴇᴀᴍɪɴɢ ...", show_alert=True)
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer("ǫᴜᴇᴜᴇᴅ ʟɪsᴛ ɪs ᴇᴍᴘᴛʏ ...", show_alert=True)
    await CallbackQuery.answer("ɢᴇᴛᴛɪɴɢ ʙᴀᴄᴋ ...", show_alert=True)

    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    if ("live_" in file) or ("vid_" in file):
        IMAGE = await gen_thumb(videoid)
    elif "index_" in file:
        IMAGE = STREAM_IMG
    else:
        if videoid == "telegram":
            IMAGE = STREAM_IMG if typo == "Audio" else STREAM_IMG
        else:
            IMAGE = await gen_thumb(videoid)

    cap = f"""**{app.mention} ᴩʟᴀʏᴇʀ**

**Tɪᴛʟᴇ:** {title[:27]}
**Dᴜʀᴀᴛɪᴏɴ:** {DUR}
**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** {user}

ᴄʟɪᴄᴋ ᴏɴ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ᴡʜᴏʟᴇ ǫᴜᴇᴜᴇᴅ ʟɪsᴛ."""
    upl = queue_markup(cp, videoid)
    basic[videoid] = True
    med = InputMediaPhoto(media=IMAGE, caption=cap)
    await CallbackQuery.edit_message_media(media=med, reply_markup=upl)


@app.on_callback_query(filters.regex("MainMarkup") & ~BANNED_USERS)
async def del_back_playlist(_, CallbackQuery: CallbackQuery):
    await CallbackQuery.answer()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    videoid, chat_id = callback_request.split("|")
    if videoid == str(None):
        buttons = telegram_markup(chat_id)
    else:
        buttons = stream_markup(videoid, chat_id)
    chat_id = CallbackQuery.message.chat.id
    try:
        await CallbackQuery.edit_message_reply_markup(InlineKeyboardMarkup(buttons))
    except:
        return
    if chat_id not in checker:
        checker[chat_id] = {}
    checker[chat_id][CallbackQuery.message.id] = True


@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
async def settings_back_markup(_, CallbackQuery: CallbackQuery):
    try:
        await CallbackQuery.answer()
    except:
        pass
    if CallbackQuery.message.chat.type == ChatType.PRIVATE:
        buttons = private_panel()
        return await CallbackQuery.edit_message_text(
            """
Hello, My name is {0}.

I'm a telegram streaming bot with some useful features. 
Supporting platforms like Youtube, Spotify, Resso, AppleMusic , Soundcloud etc.
Feel free to add me to your groups.""".format(app.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    else:
        buttons = setting_markup()
        return await CallbackQuery.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(buttons)
        )


@app.on_callback_query(filters.regex("forceclose"))
async def forceclose_command(_, CallbackQuery: CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    query, user_id = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer("You're not allowed to close this ...", show_alert=True)
        except:
            return
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        return
