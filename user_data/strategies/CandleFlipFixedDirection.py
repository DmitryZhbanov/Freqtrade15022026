from datetime import datetime
from typing import Optional

import pandas as pd
from freqtrade.strategy import IStrategy
from freqtrade.persistence import Trade


class CandleFlipFixedDirection(IStrategy):

    timeframe = "15m"
    process_only_new_candles = True
    startup_candle_count = 1

    trade_direction = "short"

    minimal_roi = {
        "0": 0.07
    }

    stoploss = -0.007

    use_exit_signal = False
    can_short = True

    # ==========================
    # Indicators
    # ==========================

    def populate_indicators(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        return dataframe

    # ==========================
    # Entry
    # ==========================

    def populate_entry_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe["enter_long"] = 0
        dataframe["enter_short"] = 0

        if self.trade_direction == "long":
            dataframe.loc[:, "enter_long"] = 1
        else:
            dataframe.loc[:, "enter_short"] = 1

        return dataframe

    # ==========================
    # REQUIRED (even if unused)
    # ==========================

    def populate_exit_trend(self, dataframe: pd.DataFrame, metadata: dict) -> pd.DataFrame:
        dataframe["exit_long"] = 0
        dataframe["exit_short"] = 0
        return dataframe

    # ==========================
    # Timed exit after 1 candle
    # ==========================

    def custom_exit(
        self,
        pair: str,
        trade: Trade,
        current_time: datetime,
        current_rate: float,
        current_profit: float,
        **kwargs
    ):
        candle_seconds = 15 * 60

        if (current_time - trade.open_date_utc).total_seconds() >= candle_seconds:
            return "time_exit"

        return None

    # ==========================
    # Futures leverage
    # ==========================

    def leverage(
        self,
        pair: str,
        current_time: datetime,
        current_rate: float,
        proposed_leverage: Optional[float] = None,
        max_leverage: float = 20.0,
        entry_tag: Optional[str] = None,
        side: Optional[str] = None,
        **kwargs
    ) -> float:
        return 1.0
