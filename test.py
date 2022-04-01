from webhooks_shopify.database.config import uri
from pymongo import MongoClient
DB = "testdb"
COLLECTION = "testdata"

item= [
       {"ArticleNumber": "NW786", "Quantity": 1, "Discount": 0, "DiscountType": "PERCENT"},
       {"ArticleNumber": "NW745", "Quantity": 4, "Discount": 0, "DiscountType": "PERCENT"},
       {"ArticleNumber": "TN234", "Quantity": 1, "Discount": 0, "DiscountType": "PERCENT"}
      ]
data={ "CustomerNumber": 93837362245, "Comments": "Test comments","OurReference": "Knitnox Webshop", "OfferRows": item}

with MongoClient(uri) as clnt:
    test_collection = clnt[DB][COLLECTION]
    result = test_collection.insert_one(data)