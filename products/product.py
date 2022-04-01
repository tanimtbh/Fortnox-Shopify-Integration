from fastapi import APIRouter, Request
from typing import Optional
from fastapi import Query
from products.schemas import ProductSchema
from dbconf import CLIENT
# import requests as rq
# import json



#Specific Database name, collection name and router sattings for this part of appliction --->Start
DB = "nawrasdb"
PD1_COLLECTION = "productsTest"

router = APIRouter(
    prefix="/productsApp",
    tags=["ProductApp"],
    responses={404: {"description": "Not found"}},
)
#Specific Database name, collection name and router sattings for this part of appliction --->End



@router.get("/")
async def read_root():
    message = {
    "channel": "from products",
    "author": "cerami",
    "text": "Hello, world!"
}
    m_coll = CLIENT[DB][PD1_COLLECTION]
    result = m_coll.insert_one(message)
    return [{"id":1,"product": "Laptop", "Testdata": "testdata"}, {"id":2,"product": "Mobile"}]

@router.get("/{product_id}")
async def read_item(product_id: int):
    return {"id": product_id, "name": "Mobile", "code": "M12", "price": 200.0}

@router.get("/detail")
async def read_item_detail(q: Optional[str] = Query(None, max_length=50)):
    results = {"products": [{"id": 1}, {"id": 2}]}
    if q:
        results.update({"q": q})
    return results

@router.post("/updates", status_code=200)
async def add_item(request: Request):
    #head= request.headers
      
    return {"message": "Ok done"}

@router.put("/update")
async def update_item(product: ProductSchema):
    return {"id": product.item_id, "name": product.name, "code":product.code, "price": product.price}

@router.delete("/{product_id}/delete")
async def delete_item(product_id: int):
    return {"id": product_id, "is_deleted": True}