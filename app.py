import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import tensorflow as tf
import plotly.express as px
from src.Forecasting_Stock_Prices.utils.plotting_indicators import Simple_line_plot, Compare_Plot, Compare_Plot_bar
from Modules.Technical_indicators import ATR, BB, RSI, ADX, MACD
# from Modules.Plotting import Simple_line_plot, Compare_Plot, Compare_Plot_bar
from src.Forecasting_Stock_Prices.utils.technical_indicators import ATR, BB, RSI, ADX, MACD
# from stocktrends import indicators
# from stocktrends import Renko
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import warnings
warnings.filterwarnings("ignore")
import copy
import numpy as np


# from src.Forecasting_Stock_Prices.components.Data_ingestion import Data_Caller
st.set_page_config(layout="wide")
st.header("Bitcoin Price Projection : Exploring Forecasting Strategies")

st.sidebar.markdown("""
[Example CSV input]()
""")

upload_file = st.sidebar.file_uploader("Upload your input csv file", type = ['CSV'])
stock = st.selectbox('Select the company',['BTC-USD'])
if upload_file is not None:
    df = pd.read_csv(upload_file)
else:
    data_address =stock+".csv"
    file_path = f"data\{data_address}"
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'] )
df_time = df.set_index('Date')
# st.write(df)
# Simple_line_plot(df,'Date', 'Adj Close')
col1, col2 = st.columns([2, 3]) 
with col1:
    st.write(df_time.sort_index(ascending=False))
with col2:
    Simple_line_plot(df, 'Date', 'Adj Close')
def apply_technical_indicators(df):
    df = MACD(df)
    df = BB(df)
    df = ATR(df)
    df['RSI'] = RSI(df)
    df['ADX']= ADX(df)
    return df
def show_technical_analysis(df):
    df = apply_technical_indicators(df)
    # st.write(df)

    st.subheader("Perform Analysis with Technical Indicators")
    Tech_indic= st.selectbox('Technical Indicator',['MACD', 'BB', 'ATR','RSI','ADX'])
    if Tech_indic == "MACD":
        st.write("""
        **MACD** (Moving Average Convergence Divergence) is a versatile indicator that provides insights into a stock's momentum and potential trading opportunities based on the relationship between short-term and long-term moving averages.""")
        col1, col3 = st.columns([10,1]) 
        with col1:
            Compare_Plot(Df = df,X_axis =  'Date', column1 = 'Adj Close',column2 = 'macd_signal')

    elif Tech_indic == 'BB':
        st.write(""" 
        **Bollinger Bands** are a volatility-based indicator that dynamically adjusts to market conditions. The width of the bands expands and contracts based on the volatility of the underlying security. When the bands contract, it suggests low volatility, while widening bands indicate higher volatility.
        """)

        col1, col2 = st.columns([10,1]) 
        with col1:
            fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['Adj Close'], mode='lines', name=df['Adj Close'].name), row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['MB'], mode='lines', name=df['MB'].name),row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['UB'], mode='lines', name=df['UB'].name),row=1, col=1)
            fig.add_trace(go.Scatter(x=df['Date'], y=df['LB'], mode='lines', name=df['LB'].name),row=1, col=1)

            fig.add_trace(go.Scatter(x=df['Date'], y=df['BB_width'], mode='lines', name=df['BB_width'].name), row=2, col=1)
            # Update layout to include a single slider below both subplots
            fig.update_layout(title = 'Bolinger Band Technical indicator',xaxis2=dict(rangeslider=dict(visible=True)),
             height=800,width = 1400)
            fig.update_xaxes(
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
                )
            )
        st.plotly_chart(fig)

    elif Tech_indic == 'ATR':
        st.write(""" 
        **RSI (Relative Strength Index)** is a versatile tool that provides insights into price momentum, trend strength, and potential reversal points. It is commonly used by traders to make informed decisions about entry and exit points in the market. However, like any technical indicator, RSI has limitations and should be used in conjunction with other analysis techniques for comprehensive market analysis.        
            The resulting RSI value oscillates between 0 and 100. A high RSI value indicates that the asset may be overbought, suggesting a potential reversal or correction in price. Conversely, a low RSI value indicates that the asset may be oversold, indicating a potential buying opportunity.
        """)

        col1, col2 = st.columns([10,1]) 
        with col1:
            Compare_Plot(Df = df,X_axis =  'Date', column1 = 'Adj Close',column2 = 'ATR')

    elif Tech_indic == 'RSI':
        st.write(""" 
        **ATR (Average True Range)** is a valuable tool for traders to assess volatility, manage risk, and make informed trading decisions. It provides a quantitative measure of price movement that helps traders navigate dynamic market conditions.
        """)

        col1, col2 = st.columns([10,1]) 
        with col1:
            Compare_Plot(Df = df,X_axis =  'Date', column1 = 'Adj Close',column2 = 'RSI')

    elif Tech_indic == 'ADX':
        st.write(""" 
        **Average Directional Index (ADX)** is a valuable tool for traders to assess the strength and direction of trends in the market. It helps traders make informed decisions about entering or exiting trades, managing risk, and identifying potential trend reversals. However, like any technical indicator, ADX has its limitations and should be used in conjunction with other forms of analysis for comprehensive market analysis.
        """)

        col1, col2 = st.columns([10,1]) 
        with col1:
            Compare_Plot(Df = df,X_axis =  'Date', column1 = 'Adj Close',column2 = 'ADX')
    return df


