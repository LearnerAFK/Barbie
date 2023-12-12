import time
import aiohttp
from .core.bot import app
from .core.git import git
from .core.dir import dirr
from .misc import dbb, sudo
from .platforms.Youtube import YouTube
from .platforms.Carbon import Carbon
from .platforms.Telegram import Telegram
from .platforms.Spotify import Spotify


__Version__ = "0.1"

boot = time.time()

dirr()

git()

dbb()

sudo()

app = app

aiohttpsession = aiohttp.ClientSession()

HELPABLE = {}
