import config
from pyrogram import filters
from .logging import LOGGER
from .core.mongo import pymongodb


SUDOERS = filters.user()


db = {}


def dbb():
    global db
    db = db
    LOGGER(__name__).info("Database Loaded Successfully ...")


def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID
    try:
        sudoersdb = pymongodb.sudoers
        sudoers = sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        for user_id in OWNER:
            SUDOERS.add(user_id)
            if user_id not in sudoers:
                sudoers.append(user_id)
                sudoersdb.update_one(
                    {"sudo": "sudo"},
                    {"$set": {"sudoers": sudoers}},
                    upsert=True,
                )
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x)
    except Exception as e:
        print(e)
    LOGGER(__name__).info("Sudo Users Loaded Successfully ...")
