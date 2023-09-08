from flask import Flask, render_template, url_for, request, redirect, json, jsonify
import os
import requests

app = Flask(__name__)

myData = {}

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':

        updateData= {
            "code":{},
            "name":{},
            "capacity":{},
            "description":{},
            "props": {
                 "key":{},
                 "value":{}
            }
        }
        Code = request.form.get("code")
        Name = request.form.get("name")
        Capacity = int(request.form.get("capacity"))
        Description = request.form.get("description")
        PropsKey = request.form.get("propsKey")
        PropsValue = request.form.get("propsValue")
        updateData["code"] = Code
        updateData["name"] = Name
        updateData["capacity"] = Capacity
        updateData["description"] = Description
        updateData["props"]["key"] = PropsKey
        updateData["props"]["value"] = PropsValue

        res = requests.post("http://192.168.0.245:42041/docks", json=updateData)
        res_json = res.json()
        print(res.status_code)
        print(res_json)

        return redirect("/")
        
    else:
                
                r = requests.get("http://192.168.0.245:42041/docks")
                data = r.json()
                myData = data
                with open("denemeData", "w") as outfile:
                    json.dump(myData, outfile)
                dumpData = json.dumps(myData, indent=2)
                with open("docks.txt","w") as f:
                    f.write(dumpData)
                return render_template("index.html", docks = myData)
            

@app.route("/delete/<string:id>")
def delete(id):

    res = requests.delete(f"http://192.168.0.245:42041/docks/{id}")
    res_json = res.json()
    print(res.status_code)
    print(res_json)

    return redirect("/")

@app.route("/update/<string:id>", methods = ["GET", "POST","PUT"])
def update(id):

    if request.method == 'POST':

        res = requests.get(f"http://192.168.0.245:42041/docks/{id}")
        data = res.json()
        myData = data

        updateData= {
            "code":{},
            "name":{},
            "capacity":{},
            "description": {},
            "props":{
                 "key":{},
                 "value":{}
            }
        }
        Code = myData.get("code")
        Name = request.form.get("name")
        Capacity = int(request.form.get("capacity"))
        Description = request.form.get("description")
        PropsKey = request.form.get("propsKey")
        PropsValue = request.form.get("propsValue")
        updateData["code"] = Code
        updateData["name"] = Name
        updateData["capacity"] = Capacity
        updateData["description"] = Description
        updateData["props"]["key"] = PropsKey
        updateData["props"]["value"] = PropsValue

        res_put = requests.put(f"http://192.168.0.245:42041/docks/{id}", json= updateData)
        res_json = res_put.json()
        print(res_put.status_code)
        print(res_json)

        return redirect("/")

    else:

        res = requests.get(f"http://192.168.0.245:42041/docks/{id}")
        data = res.json()
        print(res.status_code)
        print(data)
        myData = data
        return render_template('update.html', dock = myData) 

if __name__ == "__main__":
    app.run(debug=True)