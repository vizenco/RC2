import requests
import json
import urllib
from urllib import parse as par
from pymongo import MongoClient


##MongoDB  Database creation 
client = MongoClient("mongodb://localhost:27017/")
print("Connection Successful")
db = client.DATABASETEST

    #TEST DATABASE
dblist = client.list_database_names()
print(dblist)
if "DATABASETEST" in dblist:
    print("Database creation successfull." )

col = db["articles"]
collist = db.list_collection_names()
if "articles" in collist:
    print("The collection exists.")
## init requete
filtres ='&fl=docid, title_s,docType_s,authFullName_s, producedDate_tdate, domain_s, domainAllCode_s, labStructName_s, labStructAddress_s, languages_s'

cursor= "*"

url='https://api.archives-ouvertes.fr/search/?q=city_s:Lyon'+filtres+'&rows=10000&sort=docid%20asc&cursorMark='+cursor

r = requests.request('GET',url)
jsons=json.loads(r.text)

nxtCurs = urllib.parse.quote(jsons['nextCursorMark'])
iteration=0


while (cursor != nxtCurs or iteration<1):
    if (cursor==nxtCurs):
        iteration+=1
    for item in jsons['response']['docs']:
        #database add    
        if col.find_one({"docid": item['docid']})== None:
            col.insert_one(item)
            print("insert success")          
    
    #2nd request init
    nxtCurs = urllib.parse.quote(jsons['nextCursorMark'])
    url= url.replace(cursor,nxtCurs)
    cursor = nxtCurs
    print("requete...")
    r=requests.request('GET', url) 
    jsons=json.loads(r.text)

print(jsons['response']['numFound'])
client.close()


