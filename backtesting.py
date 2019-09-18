from collections import defaultdict
from datetime import date, datetime, timedelta

import sys
sys.path.append('/Users/vanzhangxun/workspace/kingsummer/vnpy')


from vnpy.trader.constant import (Direction, Offset, Exchange, Interval, Status)
from vnpy.trader.object import  BarData
from vnpy.trader.database import database_manager


# buckets = [0, 50, 100, 200, 300, 400, 500, 600, 700, 800]

class BacktestingEngine:
    """"""

    gateway_name = "BACKTESTING"

    def __init__(self):
        """"""
        self.start = None
        self.end = None
        self.step_days = 1

        self.a_count = 0
        self.b_count = 0
        self.c_count = 0
        self.db_mgr = None
        self.strategy_class = None
        self.strategy = None   
        
    def set_parameters(
        self,
        # interval: Interval,
        start: datetime,
        end: datetime = None,
    ):
        """"""
        self.start = start
        self.cur = start
        if end:
            self.end = end

    def add_strategy(self, strategy_class: type, setting: dict):
        """"""
        self.strategy_class = strategy_class
        self.strategy = strategy_class(
            self, strategy_class.__name__, setting
        )

    def load_data(self, symbol, start, end):
        # return self.db_mgr
        return database_manager.load_bar_data(symbol, Exchange('BITMEX'), Interval.MINUTE, start, end)
 
    def run_backtesting(self, start, end):

        self.strategy.on_init()
        self.strategy.inited = True
        self.output("策略初始化完成")

        self.strategy.on_start()
        # self.strategy.trading = True
        self.output("开始回放历史数据")

        start = start or datetime(2019, 6, 13)
        end = end or datetime(2019, 8, 15)
        while start < end:
            self.step(start)
            start += timedelta(days=1)
        self.strategy.on_stop()

    def step(self, start):
        """"""
        end = start + timedelta(days=1)
        arr_z19 = self.load_data('XBTZ19', start, end)
        if len(arr_z19) > 1:
            start = arr_z19[0].datetime
            end = arr_z19[-1].datetime
            arr_u19 = self.load_data('XBTU19', start, end)
            j = 0
            while j < len(arr_z19) and j < len(arr_u19):
                # print(arr_z19[j].datetime, arr_u19[j].close_price, arr_z19[j].close_price)
                self.new_bar(arr_u19[j], arr_z19[j])
                j += 1
       

        # # Use the rest of history data for running backtesting
        # for data in self.history_data[ix:]:
        #     func(data)

    def new_bar(self, bar_a: BarData, bar_b: BarData):
        """"""
        # self.cross_limit_order()
        # self.cross_stop_order()
        self.strategy.on_bar(bar_a, bar_b)
  
    def write_log(self, msg):
        """
        Write log message.
        """
        msg = f"{self.datetime}\t{msg}"
        self.logs.append(msg)

    def output(self, msg):
        """
        Output message of backtesting engine.
        """
        print(f"{datetime.now()}\t{msg}")

