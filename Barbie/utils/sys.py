import time
import psutil
from Barbie import boot
from .formatters import get_readable_time


async def bot_sys_stats():
    bot_uptime = int(time.time() - boot)
    cpu = psutil.cpu_percent(interval=0.5)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    UP = get_readable_time((bot_uptime))
    CPU = f"{cpu}%"
    RAM = f"{mem}%"
    DISK = f"{disk}%"
    return UP, CPU, RAM, DISK
