from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MongoDB ----------------
MONGO_URI = "mongodb://10.0.3.90:27017"

client = AsyncIOMotorClient(MONGO_URI)
db = client.my_database
collection = db.users

# ---------------- Model ----------------
class User(BaseModel):
    name: str
    email: str
    age: int | None = None


# ---------------- HTML PAGE ----------------
@app.get("/", response_class=HTMLResponse)
async def home():
    return "<h2>FastAPI Running Successfully 🚀</h2>"


# ---------------- CREATE USER ----------------
@app.post("/users")
async def create_user(user: User):
    result = await collection.insert_one(user.dict())
    return {
        "id": str(result.inserted_id),
        "message": "User created successfully"
    }


# ---------------- GET ALL USERS ----------------
@app.get("/users")
async def get_users():
    users = []
    cursor = collection.find()

    async for user in cursor:
        user["_id"] = str(user["_id"])
        users.append(user)

    return users


# ---------------- GET SINGLE USER ----------------
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    user = await collection.find_one({"_id": ObjectId(user_id)})

    if user:
        user["_id"] = str(user["_id"])
        return user

    return {"message": "User not found"}