def show_forecasting(df):
    df = apply_technical_indicators(df)
    data = df.drop(columns = ['Date', 'Open', 'High', 'Low', 'Close','Volume', 'MB', 'UB', 'LB'])
    df_copy = copy.deepcopy(df)
    st.subheader(f"Price Forecasting using last 15 days performance of {stock}")

    df_predict = []
    data = data.iloc[-15:]
    data = np.array(data)
    data = np.array(data)
    df_predict.append(data)
    data = tf.convert_to_tensor(df_predict)


    saved_model_path = r'Research\Model\model_11_multivariate_parameter\20240418-184534\best_model.h5'
    loaded_model = tf.keras.models.load_model(saved_model_path)
    predicted_values = loaded_model.predict(data)
    predicted_values = (np.array(predicted_values)).T


    next_7_days_dates = []
    last_date = pd.to_datetime(df_time.index[-1])
    for i in range(0, 7):
        next_day = last_date + pd.Timedelta(days=i)
        next_7_days_dates.append(next_day)
    next_7_days_price = []
    for i in range(7):
        next_7_days_price.append(float(predicted_values[i]))

    df_pred = pd.DataFrame({'Adj Close':next_7_days_price, 'Date':next_7_days_dates })

    st.subheader("""
    **Forcasting for next saven days**
    """) 
    df_30 = df.iloc[-30:]
    st.write(df_pred.set_index('Date').T)
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
    fig.add_trace(go.Scatter(x=df_30['Date'], y=df_30['Adj Close'], mode='lines', name=df_30['Adj Close'].name), row=1, col=1)
    fig.add_trace(go.Scatter(x=df_pred['Date'], y=df_pred['Adj Close'], mode='lines', name=df_pred['Adj Close'].name),row=1, col=1)
    fig.update_layout(title = 'Bolinger Band Technical indicator',xaxis2=dict(rangeslider=dict(visible=True)),
    height=800,width = 1400)
    fig.update_xaxes(
    rangeselector=dict(
    buttons=list([
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")
                ])
                )
            )
    st.plotly_chart(fig)
    #st.write(predicted_values)

analysis_type = st.radio("Select Analysis Type", ("Technical Analysis", "Forecasting"))
if analysis_type == "Technical Analysis":
    show_technical_analysis(df)
elif analysis_type == "Forecasting":
        show_forecasting(df)



