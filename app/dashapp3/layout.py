from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import os
import pickle
from app.dashapp2.layout import navbar

major_indices_path = os.getcwd() + "/app/dashapp3/major_indices.pickle"

with open(major_indices_path, "rb") as f:
    major_indices = pickle.load(f)

index_table = dash_table.DataTable(
    id="index-table",
)

major_indices_dropdown = dcc.Dropdown(
    id="index-selector",
    className="mb-3",
    options=[
        {
            "label": str(major_indices.loc[i, "Index Name"]),
            "value": str(major_indices.loc[i, "Symbol"])
        }
        for i in range(len(major_indices))
    ],
)

layout = html.Div(
    children= [
        navbar,
        html.Div(
                children = [dbc.Row(
                    children = [
                        dbc.Col(
                            major_indices_dropdown, width=10, align="center"
                        )
                    ], justify="center"
                ),           
            ]
        ),

        html.Div(
            children=[
                dbc.Row(
                    children= [
                        dbc.Col(
                            index_table, width = 10, align="center"
                        )
                    ], justify="center"
                )
            ]
        )
    ]
)