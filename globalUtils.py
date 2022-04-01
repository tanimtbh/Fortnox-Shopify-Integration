import requests
import time
import datetime
import json
import datetime
from bson.objectid import ObjectId
from globalConfig import UNIQ, SECRET
import hmac
import hashlib
import base64

DB = "nawrasdb"
OF_COLLECTION = "tockens"

def refresh_new_token(conn):
    collection = conn[DB][OF_COLLECTION]
    refresh_token=collection.find_one({"uniq": UNIQ})["refresh_token"]
    data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    print("refreshing for new access token...")
    access_token_response = requests.post("https://apps.fortnox.se/oauth-v1/token", data=data, verify=True, allow_redirects=False, auth=("QyzzQyjF7fSI", "BJlw5IuY1p"))

    # we can now use the access_token as much as we want to access protected resources.
    tokens = json.loads(access_token_response.text)
    print(tokens)
    try:
        access_token = tokens['access_token']
        refresh_token=tokens['refresh_token']
    except:
        tempdb ={
        "last_log":tokens
           }
        #simulation of db
        filt = { "uniq":UNIQ}
        values = { "$set": tempdb }
        collection.update_one(filt, values, True)
            
    print ("access token: " + access_token)
    print ("refresh token: " + refresh_token)
    # Data to be written
    tempdb ={
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "updated_time" : str(datetime.datetime.now()),
        "last_log":tokens
           }
    #simulation of db
    filt = { "uniq":UNIQ}
    values = { "$set": tempdb }
    collection.update_one(filt, values, True)
    

def make_signature(data):    
    digest = hmac.new(SECRET.encode('utf-8'), data, hashlib.sha256).digest()
    genHmac = base64.b64encode(digest)
    print(genHmac)


def verify_signature(data, hmac_header):    
    digest = hmac.new(SECRET.encode('utf-8'), data, hashlib.sha256).digest()
    genHmac = base64.b64encode(digest)
    return hmac.compare_digest(genHmac, hmac_header.encode('utf-8'))