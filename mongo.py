import pymongo
import json

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["json_db"]

def readjson(filepath):
    try:
        with open(filepath, 'r') as jsonfile:
            data = json.load(jsonfile)
            data = list(data)
            return data
    except Exception:
        raise "Read Error. Json syntax or file path error"

def createCollection(collection_name,data):
    try:
        collection = db[collection_name]
        for x in data:
            if collection.find_one({"title":x["title"],"added":x["added"]}):
                print('document exists.')
            else:
                print('document inserted.')
                collection.insert_one(x)
        print([x for x in collection.find({})])
    except Exception:
        print("database insertion or updating error")

def getData(filter=None): #example filter = {'endyear':''}
    collection = db["data"]
    if filter:
        data=collection.find(filter)
        return [x for x in data]
    else:
        data = collection.find({})
        return [x for x in data]