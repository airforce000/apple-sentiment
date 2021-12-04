# set chdir to current dir
import os
import sys

sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
os.chdir(os.path.realpath(os.path.dirname(__file__)))
import dash
from dash.dependencies import Output, Event, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import pandas as pd
from config import data_dict_df
from cachetools import cached, TTLCache
import mysql.connector
import plotly.express as px

##Connection to MYSQL DATABASE
mydb = mysql.connector.connect(
    host="",
    user="",
    passwd="",
    database=""
)
mycursor = mydb.cursor()
##reads stock price over window of semester for apple
bf = pd.read_csv('AAPL (1).csv')

fig2 = px.line(bf, x='Date', y='Close')
sentiment_colors = {-1: "#EE6055",
                    -0.5: "#FDE74C",
                    0: "#FFE6AC",
                    0.5: "#D0F2DF",
                    1: "#9CEC5B", }

app_colors = {
    'backgrd': '#FFFFFF',
    'txt': '#0C0F0A',
    'sent-plot': '#41EAD4',
    'vol-bar': '#FBFC74',
    'sotcol': '#FF206E',
}

POS_NEG_NEUT = 0.1
MAX_DF_LENGTH = 100

app = dash.Dash(__name__)
## html laying out for a the dashboard page
app.layout = html.Div(
    [html.Div(className='container-fluid', children=[html.H5('-------------------', style={'color': "#FFFFFF"}),
                                                     html.H5('Search Ticker/Stock:', style={'color': app_colors['text'],
                                                                                            'font-family': 'Raleway',
                                                                                            'font-weight': '600',
                                                                                            'font-size': '24px'}),
                                                     dcc.Dropdown(id='sentiment_term',
                                                                  options=[{'label': s, 'value': s} for s in
                                                                           data_dict_df.keys()], value="apple(AAPL)",
                                                                  multi=False),
                                                     ],
              style={'width': '98%', 'margin-left': 10, 'margin-right': 10, 'max-width': 50000}),
     html.Div([
         dcc.Graph(figure=fig2)
     ]),

     html.Div(className='row', children=[html.H4('Live Market Sentiment',
                                                 style={'color': "#0C0F0A", 'text-align': 'center',
                                                        'font-family': 'Raleway', 'font-weight': '600',
                                                        'font-size': '32px'}),
                                         html.Div(dcc.Graph(id='live-graph', config={'displayModeBar': False},
                                                            animate=False), className='col s12'),
                                         html.H4('Long Term Market Sentiment',
                                                 style={'color': "#0C0F0A", 'text-align': 'center',
                                                        'font-family': 'Raleway', 'font-weight': '600',
                                                        'font-size': '32px'}),
                                         html.Div(dcc.Graph(id='historical-graph', config={'displayModeBar': False},
                                                            animate=False), className='col s12')]),

     dcc.Interval(
         id='graph-update',
         interval=1 * 1000,
     ),
     dcc.Interval(
         id='historical-update',
         interval=600 * 1000,
     ),

     ], style={'backgroundColor': app_colors['background'], 'margin-top': '-30px', 'height': '2000px', },
)


# resampling
def df_resample_sizes(df, maxlen=MAX_DF_LENGTH):
    vol_df = df.copy()
    vol_df['volume'] = 1
    ms_span = (df.index[-1] - df.index[0]).seconds * 1000
    rs = int(ms_span / maxlen)
    df = df.resample('{}ms'.format(int(rs))).mean()
    df.dropna(inplace=True)
    vol_df = vol_df.resample('{}ms'.format(int(rs))).sum()
    vol_df.dropna(inplace=True)
    df = df.join(vol_df['volume'])
    return df


# callback loop for live graph
@app.callback(Output('live-graph', 'figure'),
              [Input(component_id='sentiment_term', component_property='value')],
              events=[Event('graph-update', 'interval')]
              )
# cache setup for live graph
@cached(cache=TTLCache(maxsize=100, ttl=600))
def update_graph_scatter(sentiment_term):
    print(data_dict_df[sentiment_term][0])
    try:
        if sentiment_term:
            df2 = pd.read_sql(
                "select * from reddit_data.reddit_data_sentiment where body like '%aapl%' and date_time >  ADDDATE(date_time, -10)",
                mydb)
            df = df2
        else:
            df2 = pd.read_sql(
                "select * from reddit_data.reddit_data_sentiment where body like '%aapl%' and date_time >  ADDDATE(date_time, -10)",
                mydb)
            df = df2
            print("df would be zero")
        df.set_index('date_time', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df) / 5)).mean()
        df = df_resample_sizes(df)
        X = df.index
        Y = df.sentiment_smoothed.values
        data = plotly.graph_objs.Scatter(
            x=X,
            y=Y,
            name='Sentiment',
            mode='lines',
            yaxis='y2',
            fill="tozeroy",
            fillcolor="#8bcbfc"
        )

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),
                                                    yaxis=dict(title="Sentiment"),
                                                    yaxis2=dict(range=[min(Y), max(Y)], side='left', overlaying='y',
                                                                title='sentiment'),
                                                    title='Live sentiment for: "{}"'.format(sentiment_term),
                                                    font={'color': app_colors['text']},
                                                    plot_bgcolor=app_colors['background'],
                                                    paper_bgcolor=app_colors['background'],
                                                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                                                    showlegend=True)}

    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')


# callback loop for history sentiment graph
@app.callback(Output('historical-graph', 'figure'),
              [Input(component_id='sentiment_term', component_property='value')],
              events=[Event('historical-update', 'interval')])
# cache for hisory sentiment graph
@cached(cache=TTLCache(maxsize=100, ttl=43200))
def update_hist_graph_scatter(sentiment_term):
    try:
        if sentiment_term:
            df2 = pd.read_sql(
                "select * from reddit_data.reddit_data_sentiment where body like '%appl%' and date_time >ADDDATE(date_time, -40)",
                mydb)
            df = df2
        else:
            df2 = pd.read_sql(
                "select * from reddit_data.reddit_data_sentiment where body like '%appl%' and date_time > ADDDATE(date_time, -40)",
                mydb)
            df = df2

        df.set_index('date_time', inplace=True)
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df) / 5)).mean()
        df.dropna(inplace=True)
        df = df_resample_sizes(df, maxlen=500)
        X = df.index
        Y = df.sentiment_smoothed.values
        data = plotly.graph_objs.Scatter(
            x=X,
            y=Y,
            name='Sentiment',
            mode='lines',
            yaxis='y2',
            fill="tozeroy",
            fillcolor="#8bcbfc"
        )
        return {'data': [data],
                'layout': go.Layout(xaxis=dict(range=[min(X), max(X)]),  # add type='category to remove gaps'

                                    yaxis2=dict(range=[min(Y), max(Y)], side='left', overlaying='y', title='sentiment'),
                                    title='Longer-term sentiment for: "{}"'.format(sentiment_term),
                                    font={'color': app_colors['text']},
                                    plot_bgcolor=app_colors['background'],
                                    paper_bgcolor=app_colors['background'],
                                    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
                                    showlegend=True)}
    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')


server = app.server
dev_server = app.run_server
