#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Flask, make_response, request
import json
import random
from Model.TextAnalyze import TextAnalyze as ta



app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
# 現在対応しているECサイト
shopList =['rakuten', 'yahoo']

@app.route('/')
def hello():

    return 'test Server'

# レビューの単語の頻出数を返す
@app.route('/total_frequent_count/')
def totalFrequentCount():

    text = request.args.get("word", "Not defined")
    txt = ta()
    returnDic = {'main': ''}
    returnDic['main'] = txt.frequentWords(text)

    response = make_response(str(json.dumps(returnDic)))
    response.status_code = 200

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['mimetype'] = 'application/json'
    response.headers['Content-Type'] = 'application/json'

    return response

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True, threaded=True)
