# -*- coding: utf-8 -*-

import pandas as pd
import data
from shapely.geometry import Point, shape

from flask import Flask
from flask import render_template
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def get_data():
    # Code from the previous section: Data preparation
    return data.cleaned_data()
    
#    return df_clean.to_json(orient='records')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)