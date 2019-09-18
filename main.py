from __future__ import absolute_import, unicode_literals
from datetime import date, datetime, timedelta

from backtesting import BacktestingEngine
from strategy_high_low import HighLowStrategy
from strategy_histogram import HistogramStrategy
from strategy_realtime import RealTimeStrategy


if __name__ == "__main__":
    btengine = BacktestingEngine()
    hs_setting = {
        'influxdb_url': 'http://localhost:8086/write?db=bitmex_prod'
    }
    # btengine.add_strategy(HistogramStrategy, hs_setting)
    btengine.add_strategy(RealTimeStrategy, {})
    start = datetime(2019, 6, 13)
    end = datetime(2019, 9, 10)
    btengine.run_backtesting(start, end)


# Keep Low=> 1145883330.0 543113964.0
# Keep High=> 201438.0 403724.0
# Keep Low=> 16037865.0 11424010.0
# Keep Low=> 138105315.0 78171996.0
# Keep Low=> 178792568.0 91789949.0
# 2019-09-12 17:41:50.230664      历史数据回放结束
# 2019-09-12 17:41:50.230706      high=1,0.0007917969832534938%
# 2019-09-12 17:41:50.230715      low=126290,99.99604101508373%
# 2019-09-12 17:41:50.230722      mid=4,0.0031671879330139752%