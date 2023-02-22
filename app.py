#importing required libraries
from flask import Flask, request, render_template, url_for
# import numpy as np
# import pandas as pd
# from sklearn import metrics 
import warnings
# import pickle
import re
import requests
import urllib
import urllib.request
import json
# import whois
# import socket, threading
import validators
warnings.filterwarnings('ignore')


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
        valid_url = validators.url(url)
        if(re.search(compile_regex, url) and valid_url==True):
            encoded_url = urllib.parse.quote(url, safe='')
            api_url = "https://ipqualityscore.com/api/json/url/4u55tgssWBVeJkP5B993zmOY0dR7GIJD/"
            data = requests.get(api_url + encoded_url)
            data_output = json.dumps(data.json(), indent=4)
            percentage = json.loads(data_output)
            perc = percentage["risk_score"]
            updated_perc = str(100-perc)
            if perc !=0:
                output = 'Website is ' + updated_perc +'% safe to use'
            else:
                output = 'Website is 100% safe to use'
            return render_template('index.html',validity='Valid url' ,url=url, additional_info=data_output, additional='Additional Information', check='Check Here', risk=output)
        else:
            return render_template('index.html', validity='Invalid url:', url=url, error='- Following error may occured:', error1='1. you forgot to add "http://" or "https://"', error2='2. Not a valid domain')
        
    return render_template("index.html", xx =-1)
if __name__ == '__main__':
    app.run()