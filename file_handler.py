import configparser as cp
from pathlib import Path
import os
from loguru import logger
import pandas as pd


class Files:
    # Object holding config and file names. Has methods for reading spin-files.
    def __init__(self,
                 file_to_read: str,
                 source_type: str):
        self.config = cp.ConfigParser()
        self.read_config()
        self.file_name = file_to_read
        self.source_type = source_type

        self.input_directory = Path(self.config['input_files_dir']['input_files_dir'])
        self.output_directory = Path(self.config['output_files_dir']['output_files_dir'])

        self.raw_data = pd.DataFrame()

        self.file_dirs_valid()

        self.read_file()

    def read_config(self):
        """
        Read file_handler_config.cfg file and return a config object. Used to set default parameters for file objects.
        :return: A ConfigParser object.
        """
        conf = cp.ConfigParser()
        conf.read('file_handler_config.ini')

        logger.info('Info read from file_handler_config.ini file.')

        self.config = conf

    def file_dirs_valid(self):
        """
        Check if file path is valid, otherwise Abort.
        """
        try:
            self.input_directory.exists()
        except IsADirectoryError:
            logger.critical('File directory is incorrect. Directory given: "' + str(self.input_directory) +
                            '". Aborted.')
            quit()

        try:
            self.output_directory.exists()
        except IsADirectoryError:
            logger.critical('File directory is incorrect. Directory given: "' + str(self.output_directory) +
                            '". Aborted.')
            quit()

    def read_file(self) -> None:
        """

        Count number of files in input_files dir.
        If one file, read it, no file name required.
        If > 1, file name needed, otherwise halt due to ambiguity.
        :return: None.
        """
        n_files = len(os.listdir(self.input_directory))
        if n_files == 1:
            self.import_file()
        elif (n_files > 1) and (len(self.file_name) > 1):
            self.import_file()
        else:
            logger.critical('Incorrect file name given for import while multiple files in the input directory.'
                            ' Aborted.')
            quit()

    def import_file(self):
        complete_path = Path(self.input_directory, self.file_name)

        if self.source_type == 'yahoo_finance':
            try:
                self.raw_data = pd.read_csv(complete_path,
                                            sep=',',
                                            decimal='.',
                                            index_col=0,
                                            parse_dates=True)
            except ValueError as e:
                logger.error('File read failed with the following exception:')
                logger.error('   ' + str(e))
                logger.info('Aborted.')
                quit()
            else:
                logger.info('Yahoo Finance file "' + str(complete_path) + '" read.')
