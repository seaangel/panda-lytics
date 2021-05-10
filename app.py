import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
from dash.dependencies import Output, Input, State
import yfinance as yf
import plotly.express as px
import plotly.figure_factory as ff
from dash.exceptions import PreventUpdate
from datetime import date


#data = pd.read_csv("avocado.csv")

#tic = pd.read_excel("tickers.xlsx")

#tickers = tic['ticker'].tolist()



#data["Date"] = pd.to_datetime(data["Date"], format="%Y-%m-%d")
#data.sort_values("Date", inplace=True)


#tickers_old = ['AAPL', 'SBER.ME',"AAL","XOM"]
#data_stock = pd.DataFrame(columns=tickers)



type_threshold = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]

d = date.today()
#print(d.year)


#for ticker in tickers:
#    data_stock[ticker] = yf.download(ticker,'2016-01-01','2016-04-30')['Close']
    
#data_stock = data_stock.dropna()

#print(data_stock)
#data_stock1 = data_stock

#data_stock1 = data_stock1.dropna()



#data_stock = data_stock.reset_index()




#fig = px.scatter_matrix(data_stock)
#fig2 = ff.create_dendrogram(data_stock.corr(), color_threshold=1.5, labels = data_stock.columns)


external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.title = "Panda Analytics: Choose Your Panda!"

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🐼", className="header-emoji"),
                html.H1(
                    children="Panda Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of prices in the stock market. "
                      "Information taken from finance.yahoo.com, closing of the day. "
                      "In the period from 2020 to today."
" For separation use ' , ' "
"to view the Moscow Exchange, add .ME, for example SBER.ME",
                    className="header-description",
                ),
            ],
            className="header",
        ),
       
        html.Div(
            children=[

                html.Div(
                    children=[
                        html.Div(children="Select Tickers (min 2)", className="menu-title"),
                        dcc.Input(id="type-filter1", type="text", placeholder="AAPL,SBER.ME",className="input1",),
                      #  dcc.Dropdown(
                      #      id="type-filter1",
                      #      options=[
                      #          {"label": avocado_type, "value": avocado_type}
                      #          for avocado_type in np.sort(tickers)
                      #      ],
                      #      value=['AAPL', 'SBER.ME'],
                      #      multi=True,
                      #      clearable=False,
                      #      searchable=True,
                      #      className="dropdown",
                      #  ),
       
    ],   
                ),
                html.Div(
                    children=[
                        html.Div(children="Select Threshold", className="menu-title"),
                        dcc.Dropdown(
                            id="type_1_threshold",
                            options=[
                                {"label": threshold, "value": threshold}
                                for threshold in np.sort(type_threshold)
                            ],
                            value= 1,
                           # multi=True,
                            clearable=False,
                            searchable=True,
                            className="dropdown",
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range1",
                            min_date_allowed=date(2020, 4, 1),
                            max_date_allowed=date(d.year, d.month, d.day),
                            start_date=date(2020, 4, 1),
                            end_date=date(d.year, d.month, d.day),
                        ),
                    ]
                ),
                
                html.Div(
                    children=[
                        html.Div(children="Go", className="menu-title"),
                        html.Button('Submit', id='submit-val', n_clicks=0,className="submit-title"),
                        
                        ],
                    
                    ),
                
                
            ],
            className="menu",
        ),

                html.Div(
            children=[
          
                 html.Div(
                    children=dcc.Graph(
                        id="volume-bags1", config={"displayModeBar": False},
                    ),
                    className="card",
                    
                ),
                 html.Div(
                    children=dcc.Graph(
                        id="dendogram", config={"displayModeBar": False},
                    ),
                    className="card",
                    
                ),
            ],
            className="wrapper",
        ),
    ]
)




@app.callback(
     
     [Output("volume-bags1","figure"),Output("dendogram","figure")],
    [
      #  Input("region-filter1", "value"),
        Input("type-filter1", "value"),
        Input("type_1_threshold", "value"),
        Input("date-range1", "start_date"),
        Input("date-range1", "end_date"),
        Input('submit-val', 'n_clicks')
    ],
   prevent_initial_call=True
)


def update_charts(avocado_type1,type_1_threshold, start_date1, end_date1,n_clicks):
    
    tickers_q = avocado_type1.split(',')
    data_stock_q = pd.DataFrame(columns=tickers_q)
    
    
    
    if n_clicks > 0:
    
    
        for ticker in tickers_q:
             data_stock_q[ticker] = yf.download(ticker, start_date1, end_date1)['Close']
    #        data_stock_q[ticker] = yf.download(ticker, start_date, end_date)['Close']
        #data_stock_q = data_stock_q.reset_index()
        data_stock_q = data_stock_q.dropna()
    
    n_clicks = 0
    
    #print(data_stock_q)
    
   # print(avocado_type1)
    
   # print(n_clicks)
    
   # figs_2 = px.line(data_stock, x="Date", y=region1)
    figs_1 = px.scatter_matrix(data_stock_q)

   #data_stock = data_stock1.drop(['Date'], axis = 1)
    
    dendro = ff.create_dendrogram(data_stock_q.corr(),color_threshold=type_1_threshold,labels=data_stock_q.columns)
    
    
    return figs_1, dendro

if __name__ == "__main__":
    app.run_server(debug=True,
                   host='127.0.0.1')
