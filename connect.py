import pymongo
uri = "mongodb+srv://fachrinajmnoer:FshsIDEkArEfJZsY@utscluster.4lijn.mongodb.net/?retryWrites=true&w=majority"
# client = pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient(uri)
db = client["db_onlineshop"]