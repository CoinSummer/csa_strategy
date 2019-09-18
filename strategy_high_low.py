from vnpy.trader.object import (
    TickData,
    BarData,
    TradeData,
)

class Period():
    def __init__(self):
        """"""
        self.volume_a = 0
        self.volume_b = 0
        self.price_sum = 0  
        self.count = 0
        self.avg_price_diff = 0

    def push(self, a, b):
        self.volume_a += a.volume
        self.volume_b += b.volume
        self.price_sum += b.open_price - a.open_price
        self.count += 1
        self.avg_price_diff = int(self.price_sum / self.count)

    def reset(self):
        self.volume_a = 0
        self.volume_b = 0
        self.price_sum = 0  
        self.count = 0
        self.avg_price_diff = 0

    def __str__(self):
        return f'total_count={self.count}, avg_price_diff={self.avg_price_diff}, total_volume_a={self.volume_a}, total_volume_b={self.volume_b}'   


class HighLowStrategy():
    """"""
    parameters = ["atr_length"]
    variables = ["atr_value"]

    def __init__(self, engine, strategy_name, setting):
        """"""
        self.engine = engine
        self.keep_high_volume_a = 0
        self.keep_high_volume_b = 0
        self.keep_high = 0  
        self.keep_high_price_sum = 0  

        self.keep_low_volume_a = 0
        self.keep_low_volume_b = 0
        self.keep_low = 0
        self.keep_low_price_sum = 0

        self.high = 300
        self.low = 100

        self.high_count = 0
        self.low_count = 0
        
        self.mid_count = 0

        self.period = Period()


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
        total_count = self.high_count + self.low_count + self.mid_count
        self.engine.output("历史数据回放结束")
        self.engine.output(f"high={self.high_count}m,avg_price_diff={self.keep_high_price_sum / self.high_count} | {self.high_count / total_count * 100}%")
        self.engine.output(f"low={self.low_count}m,avg_price_diff={self.keep_low_price_sum / self.low_count} | {self.low_count / total_count * 100}%")
        self.engine.output(f"mid={self.mid_count}m,{self.mid_count / total_count * 100}%")    
        # self.write_log("策略停止")

    # def on_tick(self, tick: TickData):
    #     """
    #     Callback of new tick data update.
    #     """
    #     self.bg.update_tick(tick)

    def on_bar(self, bar_a: BarData, bar_b: BarData):
        """
        Callback of new bar data update.
        """
        price_m = bar_b.open_price - bar_a.open_price
        if price_m > self.high:
            self.high_count += 1
            self.stop_keep_low()

            self.keep_high = 1
            self.keep_high_price_sum += price_m
            self.period.push(bar_a, bar_b)

            # print('A', price_m)
        elif price_m < self.low:
            self.low_count += 1
            self.stop_keep_high()

            self.keep_low = 1
            self.keep_low_price_sum += price_m
            self.period.push(bar_a, bar_b)
            # print('B', price_m)
        else:
            self.mid_count += 1
            self.stop_keep_high()
            self.stop_keep_low()
            # print('C', price_m)    
                
    def stop_keep_high(self):
        if self.keep_high == 1:
            print('Keep High=>', self.period)
            self.keep_high = 0

            self.period.reset()

    def stop_keep_low(self):
        if self.keep_low == 1:
            print('Keep Low=>', self.period)
            self.keep_low = 0
            self.period.reset()       