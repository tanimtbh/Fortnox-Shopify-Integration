from pymongo import MongoClient
from globalConfig import URI


CLIENT= MongoClient(URI)

def connClose():
    CLIENT.close()
    print("connect closed from dbconfig")