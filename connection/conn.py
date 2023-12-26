from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from data.constants import url, _database, _collection

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