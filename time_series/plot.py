import plotly.offline as pyo
import plotly.graph_objs as go
from loguru import logger


def axis_data_and_names(series: ts.TimeSeries, x_axis_column: str, y_axis_column: str,
                        x_axis_name: str = None, y_axis_name: str = None):
    """
    Get y-axis and x-axis names. Option to use different axis names than pd.DataFrame column names.
    :param series: ts.TimeSeries.
    :param x_axis_column: str. pd.DataFrame column name.
    :param y_axis_column: str. pd.DataFrame column name.
    :param x_axis_name: str. Name to be used if not x_axis_column_name.
    :param y_axis_name: str. Name to be used if not y_axis_column_name.
    :return: str, str.
    """
    # check if column strings is in ts.pd_frame, otherwise break
    if x_axis_column not in series.pd_frame.columns:
        logger.critical('Column name "' + x_axis_column +
                        '" does not exist in TimeSeries object "' + series.ticker + '". Aborted.')
        quit()
    if y_axis_column not in series.pd_frame.columns:
        logger.critical('Column name "' + y_axis_column +
                        '" does not exist in TimeSeries object "' + series.ticker + '". Aborted.')
        quit()

    # if no specific axis names are provided, use ts.pd_frame column names
    if not x_axis_name:
        x_axis_name = x_axis_column
    if not y_axis_name:
        y_axis_name = y_axis_column

    return x_axis_name, y_axis_name


def time_series_plot(series: ts.TimeSeries, x_axis_column: str, y_axis_column: str,
                     title: str, x_axis_name: str = None, y_axis_name: str = None) -> None:
    """
    Plot a plotly time series plot. Save a html-file. Option to use either column names from series or new ones.
    :param series: ts.TimeSeries.
    :param x_axis_column: str. pd.DataFrame column name.
    :param y_axis_column: str. pd.DataFrame column name.
    :param title: str. Title to be used on plot.
    :param x_axis_name: str. Name to be used if not x_axis_column_name.
    :param y_axis_name: str. Name to be used if not y_axis_column_name.
    :return: None.
    """
    file_name = 'Line plot.html'
    # if axis names should be different than series.pd_frame column names
    x_name, y_name = axis_data_and_names(ts, x_axis_column, y_axis_column, x_axis_name, y_axis_name)

    trace = go.Scatter(x=series.pd_frame['Date'],
                       y=series.pd_frame[y_axis_column],
                       mode='lines',
                       name='line',
                       opacity=0.85,
                       marker=dict(
                           size=6,
                           color='rgb(181, 32, 160)',
                           symbol='pentagon',
                           line={'width': 0.5}
                       ))

    data = [trace]
    layout = ds.scatter_layout(title, x_name, y_name)
    fig = go.Figure(data=data, layout=layout)

    try:
        pyo.plot(fig, filename=file_name)
        logger.info('Line plot created. File name: "' + file_name + '".')
    except Exception as e:
        logger.critical('Line plot creation failed. Exception: "' + str(e) + '".')
