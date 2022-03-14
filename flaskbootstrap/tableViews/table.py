from flask import Blueprint,render_template,abort
import requests
import os
from requests import ConnectionError,ConnectTimeout,HTTPError,TooManyRedirects
import csv

tableApp = Blueprint('table_page',__name__)

import json
with open('./reptile_final.json')as f:
    data = json.load(f)




@tableApp.route('/衛生紙',defaults={'region':None})
@tableApp.route('/衛生紙/<region>')
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