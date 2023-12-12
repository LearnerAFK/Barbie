import sys
import config
from pyrogram import Client
from ..logging import LOGGER


assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="Barbie1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1)
        )
        self.two = Client(
            name="Barbie2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2)
        )
        self.three = Client(
            name="Barbie3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3)
        )

    
    async def start(self):
        if config.STRING1:
            await self.one.start()
            try:
                await self.one.join_chat("TeamBarbie")
            except:
                pass
            assistants.append(1)
            get_me = await self.one.get_me()
            self.one.username = get_me.username
            self.one.id = get_me.id
            self.one.mention = get_me.mention
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant One Started ...")
            try:
                await self.one.send_message(config.LOG_GROUP_ID, f"**» ᴀssɪsᴛᴀɴᴛ ᴏɴᴇ sᴛᴀʀᴛᴇᴅ :** {self.one.mention} ...")
            except:
                LOGGER(__name__).error(f"Assistant Account 1 Has Failed To Access The Log Group ...")
                sys.exit()

        if config.STRING2:
            await self.two.start()
            try:
                await self.two.join_chat("TeamBarbie")
            except:
                pass
            assistants.append(2)
            get_me = await self.two.get_me()
            self.two.username = get_me.username
            self.two.id = get_me.id
            self.two.mention = get_me.mention
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant Two Started ...")
            try:
                await self.two.send_message(config.LOG_GROUP_ID, f"**» ᴀssɪsᴛᴀɴᴛ ᴛᴡᴏ sᴛᴀʀᴛᴇᴅ :** {self.two.mention} ...")
            except:
                LOGGER(__name__).error(f"Assistant Account 2 Has Failed To Access The Log Group ...")
                sys.exit()
                
        if config.STRING3:
            await self.three.start()
            try:
                await self.three.join_chat("TeamBarbie")
            except:
                pass
            assistants.append(3)
            get_me = await self.three.get_me()
            self.three.username = get_me.username
            self.three.id = get_me.id
            self.three.mention = get_me.mention
            assistantids.append(get_me.id)
            LOGGER(__name__).info(f"Assistant Two Started ...")
            try:
                await self.three.send_message(config.LOG_GROUP_ID, f"**» ᴀssɪsᴛᴀɴᴛ ᴛhree sᴛᴀʀᴛᴇᴅ :** {self.three.mention} ...")
            except:
                LOGGER(__name__).error(f"Assistant Account 3 Has Failed To Access The Log Group ...")
                sys.exit()
            

userbot = Userbot()
