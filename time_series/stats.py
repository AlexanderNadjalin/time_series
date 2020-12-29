from loguru import logger
from time_series.time_series import Time_series as ts


@logger.catch
def add_relative_strength_index(series: ts, fields, window: int = 14, technique: str = 'SMA') -> None:
    """
    Calculate RSI (Relative Strength Index) with either SMA or EWMA ("SMA" for
    Simple Moving Average or "EWMA" for Exponential Moving Average) for all given field names.
    :param series: Time_series.
    :param fields: List of field names to use in RSI calculation.
    :param window: int: Period for the RSI.
    :param technique: str: Options are "SMA" or EWMA".
    :return: pandas.DataFrame.
    """
    df = series.data.copy()
    for field in fields:
        deltas = series.data[field].diff()
        deltas = deltas[1:]
        d_up, d_down = deltas.copy(), deltas.copy()
        d_up[d_up < 0] = 0
        d_down[d_down > 0] = 0

        if technique == 'EWMA':
            roll_up = d_up.ewm(span=window, freq='D').mean()
            roll_down = d_down.ewm(span=window, freq='D').mean()
            rs = roll_up / roll_down.abs()
            rsi = 100.0 - (100.0 / (1.0 + rs))
            col_str = field + '_RSI_EWMA(' + str(window) + ')'
            df[col_str] = rsi
        elif technique == 'SMA':
            roll_up = d_up.rolling(window).mean()
            roll_down = d_down.rolling(window).mean()
            rs = roll_up / roll_down.abs()
            rsi = 100.0 - (100.0 / (1.0 + rs))
            col_str = field + '_RSI_SWA(' + str(window) + ')'
            df[col_str] = rsi
        else:
            logger.critical('Function was passed "' + technique +
                            '" as parameter. Needs to be either "EWMA" or "SMA". Aborted.')
            quit()

        df.dropna(inplace=True)
    series.data = df
    logger.success('Relative Strength Index column(s) added.')
