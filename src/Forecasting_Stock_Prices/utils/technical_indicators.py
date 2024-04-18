import numpy as np
import pandas as pd


def MACD(DF, a=12, b=26, c=9):
    # Create a copy of the input DataFrame to avoid modifying the original DataFrame
    df = DF.copy()
    
    # Calculate the fast and slow exponential moving averages
    df['ma_fast'] = df['Adj Close'].ewm(span=a, min_periods=a).mean()
    df['ma_slow'] = df['Adj Close'].ewm(span=b, min_periods=b).mean()
    
    # Calculate MACD line
    df['macd'] = df['ma_fast'] - df['ma_slow']
    
    # Calculate MACD signal line
    df['macd_signal'] = df['macd'].ewm(span=9, min_periods=c).mean()
    
    # Drop intermediate columns to clean up the DataFrame
    df = df.drop(columns=['ma_fast', 'ma_slow', 'macd'])
    
    # Return the DataFrame with MACD and its signal line
    return df


# Average True Range (ATR) 
def ATR(Df, n=7):
    # Create a copy of the input DataFrame to avoid modifying the original DataFrame
    df = Df.copy()
    
    # Calculate the True Range (TR) using high, low, and previous close prices
    df['C_H - C_L'] = df['High'] - df['Low']
    df['C_H - P_C'] = df['High'] - df['Adj Close'].shift(1)
    df['C_L - P_C'] = df['Low'] - df['Adj Close'].shift(1)
    df['TR'] = df[['C_H - C_L', 'C_H - P_C', 'C_L - P_C']].max(axis=1, skipna=False)
    
    # Calculate the Exponential Moving Average (EMA) of the True Range to get the Average True Range (ATR)
    df['ATR'] = df['TR'].ewm(span=n, min_periods=n).mean()
    
    # Drop the intermediate columns used to calculate TR
    df = df.drop(columns=['C_H - C_L', 'C_H - P_C', 'C_L - P_C', 'TR'])
    # Return the modified DataFrame with ATR values
    return df


# Bollinger Bands (BB) 
def BB(Df, n=7):
    # Create a copy of the input DataFrame to avoid modifying the original DataFrame
    df = Df.copy()
    
    # Calculate the Middle Bollinger Band (MB) using the rolling mean of the adjusted close prices
    df['MB'] = df['Adj Close'].rolling(n).mean()
    
    # Calculate the Upper Bollinger Band (UB) and Lower Bollinger Band (LB) using the rolling standard deviation
    df['UB'] = df['MB'] + 2 * df['Adj Close'].rolling(n).std(ddof=0)
    df['LB'] = df['MB'] - 2 * df['Adj Close'].rolling(n).std(ddof=0)
    
    # Calculate the Bollinger Band width
    df['BB_width'] = df['UB'] - df['LB']
    
    # Return the modified DataFrame with Bollinger Bands and width
    return df


# Relative Strength Index (RSI)
def RSI(Df, n=7):
    # Create a copy of the input DataFrame to avoid modifying the original DataFrame
    df = Df.copy()
    
    # Calculate the price change from the previous day
    df['change'] = df['Adj Close'] - df['Adj Close'].shift(1)
    
    # Calculate gains and losses
    df["gain"] = np.where(df['change'] >= 0, df['change'], 0)
    df["loss"] = np.where(df['change'] <= 0, -1 * df['change'], 0)
    
    # Calculate the exponential moving average of gains and losses
    df['avg_gain'] = df['gain'].ewm(alpha=1/n, min_periods=n).mean()
    df['avg_loss'] = df['loss'].ewm(alpha=1/n, min_periods=n).mean()
    
    # Calculate the relative strength (RS)
    df['rs'] = df['avg_gain'] / df['avg_loss']
    
    # Calculate the Relative Strength Index (RSI)
    df['RSI'] = 100 - (100 / (1 + df['rs']))
    
    # Return the RSI values
    return df['RSI']



