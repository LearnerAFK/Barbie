from os import getenv
from dotenv import load_dotenv
from pyrogram import filters


load_dotenv()
    
    
#----------------------------------REQUIRED-------------------------------#


API_ID = int(getenv("API_ID", None))

API_HASH = getenv("API_HASH", None)

BOT_TOKEN = getenv("BOT_TOKEN", None)

MONGO_DB = getenv("MONGO_DB", None)

STRING1 = getenv("STRING1", None)

LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", None))

OWNER_ID = list(map(int, getenv("OWNER_ID").split()))


#----------------------------OPTIONAL--------------------------------#


STRING2 = getenv("STRING2", None)

STRING3 = getenv("STRING3", None)

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", "900"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "900"))

UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/LearnerAFK/Barbie")

UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "master")

GIT_TOKEN = getenv("GIT_TOKEN", None)

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/LearnerPrivate")

SUPPORT_GROUP = getenv("SUPPORT_GROUP", "https://t.me/LearnerPrivate")

SUPPORT_HEHE = SUPPORT_GROUP.split("me/")[1]

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "True")

AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "18000"))

AUTO_DOWNLOADS_CLEAR = getenv("AUTO_DOWNLOADS_CLEAR", "True")

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "04bd2cf9ebad4b6cb54b0e24a039b15e")

SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "ac02869b41964e349fcda21cd87a902c")

VIDEO_STREAM_LIMIT = int(getenv("VIDEO_STREAM_LIMIT", "50"))

SERVER_PLAYLIST_LIMIT = int(getenv("SERVER_PLAYLIST_LIMIT", "200"))

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", "100"))

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600"))

TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "10737418240"))


#--------------------------DIRECTORIES--------------------------#


LOAD = []

NO_LOAD = []

BANNED_USERS = filters.user()

adminlist = {}

lyrical = {}

chatstats = {}

userstats = {}

autoclean = []


#----------------------------------------IMAGES-------------------------------------------#


START_IMG = getenv("START_IMG", "https://telegra.ph/file/922c8ce3f77386c5a0d3a.jpg")

EXTRA_IMG = getenv("EXTRA_IMG", "https://graph.org/file/b9fa0e997622ce29325fe.jpg")

STREAM_IMG = getenv("STREAM_IMG", "https://telegra.ph/file/4f495b755482386679925.jpg")


#-------------------------------------FUNCTION---------------------------------------#


def time_to_seconds(time):
    stringt = str(time)
    return sum(
        int(x) * 60**i
        for i, x in enumerate(reversed(stringt.split(":")))
    )


DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

SONG_DOWNLOAD_DURATION_LIMIT = int(time_to_seconds(f"{SONG_DOWNLOAD_DURATION}:00"))

