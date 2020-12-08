from pymongo import MongoClient
import json
import random
import sys
from threading import Thread, Lock

mutex = Lock()

client = MongoClient("mongodb://localhost:27017/")
#print("Connection Successful")
db = client.DATABASETEST
col = db["articles"]


def fctListe():
    liste = []
    for x in col.find({"labStructName_s": {'$exists': 1},  "labStructAddress_s": {'$exists': 1}}):
        tabLab = x["labStructName_s"]
        tabAddress = x["labStructAddress_s"]
        tailleLab = len(tabLab)
        tailleAddress = len(tabAddress)
        if tailleLab == tailleAddress:
            for i in range(0,tailleLab):
                # print(x["labStructName_s"])
                if tabLab[i] not in liste:
                    # print(x["labStructName_s"])
                    try:
                        b1 = tabAddress[i].find('Lyon')
                        b2 = tabAddress[i].find('Villeurbanne')
                        if b1 != -1 or b2 != -1:
                            liste.append(tabLab[i])
                    except IndexError:
                        print("error")
    return liste

def fctListe5(l):
    liste5 =random.sample(l, 5)
    #print(liste5)
    return liste5

def fctCollab5(l5):
    listeCollab = [0,0,0,0,0]
    for x in col.find({"labStructName_s": {'$exists': 1}}):
        for y in x["labStructName_s"]:
           # print(y)
            if l5[0] == y :
                listeCollab[0] = listeCollab[0] +1

            elif l5[1] == y :
                listeCollab[1] = listeCollab[1] +1
 
            elif l5[2] == y :
                listeCollab[2] = listeCollab[2] +1

            elif l5[3] == y :
                listeCollab[3] = listeCollab[3] +1

            elif l5[4] == y :
                listeCollab[4] = listeCollab[4] +1
    
    #print(listeCollab)
    return listeCollab


liste = fctListe()
for arg in sys.argv:
        
    if arg == "liste5":
        liste5 = fctListe5(liste)
        #print(liste5)
        listCollab = fctCollab5(liste5)
        #print(listCollab)
        # liste5 = json.dumps(liste5)
        # listCollab = json.dumps(listCollab)
        # json.dumps([1, 2, 3, {'4': 5, '6': 7}], separators=(',', ':'))
        mutex.acquire()
        print(json.dumps([liste5,json.dumps(listCollab)]))
        mutex.release()

        # print(json.dumps('[','[',json.dumps(liste5), ':',json.dumps(listCollab),']',']' ),separators=(':')) 
        # print(lf) 

    if arg == "liste":
        mutex.acquire()
        print(json.dumps(liste))
        mutex.release()
