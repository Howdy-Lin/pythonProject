from flask import Flask,render_template,request,redirect,url_for
from tableViews.table import  tableApp
from tableViews.youbike2 import youbikeApp

app = Flask(__name__)
app.register_blueprint(tableApp)
app.register_blueprint(youbikeApp)

import json
with open('./reptile_final.json')as f:
    data = json.load(f)
#@app.route('/')

#def index():
 #   return render_template('index.html')

@app.route('/',methods=['GET','POST'])
def home():
    if request.method =='GET':
        return redirect(url_for('table'))
    return render_template('home.html')
@app.route('/table',defaults={'region':None})
@app.route('/table/<region>')
def table(region):

    jsonObject = data
    sareas = list({datalist['品牌'] for datalist in jsonObject})

    if region is None:

        dataDict = dict()
        for key in sareas:
            regionList = [item for item in jsonObject if item['品牌'] == key]
            dataDict[key] = regionList

        for key, value in dataDict.items():
            print(key)
            #print(value)
            #print(value.__class__)
            print("=========")

        return render_template('table.html', data=data, regions=sareas)
    else:
        areaList = [item for item in jsonObject if item['品牌'] == region]
        print(areaList)
        return render_template('table.html', data=areaList, regions=sareas, region=region)



@app.route('/layout')
@app.route('/layout/box')
def layout():
    return render_template('layout.html',name='layout')

@app.route('/layout/container')
def container():
    return  render_template('container.html',name="container")

@app.route('/layout/columns')
def columns():
    return render_template('columns.html',name="columns")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)