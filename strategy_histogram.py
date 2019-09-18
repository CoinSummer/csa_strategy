from vnpy.trader.object import (
    TickData,
    BarData,
    TradeData,
)
from datetime import datetime
from influxdb import WriteInfluxCli


class HistogramStrategy():
    """"""
    parameters = ["atr_length"]
    variables = ["atr_value"]

    def __init__(self, engine, name, setting):
        """"""
        self.engine = engine
        self.name = name
        self.setting = setting
        self.influxdb_cli = WriteInfluxCli(setting['influxdb_url'])
        self.buckets = {
            "0": 0,
            "50": 0,
            "80": 0,
            "100": 0, 
            "200": 0, 
            "300": 0, 
            "400": 0, 
            "500": 0, 
            "600": 0, 
            "700": 0, 
            "800": 0,
        }

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        pass

    def on_start(self):
        """
        Callback when strategy is started.
        """
        # self.write_log("策略启动")
        pass

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        pass
        # self.write_log("策略停止")

    # def on_tick(self, tick: TickData):
    #     """
    #     Callback of new tick data update.
    #     """
    #     self.bg.update_tick(tick)

    def write_influx(self, mix):
        ts = int(datetime.timestamp(mix['bar_pre'].datetime) * 1000)
        data = {
            "price_pre": mix['bar_pre'].open_price,
            "price_next": mix['bar_next'].open_price,
            "volume_pre": mix['bar_pre'].volume,
            "volume_next": mix['bar_next'].volume,
            "price_diff": mix['price_m'],
        }
        for kv in mix['buckets'].items():
            data['H'+kv[0]] = kv[1]

        tags = {
            "symbol_pre": mix['bar_pre'].symbol,
            "symbol_next": mix['bar_next'].symbol,
            "interval": mix['bar_pre'].interval,
        }
        name = 'csa' # f"{mix['bar_pre'].symbol}_{mix['bar_next'].symbol}"
        self.influxdb_cli.add_point(name, tags, data, ts)

    def on_bar(self, bar_a: BarData, bar_b: BarData):
        """
        Callback of new bar data update.
        """
        mix = {
            "bar_pre": bar_a,
            "bar_next": bar_b,
        }
        
        price_m = bar_b.open_price - bar_a.open_price
        mix["price_m"] = price_m

        g_buckets = self.buckets
        ktag = -1
        for k in g_buckets.keys():
            if price_m > int(k):
                ktag = k
                continue

        if int(ktag) > -1:
            g_buckets[ktag] += 1    
        else:
            g_buckets['0'] += 1      
        mix["buckets"] = g_buckets

        # print(mix)
        self.write_influx(mix)
                