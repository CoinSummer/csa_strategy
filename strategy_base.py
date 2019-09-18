from vnpy.trader.object import (
    TickData,
    BarData,
)


class BaseStrategy():
    """"""
    parameters = [""]
    variables = [""]

    def __init__(self, engine, name, setting):
        """"""
        self.engine = engine
        self.name = name
        self.setting = setting

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

    def on_tick(self, tick: TickData):
        pass

    def on_bar(self, bar_a: BarData, bar_b: BarData):
        pass
                