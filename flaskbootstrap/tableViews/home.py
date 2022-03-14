from flask import Blueprint,render_template,abort
import requests
import os
from requests import ConnectionError,ConnectTimeout,HTTPError,TooManyRedirects
import csv

homeApp = Blueprint('table_page',__name__)



@homeApp.route('/home',methods=['GET','POST'])
def home():
    if requests.method =='GET':
        return render_template('table.html')
    return render_template('home.html')