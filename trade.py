import json
import statistics
from typing import Union, List
import pandas as pd
import numpy as np
import sys

class Utils:
    @staticmethod
    def convert_to_float_list(data_list: List[Union[str, float]]) -> List[float]:
        return [float(x) for x in data_list]

    @staticmethod
    def calculate_average(data_list: List[float]) -> float:
        return statistics.mean(data_list)

    @staticmethod
    def validate_risk_percentage(risk_percentage: Union[int, str]) -> float:
        try:
            risk_value = int(risk_percentage)
            if not 0 <= risk_value <= 100:
                raise ValueError("Error")
        except ValueError as error:
            print(error, file=sys.stderr)
            sys.exit(84)
        return risk_value / 100

    @staticmethod
    def validate_money_saver(money_saver: str) -> bool:
        if money_saver.lower() not in ["yes", "no"]:
            print("Use 'keep dollars' parameter", file=sys.stderr)
            sys.exit(84)
        return money_saver.lower() == "yes"

class VolumeVerifier:
    def verify_volume(self, volume_list: List[Union[str, float]]) -> bool:
        volume_list = Utils.convert_to_float_list(volume_list)
        return volume_list[-1] * 1.1 < Utils.calculate_average(volume_list[-6:])

class ConfigLoader:
    @staticmethod
    def load_config(config_path: str) -> dict:
        with open(config_path) as config_file:
            return json.load(config_file)

class IndicatorCalculator:
    @staticmethod
    def calculate_sma(data_list: List[float]) -> float:
        return np.mean(data_list)

    @staticmethod
    def calculate_std_dev(data_list: List[float]) -> float:
        return np.std(data_list)

    @staticmethod
    def calculate_bollinger_bands(sma: float, std_dev: float) -> List[float]:
        offset = 0.5 * std_dev
        return [sma - offset, sma, sma + offset]

    @staticmethod
    def calculate_bollinger(n: int, closing_prices: List[float]) -> List[float]:
        if len(closing_prices) < n:
            return [0, 0, 0]
        recent_closing_prices = closing_prices[-n:]
        sma = IndicatorCalculator.calculate_sma(recent_closing_prices)
        std_dev = IndicatorCalculator.calculate_std_dev(recent_closing_prices)
        return IndicatorCalculator.calculate_bollinger_bands(sma, std_dev)

    @staticmethod
    def calculing_RSI_func(data: pd.Series, period: int = 14) -> pd.Series:
        A = data.diff()
        gain, loss = A.clip(lower=0), -A.clip(upper=0)
        avg_up = gain.rolling(window=period).mean()
        avg_down = loss.rolling(window=period).mean()
        rs = avg_up / avg_down
        return 100 - (100 / (1 + rs))

    @staticmethod
    def compute_ema(period: int, data: List[float]) -> float:
        if not data:
            return None
        ema = data[0]
        multiplier = 2 / (period + 1)
        for price in data:
            ema += (price - ema) * multiplier
        return ema

class MarketCandle:
    def __init__(self, format: list, data: str) -> None:
        parts = data.split(",")
        for key, value in zip(format, parts):
            setattr(self, key, float(value) if key != "pair" else value)

    def __repr__(self) -> str:
        return f"{self.pair}{self.date}{self.close}{self.volume}"

class MarketChart:
    def __init__(self) -> None:
        self.dates, self.opens, self.highs, self.lows, self.closes, self.volumes = [], [], [], [], [], []
        self.indicators = {}

    def add_candle(self, candle: MarketCandle) -> None:
        for attr in ['date', 'open', 'high', 'low', 'close', 'volume']:
            getattr(self, attr + 's').append(getattr(candle, attr))

