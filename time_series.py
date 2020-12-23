from pathlib import Path
from loguru import logger
import configparser as cp
import pandas as pd


class Time_series:
    def __init__(self, name, source='Refinitiv'):
        logger.info('Creating time series object for ' + name + '.')
        self.name = name
        self.source = source
        self.raw_data = None
        self.data = None
        self.all_fields = []
        self.data_fields = []

    @logger.catch
    def io_read_raw(self, input_file_name: str):
        """

        Read config.ini file. Read specified input .csv file.
        :param input_file_name: Filename including suffix.
        :return: None.
        """
        conf = cp.ConfigParser()
        conf.read('config.ini')
        logger.info('')
        logger.success('I/O info read from config.ini file.')

        input_file_directory = Path(conf['input_data']['input_file_directory'])
        input_file_path = Path.joinpath(input_file_directory, input_file_name)

        if self.io_file_valid(input_file_path):
            try:
                self.raw_data = pd.read_csv(input_file_path, sep=',', index_col='Date', parse_dates=True)
            except ValueError:
                logger.error('Value error. Check file format (date column name). Aborted.')
                quit()
            else:
                for col in self.raw_data:
                    self.all_fields.append(col)
                logger.success('Data file "' + input_file_name + '" read.')

    @logger.catch
    def io_file_valid(self, file_path: Path):
        """

        Check if file path is valid. Otherwise Abort.
        :param file_path: File Path object (directory + file name).
        :return: Boolean.
        """
        if file_path.exists():
            return True
        else:
            logger.info('')
            logger.critical('File directory or file name is incorrect. Aborted')
            quit()

    @logger.catch()
    def data_set_fields(self, fields: list):
        self.data_fields = fields
        logger.info('')
        try:
            self.data = self.raw_data[self.data_fields]
        except KeyError as message:
            logger.error(str(message) + '. Aborted.')
            quit()
        else:
            logger.success('Time series data set with fields: ' + str(self.data_fields) + '.')

    def stats_add_relative_strength_index(self, window: int = 14, technique: str = 'SMA') -> None:
        """
        Calculates RSI (Relative Strength Index) with either SMA or EWMA ("SMA" for
        Simple Moving Average or "EWMA" for Exponential Moving Average).
        :param window: int: Period for the RSI.
        :param technique: str: Options are "SMA" or EWMA".
        :return: pandas.DataFrame.
        """
        for field in self.data_fields:
            deltas = self.data[field].diff()
            deltas = deltas[1:]
            d_up, d_down = deltas.copy(), deltas.copy()
            d_up[d_up < 0] = 0
            d_down[d_down > 0] = 0

            if technique == 'EWMA':
                roll_up = d_up.ewm(span=window, freq='D').mean()
                roll_down = d_down.ewm(span=window, freq='D').mean()
                rs = roll_up / roll_down.abs()
                rsi = 100.0 - (100.0 / (1.0 + rs))
                self.data[field + '_RSA_EWMA_' + str(window)] = rsi
            elif technique == 'SMA':
                roll_up = d_up.rolling(window).mean()
                roll_down = d_down.rolling(window).mean()
                rs = roll_up / roll_down.abs()
                rsi = 100.0 - (100.0 / (1.0 + rs))
                self.data[field + '_RSI_SWA_' + str(window)] = rsi
            else:
                logger.critical('Function was passed "' + technique +
                                '" as parameter. Needs to be either "EWMA" or "SMA". Aborted.')
                quit()

        self.data.dropna(inplace=True)
