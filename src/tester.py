from typing import Tuple
import pandas as pd


class BackTester:
    def __init__(self, fee: float = 0.05):
        self.fee = fee

    def really_bought(
        self, price: float, volume: float, low: float, high: float
    ) -> Tuple[bool, float, float]:
        assert low <= high
        action_price = min(high, price) + self.fee * price
        action_volume = volume
        if low < price:
            action_result = True
        else:
            action_result = False
        return action_result, action_price, action_volume

    def really_sold(
        self, price: float, volume: float, low: float, high: float
    ) -> Tuple[bool, float, float]:
        assert low <= high
        action_price = price - self.fee * price
        action_volume = volume
        if price < high:
            action_result = True
        else:
            action_result = False
        return action_result, action_price, action_volume

    def run_test(self, trader, data):
        result = {}
        for index, value in data.iterrows():
            action, price, volume = trader.run_trade(data)
            if action == "buy":
                action_result, action_price, action_volume = self.really_bought(
                    price, volume, value.low, value.high
                )
            elif action == "sell":
                action_result, action_price, action_volume = self.really_sold(
                    price, volume, value.low, value.high
                )
            else:
                action_result = None
                action_price = price
                action_volume = volume
            trader.update_wallet(action, action_result, action_price, action_volume)
            result[index] = dict(
                action=action,
                action_result=action_result,
                action_price=action_price,
                trader_wallet=trader.wallet,
                trader_balance=trader.balance,
            )
        return pd.DataFrame(result.values(), index=result.keys())
