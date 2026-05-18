from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "gestion_eventos_db"

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]


def get_database():
    return db