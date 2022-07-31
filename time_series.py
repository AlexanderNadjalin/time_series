from file_handler import Files
import configparser as cp
from loguru import logger
import pandas as pd


class TimeSeries:
    def __init__(self,
                 file: Files = None,
                 fill_missing_method: str = None):
        self.config = cp.ConfigParser()
        self.read_config()

        self.file = file
        self.data = pd.DataFrame()
        self.fill_missing_method = self.config['missing_values']['fill_missing_method']
        if fill_missing_method is not None:
            self.fill_missing_method = fill_missing_method

        # Blank TimeSeries, no file to import data from.
        if self.file is None:
            logger.info('Creating empty TimeSeries object.')
        # TimeSeries from file with data to import.
        else:
            logger.info('Creating TimeSeries object for file ' + self.file.file_name + '.')
            self.column_names = self.file.raw_data.columns
            self.data = self.file.raw_data.copy()

        self.data_valid()

        logger.success('TimeSeries object created.')

    def read_config(self):
        """
        Read time_series_config.cfg file and return a config object. Used to set default parameters for file objects.
        :return: A ConfigParser object.
        """
        conf = cp.ConfigParser()
        conf.read('time_series_config.ini')

        logger.info('Info read from time_series_config.ini file.')

        self.config = conf

    def data_valid(self) -> None:
        """
        Check for NaN, empty values and non-floats.
        Fill missing values.
        :return: None
        """
        cols = list(self.data.columns)
        empties = 0
        nans = 0
        floats_ints = 0
        for col in cols:
            col_empties = len(self.data[self.data[col] == ''])
            col_nans = self.data[col].isna().sum()
            if (self.data[col].dtypes != 'float64') and (self.data[col].dtypes != 'int64'):
                floats_ints += 1
            empties += col_empties
            nans += col_nans

            if col_empties > 0:
                logger.warning('Column ' + col + ' has ' + str(col_empties) + ' number of empty values.')
                self.fill_missing(col_name=col)
            if col_nans > 0:
                logger.warning('Column ' + col + ' has ' + str(col_nans) + ' number of NaN values.')
            if floats_ints > 0:
                logger.warning('Column ' + col + ' has one or more non-float values.')

        if (empties == 0) and (nans == 0) and (floats_ints == 0):
            logger.info('No empty, NaN or non-float/int values in imported file.')

    def fill_missing(self,
                     col_name: str) -> None:
        """
        Fill missing values in a column of self.data with given method.
        :param col_name: Column name. Passing "None" does nothing.
        :return: None.
        """
        if self.fill_missing_method == 'forward':
            self.data[col_name].fillna(method='ffill', inplace=True)
            logger.info('Column ' + col_name + ' forward-filled.')
        elif self.fill_missing_method == 'backward':
            self.data[col_name].fillna(method='bfill', inplace=True)
            logger.info('Column ' + col_name + ' backward-filled.')
        elif self.fill_missing_method == 'interpolate':
            self.data[col_name].interpolate(method='polynomial')
            logger.info('Column ' + col_name + ' filled by interpolation.')
        elif self.fill_missing_method is None:
            pass
        else:
            logger.critical('Fill method ' + self.fill_missing_method + ' not implemented. Aborted.')
            quit()
