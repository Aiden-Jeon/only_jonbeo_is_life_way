import random
from typing import Tuple

import pandas as pd


class Trader:
    def __init__(self, seed_money: float = 1e5, wallet: float = 0):
        self.balance = seed_money
        self.wallet = wallet
        self.avg_price = 0
        self.prev_data = None

    def sell_or_buy(self, prev_data: pd.DataFrame) -> Tuple[str, float, float]:
        # init
        coin = random.uniform(-1, 1)
        if coin < 0:
            action = "buy"
            price = self.how_much_to_buy(prev_data)
            volume = 1
        else:
            action = "sell"
            price = self.how_much_to_sell(prev_data)
            volume = 1
        # policy
        if self.wallet == 0:
            action = "buy"
            price = self.how_much_to_buy(prev_data)
            volume = 1
        elif action == "sell":
            if price <= self.avg_price * 0.95:
                action = "not sell"
        return action, price, volume

    def how_much_to_buy(self, data: pd.DataFrame) -> float:
        return data.iloc[-1].min()

    def how_much_to_sell(self, data: pd.DataFrame) -> float:
        return data.iloc[-1].max()

    def enough_to_sell(self, volume: float) -> bool:
        if self.wallet >= volume:
            return True
        else:
            return False

    def update_wallet(
        self, action: str, result: bool, price: float, volume: float
    ) -> None:
        if result:
            if action == "buy":
                if volume * price > self.balance:
                    volume = self.balance // price
                self.avg_price = self.wallet * self.avg_price + volume * price
                self.wallet += volume
                self.avg_price /= self.wallet
                self.balance -= volume * price
            elif action == "sell":
                if self.wallet < volume:
                    volume = self.wallet
                self.wallet -= volume
                self.balance += volume * price

    def run_trade(self, data):
        if self.prev_data is None:
            action = "do nothing"
            price = 0
            volume = 0
        else:
            action, price, volume = self.sell_or_buy(self.prev_data)
        self.prev_data = data
        return action, price, volume
