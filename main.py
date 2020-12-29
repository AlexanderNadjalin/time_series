import time_series.time_series as ts
from loguru import logger


def main():
    series = ts.Time_series(name='PLTR')
    series.io_read_raw('PLTR.csv')
    series.set_fields(['Adj_Close'])
    series.returns(fields=['Adj_Close'])
    # ts.stats.add_relative_strength_index(fields='Adj_Close_rets', window=14)

    logger.info('Done.')


if __name__ == '__main__':
    main()
