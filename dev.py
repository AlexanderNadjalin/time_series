import time_series
import file_handler
from loguru import logger


def main():
    input_file_name = 'PLTR.csv'
    source_type = 'yahoo_finance'
    fh = file_handler.Files(file_to_read=input_file_name,
                            source_type=source_type)
    ts = time_series.TimeSeries(file=fh)
    logger.info(ts.file.raw_data)


if __name__ == '__main__':
    main()
