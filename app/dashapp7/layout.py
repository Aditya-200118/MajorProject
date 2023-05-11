from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import os
import pickle
from app.dashapp2.layout import navbar


nasdaq_pickle_path = os.getcwd() + "/app/dashapp7/nasdaq_pickle.pickle"

with open(nasdaq_pickle_path, "rb") as f:
    nasdaq_pickle = pickle.load(f)

nasdaq_dropdown = dcc.Dropdown(
    id="nasdaq-selector",
    className="my-3",
    options=[
        {
            "label": str(nasdaq_pickle.loc[i, "Company Name"]),
            "value": str(nasdaq_pickle.loc[i, "Symbol"])
        }
        for i in range(len(nasdaq_pickle))
    ],
    searchable=True,
    multi=False,
    value='TSLA',
    placeholder="Enter Stock",
    optionHeight = 45
)


nasdaq_table = dash_table.DataTable(
    id="nasdaq-table",
)

date_dropdown = dcc.Dropdown(
    id="date-selector",
    className="my-3",
)

call_put_dropdown = dcc.Dropdown(
    id="call-put-selector",
    className="my-3",
    options=[
        {
            "label":"Calls", "value": "calls"
        },
        {
            "label":"Puts", "value":"puts"
        }
    ],
    value="calls",
    searchable=True,
    multi=False,
    placeholder="Select Call/Put"
)

layout = html.Div(
    children= [
        navbar,
        html.Div(
                children = [dbc.Row(
                    children = [
                        dbc.Col(
                            children = [nasdaq_dropdown], width=3, align="center"
                        ),
                        dbc.Col(
                            children=[call_put_dropdown], width = 3, align="center"
                        ),
                        dbc.Col(
                            children=[date_dropdown], width = 3, align="center"
                        )
                    ], justify="center"
                ),           
            ], style={"margin-top":"5rem"}
        ),

        html.Div(
            children=[
                dbc.Row(
                    children= [
                        dbc.Col(
                            nasdaq_table, width = 9, align="center"
                        )
                    ], justify="center"
                )
            ]
        )
    ]
)