from file_handler import Files
from loguru import logger
import pandas as pd


class TimeSeries:
    def __init__(self,
                 file: Files):
        self.file = file
        logger.info("Creating TimeSeries object for file " + self.file.file_name + ".")

        self.column_names = self.file.raw_data.columns
        self.data = self.file.raw_data.copy()

        logger.success('TimeSeries object created.')

