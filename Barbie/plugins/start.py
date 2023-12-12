import asyncio
import config
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from youtubesearchpython.__future__ import VideosSearch
from Barbie import app, HELPABLE, YouTube
from ..utils import add_served_user, page_load, get_userss, is_on_off, private_panel


loop = asyncio.get_running_loop()


@app.on_message(filters.command(["start", "help"]) & ~config.BANNED_USERS & ~filters.group & ~filters.forwarded)
async def private_start(app, message: Message):
    user_id = message.from_user.id
    await add_served_user(user_id)
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            buttons = page_load(0, HELPABLE, "help")
            return await message.reply_photo(
                photo=config.START_IMG,
                caption="ᴄʜᴏᴏsᴇ ᴛʜᴇ ᴄᴀᴛᴇɢᴏʀʏ ғᴏʀ ᴡʜɪᴄʜ ʏᴏᴜ ᴡᴀɴɴᴀ ɢᴇᴛ ʜᴇʟᴩ.\nᴀsᴋ ʏᴏᴜʀ ᴅᴏᴜʙᴛs ᴀᴛ @{}\n\n๏ ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : `/`".format(
                    config.SUPPORT_HEHE
                ),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        if name[0:4] == "song":
            return await message.reply_text(
                "**ᴜsᴀɢᴇ:**\n/song [ᴍᴜsɪᴄ ɴᴀᴍᴇ] ᴏʀ [ʏᴏᴜᴛᴜʙᴇ ʟɪɴᴋ]"
            )
        if name[0:3] == "sta":
            m = await message.reply_text(
                f"> ɢᴇᴛᴛɪɴɢ ʏᴏᴜʀ ᴩᴇʀsᴏɴᴀʟ sᴛᴀᴛs ғʀᴏᴍ {app.mention} sᴇʀᴠᴇʀ ..."
            )
            stats = await get_userss(user_id)
            tot = len(stats)
            if not stats:
                await asyncio.sleep(1)
                return await m.edit("ɴᴏ ᴜsᴇʀ sᴛᴀᴛs ꜰᴏᴜɴᴅ ...")

            def get_stats():
                msg = ""
                limit = 0
                results = {}
                for i in stats:
                    top_list = stats[i]["spot"]
                    results[str(i)] = top_list
                    list_arranged = dict(
                        sorted(
                            results.items(),
                            key=lambda item: item[1],
                            reverse=True,
                        )
                    )
                if not results:
                    return m.edit("ɴᴏ ᴜsᴇʀ sᴛᴀᴛs ꜰᴏᴜɴᴅ ...")
                tota = 0
                videoid = None
                for vidid, count in list_arranged.items():
                    tota += count
                    if limit == 10:
                        continue
                    if limit == 0:
                        videoid = vidid
                    limit += 1
                    details = stats.get(vidid)
                    title = (details["title"][:35]).title()
                    if vidid == "telegram":
                        msg += f"🔗 [ᴛᴇʟᴇɢʀᴀᴍ ᴍᴇᴅɪᴀ] ** ᴩʟᴀʏᴇᴅ {count} ᴛɪᴍᴇs**\n\n"
                    else:
                        msg += f"🔗 [{title}](https://www.youtube.com/watch?v={vidid}) ** ᴩʟᴀʏᴇᴅ {count} ᴛɪᴍᴇs**\n\n"
                msg = (
                    "ɢʀᴇᴇᴛɪɴɢs ! ʏᴏᴜ ʜᴀᴠᴇ ᴘʟᴀʏᴇᴅ **{0}** ᴛʀᴀᴄᴋs ᴛɪʟʟ ɴᴏᴡ ᴡɪᴛʜ ᴀ ᴡʜᴏᴘᴘɪɴɢ ᴄᴏᴜɴᴛ ᴏꜰ **{1}** ᴛɪᴍᴇs\n\nᴛᴏᴘ **{2}** ᴘʟᴀʏᴇᴅ ʙʏ ʏᴏᴜ :\n\n".format(
                        tot, tota, limit
                    )
                    + msg
                )
                return videoid, msg

            try:
                videoid, msg = await loop.run_in_executor(None, get_stats)
            except Exception as e:
                print(e)
                return
            thumbnail = await YouTube.thumbnail(videoid, True)
            await m.delete()
            await message.reply_photo(photo=thumbnail, caption=msg)
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎 **ғᴇᴛᴄʜɪɴɢ ɪɴғᴏ ...**")
            query = name.replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
            searched_text = f"""
>> <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀɴᴀᴛɪᴏɴ</b>

<b>Tɪᴛʟᴇ:</b> {title}
⏳ <b>Dᴜʀᴀᴛɪᴏɴ:</b> {duration} ᴍɪɴᴜᴛᴇs
👀 <b>ᴠɪᴇᴡs:</b> <code>{views}</code>
<b>ᴩᴜʙʟɪsʜᴇᴅ ᴏɴ:</b> {published}
🎥 <b>ᴄʜᴀɴɴᴇʟ:</b> {channel}
📎 <b>ᴄʜᴀɴɴᴇʟ ʟɪɴᴋ:</b> <a href="{channellink}">ᴠɪsɪᴛ ᴄʜᴀɴɴᴇʟ</a>
🔗 <b>ʟɪɴᴋ:</b> <a href="{link}">ᴡᴀᴛᴄʜ ᴏɴ ʏᴏᴜᴛᴜʙᴇ</a>

⚡ sᴇᴀʀᴄʜ ᴩᴏᴡᴇʀᴇᴅ ʙʏ {app.mention}
"""
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="ʏᴏᴜᴛᴜʙᴇ", url=link),
                        InlineKeyboardButton(text="ᴄʟᴏsᴇ", callback_data="close"),
                    ],
                ]
            )
            await m.delete()
            await app.send_photo(
                message.chat.id,
                photo=thumbnail,
                caption=searched_text,
                parse_mode=ParseMode.HTML,
                reply_markup=key,
            )
            if await is_on_off(2):
                sender_id = message.from_user.id
                sender_name = message.from_user.mention
                return await app.send_message(
                    config.LOG_GROUP_ID,
                    f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>\n\n<b>ᴜsᴇʀ ɪᴅ:</b> {sender_id}\n<b>ᴜsᴇʀɴᴀᴍᴇ:</b> {sender_name}",
                )
    else:
        out = private_panel()
        image = config.START_IMG
        TXT = f"""ʜᴇʏ {message.from_user.mention}
ᴛʜɪs ɪs {app.mention} ᴀ ᴛᴇʟᴇɢʀᴀᴍ ꜱᴛʀᴇᴀᴍɪɴɢ ʙᴏᴛ ᴡɪᴛʜ ꜱᴏᴍᴇ ᴀᴡᴇꜱᴏᴍᴇ ꜰᴇᴀᴛᴜʀᴇꜱ. ꜱᴜᴘᴘᴏʀᴛɪɴɢ ᴘʟᴀᴛꜰᴏʀᴍꜱ ʟɪᴋᴇ **ʏᴏᴜᴛᴜʙᴇ**, **ᴛᴇʟᴇɢʀᴀᴍ**, **ꜱᴘᴏᴛɪꜰʏ** ᴇᴛᴄ ...
ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴩ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ ᴛᴏ ɢᴇᴛ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴍʏ ᴄᴏᴍᴍᴀɴᴅs :**"""
        try:
            await message.reply_photo(
                photo=image,
                caption=TXT,
                reply_markup=InlineKeyboardMarkup(out),
            )
        except:
            await message.reply_text(
                text=TXT,
                reply_markup=InlineKeyboardMarkup(out),
            )
        if await is_on_off(2):
            sender_id = message.from_user.id
            sender_name = message.from_user.mention
            sender_uname = message.from_user.username
            return await app.send_message(
                config.LOG_GROUP_ID,
                f"{message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ.\n\n**ᴜsᴇʀ ɪᴅ:** `{sender_id}`\n**ᴜsᴇʀɴᴀᴍᴇ:** @{sender_uname}",
            )
