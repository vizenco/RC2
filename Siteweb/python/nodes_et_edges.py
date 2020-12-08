from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/");
print("Connection Successful")
db = client.DATABASETEST
col = db["articles"]




listeLabTotal = []
listeNbPubli = []
for x in col.find({ "labStructName_s": { '$exists': 1 }, "labStructAddress_s": {'$exists': 1} }):
    tabLab = x["labStructName_s"]
    tabAddress = x["labStructAddress_s"]
    tabId = x["_id"]
    tailleLab = len(tabLab)
    tailleAddress = len(tabAddress)
    if tailleLab == tailleAddress:
        for i in range(0,tailleLab):
            if tabLab[i] not in listeLabTotal:
                b1 = tabAddress[i].find('Lyon')
                b2 = tabAddress[i].find('Villeurbanne')
                if b1 != -1 or b2 != -1:
                    listeLabTotal.append(tabLab[i])
                    listeNbPubli.append(1)
            else:
                indice = listeLabTotal.index(tabLab[i])
                listeNbPubli[indice] += 1

fichier = open('public/donnees_graphe.json','w')

tabEdges = []
for x in col.find({ "labStructName_s": { '$exists': 1 }, "labStructAddress_s": {'$exists': 1} }):
    tabLab = x["labStructName_s"]
    tabAddress = x["labStructAddress_s"]
    tabId = x["_id"]
    tailleLab = len(tabLab)
    tailleAddress = len(tabAddress)
    if tailleLab > 1 and tailleLab == tailleAddress:
        for i in range(0,tailleLab-1):
            for j in range(i+1,tailleLab):
                if tabLab[i] != tabLab[j]:
                    try:
                        b1 = tabAddress[i].find('Lyon')
                        b2 = tabAddress[i].find('Villeurbanne')
                        b3 = tabAddress[j].find('Lyon')
                        b4 = tabAddress[j].find('Villeurbanne')
                        if (b1 != -1 or b2 != -1) and (b3 != -1 or b4 != -1):
                            tabEdges.append(tabLab[i])
                            tabEdges.append(tabLab[j])
                    except IndexError:
                        col.delete_one({'_id': ObjectId(tabId)})


listeLab = []
fichier.write('{\n    "nodes": [\n')

for name in tabEdges:
    if name not in listeLab:
        listeLab.append(name)
        indice = listeLabTotal.index(name)
        nbPubli = listeNbPubli[indice]
        nbP = str(nbPubli)
        fichier.write('        {"labStructName":"'+name+'", "poids":' +nbP+ '},\n')
fichier.write('    ],')



fichier.write('    "edges": [\n')
tabStructName = col["labstructName_s"]
for x in col.find({ "labStructName_s": { '$exists': 1 }, "labStructAddress_s": {'$exists': 1} }):
    tabLab = x["labStructName_s"]
    tabAddress = x["labStructAddress_s"]
    tabId = x["_id"]
    tailleLab = len(tabLab)
    tailleAddress = len(tabAddress)
    if tailleLab > 1 and tailleLab == tailleAddress:
        for i in range(0,tailleLab-1):
            for j in range(i+1,tailleLab):
                if tabLab[i] != tabLab[j]:
                    b1 = tabAddress[i].find('Lyon')
                    b2 = tabAddress[i].find('Villeurbanne')
                    b3 = tabAddress[j].find('Lyon')
                    b4 = tabAddress[j].find('Villeurbanne')
                    if (b1 != -1 or b2 != -1) and (b3 != -1 or b4 != -1):
                        indice1 = listeLab.index(tabLab[i])
                        i1 = str(indice1)
                        indice2 = listeLab.index(tabLab[j])
                        i2 = str(indice2)
                        fichier.write('        {"source":' +i1+', "target":' +i2+ '},\n')
fichier.write('    ]\n}')

fichier.close()
