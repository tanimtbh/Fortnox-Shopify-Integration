import requests
import time
import datetime
import json
from pymongo import MongoClient
import datetime
from bson.objectid import ObjectId
from dbconf import CLIENT
DB = "nawrasdb"
PRODUCTS_COLLECTION = "products"
collections=CLIENT[DB][PRODUCTS_COLLECTION]
OF_COLLECTION = "tockens"
token_collection = CLIENT[DB][OF_COLLECTION]


def refresh_new_token():
    refresh_token=token_collection.find_one({"uniq": "nawras001"})["refresh_token"]

    data = {'grant_type': 'refresh_token', 'refresh_token': refresh_token}
    print("refreshing for new access token...")
    access_token_response = requests.post("https://apps.fortnox.se/oauth-v1/token", data=data, verify=False, allow_redirects=False, auth=("fSI", "Brw5I1p"))

    # we can now use the access_token as much as we want to access protected resources.
    tokens = json.loads(access_token_response.text)
    access_token = tokens['access_token']
    refresh_token=tokens['refresh_token']
    print ("access token: " + access_token)
    print ("refresh token: " + refresh_token)
    # Data to be written
    tempdb ={
        "access_token" : access_token,
        "refresh_token" : refresh_token,
        "updaded_time" : str(datetime.datetime.now()),
        "last_log":tokens
           }
    #simulation of db
    filt = { "uniq":"nawras001"}
    values = { "$set": tempdb }
    token_collection.update_one(filt, values, True)


def one_request(num):
    access_token=token_collection.find_one({"uniq": "nawras001"})["access_token"] #fetching from DB
    try:
        #print("trying to one_request")
        r = requests.get(
            url="https://api.fortnox.se/3/articles/{}".format(num),
            headers = {
                            "Authorization": "Bearer {}".format(access_token),
                            "Content-Type":"application/json",
                            "Accept":"application/json",
                        },
        )
        
        return r.content
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')
#formating and unicode corrections

def get_one_from_fortnox(article_num, shopify_id):
    try:
        data=json.loads(one_request(article_num))
        single_data= json.dumps(data, indent=2)
        single_data=single_data.replace(r"\u00e4", "ä").replace(r"\u00f6", "ö").replace(r"\u00e5", "å")
        x = json.loads(single_data)
        html= '<div class="custom_bottom_border"><strong>Produktnummer: '+x["Article"]["ArticleNumber"]+' </strong></div><hr> '+x["Article"]["Description"] + '<br><br> This product contain '+x["Article"]["ManufacturerArticleNumber"]+' items per box/bag <br> يحتوي هذا المنتج على '+x["Article"]["ManufacturerArticleNumber"]+' عناصر لكل صندوق / كيس <br> Denna produkt innehåller '+x["Article"]["ManufacturerArticleNumber"]+' artiklar per låda/påse.',
        data= {'product': {
                       'id': shopify_id ,
                      'title': x["Article"]["Description"],
                      'body_html': html[0],
                      'vendor': 'Nawras',
                      'product_type': 'nawras',
                      'template_suffix': '',
                      'handle': x["Article"]["ArticleNumber"],
                      'status': 'active' if x['Article']['Active'] else 'draft',
                      "published_scope": "global",
                      'tags': x["Article"]["ManufacturerArticleNumber"],
                      'variants': [{
                                    'title': 'Default Title',
                                    'price': x["Article"]["SalesPrice"],
                                    'sku': x["Article"]["ArticleNumber"],
                                    "inventory_management": "",
                                }],
                            }},
        document={
                    'shopify_id': shopify_id ,
                    "articleNumber":x["Article"]["ArticleNumber"],
                    "productName":x["Article"]["Description"],
                    "description":x["Article"]["Description"],
                    "netPrice":float(x["Article"]["SalesPrice"]),
                    "price":float(x["Article"]["SalesPrice"]),
                    "offer":0,
                    "isAvailable":True,
                    "vat": "12%"if int(x["Article"]["SalesAccount"])==3016 else "25%",
                    "SalesAccount": x["Article"]["SalesAccount"],
                    "qtyPerBox":int(x["Article"]["ManufacturerArticleNumber"]) if x["Article"]["ManufacturerArticleNumber"] else 1,
                    "createdAt":datetime.datetime.utcnow()}
        try:
            values = { "$set": document }
            filt = { "articleNumber": x["Article"]["ArticleNumber"] }
            collections.update_one(filt, values, True)
        except:
            print("unable to write to remoteDB")
        return data
    except:
        print("creating new token")
        refresh_new_token()
        return False
    
def update_product_shopify(id_shopify_product, payload):
    try:
        r = requests.put(url="https://3fb221feeert22569c19b439dev.myshopify.com/admin/api/2022-01/products/{}.json".format(id_shopify_product), data=json.dumps(payload),
                         headers = {
                                "Content-Type":"application/json",
                                "Accept":"application/json",
                            },)
        return r.content
    except requests.exceptions.RequestException as e:
        print('HTTP Request failed')


def main_call(datashopify):
    try_to_get=get_one_from_fortnox(datashopify['variants'][0]['sku'], datashopify['id'])
    if try_to_get:
        print("successfully retrive data")
        update_product_shopify(datashopify['id'], try_to_get[0])
        print("successfully updated")

    else:
        try_to_get=get_one_from_fortnox(datashopify['variants'][0]['sku'], datashopify['id'])
        if try_to_get:
            print("successfully retrive data on second try")
            update_product_shopify(datashopify['id'], try_to_get[0])
            print("successfully updated")
        else:
            print("something wrong during fetching data from fortnox")
