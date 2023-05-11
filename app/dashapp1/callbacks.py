
from dash.dependencies import Input, Output, State
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import random
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
        Output("growth_chart", "figure"),
        [
            Input("stock_selector", "value"),
            Input(
                "growth_selector",
                "value"
            )
        ]
    )
    def update_growth_chart(stocks, growth_mode):

        def get_price_change(price_list):
            base_price = price_list[0]
            return [(price/base_price)-1 for price in price_list]
            
        df_stocks = []
        time = '1y'

        if stocks != None and len(stocks) > 0:
            for stock in stocks:
                Close = stock + '_Close'
                Open = stock + '_Open'
                High = stock + '_High'
                Low = stock + '_Low'
                Volume = stock + '_Volume'
                stock_df = yf.Ticker(stock).history(period=time).reset_index()[['Date', 'Open', 'Close', 'High', 'Low', 'Volume']] # make sure order of columns is as intended
                stock_df.columns = ['Date', Open, Close, High, Low, Volume] #renaming columns
                df_stocks.append(stock_df)
        else:
            print("Stocks Not Entered")
            
        SP_ticker = '^GSPC'
        index_col = 'S&P 500'
        
        Close_I = index_col + '_Close'
        Open_I = index_col + '_Open'
        High_I = index_col + '_High'
        Low_I = index_col + '_Low'
        Volume_I = index_col + '_Volume'
        
        index = yf.Ticker(SP_ticker)

        df_index = index.history(period=time).reset_index()[['Date', 'Open', 'Close', 'High', 'Low', 'Volume']]
        df_index.columns = ['Date',Open_I, Close_I, High_I, Low_I, Volume_I ]
        
        if stocks != None and len(stocks) > 0:
            for df_temp in df_stocks:
                df_index = pd.merge(df_index, df_temp, how="left",on="Date")
                df_index = df_index.fillna(method="backfill", axis=1)
                df_index = df_index.loc[:,~df_index.columns.duplicated()]
        fig = make_subplots(specs = [[{"secondary_y": True}]])
        

        if growth_mode == False:
            for stock in stocks:
                x_value = 'Date'
                y_value = stock + '_Close'
                x_value = df_index[x_value].tolist()
                y_value = df_index[y_value].tolist()
                fig.add_trace(
                    go.Scatter(
                        x = x_value,
                        y = y_value,
                        name = stock,
                        mode = "lines",
                        line_shape = "spline"
                    )
                )
        elif growth_mode == True:
            for stock in stocks:
                for col in df_index.columns:
                    if col == (stock + "_Close"):
                        df_index[col] = get_price_change(df_index[col].tolist())

                x_value1 = 'Date'
                y_value1 = stock + "_Close"
                x_value = df_index[x_value1].tolist()
                y_value = df_index[y_value1].tolist()
                color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])]
                # for i in range(number_of_colors)]
                fig.add_trace(
                        go.Scatter(
                        x = x_value,
                        y= y_value,
                        name = stock,
                        line = dict(width = 2, color = color[0]),
                        mode = "lines",
                        line_shape = "spline",
                        legendgroup = str(stock).upper() + ' Line',
                        legendgrouptitle_text = str(stock).upper()
                    )
                )                
        return fig