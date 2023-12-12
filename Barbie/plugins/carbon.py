from config import BANNED_USERS
from pyrogram import filters
from Barbie import app, aiohttpsession
from io import BytesIO


__MODULE__ = "Cᴀʀʙᴏɴ"
__HELP__ = """
/carbon - ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴀɴᴅ ɢɪᴠᴇ ᴄᴀʀʙᴏɴ ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ ᴍᴀᴋᴇ ᴀ ᴛᴇxᴛ ɪɴᴛᴏ ᴄᴀʀʙᴏɴ
"""


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttpsession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


@app.on_message(filters.command("carbon") & ~BANNED_USERS)
async def carbon_func(_, message):
    try:
        await message.delete()
    except:
        pass
    if not message.reply_to_message:
        return await message.reply_text("Reply to a text message to make carbon.")
    if not message.reply_to_message.text:
        return await message.reply_text("Reply to a text message to make carbon.")
    m = await message.reply_text("ᴘʀᴇᴘᴀʀɪɴɢ ᴄᴀʀʙᴏɴ ...")
    carbon = await make_carbon(message.reply_to_message.text)
    await m.edit("ᴜᴘʟᴏᴀᴅɪɴɢ ...")
    await app.send_photo(message.chat.id, carbon)
    await m.delete()
    carbon.close()
