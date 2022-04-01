import requests as rq
import json
from globalConfig import UNIQ
from globalUtils import refresh_new_token
#we have to work on this page

DB = "nawrasdb"
OF_COLLECTION = "offerFortnox"
TOKEN_COLLECTIONS = "tockens" #lol tockens

def Offer_try(data,conn):
    #print(data)
    token_collection=conn[DB][TOKEN_COLLECTIONS]
    try:
        access_token=token_collection.find_one({"uniq": UNIQ})["access_token"]
        r = rq.post('https://api.fortnox.se/3/offers', data=json.dumps(data),
                headers = {
                                "Authorization": "Bearer {}".format(access_token),
                                "Content-Type":"application/json",
                                "Accept":"application/json",
                            },
            )
        
        print(r.status_code)
        return r
    except rq.exceptions.RequestException as e:
        print('HTTP Request failed')
        
        
    
def Offer(data,shopifyID,conn):
    returnedD=Offer_try(data,conn)
    if returnedD.status_code==401:
        refresh_new_token(conn)
        returnedD=Offer_try(data,conn)
    returnedData=json.loads(returnedD.content)
    try:
        data["Offer"]["shopifyID"]=int(shopifyID)
        data["Offer"]["CustomerName"]=returnedData["Offer"]["CustomerName"]
        data["Offer"]["DocumentNumber"]=int(returnedData["Offer"]["DocumentNumber"])
        data["Offer"]["Total"]=float(returnedData["Offer"]["Total"])
        data["Offer"]["CustomerNumber"]=returnedData["Offer"]["CustomerNumber"]
        collection = conn[DB][OF_COLLECTION]
        result = collection.insert_one(data["Offer"])
        print(result)
    except:
        print("there some problem with the returned data from fortnox or maybe database connection")
    