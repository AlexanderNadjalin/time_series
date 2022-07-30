import configparser as cp
from pathlib import Path
from loguru import logger


class Files:
    # Object holding config and file names. Has methods for reading spin-files.
    def __init__(self,
                 file_to_read: str):
        self.config = cp.ConfigParser()
        self.read_config()
        self.file_name = file_to_read

        self.input_directory = Path(self.config['input_files_dir']['input_files_dir'])
        self.output_directory = Path(self.config['output_files_dir']['output_files_dir'])
        self.file_dirs_valid()

    def read_config(self):
        """
        Read config.cfg file and return a config object. Used to set default parameters for file objects.
        :return: A ConfigParser object.
        """
        conf = cp.ConfigParser()
        conf.read('config.ini')

        logger.info('Info read from config.ini file.')

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
