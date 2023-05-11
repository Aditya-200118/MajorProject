"""Stock Option Chain"""

from dash import Input, Output, dcc, State
import pickle
import os
import yfinance as yf
import yahooquery as yq
import yahoo_fin.options as ops
import nsepython as nse
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
        Input('nse-selector', 'value')
    )
    def date_update(val):
        # dates = ops.get_expiration_dates(val)
        dates = nse.expiry_list(val)
        dates.append("latest")
        return [
            {
                "label": dates[i], 
                "value": dates[i]
            }
            for i in range(len(dates))
        ]
        
    @dashapp.callback(
    [
        Output('nse-table', 'data'),
        Output('nse-table', 'columns')
    ],
    [
        Input('nse-selector', 'value'),
        Input('date-selector', 'value'),
        Input('data-selector', 'value')
    ]
    )
    def table_update(val, date, oi_mode):
        # df = yf.download(str(val),period="6mo", interval='5d')
        # df = df.round(2)
        if oi_mode == "full":
            df,stock_ltp,time = nse.oi_chain_builder(str(val).upper(), date, oi_mode)
            print(type(df))
            data = df.to_dict('records')
            columns = [{"name": i, "id":i} for i in df.columns]
            return data, columns
        elif type == "compact":
            df, stock_ltp, time = nse.oi_chain_builder(val, date, oi_mode)
            data = df.to_dict('records')
            columns = [{"name": i, "id":i} for i in df.columns]
            return data, columns