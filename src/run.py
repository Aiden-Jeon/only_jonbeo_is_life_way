from parsing import get_timepoint_ohlcv
from trader import Trader
from tester import BackTester


def main():
    url = "https://api.upbit.com/v1/candles/minutes/30"
    data = get_timepoint_ohlcv(url, count=200).drop("volume", axis=1)
    trader = Trader()
    tester = BackTester()
    result_df = tester.run_test(trader, data)
    print(result_df)


if __name__ == "__main__":
    main()