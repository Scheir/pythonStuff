import pymongo
from bson import ObjectId


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["testDB"]
mycol = mydb["customers"]
mydict = { "name": "Andre", "type": "Small company"}
x = mycol.insert_one(mydict).inserted_id
if x:
    print(x)
else:
    print("No match")


query_res = mycol.find_one({"_id":ObjectId(x)})
print(query_res)
mydict = { "name": "Andre", "type": "Big company"}
mycol.update_many({"_id":ObjectId(x)},{"$set":mydict})

query_res = mycol.find_one({"_id":ObjectId(x)})
print(query_res)