#importing required libraries

from flask import Flask, request, render_template, url_for
import numpy as np
import pandas as pd
from sklearn import metrics 
import warnings
import pickle
import re
import requests
import urllib
import urllib.request
import json
import whois
import socket, threading
warnings.filterwarnings('ignore')
from feature import FeatureExtraction

file = open("pickle/model.pkl","rb")
gbc = pickle.load(file)
file.close()

   # Regex to check valid URL
regex = ("((http|https)://)(www.)?" +
         "[a-zA-Z0-9@:%._\\+~#?&//=]" +
         "{2,256}\\.[a-z]" +
         "{2,6}\\b([-a-zA-Z0-9@:%" +
         "._\\+~#?&//=]*)")
compile_regex = re.compile(regex)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        if(re.search(compile_regex, url)):
            encoded_url = urllib.parse.quote(url, safe='')
            api_url = "https://ipqualityscore.com/api/json/url/4u55tgssWBVeJkP5B993zmOY0dR7GIJD/"
            data = requests.get(api_url + encoded_url)
            data_output = json.dumps(data.json(), indent=4)
            whois_info = whois.whois(url)
            result = whois_info.__dict__
            obj = FeatureExtraction(url)
            x = np.array(obj.getFeaturesList()).reshape(1,30)
            y_pred =gbc.predict(x)[0]
            #1 is safe       
            #-1 is unsafe
            y_pro_phishing = gbc.predict_proba(x)[0,0]
            y_pro_non_phishing = gbc.predict_proba(x)[0,1]
            # if(y_pred ==1 ):
            pred = "It is {0:.2f} % safe to go ".format(y_pro_phishing*100)
            return render_template('index.html',xx =round(y_pro_non_phishing,2),validity='Valid url:' ,url=url, additional_info=data_output, additional='Additional Information', check='Check Here' )
        else:
            return render_template('index.html', xx=-1, validity='Invalid url:', url=url, error='- Following error may occured:', error1='1. you forgot to add "http://" or "https://"', error2='2. Not a valid domain')
        
    return render_template("index.html", xx =-1)

app.run()
