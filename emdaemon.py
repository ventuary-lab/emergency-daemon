import pywaves as pw
from time import sleep
import requests as req
import json as jsn

oraclesSC = ""
oracle = pw.Oracle(oracleAddress = oraclesSC)
oraclePrice = pw.Oracle(oracleAddress = "")

address = pw.Address(privateKey = '') #production_prk

def main():
    while True:
        try:
            bh = pw.height()
            r = req.get(url = "https://api.binance.com/api/v3/avgPrice", 
                        params = {'symbol': 'WAVESUSDT'})
            if r.status_code == 200:
                refPrice = float(jsn.loads(r.text)['price'])
                scPrice = float((oraclePrice.getData(regex = 'price')[0])['value'])/100
                diff = 100*((refPrice - scPrice)/refPrice)
                is_blocked_status = (oracle.getData(regex = 'is_blocked')[0])['value']
                if not is_blocked_status and (diff >= 7 or diff <= -10):
                    tx = address.invokeScript(oraclesSC, 'callEmergencyShutdown', 
                              [{ "type": "string", "value": "more_7-10prc_price_deviation_from_ref" }], [])
                    print("Status- ES: price-ref: " + str(refPrice) + "; price-sc: " + str(scPrice) + "; diff (%): " + str(diff))
                elif is_blocked_status:
                    print("Status- SHUTDOWN: price-ref: " + str(refPrice) + "; price-sc: " + str(scPrice) + "; diff (%): " + str(diff))
                else:
                    print("Status- OK: price-ref: " + str(refPrice) + "; price-sc: " + str(scPrice) + "; diff (%): " + str(diff))
        except Exception as inst:
            print(inst)
        sleep(11)

if __name__ == "__main__":
    main()