from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import os
import pickle
from app.dashapp2.layout import navbar


nse_pickle_path = os.getcwd() + "/app/dashapp8/FNO_NSE_LIST.pickle"

with open(nse_pickle_path, "rb") as f:
    nse_pickle = pickle.load(f)

nse_dropdown = dcc.Dropdown(
    id="nse-selector",
    className="my-3",
    options=[
        {
            "label": str(nse_pickle.loc[i, "Company Name"]),
            "value": str(nse_pickle.loc[i, "Symbol"])
        }
        for i in range(len(nse_pickle))
    ],
    searchable=True,
    multi=False,
    value='RELIANCE',
    placeholder="Enter Stock",
    optionHeight = 45
)


nse_table = dash_table.DataTable(
    id="nse-table",
)

date_dropdown = dcc.Dropdown(
    id="date-selector",
    className="my-3",
)

full_compact_data = dcc.Dropdown(
    id="data-selector",
    className="my-3",
    options=[
        {
            "label":"Full", "value": "full"
        },
        {
            "label":"Compact", "value":"compact"
        }
    ],
    value="full",
    searchable=True,
    multi=False,
    placeholder="Select Full/Compact Representation"
)

layout = html.Div(
    children= [
        navbar,
        html.Div(
                children = [dbc.Row(
                    children = [
                        dbc.Col(
                            children = [nse_dropdown], width=3, align="center"
                        ),
                        dbc.Col(
                            children=[full_compact_data], width = 3, align="center"
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
                            nse_table, width = 9, align="center"
                        )
                    ], justify="center"
                )
            ]
        )
    ]
)