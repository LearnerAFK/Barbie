import config
import asyncio
import importlib
from Barbie import app, HELPABLE
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
from .logging import LOGGER
from .core.call import CallMusic
from .core.userbot import userbot
from .plugins import ALL_MODULES
from .utils import get_gbanned, get_banned_users


async def init():
    if not config.STRING1 and not config.STRING2 and not config.STRING3:
        LOGGER("Barbie").error("Atleast Add A Pyrogram V2 String ...")
        return

    if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
        LOGGER("Barbie").warning("Fill SPOTIFY_CLIENT_ID & SPOTIFY_CLIENT_SECRET ...")

    try:
        users = await get_gbanned()
        for user_id in users:
            config.BANNED_USERS.add(user_id)
        userss = await get_banned_users()
        for user_id in userss:
            config.BANNED_USERS.add(user_id)
    except:
        pass

    await app.start()
    for all_module in ALL_MODULES:
        imported_module = importlib.import_module("Barbie.plugins." + all_module)
        if hasattr(imported_module, "__MODULE__") and imported_module.__MODULE__:
            imported_module.__MODULE__ = imported_module.__MODULE__
            if hasattr(imported_module, "__HELP__") and imported_module.__HELP__:
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    LOGGER("Barbie.plugins").info("Necessary Modules Imported Successfully ...")

    await userbot.start()
    await CallMusic.start()

    try:
        await CallMusic.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("Barbie").error("Please Turn On Your Logger Group's Voice Call ...")
    except:
        pass

    await CallMusic.decorators()
    LOGGER("Barbie").info("Barbie Started Successfully ...")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
    LOGGER("Barbie").info("Stopping Music Bot ...")
