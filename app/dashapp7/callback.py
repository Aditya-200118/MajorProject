"""Stock Option Chain"""

from dash import Input, Output, dcc, State
import pickle
import os
import yfinance as yf
import yahooquery as yq
import yahoo_fin.options as ops
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
        Output("date-selector", 'options'),
        Input('nasdaq-selector', 'value')
    )
    def date_update(val):
        dates = ops.get_expiration_dates(val)
        return [
            {
                "label": dates[i], 
                "value": dates[i]
            }
            for i in range(len(dates))
        ]
    
    @dashapp.callback(
    [
        Output('nasdaq-table', 'data'),
        Output('nasdaq-table', 'columns')
    ],
    [
        Input('nasdaq-selector', 'value'),
        Input('call-put-selector', 'value'),
        Input('date-selector', 'value')
    ]
    )
    def table_update(val, type, date):
        if type == "calls":
            df = ops.get_calls(val, date)
            data = df.to_dict('records')
            columns = [{"name": i, "id":i} for i in df.columns]
            return data, columns
        elif type == "puts":
            df = ops.get_puts(val, date)
            data = df.to_dict('records')
            columns = [{"name": i, "id":i} for i in df.columns]
            return data, columns