import sys
import config
from pyrogram import Client
from ..logging import LOGGER


class MusicBot(Client):
    def __init__(self):
        super().__init__(
            name="Barbie",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True
        )

    async def start(self):
        await super().start()
        get_me = await self.get_me()
        if get_me.last_name:
            self.name = get_me.first_name + "" + get_me.last_name
        else:
            self.name = get_me.last_name
        self.username = get_me.username
        self.mention = get_me.mention
        self.id = get_me.id
        try:
            LOGGER(__name__).info(f"MusicBot Started As Barbie ...")
            await self.send_message(config.LOG_GROUP_ID, f"**» ʙᴏᴛ sᴛᴀʀᴛᴇᴅ : {self.mention}** ...")
        except:
            LOGGER(__name__).error("Bot Has Failed To Access The Log Group ...")
            sys.exit()
        

app = MusicBot()
