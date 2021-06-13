import sys
from iqoptionapi.stable_api import IQ_Option
import time
from datetime import datetime
from datetime import timedelta
from dateutil import tz
import numpy as np
import pandas as pd
from connect import *


df = 0


class temp_candles:
    c = connect()
    c.conn()

    def timestamp_converter(self, x):  # Function to convert timestamp
        hour = datetime.strptime(
            datetime.utcfromtimestamp(x).strftime("%Y-%m-%d %H:%M:%S"),
            "%Y-%m-%d %H:%M:%S",
        )
        hour = hour.replace(tzinfo=tz.gettz("GMT"))
        return hour

    def get_candles(self):

        timestamp = Iq.get_server_timestamp()
        hour = self.timestamp_converter(timestamp)
        candles = []
        # Take the last 20,000 candles and create a dataframe
        for i in range(20):
            X = Iq.get_candles(pair, 300, 2000, timestamp)
            timestamp = int(X[0]["from"]) - 1
            candles += X

        price_data = pd.DataFrame(candles)
        price_data.sort_values(by=["from"], inplace=True, ascending=True)
        price_data = price_data[
            [
                "from",
                "open",
                "close",
                "min",
                "max",
                "volume",
            ]
        ]
        price_data["change_price"] = price_data["close"].diff()
        df = price_data
        c = []
        h = []
        t = []
        b = []
        p = 10000000
        for i in range(len(df)):
            if df["open"][i] > df["close"][i]:
                c.append("down")
                t.append(((df["close"][i] * p) - (df["min"][i] * p)) / 2)
                h.append(((df["max"][i] * p) - (df["open"][i] * p)) / 2)
                b.append(((df["open"][i] * p) - (df["close"][i] * p)) / 2)
            elif df["open"][i] < df["close"][i]:
                c.append("up")
                h.append(((df["max"][i] * p) - (df["close"][i] * p)) / 2)
                t.append(((df["open"][i] * p) - (df["min"][i] * p)) / 2)
                b.append(((df["close"][i] * p) - (df["open"][i] * p)) / 2)
            else:
                c.append("nan")
                h.append(0)
                t.append(0)
                b.append(0)
        df["candle"] = c
        df["head"] = h
        df["body"] = b
        df["tail"] = t

        df = df.dropna(axis=0, how="any")
        # print(df)
        return df

    def get_candle(self):
        df = Iq.get_candles(pair, 60, 3, time.time())
        # print(df)
        return df