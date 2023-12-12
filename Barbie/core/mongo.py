import config
from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_


_mongo_async_ = _mongo_client_(config.MONGO_DB)
_mongo_sync_ = MongoClient(config.MONGO_DB)
mongodb = _mongo_async_.Barbie
pymongodb = _mongo_sync_.Barbie
