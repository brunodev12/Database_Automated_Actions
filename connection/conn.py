from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os

url = os.environ.get('URL_MONGODB')
_database = os.environ.get('DATABASE')
_collection = os.environ.get('COLLECTION')

client = MongoClient(url, server_api=ServerApi('1'))

db = client[_database]
collection = db[_collection]

def createData(data):
    collection.insert_many(data)

def insertData(element):
    collection.insert_one(element)

def findElement(contract, tokenId, chain, owner):
    result = collection.find_one({"contract": contract, "tokenId": tokenId, "chain": chain, "owner": owner})
    return result

def readAllData(address):
    results = list(collection.find({"owner": address}))
    return results

def deleteData(element):
    collection.delete_one({"_id": element["_id"]})

def closeConnection():
    client.close()