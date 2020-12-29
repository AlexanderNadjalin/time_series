import plotly.graph_objs as go
import dash_core_components as dcc
import datetime as dt
from loguru import logger


@logger.catch
def hist_graph(ts_collection: ts_col.TimeSeriesCollection, column_name: str = 'Adj Close'):
    """
    Dash Core Component Graph for historical prices.
    :param ts_collection: ts_col.TimeSeriesCollection
    :param column_name: str. default='Adj Close'
    :return: dcc.Graph
    """
    start = ts_collection.common_end_date() - dt.timedelta(days=252)
    end = ts_collection.common_end_date()
    ts = ts_collection.ts_list[0].ticker
    time_series = ts_collection.get_time_series(ts)
    df = time_series.select_ts_dates(start, end)
    return dcc.Graph(
        id='hist_graph',
        figure={
            'data': [
                {'x': df['Date'], 'y': df[column_name]}
            ]
        },
        style={'width': '800'}
    )


@logger.catch
def returns_graph(ts_collection: ts_col.TimeSeriesCollection):
    """
    Dash Core Component Graph for historical returns.
    :param ts_collection: ts_col.TimeSeriesCollection
    :return: dcc.Graph
    """
    start = ts_collection.common_end_date() - dt.timedelta(days=252)
    end = ts_collection.common_end_date()
    ts = ts_collection.ts_list[0].ticker
    time_series = ts_collection.get_time_series(ts)
    df = time_series.cumulative_returns(start, end)
    return dcc.Graph(
        id='returns_graph',
        figure={
            'data': [
                {'x': df['Date'], 'y': df['cum_rets']}
            ]
        },
        style={'width': '800'}
    )


@logger.catch
def scatter_layout(title: str, x_name: str, y_name: str) -> go.Layout:
    """
    Scatter type Layout for plots.
    :param title: str.
    :param x_name: str. Name to be used in plot.
    :param y_name: str. Name to be used in plot.
    :return: go.Layout.
    """
    return go.Layout(title=title,
                     xaxis={'title': x_name},
                     yaxis={'title': y_name},
                     hovermode='closest')


@logger.catch
def box_layout(title: str, y_name: str) -> go.Layout:
    """
    Box type Layout for plots.
    :param title: str.
    :param y_name: str. Name to be used in plot.
    :return: go.Layout
    """
    return go.Layout(title=title,
                     yaxis={'title': y_name},
                     hovermode='closest')


@logger.catch
def bollinger_layout(fig):
    fig['layout'] = dict()
    fig['layout']['plot_bgcolor'] = 'rgb(250, 250, 250)'
    fig['layout']['xaxis'] = dict(rangeselector=dict(visible=True))
    fig['layout']['yaxis'] = dict(domain=[0, 0.2], showticklabels=False)
    fig['layout']['yaxis2'] = dict(domain=[0.2, 0.8])
    fig['layout']['legend'] = dict(orientation='h', y=0.9, x=0.3, yanchor='bottom')
    fig['layout']['margin'] = dict(t=40, b=40, r=40, l=40)
    return fig['layout']


@logger.catch
def bollinger_range_selector():
    range_selector = dict(
        visibe=True,
        x=0, y=0.9,
        bgcolor='rgba(150, 200, 250, 0.4)',
        font=dict(size=13),
        buttons=list([
            dict(count=1,
                 label='reset',
                 step='all'),
            dict(count=1,
                 label='1yr',
                 step='year',
                 stepmode='backward'),
            dict(count=3,
                 label='3 mo',
                 step='month',
                 stepmode='backward'),
            dict(count=1,
                 label='1 mo',
                 step='month',
                 stepmode='backward'),
            dict(step='all')
        ]))
    return range_selector
