import time_series.time_series as ts
import time_series.stats as stats
import time_series.plot as plt
from loguru import logger


def main():
    series = ts.Time_series(name='EUR / USD')
    series.read_raw('test_data_SEK_EUR_vs_USD.csv')

    # Fields from file to use.
    # flds = ['Adj Close']
    flds = ['SEK=_MID_PRICE', 'EUR=_MID_PRICE']
    series.set_fields(flds)

    # Fields from dataframe to use.
    fields = []
    for f in flds:
        fields.append(f.replace(' ', '_'))

    # Add daily returns column(s).
    # series.returns(fields=fields)

    # series.returns_dates(['SEK=_MID_PRICE_rets', 'EUR=_MID_PRICE_rets'])

    # Line plot
    # plt.time_series_plot(series=series, title='Close', x_axis_column='Date', y_axis_column='Adj_Close', y_axis_name='Date', x_axis_name='Close')
    lp = plt.create_single_line_plot(series,
                                     x_axis_column=series.data.index.name,
                                     y_axis_column='EUR=_MID_PRICE',
                                     title=series.name,
                                     x_axis_name='Date',
                                     y_axis_name='EUR=_MID_PRICE')
    plt.show(lp)
    plt.save(lp, output_file_name='Line_plot.html')
    # plt.ftp_put_file(output_file_name='Line_plot.html')
    # print(stats.aggregated_returns(series=series, field='Adj_Close_rets', convert_to='weekly'))

    logger.info('Done.')


if __name__ == '__main__':
    main()
