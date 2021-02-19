from typing import Tuple
import pandas as pd


class BackTester:
    def __init__(self, fee: float = 0.05):
        self.fee = fee

    def really_bought(
        self, price: float, low: float, high: float
    ) -> Tuple[bool, float, float]:
        assert low <= high
        action_price = min(high, price) + self.fee * price
        if low < price:
            action_result = True
        else:
            action_result = False
        return action_result, action_price

    def really_sold(
        self, price: float, low: float, high: float
    ) -> Tuple[bool, float, float]:
        assert low <= high
        action_price = price - self.fee * price
        if price < high:
            action_result = True
        else:
            action_result = False
        return action_result, action_price

    def run_test(self, trader, data):
        result = {}
        for index, value in data.iterrows():
            action, price, volume = trader.run_trade(value)
            if action == "buy":
                action_result, action_price = self.really_bought(
                    price, value.low, value.high
                )
            elif action == "sell":
                action_result, action_price = self.really_sold(
                    price, value.low, value.high
                )
            else:
                action_result = None
                action_price = price
            trader.update_wallet(action, action_result, action_price, volume)
            result[index] = dict(
                action=action,
                action_result=action_result,
                action_price=action_price,
                volume=volume,
                trader_wallet=trader.wallet,
                trader_balance=trader.balance,
                cur_high=value.high,
                cur_low=value.low,
                cur_avg=(value.high + value.low) / 2,
                total_balance=trader.balance
                + trader.wallet * (value.high + value.low) / 2,
            )
        return pd.DataFrame(result.values(), index=result.keys())
