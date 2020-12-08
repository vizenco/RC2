from pymongo import MongoClient
import json
import re

def decoupeTitre(titre , liste, countKW):
    titre=re.sub("[\[\],.';]",'', titre)
    listeTitre = titre.split(' ')
    for x in listeTitre:
        #print(x)
        if  len(x)> 10:
            if x in liste:
                countKW[liste.index(x)] += 1
            else:
                try:
                    liste.append(x)
                    countKW.append(1)
                except IndexError:
                    print(IndexError)
   
            
def KWClassement(): 
    dico={}
    i =0
    
    max = 0
    idMax=0
    while i < 10:
        for it in countKW:
            
            if it>max:
                max=countKW[it]
                idMax = countKW.index(it)
            
               

        dico[str((i+1))] = listeKW[idMax]
        countKW[idMax]=-1
        
        i+=1
    return dico

#recup docs
cli = MongoClient("mongodb://localhost:27017/")

db = cli.DATABASETEST
col =db["articles"]

listeKW=[]
countKW=[]

for x in col.find({"labStructName_s": {'$exists': 1},  "labStructAddress_s": {'$exists': 1}}):
    for y in x['title_s']:
        
        s=json.dumps(x["labStructAddress_s"])
        if(('Lyon' or 'Villeurbanne' or "BRON")in s):
            
            decoupeTitre(y, listeKW, countKW)
    


d= KWClassement()
res = str(d)
res = re.sub("(^:)|([\{\}\[\],.\"';\\ [0-9])",'',str(d))
res = re.sub("^:",'',res)
res = res.split(':')

#res.pop(0)
print(res) 
cli.close()
    

