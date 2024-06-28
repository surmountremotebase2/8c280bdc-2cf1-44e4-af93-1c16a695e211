from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Replace 'AAPL' with your targeted ticker
        self.ticker = "AAPL"  

    @property
    def interval(self):
        # Using '1day' as the interval for daily moving averages
        return "1day"

    @property
    def assets(self):
        # The targeted assets for the strategy
        return [self.ticker]

    @property
    def data(self):
        # No additional data requirements for this strategy
        return []

    def run(self, data):
        # Fetch daily data for the selected ticker
        d = data["ohlcv"]
        
        # Calculate the 20-day and 200-day simple moving averages (SMAs)
        short_sma = SMA(self.ticker, d, 20)
        long_sma = SMA(self.ticker, d, 200)
        
        # Ensure we have enough data points to calculate both SMAs
        if short_sma is None or long_sma is None or len(short_sma) < 1 or len(long_sma) < 1:
            log("Insufficient data for SMA calculations.")
            return TargetAllocation({self.ticker: 0})
        
        # Compare the latest values of the short and long SMA to determine the trend
        latest_short_sma = short_sma[-1]
        latest_long_sma = long_sma[-1]
        
        allocation = 0
        if latest_short_sma > latest_long_sma:
            # If the 20-day SMA is above the 200-day SMA, consider it a bullish signal
            log(f"Bullish crossover detected for {self.ticker}.")
            allocation = 1  # Fully allocate to this asset
        elif latest_short_sma < latest_long_sma:
            # If the 20-day SMA is below the 200-day SMA, consider it a bearish signal
            log(f"Bearish crossover detected for {self.ticker}.")
            allocation = 0  # Do not allocate to this asset
        
        # Return the allocation decision
        return TargetAllocation({self.ticker: allocation})