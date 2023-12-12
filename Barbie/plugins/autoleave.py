import asyncio
from datetime import datetime
from config import AUTO_LEAVING_ASSISTANT, AUTO_LEAVE_ASSISTANT_TIME, LOG_GROUP_ID
from pyrogram.enums import ChatType
from Barbie import app
from ..core.call import CallMusic, autoend
from ..core.userbot import assistants
from ..utils import get_client, is_active_chat, is_autoend


async def auto_leave():
    if AUTO_LEAVING_ASSISTANT == str(True):
        while not await asyncio.sleep(AUTO_LEAVE_ASSISTANT_TIME):
            for num in assistants:
                client = await get_client(num)
                left = 0
                try:
                    async for i in client.iter_dialogs():
                        chat_type = i.chat.type
                        if chat_type in [ChatType.SUPERGROUP, ChatType.GROUP]:
                            chat_id = i.chat.id
                            if (chat_id != LOG_GROUP_ID) and (
                                chat_id != -1001566470663
                            ):
                                if left == 20:
                                    continue
                                if not await is_active_chat(chat_id):
                                    try:
                                        await client.leave_chat(chat_id)
                                        left += 1
                                    except:
                                        continue
                except:
                    pass


async def auto_end():
    while not await asyncio.sleep(5):
        if not await is_autoend():
            continue
        for chat_id in autoend:
            timer = autoend.get(chat_id)
            if not timer:
                continue
            if datetime.now() > timer:
                if not await is_active_chat(chat_id):
                    autoend[chat_id] = {}
                    continue
                autoend[chat_id] = {}
                try:
                    await CallMusic.stop_stream(chat_id)
                except:
                    continue
                try:
                    await app.send_message(
                        chat_id,
                        "» ʙᴏᴛ ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ ʟᴇғᴛ ᴠɪᴅᴇᴏᴄʜᴀᴛ ʙᴇᴄᴀᴜsᴇ ɴᴏ ᴏɴᴇ ᴡᴀs ʟɪsᴛᴇɴɪɴɢ ᴏɴ ᴠɪᴅᴇᴏᴄʜᴀᴛ ...",
                    )
                except:
                    continue


asyncio.create_task(auto_leave())
asyncio.create_task(auto_end())
