from vnpy.trader.object import (
    TickData,
    BarData,
    TradeData,
)
from datetime import datetime
from strategy_base import BaseStrategy

XBt = 1 # sotoshi
XBT = 100000000  # bitcoin

class RealTimeStrategy(BaseStrategy):
    """"""

    def __init__(self, engine, name, setting):
        """"""
        super(RealTimeStrategy, self).__init__(engine, name, setting)
        self.volume_limit = 100000
        self.leverage = 3

        self.price_diff_h = 300
        self.price_diff_l = 100

        self.mode_pre = 0
        # self.orders_pre = []
        # self.orders_next = []
        self.volume_long_pre = 0
        self.value_long_pre = 0
        self.earn_long_pre = 0

        self.volume_short_pre = 0
        self.value_short_pre = 0
        self.earn_short_pre = 0

        self.volume_short_next = 0
        self.value_short_next = 0
        self.earn_short_next = 0

        self.volume_long_next = 0
        self.value_long_next = 0
        self.earn_long_next = 0
     
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

        # 平仓所有 计算收益
        if self.volume_short_pre > 0:
            v_s_p = self.volume_short_pre
            self.volume_short_pre -= v_s_p
            self.earn_short_pre -= self.last_bar['pre'].open_price * v_s_p
                # 平仓远期
        if self.volume_long_next > 0:        
            v_l_n = self.volume_long_next
            self.volume_long_next -= v_l_n  
            self.earn_long_next += self.last_bar['next'].open_price * v_l_n

        if self.volume_long_pre > 0:
            v_l_p = self.volume_long_pre
            self.volume_long_pre -= v_l_p
            self.earn_long_pre += self.last_bar['pre'].open_price * v_l_p
        # 平仓远期
        if self.volume_short_next > 0:       
            v_s_n = self.volume_short_next
            self.volume_short_next -= v_s_n    
            self.earn_short_next -= self.last_bar['next'].open_price * v_s_n

        print('short_pre', self.volume_short_pre, self.earn_short_pre)
        print('long_next', self.volume_long_next, self.earn_long_next)
        print('long_pre', self.volume_long_pre, self.earn_long_pre)
        print('short_next', self.volume_short_next, self.earn_short_next)

        earn = self.earn_short_pre + self.earn_long_next + self.earn_long_pre + self.earn_short_next
        print('earn',  earn)
        # self.write_log("策略停止")


    def on_bar(self, bar_a: BarData, bar_b: BarData):
        """
        Callback of new bar data update.
        """
        self.last_bar = {
            'pre': bar_a,
            'next': bar_b,
        }
        price_m = bar_b.open_price - bar_a.open_price
        if price_m > self.price_diff_h:
            # 先做平仓 快速平仓
            
            if self.volume_short_pre > 0 or self.volume_long_next > 0:
                v_s_p = min(self.volume_short_pre, bar_a.volume)
                self.volume_short_pre -= v_s_p
                self.earn_short_pre -= bar_a.open_price * v_s_p
                # 平仓远期
                v_l_n = min(self.volume_long_next, bar_b.volume)
                self.volume_long_next -= v_l_n  
                self.earn_long_next += bar_b.open_price * v_l_n
                print(f'{bar_a.datetime} =平仓 U19空仓 Z19多仓 U19:price={bar_a.open_price},Z19:price={bar_b.open_price},volume_short_pre={self.volume_short_pre},volume_long_next={self.volume_long_next}')
                return
            # else:
            #     print('-----A') 
            v = min(bar_a.volume, bar_b.volume)

            # 购买不能超过限制
            v_l_p = v if self.volume_long_pre + v < self.volume_limit else (self.volume_limit - self.volume_long_pre)
            self.volume_long_pre += v_l_p
            self.earn_long_pre -= v_l_p * bar_a.open_price

            v_s_n = v if self.volume_short_next + v < self.volume_limit else self.volume_limit - self.volume_short_next
            self.volume_short_next += v_s_n
            self.earn_short_next += bar_b.open_price * v_s_n
            #
            if v_l_p > 0 or v_s_n > 0:
                print(f'{bar_a.datetime} U19开多 Z19开空 U19:price={bar_a.open_price},Z19:price={bar_b.open_price},volume={v},volume_long_pre={self.volume_long_pre},volume_short_next={self.volume_short_next}')
            # else:
                # print('--------C')
            # self.orders_pre.push({ 'mode': 'long', 'price': bar_a.open_price, 'volume': v, 'cost': cost_a, 'ts': datetime.time() })
            # self.orders_next.push({ 'mode': 'short', 'price': bar_a.open_price, 'volume': v, 'cost': cost_a, 'ts': datetime.time() })

        elif price_m < self.price_diff_l:
            # 如果当前还有仓位 要先平仓
            if self.volume_long_pre > 0 or self.volume_short_next > 0:
                v_l_p = min(self.volume_long_pre, bar_a.volume)
                self.volume_long_pre -= v_l_p
                self.earn_long_pre += bar_a.open_price * v_l_p
                # 平仓远期
                v_s_n = min(self.volume_short_next, bar_b.volume)
                self.volume_short_next -= v_s_n    
                self.earn_short_next -= bar_b.open_price * v_s_n
                print(f'{bar_a.datetime} =平仓 U19多仓 Z19空仓 U19:price={bar_a.open_price},Z19:price={bar_b.open_price},volume_long_pre={self.volume_long_pre},volume_short_next={self.volume_short_next}')
                return
            # else:
            #     print('-----B')    

            v = min(bar_a.volume, bar_b.volume)

            # 购买不能超过限制
            v_s_p = v if self.volume_short_pre + v < self.volume_limit else self.volume_limit - self.volume_short_pre
            self.earn_short_pre += v_s_p * bar_a.open_price
            self.volume_short_pre += v_s_p

            v_l_n = v if self.volume_long_next + v < self.volume_limit else self.volume_limit - self.volume_long_next
            self.earn_long_next -= bar_b.open_price * v_l_n
            self.volume_long_next += v_l_n
            if v_s_p > 0 or v_l_n > 0:
                print(f'{bar_a.datetime} u19开空 Z19开多 U19:price={bar_a.open_price},Z19:price={bar_b.open_price},volume={v},volume_short_pre={self.volume_short_pre},volume_long_next={self.volume_long_next}')
            # else:
                # print('-------D')
        