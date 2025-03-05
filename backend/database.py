from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "gestion_trabajadores"

client = AsyncIOMotorClient(MONGO_URI)
database = client[DB_NAME]
trabajadores_collection = database.get_collection("trabajadores")
