from pathlib import Path
from loguru import logger
import configparser as cp
import pandas as pd
import numpy as np


class Time_series:
    def __init__(self, name, source='Refinitiv'):
        logger.info('Creating time series object for ' + name + '.')
        self.name = name
        self.source = source
        self.raw_data = None
        self.data = None
        self.raw_fields = []
        self.data_fields = []

    @logger.catch
    def read_raw(self, input_file_name: str):
        """

        Read config.ini file. Read specified input .csv file.
        :param input_file_name: Filename including suffix.
        :return: None.
        """
        conf = cp.ConfigParser()
        conf.read('config.ini')
        logger.success('I/O info read from config.ini file.')

        input_file_directory = Path(conf['input_data']['input_file_directory'])
        input_file_path = Path.joinpath(input_file_directory, input_file_name)

        if self.file_valid(input_file_path):
            try:
                self.raw_data = pd.read_csv(input_file_path, sep=',', index_col='Date', parse_dates=True)
            except ValueError as e:
                logger.error('File read failed with the following exception:')
                logger.error('   ' + str(e))
                logger.info('Aborted.')
                quit()
            else:
                for col in self.raw_data:
                    self.raw_fields.append(col)
                logger.success('Data file "' + input_file_name + '" read.')

    @logger.catch
    def file_valid(self, file_path: Path):
        """

        Check if file path is valid. Otherwise Abort.
        :param file_path: File Path object (directory + file name).
        :return: Boolean.
        """
        if file_path.exists():
            return True
        else:
            logger.critical('File directory or file name is incorrect. Aborted')
            quit()

    @logger.catch()
    def set_fields(self, fields: list) -> None:
        """

        Copy data from self.raw_data (imported data) to self.data (data to be used in Time_series object).
        :param fields: List of column names from the imported data.
        :return: None.
        """
        logger.info('')
        try:
            self.data = self.raw_data[fields]
        except KeyError as e:
            logger.error('Field set failed with exception:')
            logger.error('   ' + str(e))
            logger.info('Aborted.')
            quit()
        else:
            self.data.index.name = 'Date'
            self.data['Date'] = self.data.index.values
            self.data.columns = self.data.columns.str.replace(' ', '_')
            self.data_fields = self.data.columns.to_list()
            logger.success('Time series data set with fields: ' + str(self.data_fields) + '.')

    def returns_dates(self, column_name: list) -> pd.DataFrame:
        """

        Get daily returns and dates from specified column.
        :return: pd.DataFrame.
        """
        df1 = self.data
        df1['Date'] = df1.index

        for f in column_name:
            if f in self.data_fields:
                df1 = pd.concat([df1['Date'], df1[f]], axis=1)
            else:
                logger.critical('Column "' + f + '" does not exist in Time_series ' + self.name + '.')
                logger.critical('Aborted.')
                quit()
        df1.fillna(0, inplace=True)
        df1.set_index('Date', inplace=True)
        return df1

    @logger.catch()
    def returns(self, fields, ret_type=None):
        """

        Add daily returns column for specified column names.
        Choice of log or regular returns.
        :param fields: List of column names.
        :param ret_type: "log" if logged returns.
        :return: None.
        """
        df = self.data.copy()
        for f in fields:
            if ret_type == 'log':
                fld_str = f + '_log_rets'
                df[fld_str] = np.log(df[f]).diff()
            else:
                fld_str = f + '_rets'
                df[fld_str] = np.log(df[f] / df[f].shift(1))
            self.data_fields.append(fld_str)
        self.data = df
        self.data.dropna(inplace=True)
