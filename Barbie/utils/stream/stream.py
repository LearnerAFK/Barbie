import os
import config
from pyrogram.types import InlineKeyboardMarkup
from typing import Union
from random import randint
from Barbie.platforms import YouTube, Carbon
from Barbie import app
from Barbie.misc import db
from Barbie.core.call import CallMusic
from Barbie.utils.pastebin import Pastebin
from Barbie.utils.exceptions import AssistantErr
from Barbie.utils.thumbnails import gen_thumb
from Barbie.utils.stream.queue import put_queue, put_queue_index
from Barbie.utils.database import is_active_chat, is_video_allowed
from Barbie.utils.inline.play import close_keyboard, stream_markup, telegram_markup


async def stream(
    mystic,
    user_id,
    result,
    chat_id,
    user_name,
    original_chat_id,
    video: Union[bool, str] = None,
    streamtype: Union[bool, str] = None,
    spotify: Union[bool, str] = None,
    forceplay: Union[bool, str] = None,
):
    if not result:
        return
    if video:
        if not await is_video_allowed(chat_id):
            raise AssistantErr("ʙᴏᴛ ᴏɴʟʏ ᴀʟʟᴏᴡs ʟɪᴍɪᴛᴇᴅ ɴᴜᴍʙᴇʀ ᴏꜰ ᴠɪᴅᴇᴏ ᴄᴀʟʟs ᴅᴜᴇ ᴛᴏ ᴄᴘᴜ ᴏᴠᴇʀʟᴏᴀᴅ ɪssᴜᴇs ...")
    if forceplay:
        await CallMusic.force_stop_stream(chat_id)
    if streamtype == "playlist":
        msg = f"ǫᴜᴇᴜᴇᴅ ᴘʟᴀʏʟɪsᴛ :\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_FETCH_LIMIT:
                continue
            try:
                (
                    title,
                    duration_min,
                    duration_sec,
                    thumbnail,
                    vidid,
                ) = await YouTube.details(
                    search, False if spotify else True
                )
            except:
                continue
            if str(duration_min) == "None":
                continue
            if duration_sec > config.DURATION_LIMIT:
                continue
            if await is_active_chat(chat_id):
                await put_queue(
                    chat_id,
                    original_chat_id,
                    f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                )
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}- {title[:70]}\n"
                msg += f"ᴘᴏsɪᴛɪᴏɴ :- {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                try:
                    file_path, direct = await YouTube.download(vidid, mystic, video=status, videoid=True)
                except:
                    raise AssistantErr("ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ ᴛʀᴀᴄᴋ ᴅᴇᴛᴀɪʟs ...")
                await CallMusic.join_call(chat_id, original_chat_id, file_path, video=status)
                await put_queue(
                    chat_id,
                    original_chat_id,
                    file_path if direct else f"vid_{vidid}",
                    title,
                    duration_min,
                    user_name,
                    vidid,
                    user_id,
                    "video" if video else "audio",
                    forceplay=forceplay,
                )
                img = await gen_thumb(vidid)
                button = stream_markup(vidid, chat_id)
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** `{3}`".format(
                        title[:27],
                        f"https://t.me/{app.username}?start=info_{vidid}",
                        duration_min,
                        user_name,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
        if count == 0:
            return
        else:
            link = await Pastebin(msg)
            lines = msg.count("\n")
            if lines >= 17:
                car = os.linesep.join(msg.split(os.linesep)[:17])
            else:
                car = msg
            carbon = await Carbon.generate(car, randint(100, 10000000))
            return await app.send_photo(
                original_chat_id,
                photo=carbon,
                caption="ᴀᴅᴅᴇᴅ {0} ᴛʀᴀᴄᴋs ᴛᴏ ǫᴜᴇᴜᴇ : [ᴄʜᴇᴄᴋ]({1})".format(position, link),
                reply_markup=close_keyboard,
            )
    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        status = True if video else None
        try:
            file_path, direct = await YouTube.download(vidid, mystic, videoid=True, video=status)
        except:
            raise AssistantErr("ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ ᴛʀᴀᴄᴋ ᴅᴇᴛᴀɪʟs ...")
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await app.send_message(
                original_chat_id,
                "**Aᴅᴅᴇᴅ Tᴏ Qᴜᴇᴜᴇ Aᴛ #{0}**\n\n**Tɪᴛʟᴇ :** `{1}`\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** `{3}`".format(
                    position, title[:30], duration_min, user_name
                ),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await CallMusic.join_call(chat_id, original_chat_id, file_path, video=status)
            await put_queue(
                chat_id,
                original_chat_id,
                file_path if direct else f"vid_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid)
            button = stream_markup(vidid, chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** `{3}`".format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
    elif streamtype == "live":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = "00:00"
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await app.send_message(
                original_chat_id,
                "**Aᴅᴅᴇᴅ Tᴏ Qᴜᴇᴜᴇ Aᴛ #{0}**\n\n**Tɪᴛʟᴇ :** `{1}`\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** `{3}`".format(position, title[:30], duration_min, user_name),
            )
        else:
            if not forceplay:
                db[chat_id] = []
            n, file_path = await YouTube.video(link)
            if n == 0:
                raise AssistantErr("ᴜɴᴀʙʟᴇ ᴛᴏ sᴛʀᴇᴀᴍ ʏᴏᴜᴛᴜʙᴇ ʟɪᴠᴇ sᴛʀᴇᴀᴍs ...")
            await CallMusic.join_call(chat_id, original_chat_id, file_path, video=status)
            await put_queue(
                chat_id,
                original_chat_id,
                f"live_{vidid}",
                title,
                duration_min,
                user_name,
                vidid,
                user_id,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            img = await gen_thumb(vidid)
            button = telegram_markup(chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=img,
                caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** `{3}`".format(
                    title[:27],
                    f"https://t.me/{app.username}?start=info_{vidid}",
                    duration_min,
                    user_name,
                ),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
    elif streamtype == "index":
        link = result
        title = "Index or M3u8 Link"
        duration_min = "URL stream"
        if await is_active_chat(chat_id):
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
            )
            position = len(db.get(chat_id)) - 1
            await mystic.edit_text(
                "**Aᴅᴅᴇᴅ Tᴏ Qᴜᴇᴜᴇ Aᴛ #{0}**\n\n**Tɪᴛʟᴇ :** `{1}`\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** `{3}`".format(position, title[:30], duration_min, user_name)
            )
        else:
            if not forceplay:
                db[chat_id] = []
            await CallMusic.join_call(chat_id, original_chat_id, link, video=True if video else None,)
            await put_queue_index(
                chat_id,
                original_chat_id,
                "index_url",
                title,
                duration_min,
                user_name,
                link,
                "video" if video else "audio",
                forceplay=forceplay,
            )
            button = telegram_markup(chat_id)
            run = await app.send_photo(
                original_chat_id,
                photo=config.STREAM_IMG,
                caption="**sᴛʀᴇᴀᴍ ᴛʏᴘᴇ :** `ʟɪᴠᴇ sᴛʀᴇᴀᴍ [ᴜʀʟ]`\n**ʀᴇǫᴜᴇsᴛᴇᴅ ʙʏ:** `{0}`".format(user_name),
                reply_markup=InlineKeyboardMarkup(button),
            )
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await mystic.delete()
