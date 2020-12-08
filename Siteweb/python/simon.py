from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/");
print("Connection Successful")
db = client.DATABASETEST
col = db["articles"]

#titres des doc produits par UCBL1

'''
for x in col.find( { 
		"structName_s" : { '$in': ["Université Claude Bernard Lyon 1"]},
} ) :
	print(x['title_s'])
'''

#nb doc produits par UCBL1 
'''
i = 0
for x in col.find({"structName_s" : { '$in': ["Université Claude Bernard Lyon 1"]}}):
	i=i+1

print(i)
'''

#titres des doc produits par UCBL1

'''
for x in col.find( { 
		"structName_s" : { '$in': ["Université Claude Bernard Lyon 1"]},
} ) :
	print(x['title_s'])
'''

#universités de lyon ( a finir )

'''for x in col.find( { 
		"structName_s" : { '$in': ["Université de Lyon"]},
} ) :
	print(x['structName_s'])'''

#universités de lyon ( a finir )


#liste des universités de lyon

'''
import re
liste =[]
for x in col.find( { 
		"structName_s" : { '$in': ["Université de Lyon"]},
} ) :
    for y in x['structName_s'] :
        if("Université" in y) and ("Lyon" in y)and (y not in liste):
            liste.append(y)
            #print("ok")         
liste
'''

#liste des universités de lyon
'''
liste =[]
for x in col.find( { 
		"structName_s" : { '$in': ["Université de Lyon"]},
} ) :
    for y in x['structName_s'] :
        if("Institut" in y) and ("Lyon" in y)and (y not in liste):
            liste.append(y)
            #print("ok")         
liste
'''

'''
import re
regx = re.compile("^foo", re.IGNORECASE)
liste =[]
i=0
#for x in col.find( { '$and': [ {"structName_s":{'$regex':'Institut'}}, {"structName_s" :{ '$regex': 'Lyon'}} ] } ) :
for x in col.find( {"structName_s":{'$regex':'Institut '}}):    
    for y in x['structName_s'] :
        i=i+1
        if("Institut" in y) and ("Lyon" in y)and (y not in liste):
            liste.append(y)
    #if("Institut" in y) and ("Lyon" in y)and (y not in liste):
   # print(x["structName_s"])         
liste
        #print(y)
    #print re.match(r"GR(.)?S", " :GRIS")
    #liste.extend(x['structName_s'])
#liste
'''


liste =[]
for x in col.find( {"labStructName_s":{'$exists': 1} } ):
    for y in x["labStructName_s"]:
        #print(x["labStructName_s"])
        if y not in liste :
            #print(x["labStructName_s"])
            liste.append(y)
print(liste)


'''
i = 0
for x in col.find( {"labStructName_s" : { '$in': ["Université Claude Bernard Lyon 1"]}} ):
	i=i+1

print(i)
'''
  
#https://docs.mongodb.com/manual/reference/operator/query/in/#op._S_in
#The { item : None } query matches documents that either contain the item field whose value is null or that do not contain the item field.