class BotState:
    def __init__(self) -> None:
        self.time_vault = self.max_time_vault = self.time_per_action = self.candle_span = 1
        self.total_ticks = self.ticks_provided = 0
        self.initial_funds, self.transaction_cost, self.present_date = 1000, 0.2, 0
        self.funds, self.graphs = {}, {}
        self.price_log, self.volume_log = [], []
        self.position_active = self.quick_above_slow = self.swifter_above_swift = False
        self.ema_9 = self.ema_13 = self.ema_20 = self.ema_50 = 0
        self.bollinger_lines, self.hold_for_safety = [], False
        self.initiated_position_price, self.risk_ratio = 0, 0
        self.saver_mode = True

    def refresh_indicators(self) -> None:
        self.ema_9 = IndicatorCalculator.compute_ema(9, self.price_log)
        self.ema_13 = IndicatorCalculator.compute_ema(13, self.price_log)
        self.ema_20 = IndicatorCalculator.compute_ema(20, self.price_log)
        self.ema_50 = IndicatorCalculator.compute_ema(50, self.price_log)
        self.quick_above_slow = self.ema_9 < self.ema_13
        self.swifter_above_swift = self.ema_20 < self.ema_50
        for pair, graph in self.graphs.items():
            graph.indicators['rsi'] = IndicatorCalculator.calculing_RSI_func(pd.Series(graph.closes)).tolist()
        self.bollinger_lines = IndicatorCalculator.calculate_bollinger(11, self.price_log)

    def refresh_market_chart(self, pair: str, new_candle_str: str) -> None:
        if pair not in self.graphs:
            self.graphs[pair] = MarketChart()
        self.graphs[pair].add_candle(MarketCandle(self.candle_format, new_candle_str))
        self.primary_currency, self.secondary_currency = pair.split('_')

    def refresh_balance(self, currency: str, amount: float) -> None:
        self.funds[currency] = amount

    def refresh_settings(self, key: str, value: str) -> None:
        if key in {"time_vault", "time_per_action", "candle_span", "total_ticks", "ticks_provided", "initial_funds"}:
            setattr(self, key, int(value))
        elif key == "transaction_cost_percent":
            self.transaction_cost = float(value)
        elif key == "candle_format":
            self.candle_format = value.split(",")

    def refresh_game_data(self, key: str, value: str) -> None:
        if key == "next_candles":
            self._process_next_candles(value)
        elif key == "stacks":
            self._process_stacks(value)

    def _process_next_candles(self, value: str) -> None:
        abc = value.split(";")
        self.present_date = int(abc[0].split(",")[1])
        for candle_data in abc:
            self.refresh_market_chart(candle_data.split(",")[0], candle_data)
        last_candle = abc[-1].split(",")
        self.price_log.append(float(last_candle[5]))
        self.volume_log.append(float(last_candle[6]))

    def _process_stacks(self, value: str) -> None:
        balances = value.split(",")
        for balance_str in balances:
            currency, amount = balance_str.split(":")
            self.refresh_balance(currency, float(amount))

class TradingBot:
    def __init__(self) -> None:
        self.state = BotState()
        self.volume_verifier = VolumeVerifier()
        self.config_loader = ConfigLoader()

    def retrieve_risk_settings(self) -> Union[list, None]:
        config = self.config_loader.load_config('./setting.json')
        return [Utils.validate_risk_percentage(config['exposure in %']), Utils.validate_money_saver(config["keep dollars"])]

    def inspect_position(self, initiated_position, present_price) -> bool:
        try:
            return initiated_position * 1.2 < present_price
        except Exception as error:
            print(error, file=sys.stderr)
            return False

    def operate(self) -> None:
        self.state.risk_ratio, self.state.saver_mode = self.retrieve_risk_settings()
        while True:
            command = input()
            if command == "end":
                sys.exit(0)
            if command:
                self.process_command(command)

    def process_command(self, command: str) -> None:
        parts = command.split(" ")
        if parts[0] == "settings":
            self.state.refresh_settings(parts[1], parts[2])
        elif parts[0] == "update" and parts[1] == "game":
            self.state.refresh_game_data(parts[2], parts[3])
        elif parts[0] == "action":
            usd_balance = self.state.funds[self.state.primary_currency]
            foreign_balance = self.state.funds[self.state.secondary_currency]
            present_price = self.state.graphs[f"{self.state.primary_currency}_{self.state.secondary_currency}"].closes[-1]
            available_quantity = (usd_balance - 1000) / present_price if self.state.saver_mode and usd_balance > 1000 else usd_balance / present_price
            self.state.refresh_indicators()
            rsi_value = self.state.graphs[f"{self.state.primary_currency}_{self.state.secondary_currency}"].indicators['rsi'][-1]
            if usd_balance + (foreign_balance * present_price) < 200:
                print('pass')
            elif self.state.hold_for_safety:
                if self.state.bollinger_lines[1] > present_price:
                    print('pass')
                    self.state.hold_for_safety = False
                else:
                    print('pass')
            elif (self.state.bollinger_lines[1] < present_price and not self.state.position_active and self.state.quick_above_slow and
                  self.state.swifter_above_swift and self.state.ema_50 > present_price and rsi_value < 45 and self.volume_verifier.verify_volume(self.state.volume_log)):
                print(f'buy {self.state.primary_currency}_{self.state.secondary_currency} {available_quantity * self.state.risk_ratio}')
                self.state.position_active = True
                self.state.initiated_position_price = present_price
            elif self.state.position_active and self.inspect_position(self.state.initiated_position_price, present_price):
                print(f'sell {self.state.primary_currency}_{self.state.secondary_currency} {foreign_balance}')
                self.state.position_active = False
                self.state.hold_for_safety = True
            elif self.state.position_active:
                if self.state.bollinger_lines[2] > present_price and not self.state.quick_above_slow or rsi_value > 70:
                    print(f'sell {self.state.primary_currency}_{self.state.secondary_currency} {foreign_balance}')
                    self.state.position_active = False
                else:
                    print('pass')
            else:
                print('pass')

if __name__ == "__main__":
    bot = TradingBot()
    bot.operate()
