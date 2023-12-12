from asyncio import sleep
from config import OWNER_ID
from pyrogram import filters
from pyrogram.errors import FloodWait
from Barbie import app
from ..core.userbot import assistants
from ..utils import get_client, get_served_chats, get_served_users


__MODULE__ = "Bʀᴏᴀᴅᴄᴀsᴛ"
__HELP__ = """
/broadcast [ᴍᴇssᴀɢᴇ ᴏʀ ʀᴇᴩʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ] : ʙʀᴏᴀᴅᴄᴀsᴛ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

/stopbroadcast : stops running broadcast


<u>ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ᴍᴏᴅᴇs:</u>

**-pin** : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇs ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.
**-pinloud** : ᴩɪɴs ʏᴏᴜʀ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ sᴇʀᴠᴇᴅ ᴄʜᴀᴛs.
**-user** : ʙʀᴏᴀᴅᴄᴀsᴛs ᴛʜᴇ ᴍᴇssᴀɢᴇ ᴛᴏ ᴛʜᴇ ᴜsᴇʀs ᴡʜᴏ ʜᴀᴠᴇ sᴛᴀʀᴛᴇᴅ ʏᴏᴜʀ ʙᴏᴛ.
**-assistant** : ʙʀᴏᴀᴅᴄᴀsᴛ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ ғʀᴏᴍ ᴛʜᴇ ᴀssɪᴛᴀɴᴛ ᴀᴄᴄᴏᴜɴᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ.
**-nobot** : ғᴏʀᴄᴇs ᴛʜᴇ ʙᴏᴛ ᴛᴏ ɴᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ᴛʜᴇ ᴍᴇssᴀɢᴇ..


**ᴇxᴀᴍᴩʟᴇ:** `/broadcast -user -assistant -pin ᴛᴇsᴛɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ`
"""


IS_BROADCASTING = False


def is_broadcasting():
    return IS_BROADCASTING


@app.on_message(filters.command(["broadcast", "gcast", "gcastx"]) & filters.user(OWNER_ID) & ~filters.forwarded)
async def braodcast_message(client, message):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        return await message.reply_text("**__ᴀʟʀᴇᴀᴅʏ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ...__**")

    copy = False
    if message.reply_to_message:
        if message.text.startswith("/gcastx"):
            copy = True
            markup = message.reply_to_message.reply_markup
        x = message.reply_to_message.id
        y = message.chat.id
    else:
        try:
            query = message.text.split(" ", 1)[1]
        except:
            return await message.reply_text("**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]\n/gcastx [Reply to a Message]")
        if "-pinloud" in query:
            query = query.replace("-pinloud", "")
        if "-pin" in query:
            query = query.replace("-pin", "")
        if "-nobot" in query:
            query = query.replace("-nobot", "")
        if "-assistant" in query:
            query = query.replace("-assistant", "")
        if "-user" in query:
            query = query.replace("-user", "")
        if query == "":
            return await message.reply_text("ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ʙʀᴏᴀᴅᴄᴀsᴛ.")

    IS_BROADCASTING = True

    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        await message.reply_text("**__sᴛᴀʀᴛᴇᴅ ʙᴏᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ...__**")
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            if not IS_BROADCASTING:
                return
            if (sent % 300 == 0) and (sent > 0):
                await sleep(180)
            try:
                if copy:
                    m = await app.copy_message(i, y, x, reply_markup=markup)
                elif message.reply_to_message:
                    m = await app.forward_messages(i, y, x)
                else:
                    m = await app.send_message(i, text=query)
                sent += 1
                if "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except:
                        continue
                elif "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except:
                        continue
                await sleep(1)
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await sleep(flood_time)
            except:
                continue
        try:
            await message.reply_text("**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ɪɴ {0} ᴄʜᴀᴛs ᴡɪᴛʜ {1} ᴘɪɴs ꜰʀᴏᴍ ʙᴏᴛ.**".format(sent, pin))
        except:
            pass

    # Bot broadcasting to users
    if "-user" in message.text:
        await message.reply_text("**__sᴛᴀʀᴛᴇᴅ ᴜsᴇʀs ʙʀᴏᴀᴅᴄᴀsᴛ ...__**")
        susr = 0
        susers = await get_served_users()
        for user in susers:
            if not IS_BROADCASTING:
                return
            if (susr % 300 == 0) and (susr > 0):
                await sleep(180)
            try:
                if copy:
                    await app.copy_message(int(user["_id"]), y, x, reply_markup=markup)
                elif message.reply_to_message:
                    await app.forward_messages(int(user["_id"]), y, x)
                else:
                    await app.send_message(int(user["_id"]), text=query)
                susr += 1
                await sleep(1)
            except FloodWait as e:
                flood_time = int(e.value)
                if flood_time > 200:
                    continue
                await sleep(flood_time)
            except:
                pass
        try:
            await message.reply_text("**ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴍᴇssᴀɢᴇ ᴛᴏ {0} ᴜsᴇʀs ...**".format(susr))
        except:
            pass

    # Bot broadcasting by assistant
    if "-assistant" in message.text:
        await message.reply_text("**__sᴛᴀʀᴛᴇᴅ ᴀssɪsᴛᴀɴᴛ ʙʀᴏᴀᴅᴄᴀsᴛ ...__**")
        text = "**ᴀssɪsᴛᴀɴᴛ ʙʀᴏᴀᴅᴄᴀsᴛ :**\n\n"
        for num in assistants:
            sent = 0
            client = await get_client(num)
            if not IS_BROADCASTING:
                return

            async for dialog in client.get_dialogs():
                if not IS_BROADCASTING:
                    return
                if (sent % 300 == 0) and (sent > 0):
                    await sleep(180)
                try:
                    if copy:
                        await client.copy_message(dialog.chat.id, y, x)
                    elif message.reply_to_message:
                        await client.forward_messages(dialog.chat.id, y, x)
                    else:
                        await client.send_message(dialog.chat.id, text=query)
                    sent += 1
                    await sleep(1)
                except FloodWait as e:
                    flood_time = int(e.value)
                    if flood_time > 200:
                        continue
                    await sleep(flood_time)
                except:
                    continue
            text += "ᴀssɪsᴛᴀɴᴛ {0} ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ɪɴ {1} ᴄʜᴀᴛs\n".format(num, sent)
        try:
            await message.reply_text(text)
        except:
            pass
    IS_BROADCASTING = False


@app.on_message(filters.command(["stopbroadcast", "stopgcast"]) & filters.user(OWNER_ID))
async def stopbraodcast_message(_, message):
    global IS_BROADCASTING
    if IS_BROADCASTING:
        IS_BROADCASTING = False
        await message.reply_text("✅ **__ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ sᴛᴏᴘᴘᴇᴅ ...__**")
    else:
        await message.reply_text("**__ɴᴏᴛʜɪɴɢ ɪs ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ...__**")
