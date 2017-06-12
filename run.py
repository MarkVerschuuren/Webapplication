from flask import Flask, render_template
from flask import request
import mysql.connector
app = Flask(__name__)
import json

@app.route('/') # simple home page, user can search for species.
def hello_world():
    return render_template("home.html")

@app.route('/search', methods=["POST"]) # search method, connection to database en making the JSON file for the sunburst
def queries():

    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="usbw", db="test", port=3307) # Database connection, is local right now.
    cursor = conn.cursor()

    cursor.execute("SELECT  gene. geneName, stressaspect . aspect  "
                   "FROM gene, stressaspect") # query for the database
    tree = {} # dictonary, contains the gene as key with the chemicals as value in a list.
    Valuelist = [] # list to put the values of the key, contains chemicals.
    cursor = cursor.fetchall()
    for i, row in enumerate(cursor): # loops over the output for the database, the output is nested.
        if row[0] not in tree.keys(): # row[0] will always be a gene. If its not in the dictonary as key.
            tree[row[0]] = Valuelist # then put the gene in the dictonary and the valuelist as value.

        if row[1] not in tree[row[0]]: # if row[1] which always will be a chemical is not in the tree
            Valuelist.append(row[1]) # add the chemical to the tree

    L1L = [] # list containing the children of the organism
    L1D = {} # dictonary which contains everything the organism has
    print(tree)
    for key,value in tree.items(): # get the key(gene) and values(chemicals)
        L2L = [] # list containing children of the genes
        for chemical in value:
            L3 = {} # dictonary containing the chemical and size of the chemical
            L3["name"] = chemical
            L3["size"] = 15
            L2L.append(L3) # add the dictonary of chemicals to the childern of the genes.
        L2D = {} # dictonary which contains everything the specific gene has.
        L2D["name"] = key # key is the gene
        L2D["children"] = L2L # L2L is a list contraing the children of the genes.
        L1L.append(L2D) # add the dictonary for everthing the gene has to the organism children



    L1D["name"] = "kas" # "arabidopsis should be the name of the query
    print(L1D)
    L1D["children"] = L1L # add the list of children to the dictonary of the specie
    print(L1D)

   # file = open("C:/Users/Mark Verschuuren/Webapplication/static/data.JSON", "w")
   # writing = json.dumps(L1D, indent=2)
   # file.write(writing)
   # file.close()

    specie = "Arabidopsis" # this should be the query of the specie
    amount = "2" # this should be the amount of times the specie was found in a pubmed

    return render_template("home.html", text="the amount of articles for " + specie + " is: " + amount, link="to sunburst")
@app.route('/sunBurst', methods=["GET"]) #page to sunburst result.
def flower():

    return render_template("sunBurst.html")








#     for x in cursor: # door een geneste loop  heen
#         for y in range(len(x)): # elke rij bekijken
#             if type(x[y]) is not int: # elke cel bekijken, als het geen int(pubmedID) is.
#
#                 if x[y] not in graaf: # wanneer de waarde nog niet is toegevoegd aan de dict, toevoegen, waarde = key
#                     graaf[x[y]] = []
#
#
#                 if x[4] not in graaf[x[y]]: # wanneer de pubmed ID nog niet in de value zit toevoegen aan de value van de key
#                     graaf[x[y]].append(x[4])
#
#     termlist = [list(graaf)[2],list(graaf)[3], len(graaf[list(graaf)[2]])]  # hier de organisme meenemen met het aantal pubmed ID's, dit wordt weergeven in home.html
#
#     corralatie = {} # dict voor het verband tussen alle nodes
#     valuelist = [] # list die steeds refresh wordt per node.
#     for key in graaf: # door alle keys heen gaat
#         if key not in corralatie: # als de key nog niet door corralatie zit deze toevoegen als een dict.
#             corralatie[key] = {}
#         for index in range(1,len(graaf)): # loop doorde lengte van de graaf van 1, tot de lengte. Dit wordt gebruikt voor indexing
#
#             key1 = graaf[key] # pubmedID's krijgen van de value
#
#             key2 = graaf[list(graaf.keys())[index]] #pubmedIDs krijgen van de andere key op basis van de index
#
#             for value in key1:
#                 if value in key2:
#                     valuelist.append(value)
#             corralatie[key].update({list(graaf.keys())[index]: valuelist}) # de correlatie update op basis van de valuelist, dus steeds een node met de pubmed ID's die overeenkwamen
#             valuelist = []
#     cursor.close()
#
#
#
#
#
#
#
#     # termlist = []
#     # term = ""
#     # count = -1
#     # imports = [["Arabidopsis thaliana",500,"Luchtdruk"],["Arabidopsis kaas",1337,"Zuurtegraad"]]
#     # data = ["Organism","Gen","Stressrespons"]
#     # select = request.form.get('dropdown1')
#     # select2 = request.form.get('dropdown2')
#     # select3 = request.form.get('dropdown3')
#     # term = request.form["Search1"]
#     # term2 = request.form["Search2"]
#     #
#     # for x in data:
#     #     count += 1
#     #     if x == select:
#     #         searchform1 = count
#     #     if x == select2:
#     #         searchform2 = count
#     #     if x == select3:
#     #         searchform3 = select3
#     #
#     # for y in imports:
#     #     if term in y[searchform1]:
#     #         termlist.append(y[searchform1])
#     #  #   if int(term2) in y[searchform2] and term in y:
#     #  #       termlist.append(y[searchform2])
#     #
#     # print(termlist)

##organism = termlist[0] + " " + termlist[1], amount = termlist[2]
# @app.route('/Result', methods=["GET"])
# def result():
#     graaf = {}
#
#     conn = mysql.connector.connect(host="127.0.0.1", user="root", password="usbw", db="test", port=3307)
#     cursor = conn.cursor()
#
#     cursor.execute(
#         "SELECT gene. geneName, stressaspect . aspect, organism . species, organism . genus, article . pubmedID "
#         "FROM gene, stressaspect, organism, article")
#
#     for x in cursor:
#         for y in range(len(x)):
#             if type(x[y]) is not int:
#
#                 if x[y] not in graaf:
#                     graaf[x[y]] = []
#
#                 if x[4] not in graaf[x[y]]:
#                     graaf[x[y]].append(x[4])
#
#     corralatie = {}
#     valuelist = []
#     for key in graaf:
#         if key not in corralatie:
#             corralatie[key] = {}
#         for index in range(1, len(graaf)):
#
#             key1 = graaf[key]
#             key2 = graaf[list(graaf.keys())[index]]
#             for value in key1:
#                 if value in key2:
#                     valuelist.append(value)
#             corralatie[key].update({list(graaf.keys())[index]: valuelist})
#             valuelist = []
#
#
#
#     #imports = {"Arabidopsis" : 500, "Pax6" : 200, "PH" : 100, "Droogte" : 20}
#     nodes = list(corralatie.keys())
#
#     return render_template("Visualisation.html", data=nodes)

if __name__ == '__main__':
    app.run()
