import config
from datetime import datetime, timedelta
from typing import Union
from pyrogram import Client
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from pyrogram.types import InlineKeyboardMarkup
from pytgcalls import PyTgCalls
from pytgcalls.exceptions import (
    AlreadyJoinedError,
    NoActiveGroupCall,
    TelegramServerError,
)
from Barbie import app
from ..platforms import YouTube
from pytgcalls.types import JoinedGroupCallParticipant, LeftGroupCallParticipant, Update
from pytgcalls.types.input_stream import AudioPiped, AudioVideoPiped
from pytgcalls.types.stream import StreamAudioEnded
from ..misc import db
from ..utils.exceptions import AssistantErr
from ..utils.inline.play import stream_markup, telegram_markup
from ..utils.stream.autoclear import auto_clean
from ..utils.thumbnails import gen_thumb
from ..utils.database import (
    add_active_chat, add_active_video_chat,
    get_assistant, get_audio_bitrate,
    get_loop, get_video_bitrate,
    group_assistant, is_autoend,
    music_on, mute_off, set_loop,
    remove_active_chat,
    remove_active_video_chat,
)


autoend = {}
counter = {}
AUTO_END_TIME = 1


async def _clear_(chat_id):
    db[chat_id] = []
    await remove_active_video_chat(chat_id)
    await remove_active_chat(chat_id)


