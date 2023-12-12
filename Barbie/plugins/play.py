import config
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup
from pytgcalls.exceptions import NoActiveGroupCall
from ..core.call import CallMusic
from ..utils.stream.stream import stream as streams
from Barbie import app, YouTube, Spotify, Telegram
from ..utils import (
    PlayWrapper, is_video_allowed,
    formats, play_logs, botplaylist_markup, 
    time_to_seconds, livestream_markup, 
    track_markup, slider_markup, seconds_to_min)


__MODULE__ = "Mᴜsɪᴄ"
__HELP__ = """
/play ᴏʀ /vplay : sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ.
/playforce ᴏʀ /vplayforce : **ғᴏʀᴄᴇ ᴩʟᴀʏ** sᴛᴏᴩs ᴛʜᴇ ᴏɴɢᴏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛs sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ʀᴇǫᴜᴇsᴛᴇᴅ ᴛʀᴀᴄᴋ./pause : ᴩᴀᴜsᴇ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.
/resume : ʀᴇsᴜᴍᴇ ᴛʜᴇ ᴩᴀᴜsᴇᴅ sᴛʀᴇᴀᴍ.
/restart : ʀᴇsᴛᴀʀᴛ ʙᴏᴛ ғᴏʀ ʏᴏᴜʀ ᴄʜᴀᴛ
/skip : sᴋɪᴩ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ᴀɴᴅ sᴛᴀʀᴛ sᴛʀᴇᴀᴍɪɴɢ ᴛʜᴇ ɴᴇxᴛ ᴛʀᴀᴄᴋ ɪɴ ǫᴜᴇᴜᴇ.
/end ᴏʀ /stop : ᴄʟᴇᴀʀs ᴛʜᴇ ǫᴜᴇᴜᴇ ᴀɴᴅ ᴇɴᴅ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ.
/player ᴏʀ /queue : ɢᴇᴛ ᴀɴ ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴩʟᴀʏᴇʀ ᴩᴀɴᴇʟ ᴏʀ sʜᴏᴡs ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs ʟɪsᴛ
/loop [ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ] ᴏʀ [ʙᴇᴛᴡᴇᴇɴ 1:10] : ᴡʜᴇɴ ᴀᴄᴛɪᴠᴀᴛᴇᴅ ʙᴏᴛ ᴡɪʟʟ ᴩʟᴀʏ ᴛʜᴇ ᴄᴜʀʀᴇɴᴛ ᴩʟᴀʏɪɴɢ sᴛʀᴇᴀᴍ ɪɴ ʟᴏᴏᴩ ғᴏʀ 10 ᴛɪᴍᴇs ᴏʀ ᴛʜᴇ ɴᴜᴍʙᴇʀ ᴏғ ʀᴇǫᴜᴇsᴛᴇᴅ ʟᴏᴏᴩs.
/shuffle : sʜᴜғғʟᴇ ᴛʜᴇ ǫᴜᴇᴜᴇᴅ ᴛʀᴀᴄᴋs.
/seek : sᴇᴇᴋ ᴛʜᴇ sᴛʀᴇᴀᴍ ᴛᴏ ᴛʜᴇ ɢɪᴠᴇɴ Dᴜʀᴀᴛɪᴏɴ.
"""


PLAY_COMMAND = ["play", "vplay", "playforce", "vplayforce"]


