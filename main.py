from time_series import Time_series
from loguru import logger


def main():
    ts = Time_series(name='PLTR')
    ts.io_read_raw('PLTR.csv')
    ts.data_set_fields(['Adj Close', 'Volume'])
    ts.stats_add_relative_strength_index()
    print(ts.data)
    logger.info('Done.')


if __name__ == '__main__':
    main()
