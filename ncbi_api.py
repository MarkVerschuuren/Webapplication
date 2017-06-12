#make request to NCBI for the gene, chemical and organism indices for the corresponding PMED ID
import simplejson as json
import requests
from Bio import Entrez
from Bio import Medline
import mysql.connector as db
import re


def search(query):
    try:
        Entrez.email = 'timvandekerkhof@hotmail.com'
        handle = Entrez.esearch(db='pubmed',
                                sort='relevance',
                                retmax='10000',
                                retmode='xml',
                                term=query)
        results = Entrez.read(handle)
        idlist = results["IdList"]
        return idlist
    e

def ncbi_gene(results):

    termDictonary = {}
    #print(len(results))

    for ids in range(0,len(results)):

        try:
            custom_url = "https://www.ncbi.nlm.nih.gov/CBBresearch/Lu/Demo/RESTful/tmTool.cgi/bioconcept/{}/JSON".format(results[ids])
            r = requests.get(custom_url)

            json_obj = r.json()
            termDictonary[results[ids]] = {"genes" : [], "Chemicals": [], "Species": []}

            geness, speciess, chemicalss, ab = parse_json(json_obj,termDictonary, results[ids])
        except:
            print("there was an error decoding json file")




    return geness, speciess, chemicalss, ab

def parse_json(json_obj, termDictonary, pubmedID):
    ab = json_obj['text']
    genes = []
    species = []
    chemicals = []

    for denot in json_obj['denotations']:
        if denot['obj'].split(":")[0] == 'Gene':
            if ab[denot['span']['begin']:denot['span']['end']].upper() not in genes:
                genes.append(ab[denot['span']['begin']:denot['span']['end']].upper())
        if denot['obj'].split(":")[0] == "Species":
            specie = getOrganism(ab[denot['span']['begin']:denot['span']['end']])
            if specie not in species:
                species.append(specie)
        if denot['obj'].split(":")[0] == "Chemical":
            if ab[denot['span']['begin']:denot['span']['end']] not in chemicals:
                if re.match("(?!anthocyanins?)",ab[denot['span']['begin']:denot['span']['end']].lower()) and re.match("(?!flavonoids?)",ab[denot['span']['begin']:denot['span']['end']].lower()):

                    chemicals.append(ab[denot['span']['begin']:denot['span']['end']])

    termDictonary[pubmedID].update({"genes" : genes})
    termDictonary[pubmedID].update({"Chemicals": chemicals})
    termDictonary[pubmedID].update({"Species": species})

    #print(pubmedID)



    exportToDatabase(genes, species, chemicals, pubmedID)

    return genes, species, chemicals, ab

#function to export found data to database
def exportToDatabase(geneList, speciesList, chemicalList, PMID):
    data = db.connector.connect(host="127.0.0.1",
                      user="root",
                      passwd="usbw",
                      db="owe8_1617_gr13")
    cur = data.cursor()
    cur.execute("SELECT max(a.articleID), max(g.geneID), max(gc.geneCollectionID),max(o.organismID), max(oc.organismCollectionID), max(s.stressAspectID),max(sc.stressSituationID) FROM article a, gene g, geneCollection gc, organism o, organismCollection oc, stressAspect s, stressSituation sc")

    #fetching max ids for all rows for non-redundant/non-faulty data insertion, all in lowercase to prevent errors in sql syntax
    for row in cur.fetchall():
        maxarticleid = row[0]
        maxgeneid = row[1]
        maxgenecollectionid = row[2]
        maxorganismid = row[3]
        maxorganismcollectionid = row[4]
        maxstressaspectid = row[5]
        maxstresssituationid = row[6]
    #insert statement for genes


    if geneList:
        maxgenecollectionid += 1
        cur.execute("""INSERT INTO geneCollection VALUES ("""+str(maxgenecollectionid)+""")""")
        data.commit()
        for gene in geneList:
            maxgeneid += 1
            cur.execute("""INSERT INTO gene VALUES (%s,%s,%s)""",(str(maxgeneid), gene, str(maxgenecollectionid)))
            data.commit()


    #insert statement for chemicals

    if chemicalList:
        maxstresssituationid += 1
        cur.execute("""INSERT INTO stressSituation VALUES ("""+str(maxstresssituationid)+""")""")
        data.commit()
        for chemical in chemicalList:
            maxstressaspectid += 1
            cur.execute("""INSERT INTO stressAspect VALUES (%s,%s,%s)""",(str(maxstressaspectid), chemical, str(maxstresssituationid)))
            data.commit()


    #insert statement for species
    if speciesList:
        maxorganismcollectionid += 1
        cur.execute("""INSERT INTO organismCollection VALUES ("""+str(maxorganismcollectionid)+""")""")
        data.commit()
        for specie in speciesList:
            maxorganismid += 1
            cur.execute("""INSERT INTO organism VALUES (%s,%s,%s,%s)""",(str(maxorganismid), "", specie, str(maxorganismcollectionid)))
            data.commit()


    #and finally, insert statement for article
    if PMID:
        if geneList:
            maxgenecollectionid = str(maxgenecollectionid)
        else:
            maxgenecollectionid = None
        if chemicalList:
            maxstresssituationid = str(maxstresssituationid)
        else:
            maxstresssituationid = None
        if speciesList:
            maxorganismcollectionid = str(maxorganismcollectionid)
        else:
            maxorganismcollectionid = None
        maxarticleid += 1
        cur.execute("""INSERT INTO article VALUES (%s,%s,%s,%s,%s,%s)""",(str(maxarticleid), str(PMID), "", maxstresssituationid, maxorganismcollectionid, maxgenecollectionid))
        data.commit()


def getOrganism(specie):
    file = open("Organismes.txt", "r")
    file = file.readlines()
    for line in range(61,len(file)):
        if "C=" in file[line]:
            lin = file[line].replace(" ","").lower()
            pattern = "c="+specie+"$"
            if re.search(pattern, lin):
                specie = file[line-1].split("=")[1].split(" ")[0]

    return specie







def main():

    results = search('Anthocyanin')

    genes, species, chemicals ,ab = ncbi_gene(results)




main()

# 4 onde
