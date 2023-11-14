from flask import Flask, render_template, jsonify, request
import mongo
import json
#initialization of server
app = Flask('__name__',static_url_path='/static')

#load filters so that not to run ask database everytime for filter names
def loadFilters():
    data = mongo.getData()
    filters = {"end_year": set(), "topic": set(), "sector": set(), "region": set(), "pestle": set(), "source": set(),
               "country": set()}

    for x in data:
        filters["end_year"].add(x["end_year"])
        filters["topic"].add(x["topic"])
        filters["sector"].add(x["sector"])
        filters["region"].add(x["region"])
        filters["pestle"].add(x["pestle"])
        filters["source"].add(x["source"])
        filters["country"].add(x["country"])
    for k in filters:
        filters[k] = list(filters[k])
        if k == "end_year":
            filters[k] = sorted(filters[k], key=lambda x: x if isinstance(x, int) else -9999999)
            continue
        filters[k] = list(filters[k])
        filters[k].sort()
    return filters
filters = loadFilters()

#entry point
@app.route("/")
def displayChart():
    return render_template("displayChart.html",data=None)

#Chosing the Filter page
@app.post("/filter=<variable>")
def displayVariable(variable):
    print(variable)
    print(filters[variable])
    return render_template("filterChose.html",type=variable,variables=filters[variable])

#Filtering the data and passing it to html file
@app.post("/filter")
def showGraph():
    filter ={}
    for x in request.args:
        try:
            filter[x] = int(request.args.get(x))
        except Exception:
            filter[x] = request.args.get(x)
    filtered_data = mongo.getData(filter)
    print(filtered_data)
    return render_template("displayChart.html",data=json.dumps(filtered_data, default=str))




#simple API to get Data from database
#Enter query in form "/getdata?end_year=2016&topic=oil"
@app.route("/getdata")
def getFullData():
    filter={}
    for k in request.args:
        try:
            filter[k]=int(request.args.get(k))
        except Exception:
            filter[k]=request.args.get(k)
    print(filter)
    temp="{"
    json_data = mongo.getData(filter)
    for x in json_data:
        temp+='{'
        for k in x:
            if k!="_id":
                temp+= f''' {'"'+(str(k)+'"'+':'+'"'+str(x[k])+'"'+',')} '''
        temp = temp[0:len(temp)-1]
        temp+= '}'
    temp+='}'
    print(temp)
    return jsonify(temp)



#script run
if __name__=="__main__":
    app.run()