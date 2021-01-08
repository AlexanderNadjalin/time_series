"""

Module for plotting using plotly.express module.
Time series data should be a Time_series object.
"""

import plotly.express as px
import configparser as cp
from loguru import logger
from ftplib import FTP
from time_series.time_series import Time_series as ts


def create_single_line_plot(series,
                            x_axis_column: str,
                            y_axis_column: str,
                            title: str = None,
                            x_axis_name: str = None,
                            y_axis_name: str = None) -> px.line():
    x_name, y_name = axis_data_and_names(series, x_axis_column, y_axis_column, x_axis_name, y_axis_name)
    try:
        fig = px.line(series.data, x=x_name, y=y_name, title=title)
        return fig
    except Exception as e:
        logger.critical('Plot creation failed with the following exception:')
        logger.critical('   ' + str(e))
        logger.info('Aborted.')
        quit()


def show(fig):
    fig.show()


def save(fig, output_file_name: str):
    conf = cp.ConfigParser()
    conf.read('config.ini')
    output_file_directory = conf['plots']['output_plot_directory']
    output_file_path = output_file_directory + '\\' + output_file_name

    try:
        fig.write_html(output_file_path)
        logger.info('Line plot saved at : "' + output_file_path + '".')
    except Exception as e:
        logger.critical('Line plot creation failed. Exception: "' + str(e) + '".')
        logger.info('Aborted.')
        quit()


def ftp_put_file(output_file_name: str):
    conf = cp.ConfigParser()
    conf.read('config.ini')

    # FTP details
    ftp = FTP(conf['ftp']['host'])
    user_name = conf['ftp']['user_name']
    password = conf['ftp']['password']

    logger.info('FTP put operation started for file ' + output_file_name + '.')

    try:
        ftp.login(user_name, password)
    except Exception as e:
        logger.critical('FTP put operation failed with the following exception:')
        logger.critical('   ' + str(e))
        logger.info('Aborted.')
        quit()

    # Put file location
    output_file_directory = conf['plots']['output_plot_directory']
    output_file_path = output_file_directory + '\\' + output_file_name

    # Destination
    put_directory = conf['ftp']['put_directory']
    try:
        ftp.cwd(put_directory)
    except Exception as e:
        logger.critical('Directory change failed on FTP with the following exception:')
        logger.critical('   ' + str(e))
        logger.info('Aborted.')
        quit()

    # Put file
    try:
        with open(output_file_path, 'rb') as ftpup:
            ftp.storbinary('STOR ' + output_file_name, ftpup)
            ftp.close()
        logger.success('File ' + output_file_name + ' succesfully put on FTP.')
    except Exception as e:
        logger.critical('FTP put file operation failed with the following exception:')
        logger.critical('   ' + str(e))
        logger.info('Aborted.')
        quit()


def axis_data_and_names(series: ts, x_axis_column: str, y_axis_column: str,
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
    if x_axis_column not in series.data.columns and x_axis_column not in series.data.index.name:
        logger.critical('Column name "' + x_axis_column +
                        '" does not exist in TimeSeries object "' + series.name + '". Aborted.')
        quit()
    if y_axis_column not in series.data.columns:
        logger.critical('Column name "' + y_axis_column +
                        '" does not exist in TimeSeries object "' + series.name + '". Aborted.')
        quit()

    # if no specific axis names are provided, use series.data_fields column names
    if not x_axis_name:
        x_axis_name = x_axis_column
    if not y_axis_name:
        y_axis_name = y_axis_column

    return x_axis_name, y_axis_name
