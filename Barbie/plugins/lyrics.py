import re
from os import remove
from lyricsgenius import Genius
from config import BANNED_USERS
from pyrogram import filters
from pyrogram.types import Message
from Barbie import app


y = Genius(
    "C7mS2YT19wBFGem83Bf12Y9Rg28I6EtuZhWLoAWfOODAzJXwS_44f56H-QWVzeKn",
    skip_non_songs=True,
    excluded_terms=["(Remix)", "(Live)"],
    remove_section_headers=True,
)

y.verbose = False


@app.on_message(filters.command(["lyrics", "lyric"]) & ~BANNED_USERS)
async def lrsearch(_, message: Message):
    if len(message.command) < 2:
        return await message.reply_text("**ᴜsᴀɢᴇ:**\n/lyrics [ᴍᴜsɪᴄ ɴᴀᴍᴇ]")
    title = message.text.split(None, 1)[1]
    m = await message.reply_text("sᴇᴀʀᴄʜɪɴɢ ʟʏʀɪᴄs ...")
    S = y.search_song(title, get_full_info=False)
    if S is None:
        return await m.edit_text(
            "❌ ꜰᴀɪʟᴇᴅ ᴛᴏ ꜰᴇᴛᴄʜ ʟʏʀɪᴄs.\n\n» **ᴛʀɪᴇᴅ sᴇᴀʀᴄʜɪɴɢ ꜰᴏʀ:** {0}".format(title),
            disable_web_page_preview=True,
        )
    lyric = S.lyrics
    if "Embed" in lyric:
        lyric = re.sub(r"\d*Embed", "", lyric)
    ran_hash = f"\\files\Lyrics{message.from_user.id}.txt"
    with open(ran_hash, "w") as lyr:
        lyr.write(lyric)
    try:
        await message.reply_document(
            ran_hash,
            caption="ʜᴇʀᴇ ɪs ʏᴏᴜʀ ʟʏʀɪᴄs\n\n**Tɪᴛʟᴇ :** `{}`".format(title),
            file_name=ran_hash,
        )
        await m.delete()
    except Exception as e:
        await m.edit_text("ᴀɴ ᴇxᴄᴇᴘᴛɪᴏɴ ᴏᴄᴄᴜʀᴇᴅ :\n{0}".format(str(e)))
    finally:
        remove(ran_hash)