# Average Directional Index
def ADX(Df, n=7):
    # Create a copy of the input DataFrame to avoid modifying the original DataFrame
    df = Df.copy()
    
    # Calculate upward and downward movements
    df['upmove'] = df['High'] - df['High'].shift()
    df['downmove'] = df['Low'].shift() - df['Low']
    
    # Calculate Positive Directional Movement (+DM) and Negative Directional Movement (-DM)
    df['+dm'] = np.where((df['upmove'] > df['downmove']) & (df['upmove'] > 0), df['upmove'], 0)
    df['-dm'] = np.where((df['downmove'] > df['upmove']) & (df['downmove'] > 0), df['downmove'], 0)
    
    # Calculate Positive Directional Indicator (+DI) and Negative Directional Indicator (-DI)
    df['+di'] = 100 * (df['+dm'] / df['ATR']).ewm(com=n, min_periods=n).mean()
    df['-di'] = 100 * (df['-dm'] / df['ATR']).ewm(com=n, min_periods=n).mean()
    
    # Calculate Directional Movement Index (DX)
    df['DX'] = (abs(df['+di'] - df['-di']) / (df['+di'] + df['-di'])) * 100
    
    # Calculate Average Directional Index (ADX)
    df['ADX'] = df['DX'].ewm(span=n, min_periods=n).mean()
    
    # Return the DataFrame with ADX and related components
    return df['ADX']



import copy
import numpy as np
# from stocktrends import indicators
# from stocktrends import Renko

def calculate_renko_brick_size(data, percentage=1):
    price_diff = data.diff().dropna()
    price_diff_abs = price_diff.abs()
    price_diff_mean = price_diff_abs.mean()
    brick_size = price_diff_mean * percentage
    return brick_size

def renko_DF(DF):
    """
    Function to convert OHLC data into Renko bricks.
    
    Args:
    - DF: DataFrame containing OHLC data.
    
    Returns:
    - renko_df: DataFrame containing Renko chart data.
    """
    def calculate_renko_brick_size(data, percentage=1):
        price_diff = data.diff().dropna()
        price_diff_abs = price_diff.abs()
        price_diff_mean = price_diff_abs.mean()
        brick_size = price_diff_mean * percentage
        return brick_size
    # Create a deep copy of the input DataFrame to avoid modifying the original data
    df1 = copy.deepcopy(DF)
    
    # Calculate the Renko brick size
    # brick_size = max(0.5, round(ATR(df1, 120)["ATR"][-1], 0))
    brick_size = calculate_renko_brick_size(df1['Adj Close'], percentage=0.15)  # Assuming calculate_renko_brick_size is defined elsewhere
    
    # Convert column names to lowercase and reset the DataFrame index
    df1.columns = [i.lower() for i in df1.columns]
    df1.reset_index(inplace=True)
    
    # Create a Renko chart object
    renko = indicators.Renko(df1)
    renko.brick_size = brick_size
    renko.chart_type = Renko.PERIOD_CLOSE
    
    # Obtain OHLC data for the Renko chart
    renko_df = renko.get_ohlc_data()
    
    # Create a new column "bar_num" to represent the direction of each Renko brick
    renko_df["bar_num"] = np.where(renko_df["uptrend"] == True, 1, np.where(renko_df["uptrend"] == False, -1, 0))
    
    # Aggregate consecutive bricks in the same direction
    for i in range(1, len(renko_df["bar_num"])):
        if renko_df["bar_num"].iloc[i] > 0 and renko_df["bar_num"].iloc[i - 1] > 0:
            renko_df["bar_num"].iloc[i] += renko_df["bar_num"].iloc[i - 1]
        elif renko_df["bar_num"].iloc[i] < 0 and renko_df["bar_num"].iloc[i - 1] < 0:
            renko_df["bar_num"].iloc[i] += renko_df["bar_num"].iloc[i - 1]
    
    # Remove duplicate rows based on the "date" column, keeping only the last occurrence
    renko_df.drop_duplicates(subset="date", keep="last", inplace=True)
    
    return renko_df