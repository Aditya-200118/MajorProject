from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pickle
import os
import random

layout = html.Div(
    children = [
        html.Div(
            children = [
                dbc.Row(
                    children = [
                        dbc.Col(
                            children = [
                                dcc.Dropdown(
                                    id = "my-dropdown",
                                    className = "mt-3",
                                    options=[
                                        {
                                            "label":str(ticker_list.loc[i, "Company Name"]),
                                            "value": str(ticker_list.loc[i, "Symbol"]),
                                        }
                                        for i in range(len(ticker_list))
                                    ],
                                    searchable=True,
                                    multi = False,
                                    value=str(
                                        random.choice(
                                            [
                                                'TSLA',
                                                'MSFT',
                                                'AAPL',
                                                'FB',
                                                'NFLX',
                                                "AMZN",
                                            ]
                                        )
                                    ),
                                    # value = False,
                                    placeholder="Enter Stock Name"
                                ),


                                dcc.Dropdown(
                                    id = "chart_selector",
                                    className='mt-3',
                                    options=[
                                        {"label": "line", "value": "Line"},
                                        {"label": "candlestick", "value": "Candlestick"},
                                        {"label": "Simple moving average", "value": "SMA"},
                                        {"label": "Exponential moving average", "value": "EMA",},
                                        {"label": "MACD", "value": "MACD"},
                                        {"label": "RSI", "value": "RSI"},
                                        {"label": "OHLC", "value": "OHLC"},
                                    ],
                                    value="Line",
                                ),


                                dbc.Button(
                                    "Plot",
                                    id="submit-button-state",
                                    className="my-3",
                                    n_clicks=1,
                                    color="secondary",
                                )
                            ]
                        ) 
                    ]
                ),
    
                html.Div(
                    children=[
                        dcc.Graph(
                            id= "my-graph",
                            animate=False, 
                        )
                    ]
                )
            ],
            style={
                "wdith": "90%",
                "height": "auto",
                "position": "relative",
                "margin": "20px",
            }
        )
    ]
)