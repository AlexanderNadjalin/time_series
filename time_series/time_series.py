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

        if self.file_valid(input_file_path):
            try:
                self.raw_data = pd.read_csv(input_file_path, sep=',', index_col='Date', parse_dates=True)
            except ValueError:
                logger.error('Value error. Check file format (date column name). Aborted.')
                quit()
            else:
                self.raw_data.columns = self.raw_data.columns.str.replace(' ', '_')
                for col in self.raw_data:
                    self.all_fields.append(col)
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
            logger.info('')
            logger.critical('File directory or file name is incorrect. Aborted')
            quit()

    @logger.catch()
    def set_fields(self, fields: list):
        self.data_fields = fields
        logger.info('')
        try:
            self.data = self.raw_data[self.data_fields]
        except KeyError as message:
            logger.error(str(message) + '. Aborted.')
            quit()
        else:
            logger.success('Time series data set with fields: ' + str(self.data_fields) + '.')

    @logger.catch()
    def returns(self, fields, ret_type=None):
        df = self.data.copy()
        for f in fields:
            fld_str = ''
            if ret_type == 'log':
                fld_str = f + '_log_rets'
                df[fld_str] = np.log(df[f]).diff()
            else:
                fld_str = f + '_rets'
                df[fld_str] = np.log(df[f] / df[f].shift(1))
            self.data_fields.append(fld_str)
        self.data = df
        self.data.dropna(inplace=True)
