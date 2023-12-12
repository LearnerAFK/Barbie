from pytgcalls.types import AudioParameters, VideoParameters
from ...utils.quality import AudioQuality, VideoQuality

audio = {}

video = {}


async def save_audio_bitrate(chat_id: int, bitrate: str):
    audio[chat_id] = bitrate


async def save_video_bitrate(chat_id: int, bitrate: str):
    video[chat_id] = bitrate


async def get_aud_bit_name(chat_id: int) -> str:
    mode = audio.get(chat_id)
    if not mode:
        return "HIGH"
    return mode


async def get_vid_bit_name(chat_id: int) -> str:
    mode = video.get(chat_id)
    if not mode:
        return "HD_720p"
    return mode


async def get_audio_bitrate(chat_id: int) -> str:
    mode = audio.get(chat_id)
    if not mode:
        return AudioParameters.from_quality(AudioQuality.STUDIO)
    if str(mode) == "STUDIO":
        return AudioParameters.from_quality(AudioQuality.STUDIO)
    elif str(mode) == "HIGH":
        return AudioParameters.from_quality(AudioQuality.HIGH)
    elif str(mode) == "MEDIUM":
        return AudioParameters.from_quality(AudioQuality.MEDIUM)
    elif str(mode) == "LOW":
        return AudioParameters.from_quality(AudioQuality.LOW)


async def get_video_bitrate(chat_id: int) -> str:
    mode = video.get(chat_id)
    if not mode:
        return VideoParameters.from_quality(VideoQuality.FHD_1080p)
    if str(mode) == "UHD_4K":
        return VideoParameters.from_quality(VideoQuality.UHD_4K)
    elif str(mode) == "QHD_2K":
        return VideoParameters.from_quality(VideoQuality.QHD_2K)
    elif str(mode) == "FHD_1080p":
        return VideoParameters.from_quality(VideoQuality.FHD_1080p)
    elif str(mode) == "HD_720p":
        return VideoParameters.from_quality(VideoQuality.HD_720p)
    elif str(mode) == "SD_480p":
        return VideoParameters.from_quality(VideoQuality.SD_480p)
    elif str(mode) == "SD_360p":
        return VideoParameters.from_quality(VideoQuality.SD_360p)
