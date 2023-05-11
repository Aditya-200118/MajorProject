from dash import Input, Output, dcc, State
from dash import Input, Output, dcc
import pickle
import os
import yfinance as yf

def register_callbacks(dashapp):

    @dashapp.callback(
        Output("navbar-collapse", "is_open"),
        [
            Input(
                "navbar-toggler", 
                "n_clicks"
            )
        ],

        [
            State(
            "navbar-collapse", 
            "is_open"
            )
        ],
    )
    def toggle_navbar_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
        

    @dashapp.callback(
        [
            Output('index-table', 'data'),
            Output('index-table', 'columns')
        ],
        Input('index-selector', 'value')
    )
    def table_update(val):
        df = yf.download(str(val),period="6mo", interval='5d')
        df = df.round(2)
        data = df.to_dict('records')
        columns = [{"name": i, "id":i} for i in df.columns]
        return data, columns