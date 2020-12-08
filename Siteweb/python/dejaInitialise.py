from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client.DATABASETEST
col = db["articles"]

test = col.estimated_document_count()
init = ""
if test > 0:
    init = "true"
else:
    init = "false"
print(init)