class Call(PyTgCalls):
    def __init__(self):
        self.userbot1 = Client(
            name="Learner",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
        )
        self.one = PyTgCalls(
            self.userbot1,
            cache_duration=100,
        )
        self.userbot2 = Client(
            name="Learner2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
        )
        self.two = PyTgCalls(
            self.userbot2,
            cache_duration=100,
        )
        self.userbot3 = Client(
            name="Learner3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
        )
        self.three = PyTgCalls(
            self.userbot3,
            cache_duration=100,
        )


    async def pause_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.pause_stream(chat_id)


    async def resume_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        await assistant.resume_stream(chat_id)


    async def stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            await _clear_(chat_id)
            await assistant.leave_group_call(chat_id)
        except:
            pass


    async def force_stop_stream(self, chat_id: int):
        assistant = await group_assistant(self, chat_id)
        try:
            check = db.get(chat_id)
            check.pop(0)
        except:
            pass
        await remove_active_video_chat(chat_id)
        await remove_active_chat(chat_id)
        try:
            await assistant.leave_group_call(chat_id)
        except:
            pass


    async def skip_stream(
        self, chat_id: int, link: str, video: Union[bool, str] = None
    ):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(link, audio_parameters=audio_stream_quality)
        )
        await assistant.change_stream(chat_id, stream)


    async def seek_stream(self, chat_id, file_path, to_seek, duration, mode):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
                additional_ffmpeg_parameters=f"-ss {to_seek} -t {duration}",
            )
            if mode == "video"
            else AudioPiped(
                file_path,
                audio_parameters=audio_stream_quality,
                additional_ffmpeg_parameters=f"-ss {to_seek} -t {duration}",
            )
        )
        await assistant.change_stream(chat_id, stream)


    async def stream_call(self, link):
        assistant = await group_assistant(self, config.LOG_GROUP_ID)
        await assistant.join_group_call(
            config.LOG_GROUP_ID,
            AudioVideoPiped(link),
        )
        await assistant.leave_group_call(config.LOG_GROUP_ID)


    async def join_assistant(self, original_chat_id, chat_id):
        userbot = await get_assistant(chat_id)
        try:
            try:
                get = await app.get_chat_member(chat_id, userbot.id)
            except ChatAdminRequired:
                raise AssistantErr("ʙᴏᴛ ʀᴇǫᴜɪʀᴇs **ᴀᴅᴍɪɴ** ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ...")
            if (
                get.status == ChatMemberStatus.BANNED
                or get.status == ChatMemberStatus.LEFT
            ):
                raise AssistantErr(
                    "ᴀssɪsᴛᴀɴᴛ ɪs ʙᴀɴɴᴇᴅ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴏʀ ᴄʜᴀɴɴᴇʟ, ᴘʟᴇᴀsᴇ ᴜɴʙᴀɴ ...\n\n**ᴀssɪsᴛᴀɴᴛ ᴜsᴇʀɴᴀᴍᴇ :** @{0}\n**ᴀssɪsᴛᴀɴᴛ ɪᴅ :** {1}".format(
                        userbot.username, userbot.id
                    )
                )
        except UserNotParticipant:
            chat = await app.get_chat(chat_id)
            if chat.username:
                try:
                    await userbot.join_chat(chat.username)
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    raise AssistantErr(
                        "ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ...\n\n**ʀᴇᴀsᴏɴ**: {0}".format(e)
                    )
            else:
                try:
                    try:
                        try:
                            invitelink = chat.invite_link
                            if invitelink is None:
                                invitelink = await app.export_chat_invite_link(chat_id)
                        except:
                            invitelink = await app.export_chat_invite_link(chat_id)
                    except ChatAdminRequired:
                        raise AssistantErr(
                            "ʙᴏᴛ ʀᴇǫᴜɪʀᴇs **ɪɴᴠɪᴛᴇ ᴜsᴇʀs ᴠɪᴀ ʟɪɴᴋ** ᴘᴇʀᴍɪssɪᴏɴ ᴛᴏ ɪɴᴠɪᴛᴇ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ɢʀᴏᴜᴘ ..."
                        )
                    except Exception as e:
                        raise AssistantErr(e)
                    m = await app.send_message(original_chat_id, "ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴡɪʟʟ ʙᴇ ᴊᴏɪɴɪɴɢ ...")
                    if invitelink.startswith("https://t.me/+"):
                        invitelink = invitelink.replace("https://t.me/+", "https://t.me/joinchat/")
                    await userbot.join_chat(invitelink)
                    await m.edit("ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ[{0}] ᴊᴏɪɴᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ...".format(userbot.name))
                except UserAlreadyParticipant:
                    pass
                except Exception as e:
                    raise AssistantErr(
                        "ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ ᴡʜɪʟᴇ ɪɴᴠɪᴛɪɴɢ ᴀssɪsᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ...\n\n**ʀᴇᴀsᴏɴ**: {0}".format(e)
                    )


    async def join_call(
        self,
        chat_id: int,
        original_chat_id: int,
        link,
        video: Union[bool, str] = None,
    ):
        assistant = await group_assistant(self, chat_id)
        audio_stream_quality = await get_audio_bitrate(chat_id)
        video_stream_quality = await get_video_bitrate(chat_id)
        stream = (
            AudioVideoPiped(
                link,
                audio_parameters=audio_stream_quality,
                video_parameters=video_stream_quality,
            )
            if video
            else AudioPiped(link, audio_parameters=audio_stream_quality)
        )
        try:
            await assistant.join_group_call(chat_id, stream)
        except NoActiveGroupCall:
            try:
                await self.join_assistant(original_chat_id, chat_id)
            except Exception as e:
                raise e
            try:
                await assistant.join_group_call(chat_id, stream)
            except Exception as e:
                raise AssistantErr("ᴘʟᴇᴀsᴇ ᴍᴀᴋᴇ sᴜʀᴇ ɢʀᴏᴜᴘ's **ᴠᴏɪᴄᴇ ᴄʜᴀᴛ** ɪs ᴇɴᴀʙʟᴇᴅ ...")
        except AlreadyJoinedError:
            raise AssistantErr(
                "**ᴀssɪsᴛᴀɴᴛ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ**\n\nᴘʟᴇᴀsᴇ ᴇɴᴅ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀɴᴅ sᴛᴀʀᴛ ғʀᴇsʜ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀɢᴀɪɴ ᴀɴᴅ ɪғ ᴛʜᴇ  ᴘʀᴏʙʟᴇᴍ ᴄᴏɴᴛɪɴᴜᴇs, ᴛʀʏ /restart"
            )
        except TelegramServerError:
            raise AssistantErr("**ᴛᴇʟᴇɢʀᴀᴍ sᴇʀᴠᴇʀ ᴇʀʀᴏʀ**\n\nᴘʟᴇᴀsᴇ ᴇɴᴅ ʏᴏᴜʀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀɴᴅ sᴛᴀʀᴛ ғʀᴇsʜ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ᴀɢᴀɪɴ ...")
        await add_active_chat(chat_id)
        await mute_off(chat_id)
        await music_on(chat_id)
        if video:
            await add_active_video_chat(chat_id)
        if await is_autoend():
            counter[chat_id] = {}
            users = len(await assistant.get_participants(chat_id))
            if users == 1:
                autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)


    async def change_stream(self, client, chat_id):
        check = db.get(chat_id)
        popped = None
        loop = await get_loop(chat_id)
        try:
            if loop == 0:
                popped = check.pop(0)
            else:
                loop = loop - 1
                await set_loop(chat_id, loop)
            if popped:
                if config.AUTO_DOWNLOADS_CLEAR == str(True):
                    await auto_clean(popped)
            if not check:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
        except:
            try:
                await _clear_(chat_id)
                return await client.leave_group_call(chat_id)
            except:
                return
        else:
            queued = check[0]["file"]
            title = (check[0]["title"]).title()
            user = check[0]["by"]
            original_chat_id = check[0]["chat_id"]
            streamtype = check[0]["streamtype"]
            audio_stream_quality = await get_audio_bitrate(chat_id)
            video_stream_quality = await get_video_bitrate(chat_id)
            videoid = check[0]["vidid"]
            check[0]["played"] = 0
            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)
                if n == 0:
                    return await app.send_message(original_chat_id, text="**ғᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ** ...")
                stream = (
                    AudioVideoPiped(
                        link,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                    if str(streamtype) == "video"
                    else AudioPiped(link, audio_parameters=audio_stream_quality)
                )
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(original_chat_id, text="**ғᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ** ...")
                img = await gen_thumb(videoid)
                button = telegram_markup(chat_id)
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                        title[:32],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            elif "vid_" in queued:
                mystic = await app.send_message(original_chat_id, "**ᴅᴏᴡɴʟᴏᴀᴅɪɴɢ ɴᴇxᴛ ᴛʀᴀᴄᴋ ғʀᴏᴍ ᴘʟᴀʏʟɪsᴛ** ...")
                try:
                    file_path, direct = await YouTube.download(
                        videoid,
                        mystic,
                        videoid=True,
                        video=True if str(streamtype) == "video" else False,
                    )
                except:
                    return await mystic.edit_text("**ғᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ** ...")
                stream = (
                    AudioVideoPiped(
                        file_path,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                    if str(streamtype) == "video"
                    else AudioPiped(
                        file_path,
                        audio_parameters=audio_stream_quality,
                    )
                )
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(original_chat_id, text="**ғᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ** ...")
                img = await gen_thumb(videoid)
                button = stream_markup(videoid, chat_id)
                await mystic.delete()
                run = await app.send_photo(
                    original_chat_id,
                    photo=img,
                    caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                        title[:32],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
            elif "index_" in queued:
                stream = (
                    AudioVideoPiped(
                        videoid,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                    if str(streamtype) == "video"
                    else AudioPiped(videoid, audio_parameters=audio_stream_quality)
                )
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(original_chat_id, text="**ғᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ** ...")
                button = telegram_markup(chat_id)
                run = await app.send_photo(
                    original_chat_id,
                    photo=config.STREAM_IMG,
                    caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                        title[:32],
                        f"https://t.me/{app.username}?start=info_{videoid}",
                        check[0]["dur"],
                        user,
                    ),
                    reply_markup=InlineKeyboardMarkup(button),
                )
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "tg"
            else:
                stream = (
                    AudioVideoPiped(
                        queued,
                        audio_parameters=audio_stream_quality,
                        video_parameters=video_stream_quality,
                    )
                    if str(streamtype) == "video"
                    else AudioPiped(queued, audio_parameters=audio_stream_quality)
                )
                try:
                    await client.change_stream(chat_id, stream)
                except Exception:
                    return await app.send_message(original_chat_id, text="**ғᴀɪʟᴇᴅ ᴛᴏ sᴡɪᴛᴄʜ sᴛʀᴇᴀᴍ** ...")
                if videoid == "telegram":
                    button = telegram_markup(chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=config.STREAM_IMG
                        if str(streamtype) == "audio"
                        else config.STREAM_IMG,
                        caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                            title[:32],
                            f"https://t.me/{app.username}?start=info_{videoid}",
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "tg"
                else:
                    img = await gen_thumb(videoid)
                    button = stream_markup(videoid, chat_id)
                    run = await app.send_photo(
                        original_chat_id,
                        photo=img,
                        caption="**Tɪᴛʟᴇ :** [{0}]({1})\n**Dᴜʀᴀᴛɪᴏɴ :** `{2}` ᴍɪɴs\n**Rᴇǫᴜᴇsᴛᴇᴅ Bʏ :** {3}".format(
                            title[:32],
                            f"https://t.me/{app.username}?start=info_{videoid}",
                            check[0]["dur"],
                            user,
                        ),
                        reply_markup=InlineKeyboardMarkup(button),
                    )
                    db[chat_id][0]["mystic"] = run
                    db[chat_id][0]["markup"] = "stream"


    async def ping(self):
        pings = []
        if config.STRING1:
            pings.append(await self.one.ping)
        if config.STRING2:
            pings.append(await self.two.ping)
        if config.STRING3:
            pings.append(await self.three.ping)
        return str(round(sum(pings) / len(pings), 3))


    async def start(self):
        if config.STRING1:
            await self.one.start()
        if config.STRING2:
            await self.two.start()
        if config.STRING3:
            await self.three.start()


    async def decorators(self):
        @self.one.on_kicked()
        @self.two.on_kicked()
        @self.three.on_kicked()
        @self.one.on_closed_voice_chat()
        @self.two.on_closed_voice_chat()
        @self.three.on_closed_voice_chat()
        @self.one.on_left()
        @self.two.on_left()
        @self.three.on_left()
        async def stream_services_handler(_, chat_id: int):
            await self.stop_stream(chat_id)

        @self.one.on_stream_end()
        @self.two.on_stream_end()
        @self.three.on_stream_end()
        async def stream_end_handler(client, update: Update):
            if not isinstance(update, StreamAudioEnded):
                return
            await self.change_stream(client, update.chat_id)

        @self.one.on_participants_change()
        @self.two.on_participants_change()
        @self.three.on_participants_change()
        async def participants_change_handler(client, update: Update):
            if not isinstance(update, JoinedGroupCallParticipant) and not isinstance(
                update, LeftGroupCallParticipant
            ):
                return
            chat_id = update.chat_id
            users = counter.get(chat_id)
            if not users:
                try:
                    got = len(await client.get_participants(chat_id))
                except:
                    return
                counter[chat_id] = got
                if got == 1:
                    autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                    return
                autoend[chat_id] = {}
            else:
                final = (
                    users + 1
                    if isinstance(update, JoinedGroupCallParticipant)
                    else users - 1
                )
                counter[chat_id] = final
                if final == 1:
                    autoend[chat_id] = datetime.now() + timedelta(minutes=AUTO_END_TIME)
                    return
                autoend[chat_id] = {}


CallMusic = Call()
