import pandas as pd
from yahoo_fin import stock_info as si
from flask import Flask,jsonify
import time
import datetime
import requests
import json 
from random import randint
import logging


def LivePrices(key):
        number = randint(1,50)
        number1 = randint(1,100)
        currencies = ["BTCUSDT", "DOGEUSDT", "LTCUSDT"]
        url = key+currencies[0]
        data = requests.get(url)
        BTCUSDT= data.json()
        BTCUSDT = float(BTCUSDT["price"]) 

        url = key+currencies[1]
        data = requests.get(url)
        DOGEUSDT= data.json()
        DOGEUSDT = float(DOGEUSDT["price"]) 

        url = key+currencies[2]
        data = requests.get(url)
        LTCUSDT= data.json()
        LTCUSDT = float(LTCUSDT["price"])

        AMZN = si.get_live_price("AMZN") 

        MSFT = si.get_live_price("MSFT") 

        AAPL = si.get_live_price("AAPL") 

        INFY = si.get_live_price("INFY") 

        GOOG = si.get_live_price("GOOG") 

        date = datetime.datetime.now()

        val = si.get_quote_table("AMZN")["Day's Range"]
        val = val.split("-")
        minAMZN = float(val[0].strip())
        maxAMZN = float(val[1].strip())

        val = si.get_quote_table("MSFT")["Day's Range"]
        val = val.split("-")
        minMSFT = float(val[0].strip())
        maxMSFT = float(val[1].strip())

        val = si.get_quote_table("AAPL")["Day's Range"]
        val = val.split("-")
        minAAPL = float(val[0].strip())
        maxAAPL = float(val[1].strip())

        val = si.get_quote_table("INFY")["Day's Range"]
        val = val.split("-")
        minINFY = float(val[0].strip())
        maxINFY = float(val[1].strip())

        val = si.get_quote_table("GOOG")["Day's Range"]
        val = val.split("-")
        minGOOG = float(val[0].strip())
        maxGOOG = float(val[1].strip())

        return (AMZN,MSFT,AAPL,INFY,GOOG,date,BTCUSDT,DOGEUSDT,LTCUSDT,minAMZN,maxAMZN,minMSFT,maxMSFT,minAAPL,maxAAPL,minINFY,maxINFY,minGOOG,maxGOOG)

app = Flask("__name__")

@app.route("/")
def home():
    try:
        while True:
            data_raw = []
            for i in range(1):
                key = "https://api.binance.com/api/v3/ticker/price?symbol="
                row = LivePrices(key)
                data_raw.append(row)
                print("Raw data - ", data_raw)

            HEADER = ["AMZN","MSFT","AAPL","INFY","GOOG","date","BTCUSDT","DOGEUSDT","LTCUSDT","minAMZN","maxAMZN","minMSFT","maxMSFT","minAAPL","maxAAPL","minINFY","maxINFY","minGOOG","maxGOOG"]
            PowerAPi= "https://api.powerbi.com/beta/abd1682b-8c75-4e59-b3b5-42c43ec58fb2/datasets/33ab5d08-de03-4fd5-8b38-9ace36ded8c7/rows?key=j%2BgeGYJbuvW3KadXDyayagDYklEr4cgSYLz4qAClpmudesu%2F3ISwKGBmvXiPSPYtP6HMuY%2BHNRTI1TTpvMAImA%3D%3D"

            data_df = pd.DataFrame(data_raw, columns=HEADER)
            data_json = bytes(data_df.to_json(orient='records'), encoding='utf-8')
            print("JSON dataset", data_json)
            req = requests.post(PowerAPi, data_json)
            logging.info("Data is inserted into Power BI ")
    except Exception as e:
        return jsonify({"status":False,"exception":e})      
    return jsonify({"status":"timeout","message":"Please restart with sending a request to api"})

if __name__=="__main__":
    
        app.run(debug=True)
        
  

