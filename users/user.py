from fastapi import APIRouter
from fastapi import Query
from users.schemas import UserModel
from typing import Optional
from dbconf import CLIENT
DB = "testdb"
MSG_COLLECTION = "testcollection"
#APIRouter creates path operations for user module
router = APIRouter(
    prefix="/users",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def read_root():
    message = {
    "channel": "from user",
    "author": "abba tanim",
    "text": "Hello, world!"
}
    m_coll = CLIENT[DB][MSG_COLLECTION]
    result = m_coll.insert_one(message)
    print(result)
    return [{"id": 1}, {"id": 2}]

@router.get("/{user_id}")
async def read_user(user_id: int):
    return {"id": user_id, "full_name": "Danny Manny", "email": "danny.manny@gmail.com"}

@router.get("/detail")
async def read_users(q: Optional[str] = Query(None, max_length=50)):
    results = {"users": [{"id": 1}, {"id": 2}]}
    if q:
        results.update({"q": q})
    return results

@router.post("/add")
async def add_user(user: UserModel):
    return {"full_name": user.first_name+" "+user.last_name}

@router.put("/update")
async def read_user(user: UserModel):
    return {"id": user.user_id, "full_name": user.first_name+" "+user.last_name, "email": user.email}

@router.delete("/{user_id}/delete")
async def read_user(user_id: int):
    return {"id": user_id, "is_deleted": True}