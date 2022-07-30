import time_series
import file_handler


def main():
    input_file_name = 'PLTR.csv'
    fh = file_handler.Files(file_to_read=input_file_name)
    ts = time_series.TimeSeries(input_file=fh)


if __name__ == '__main__':
    main()
