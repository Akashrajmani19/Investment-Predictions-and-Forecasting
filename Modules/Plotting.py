import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd
import copy

def Compare_Plot(Df, X_axis, column1, column2):
    # Assuming your data is stored in a DataFrame named 'data'
    # Let's say 'Adj Close' and 'MACD' are the columns you want to plot
    # Create subplots with shared x-axis (date)
    data = copy.deepcopy(Df)
    data['Date'] = pd.to_datetime(data['Date'])
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
    # Add trace for Adj Close
    fig.add_trace(go.Scatter(x=data[X_axis], y=data[column1], mode='lines', name=data[column1].name), row=1, col=1)
    # Add trace for MACD
    fig.add_trace(go.Scatter(x=data[X_axis], y=data[column2], mode='lines', name=data[column2].name), row=2, col=1)
    # Update layout to include a single slider below both subplots
    #fig.update_layout(xaxis=dict(rangeslider=dict(visible=True)), height=800)
    fig.update_layout(
        #xaxis=dict(rangeslider=dict(visible=True)),
        height=800,
        xaxis2=dict(
            rangeslider=dict(visible=True),
            type="date",
            # range=[data[X_axis].min(), data[X_axis].min() + pd.Timedelta(days=365)]  # Display one year initially
        )
    )
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
    fig.show()



def Compare_Plot_bar(Df, X_axis, column1, column2):
    data = copy.deepcopy(Df)
    data['Date'] = pd.to_datetime(data['Date'])
    # Assuming your data is stored in a DataFrame named 'data'
    # Let's say 'Adj Close' and 'uptrend' are the columns you want to plot
    # Create subplots with shared x-axis (date)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.1)
    
    # Add trace for Adj Close
    fig.add_trace(go.Scatter(x=data[X_axis], y=data[column1], mode='lines', name=data[column1].name), row=1, col=1)
    
    # Add trace for uptrend (using Bar chart for better interpretation)
    fig.add_trace(go.Bar(x=data[X_axis], y=data[column2], name=data[column2].name), row=2, col=1)
    
    # Update layout to include a single slider below both subplots
    fig.update_layout(
        #xaxis=dict(rangeslider=dict(visible=True)),
        height=800,
        xaxis2=dict(
            rangeslider=dict(visible=True),
            type="date"
            # range=[data[X_axis].min(), data[X_axis].min() + pd.Timedelta(days=365)]  # Display one year initially
        )
    )
    
    fig.update_xaxes(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ]))
        # ),
        # row=2, col=1
    )
    
    fig.show()
