import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["testDB"]
mycol = mydb["customers"]
mydict = { "name": "Lollo", "type": "Private"}
mydict = { "name": "Andre", "type": "Small company"}
x = mycol.insert_one(mydict)
x = mycol.find_one({"name":"Lollo"},{"_id":0})
print(x)
x = mycol.find_one({"name":"Unknow"})
if x:
    print(x)
else:
    print("No match")

