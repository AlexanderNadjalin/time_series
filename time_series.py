from file_handler import Files
from loguru import logger
import pandas as pd


class TimeSeries:
    def __init__(self,
                 input_file: Files):
        self.input_file = input_file

        logger.success('TimeSeries object created.')


