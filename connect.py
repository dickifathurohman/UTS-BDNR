import pymongo

# connect fachri db
#uri = "mongodb+srv://fachrinajmnoer:FshsIDEkArEfJZsY@utscluster.4lijn.mongodb.net/?retryWrites=true&w=majority"
#client = pymongo.MongoClient(uri)

# connect ke lokal
client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["db_onlineshop"]