#growth chart or analysis
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import pickle
import os
from app.dashapp2.layout import navbar

path = os.getcwd() + "/app/dashapp1/nasdaq.pickle"
with open(path, 'rb') as f:
    ticker_list = pickle.load(f)

layout = html.Div(
    children=[
        navbar,
        html.Div(
            id="container",
            children=[
                dbc.Row(
                    children=[
                        dbc.Col(
                            children=[
                                dcc.Dropdown(
                                    id = "stock_selector",
                                    className="mb-3",
                                    options=[
                                        {
                                            "label":str(ticker_list.loc[i, "Company Name"]),
                                            "value": str(ticker_list.loc[i, "Symbol"]),
                                        }
                                        for i in range(len(ticker_list))
                                    ],
                                    searchable=True,
                                    multi = True,
                                    value = ['TSLA'],
                                    placeholder="Enter Stock Name",
                                ),

                                dcc.Dropdown(
                                    id="growth_selector",
                                    className="mb-3",
                                    options = [
                                        {
                                            "label": "Turn On",
                                            "value": True,
                                        },
                                        {
                                            "label": "Turn Off",
                                            "value": False
                                        }
                                    ],
                                    value=False,
                                    multi = False,
                                    searchable=True,
                                    placeholder="Show Index Growth"
                                )
                            ]
                        )
                    ]
                ),

                html.Div(
                    children = [
                        dcc.Graph(
                            id='growth_chart',
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