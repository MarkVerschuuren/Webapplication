from flask import Flask, render_template
from flask import request
import mysql.connector
from mysql.connector import errorcode
app = Flask(__name__)
sults = []

@app.route('/')
def hello_world():
    return render_template("home.html",data=[{'name':'Organism'}, {'name':'Gen'}, {'name':'Stressrespons'}])

@app.route('/search', methods=["POST"])
def queries():
    graaf = {}

    conn = mysql.connector.connect(host="127.0.0.1", user="root", password="usbw", db="test", port=3307)
    cursor = conn.cursor()

    cursor.execute("SELECT gene. geneName, stressaspect . aspect, organism . species, organism . genus, article . pubmedID "
                   "FROM gene, stressaspect, organism, article")

    for x in cursor:
        for y in range(len(x)):


            if x[y] not in graaf:
                graaf[x[y]] = []


            if x[4] not in graaf[x[y]]:
                graaf[x[y]].append(x[4])
    print(graaf)
    termlist ={}
    corralatie = {}
    for key in graaf:
        if key not in corralatie:
            corralatie[key] = {}
        for index in range(1,len(graaf)):

            key1 = graaf[key]
            key2 = graaf[list(graaf.keys())[index]]
            for value in key1:
                if value in key2:
                    corralatie[key].update({list(graaf.keys())[index]: value})




    

    # termlist = []
    # term = ""
    # count = -1
    # imports = [["Arabidopsis thaliana",500,"Luchtdruk"],["Arabidopsis kaas",1337,"Zuurtegraad"]]
    # data = ["Organism","Gen","Stressrespons"]
    # select = request.form.get('dropdown1')
    # select2 = request.form.get('dropdown2')
    # select3 = request.form.get('dropdown3')
    # term = request.form["Search1"]
    # term2 = request.form["Search2"]
    #
    # for x in data:
    #     count += 1
    #     if x == select:
    #         searchform1 = count
    #     if x == select2:
    #         searchform2 = count
    #     if x == select3:
    #         searchform3 = select3
    #
    # for y in imports:
    #     if term in y[searchform1]:
    #         termlist.append(y[searchform1])
    #  #   if int(term2) in y[searchform2] and term in y:
    #  #       termlist.append(y[searchform2])
    #
    # print(termlist)
    return render_template("home.html", data=[{'name': 'Organism'}, {'name': 'Gen'}, {'name': 'Stressrespons'}])

@app.route('/Result', methods=["GET"])
def result():
    imports = {"Arabidopsis" : 500, "Pax6" : 200, "PH" : 100, "Droogte" : 20}
    return render_template("Visualisation.html", data=imports)

if __name__ == '__main__':
    app.run()