@app.on_message(filters.command(PLAY_COMMAND) & filters.group & ~BANNED_USERS)
@PlayWrapper
async def play_commnd(_, message: Message, chat_id, video, playmode, url, fplay):
    mystic = await message.reply_text("🔄 ᴘʀᴏᴄᴇssɪɴɢ ǫᴜᴇʀʏ ...")
    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    audio_telegram = (
        (
            message.reply_to_message.audio
            or message.reply_to_message.voice
        )
        if message.reply_to_message
        else None
    )
    video_telegram = (
        (
            message.reply_to_message.video
            or message.reply_to_message.document
        )
        if message.reply_to_message
        else None
    )
    if audio_telegram:
        if audio_telegram.file_size > config.TG_AUDIO_FILESIZE_LIMIT:
            return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ᴀᴜᴅɪᴏ ғɪʟᴇ ...")
        duration_min = seconds_to_min(audio_telegram.duration)
        if (audio_telegram.duration) > config.DURATION_LIMIT:
            return await mystic.edit_text(
                "**ᴅᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ**\n\n**ᴀʟʟᴏᴡᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ : **{0} ᴍɪɴᴜᴛᴇ(s)\n**ʀᴇᴄᴇɪᴠᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ :** {1} ʜᴏᴜʀ(s)".format(
                    config.DURATION_LIMIT_MIN, duration_min
                )
            )
        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }

            try:
                await streams(
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                print(f"[ERROR] : {e}")
                ex_type = type(e).__name__
                err = (
                    e
                    if ex_type == "AssistantErr"
                    else "sᴏᴍᴇ **ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ** ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ ...\n\nᴇxᴄᴇᴘᴛɪᴏɴ ᴛʏᴘᴇ :- {0}".format(ex_type)
                )
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif video_telegram:
        if not await is_video_allowed(message.chat.id):
            return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
        if message.reply_to_message.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in formats:
                    return await mystic.edit_text(
                         "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴇxᴛᴇɴsɪᴏɴ !\n\n**sᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛs :** {0}".format(f"{' | '.join(formats)}")
                    )
            except:
                return await mystic.edit_text(
                     "ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ ᴠɪᴅᴇᴏ ғɪʟᴇ ᴇxᴛᴇɴsɪᴏɴ !\n\n**sᴜᴘᴘᴏʀᴛᴇᴅ ғᴏʀᴍᴀᴛs :** {0}".format(f"{' | '.join(formats)}")
                )
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text("Video File Size Should Be Less Than 1 GiB")
        file_path = await Telegram.get_filepath(video=video_telegram)
        
        if await Telegram.download(message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(video_telegram)
            dur = await Telegram.get_duration(video_telegram)
            details = {
                "title": file_name,
                "link": message_link,
                "path": file_path,
                "dur": dur,
            }
            try:
                await streams(
                    mystic,
                    user_id,
                    details,
                    chat_id,
                    user_name,
                    message.chat.id,
                    video=True,
                    streamtype="telegram",
                    forceplay=fplay,
                )
            except Exception as e:
                print(f"[ERROR] : {e}")
                ex_type = type(e).__name__
                err = (
                    e
                    if ex_type == "AssistantErr"
                    else "sᴏᴍᴇ **ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ** ᴡʜɪʟᴇ ᴘʀᴏᴄᴇssɪɴɢ ʏᴏᴜʀ ǫᴜᴇʀʏ ...\n\nᴇxᴄᴇᴘᴛɪᴏɴ ᴛʏᴘᴇ:- {0}".format(ex_type)
                )
                return await mystic.edit_text(err)
            return await mystic.delete()
        return
    elif url:
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(
                        url,
                        config.PLAYLIST_FETCH_LIMIT,
                        message.from_user.id,
                    )
                except Exception as e:
                    print(f"[ERROR] : {e}")
                    return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
                streamtype = "playlist"
                plist_type = "yt"
                if "&" in url:
                    plist_id = (url.split("=")[1]).split("&")[0]
                else:
                    plist_id = url.split("=")[1]
                img = config.STREAM_IMG
                cap = "**ʏᴏᴜᴛᴜʙᴇ ᴘʟᴀʏʟɪsᴛ ғᴇᴀᴛᴜʀᴇ**\n\nsᴇʟᴇᴄᴛ ᴛʜᴇ ᴍᴏᴅᴇ ɪɴ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴘʟᴀʏ ᴡʜᴏʟᴇ ʏᴏᴜᴛᴜʙᴇ ᴘʟᴀʏʟɪsᴛ"
            else:
                try:
                    details, track_id = await YouTube.track(url)
                except Exception as e:
                    print(f"[ERROR] : {e}")
                    return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
                streamtype = "youtube"
                img = details["thumb"]
                cap = "📎Title: **{0}\n\n⏳Duration:** {1} Mins".format(
                    details["title"],
                    details["duration_min"],
                )
        elif await Spotify.valid(url):
            spotify = True
            if (
                not config.SPOTIFY_CLIENT_ID
                and not config.SPOTIFY_CLIENT_SECRET
            ):
                return await mystic.edit_text(
                    "This bot isn't able to play spotify queries. Please ask my owner to enable spotify."
                )
            if "track" in url:
                try:
                    details, track_id = await Spotify.track(url)
                except Exception:
                    return await mystic.edit_text("Failed to Process Query !")
                streamtype = "youtube"
                img = details["thumb"]
                cap = "📎Title: **{0}\n\n⏳Duration:** {1} Mins".format(
                    details["title"], details["duration_min"]
                )
            elif "playlist" in url:
                try:
                    details, plist_id = await Spotify.playlist(url)
                except Exception:
                    return await mystic.edit_text("Failed to Process Query !")
                streamtype = "playlist"
                plist_type = "spplay"
                img = config.SPOTIFY_PLAYLIST_IMG_URL
                cap = "**Spotify Play Mode**\n\nRequested By:- {0}".format(
                    message.from_user.first_name
                )
            elif "album" in url:
                try:
                    details, plist_id = await Spotify.album(url)
                except Exception:
                    return await mystic.edit_text("Failed to Process Query !")
                streamtype = "playlist"
                plist_type = "spalbum"
                img = config.SPOTIFY_ALBUM_IMG_URL
                cap = "**Spotify Play Mode**\n\nRequested By:- {0}".format(
                    message.from_user.first_name
                )
            elif "artist" in url:
                try:
                    details, plist_id = await Spotify.artist(url)
                except Exception:
                    return await mystic.edit_text("Failed to Process Query !")
                streamtype = "playlist"
                plist_type = "spartist"
                img = config.SPOTIFY_ARTIST_IMG_URL
                cap = "**Spotify Play Mode**\n\nRequested By:- {0}".format(
                    message.from_user.first_name
                )
            else:
                return await mystic.edit_text("Unable to play this type of spotify query !")
      
        else:
            try:
                await CallMusic.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text("There's an issue with the bot ...")
                return
            except Exception as e:
                print(f"[ERROR] : {e}")
                await mystic.delete()
                return 
            await mystic.edit_text("✅ ᴠᴀʟɪᴅ sᴛʀᴇᴀᴍ ᴠᴇʀɪғɪᴇᴅ ...")
            try:
                await streams(
                    mystic,
                    message.from_user.id,
                    url,
                    chat_id,
                    message.from_user.first_name,
                    message.chat.id,
                    video=video,
                    streamtype="index",
                    forceplay=fplay,
                )
            except Exception as e:
                print(f"[ERROR] : {e}")
                return await mystic.delete()
            return await play_logs(message, streamtype="M3u8 or Index Link")
    else:
        if len(message.command) < 2:
            buttons = botplaylist_markup()
            return await mystic.edit_text(
                "**ᴜsᴀɢᴇ:** /play [ᴍᴜsɪᴄ ɴᴀᴍᴇ ᴏʀ ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ ᴏʀ ʀᴇᴘʟʏ ᴛᴏ ᴀᴜᴅɪᴏ]",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")
        try:
            details, track_id = await YouTube.track(query)
        except Exception:
            return await mystic.edit_text("ғᴀɪʟᴇᴅ ᴛᴏ ᴘʀᴏᴄᴇss ǫᴜᴇʀʏ !")
        streamtype = "youtube"
    if str(playmode) == "Direct":
        if not plist_type:
            if details["duration_min"]:
                duration_sec = time_to_seconds(
                    details["duration_min"]
                )
                if duration_sec > config.DURATION_LIMIT:
                    return await mystic.edit_text(
                        "**ᴅᴜʀᴀᴛɪᴏɴ ʟɪᴍɪᴛ ᴇxᴄᴇᴇᴅᴇᴅ**\n\n**ᴀʟʟᴏᴡᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ **{0} ᴍɪɴᴜᴛᴇ(s)\n**ʀᴇᴄᴇɪᴠᴇᴅ ᴅᴜʀᴀᴛɪᴏɴ :** {1} ʜᴏᴜʀ(s)".format(
                            config.DURATION_LIMIT_MIN,
                            details["duration_min"],
                        )
                    )
            else:
                buttons = livestream_markup(
                    track_id,
                    user_id,
                    "v" if video else "a",
                    "f" if fplay else "d",
                )
                return await mystic.edit_text(
                    "**ʟɪᴠᴇ sᴛʀᴇᴀᴍ ᴅᴇᴛᴇᴄᴛᴇᴅ ...**",
                    reply_markup=InlineKeyboardMarkup(buttons),
                )
        try:
           await streams(
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                message.chat.id,
                video=video,
                streamtype=streamtype,
                spotify=spotify,
                forceplay=fplay,
            )
        except Exception as e:
            print(f"[ERROR] : {e}")
            return await mystic.delete()
        await mystic.delete()
        return await play_logs(message, streamtype=streamtype)
    else:
        if slider:
            buttons = slider_markup(
                track_id,
                message.from_user.id,
                query,
                0,
                "f" if fplay else "d",
            )
            await mystic.delete()
            await message.reply_photo(
                photo=details["thumb"],
                caption="📎Title: **{0}\n\n⏳Duration:** {1} Mins".format(
                    details["title"].title(),
                    details["duration_min"],
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return await play_logs(message, streamtype=f"Searched on Youtube")
        else:
            buttons = track_markup(
                track_id,
                message.from_user.id,
                "f" if fplay else "d",
            )
            await mystic.delete()
            await message.reply_photo(
                photo=img,
                caption=cap,
                reply_markup=InlineKeyboardMarkup(buttons),
            )
            return await play_logs(message, streamtype=f"URL Searched Inline")
