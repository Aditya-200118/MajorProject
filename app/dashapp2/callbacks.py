#indicators
from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

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
        
        Output(
            'my-graph', 
            'figure'
        ),

        [
            State(
                'my-dropdown', 
                'value'
            ),
            
            State(
                'chart_selector', 
                'value'
            ),
        ],
        Input(
            "submit-button-state", 
            "n_clicks"
        )
    )
    
    def update_graph(selected_dropdown_value, chart_name,n_clicks):
        if n_clicks >= 1:    
            start_date = datetime.now().date() - timedelta(days = 365)
            end_date = datetime.now().date()
            df = yf.download(selected_dropdown_value, start=start_date, end=end_date, interval="1h")
            stock = df.copy(deep=True)
            stock = Sdf.retype(stock)

            if chart_name == "Line":
                fig = go.Figure(
                    data=[
                        go.Scatter(
                            x=df.index, 
                            y=df['Close'], 
                            # fill="tozeroy", 
                            name="close"
                        )
                    ],
                    layout={
                        "height": 600,
                        "title": chart_name,
                    },
                )
                


            if chart_name == "Candlestick":
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    
                    go.Candlestick(
                        open=df['Open'],
                        x=df.index,
                        high=df['High'],
                        low=df['Low'],
                        close=df['Close'],
                        name="Candlestick",
                        increasing_line_color='#28C5FA',
                        decreasing_line_color='#EE1755'
                    ),
                    secondary_y=False,
                )
            if chart_name == "SMA":
                close_ma_10 = df.Close.rolling(10).mean()
                close_ma_15 = df.Close.rolling(15).mean()
                close_ma_30 = df.Close.rolling(30).mean()
                close_ma_100 = df.Close.rolling(100).mean()
                fig = go.Figure(
                    data = [
                        go.Scatter(
                            x=list(close_ma_10.index), 
                            y=list(close_ma_10), 
                            name="10 Days"
                        ),
                        go.Scatter(
                            x=list(close_ma_15.index), 
                            y=list(close_ma_15), 
                            name="15 Days"
                        ),
                        go.Scatter(
                            x=list(close_ma_30.index), 
                            y=list(close_ma_15), 
                            name="30 Days"
                        ),
                        go.Scatter(
                            x=list(close_ma_100.index), 
                            y=list(close_ma_15), 
                            name="100 Days"
                        ),
                    ],
                    layout={
                        "height": 600,
                        "title": chart_name,
                        "showlegend": True,
                    },
                )
                
            
            if chart_name == "OHLC":
                fig = go.Figure(
                    data=[
                        go.Ohlc(
                            x=df.index,
                            open=df.Open,
                            high=df.High,
                            low=df.Low,
                            close=df.Close,
                            increasing_line_color='#28C5FA',
                            decreasing_line_color='#EE1755'
                        )
                    ],
                    layout={
                        "height": 600,
                        "title": chart_name,
                        "showlegend": True,
                    },
                )
                
            # Exponential moving average
            if chart_name == "EMA":
                close_ema_10 = df.Close.ewm(span=10).mean()
                close_ema_15 = df.Close.ewm(span=15).mean()
                close_ema_30 = df.Close.ewm(span=30).mean()
                close_ema_100 = df.Close.ewm(span=100).mean()
                fig = go.Figure(
                    data=[
                        go.Scatter(
                            x=list(close_ema_10.index), 
                            y=list(close_ema_10), 
                            name="10 Days"
                        ),
                        go.Scatter(
                            x=list(close_ema_15.index), 
                            y=list(close_ema_15), 
                            name="15 Days"
                        ),
                        go.Scatter(
                            x=list(close_ema_30.index), 
                            y=list(close_ema_30), 
                            name="30 Days"
                        ),
                        go.Scatter(
                            x=list(close_ema_100.index),
                            y=list(close_ema_100),
                            name="100 Days",
                        ),
                    ],
                    layout={
                        "height": 600,
                        "title": chart_name,
                        "showlegend": True,
                    },
                )
                
            # Moving average convergence divergence
            if chart_name == "MACD":
                df["MACD"], df["signal"], df["hist"] = (
                    stock["macd"],
                    stock["macds"],
                    stock["macdh"],
                )
                fig = go.Figure(
                    data=[
                        go.Scatter(
                            x=list(df.index), 
                            y=list(df.MACD), 
                            name="MACD"),
                        go.Scatter(
                            x=list(df.index), 
                            y=list(df.signal), 
                            name="Signal"
                        ),
                        go.Scatter(
                            x=list(df.index),
                            y=list(df["hist"]),
                            line=dict(color="rgba(255,144,162,0.23)", width=4, dash="dot"),
                            name="Histogram",
                        ),
                    ],
                    layout={
                        "height": 600,
                        "title": chart_name,
                        "showlegend": True,
                    },
                )
                
            # Relative strength index
            if chart_name == "RSI":
                rsi_6 = stock["rsi_6"]
                rsi_12 = stock["rsi_12"]
                fig = go.Figure(
                    data=[
                        go.Scatter(
                            x=list(df.index), 
                            y=list(rsi_6), 
                            name="RSI 6 Day"
                        ),
                        go.Scatter(
                            x=list(df.index), 
                            y=list(rsi_12), 
                            name="RSI 12 Day"
                        ),
                    ],
                    layout={
                        "height": 600,
                        "title": chart_name,
                        "showlegend": True,
                    },
                )
                
            return fig