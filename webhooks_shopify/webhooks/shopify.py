from fastapi import APIRouter, Request, BackgroundTasks
import json
import datetime
from webhooks_shopify.utills.fortnoxOffer import Offer
from webhooks_shopify.utills.product_update import main_call
from webhooks_shopify.utills.crossCheck import verify_webhook
from dbconf import CLIENT


DB = "nawrasdb"
OF_COLLECTION = "offerFortnox"
PRODUCTS_COLLECTION = "products"
collections=CLIENT[DB][PRODUCTS_COLLECTION]



router = APIRouter(
    prefix="/webhooks",
    tags=["Webhooks"],
    responses={404: {"description": "Not found"}},
)


@router.post("/fortnox/offer", status_code=200)
async def add_item(request: Request,  background_tasks: BackgroundTasks):
    head= request.headers
    try:
        data= await request.body()
        if verify_webhook(data, head["x-shopify-hmac-sha256"]): #checking is it shopify payload or not
            print("Authorizied")
            json_object = json.loads(data)
            itemlist=[]
            OF_collection = CLIENT[DB][OF_COLLECTION]
            result = OF_collection.find_one({"shopifyID": int(json_object["id"])})
            if result:
                print("Already have this one")
                return {"message": "We already have this one"}
        else: 
            raise Exception('varification false')
    except:
        return {"message": "Missing body or header value"}
    
    

    
    try:
        try:
            customerNumber=int(json_object['customer']['note'].split()[0]) # CustomerNumber
        except:
            customerNumber="2"
        # print("Customer Number: "+ customerNumber)
        for i in json_object['line_items']:
            item= {"ArticleNumber": i['sku'], "Quantity": i['quantity'], "Discount": round((100*(float(i["total_discount"])/float(i["quantity"])))/(float(i["price"]))), "DiscountType": "PERCENT"}
            itemlist.append(item)
        data={ "Offer": { "CustomerNumber": customerNumber, "Comments": json_object["note"] if json_object["note"] else "","OurReference": "Knitnox Webshop", "OfferRows": itemlist}} 
        background_tasks.add_task(Offer,data, json_object["id"], CLIENT)
  
        # print("------------")
        # print(head["x-shopify-hmac-sha256"])
        return {"message": "task running in background"}
    except:
        return {"message": "something wrong"}





@router.post("/fortnox/singleproduct", status_code=200)
async def add_item(request: Request,  background_tasks: BackgroundTasks):
    head= request.headers
    try:
        data= await request.body()
        if verify_webhook(data, head["x-shopify-hmac-sha256"]): #checking is it shopify payload or not
            print("Authorizied")
            json_object = json.loads(data)
            #print(json_object)
            try:
                last_time=collections.find_one({"shopify_id": json_object["id"]})
                time_delta=datetime.datetime.utcnow()-last_time['createdAt']
                if int(str(time_delta).split(":")[1]) < 2:
                    print("less than 2 second")
                    return {"message": "we already up to date"}
                else:
                    print("carry on")
                    background_tasks.add_task(main_call,json_object)
                    return {"message": "data recieved"}
            except:
                background_tasks.add_task(main_call,json_object)
                return {"message": "data recieved"}
    except:
        return {"message": "Missing body or header value"}
    
    
