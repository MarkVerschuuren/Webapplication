from flask import Flask, render_template
from flask import request
import mysql.connector
from mysql.connector import errorcode
app = Flask(__name__)
import json
sults = []

@app.route('/')
def hello_world():
    return render_template("home.html",data=[{'name':'Organism'}, {'name':'Gen'}, {'name':'Stressrespons'}])

@app.route('/search', methods=["POST"])
def queries():
    graaf = {}

    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="usbw", db="test", port=3307) # Database connectie, moet op de server werkend zijn anders even melden dat je een lokale database wilt maken is zo gebeurt.
    cursor = conn.cursor()

    cursor.execute("SELECT gene. geneName, stressaspect . aspect, organism . species, organism . genus "
                   "FROM gene, stressaspect, organism") # query voor de database
    tree = {}
    for row in cursor:
        print(tree)
        subtree = tree
        for i,cell in enumerate(row):
            if cell:
                if cell not in subtree:
                    subtree[cell] = {} if i<len(row)-1 else 1
                subtree = subtree[cell]

    file = open("C:/Users/Mark Verschuuren/Webapplication/static/data.JSON", "w")
    json.dump(tree,file)











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
    return render_template("home.html", data=[{'name': 'Organism'}, {'name': 'Gen'}, {'name': 'Stressrespons'}])
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
