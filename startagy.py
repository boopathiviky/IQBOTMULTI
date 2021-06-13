from candlestick import candlestick
import pandas as pd
from datetime import datetime
from levefinderv_2 import get_pivote
import asyncio

# from temp_candle import temp_candles
from trade import trade
import time


# c = connect()
# c.conn()
# tc = temp_candles()

def my_bot(pair, connect, Iq):

    print("\n starting bot for "+pair)
    print("\n checking candles wait... "+pair)
    ACTIVES = pair
    Money = 7
    print(ACTIVES)
    expirations_mode = 1
    x = 0
    while x < 10:
        x = x+1
        #     minute = float(((datetime.now()).strftime("%M.%S"))[1:])
        #     enter = True if (minute >= 4.58 and minute <= 5) or minute >= 9.58 else False
        #     print("Time to get in?", enter, "/Minutes:", minute)
        remaning_time = Iq.get_remaning(expirations_mode)
        purchase_time = remaning_time - 30
        print('For '+str(pair)+' ' +str(purchase_time))
        if purchase_time == 37:
            d = Iq.get_candles(pair, 60, 3, time.time())
            current_close = d[2]["close"]
            print('For '+str(pair)+' ' +str(current_close))
            p1, p, p2 = get_pivote(current_close)
            print('For '+str(pair)+' ' +str(p1))
            print('For '+str(pair)+' ' +str(p))
            print('For '+str(pair)+' ' +str(p2))
            
        if purchase_time == 31:
            data = Iq.get_candles(pair, 60, 3, time.time())
            print("\n enter into trade for "+str(pair))
            df = pd.DataFrame.from_dict(data)

            df.rename(columns={"max": "high", "min": "low"}, inplace=True)
            print(str(df)+' For '+str(pair))
            current_close = df["close"][2]
            res = candlestick.bullish_engulfing(df, target="bullish_engulfing")
            df = res
            res = candlestick.bearish_engulfing(df, target="bearish_engulfing")
            ca1 = res.to_dict("records")
            for data in ca1:
                if data["bullish_engulfing"] == True:
                    print(
                        "bullish_engulfing---> for "+str(pair),
                        datetime.fromtimestamp(int(data["from"])),
                        data["bullish_engulfing"],
                    )
                    if p < current_close:
                        trade("buy", Money)
                        print("bullish engaling to buy for "+str(pair))
                    else:
                        print("levels does not match for "+str(pair))
                if data["bearish_engulfing"] == True:
                    print(
                        "bearish engalifing----> for "+str(pair),
                        datetime.fromtimestamp(int(data["from"])),
                        data["bearish_engulfing"],
                    )
                    if p > current_close:
                        print("bearish engalifing to sell for "+str(pair))
                        trade("sell", Money)
                    else:
                        print("levels does not match for "+str(pair))
                    break

        time.sleep(1)