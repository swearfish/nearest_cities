import argparse

import pandas as pd

from nearest_city_finder import find_nearest_cities


def report_progress(index, total, force=False):
    if index % 1000 != 0 and not force:
        return
    max_dots = 30
    percent = index / total * 100
    dots = int(max_dots * percent / 100)
    print(f'[{dots * "•"}{" " * (max_dots - dots)}] {percent:.2f}% ({index} / {total}) processed', end='\r')


def process_cities(input_file: str, output_file: str, distance_threshold_km: int, print_results: bool):
    try:
        cities = pd.read_csv(input_file)
    except FileNotFoundError:
        print(f'File not found: {input_file}')
        return 1
    except pd.errors.EmptyDataError:
        print(f'File is empty: {input_file}')
        return 2
    except pd.errors.ParserError as e:
        print(f'Error parsing file {input_file}: {e}')
        return 3

    try:
        find_nearest_cities(cities, distance_threshold_km,
                            print_results=print_results,
                            report_progress=report_progress)
    except ValueError as e:
        print(f'Error processing cities: {e}')
        return 4
    except Exception as e:
        print(f'Unexpected error when processing cities: {e}')
        return 5

    try:
        cities.to_csv(output_file, index=False)
    except Exception as e:
        print(f'Error saving {output_file}: {e}')
        return 6

    return 0


def main():

    parser = argparse.ArgumentParser(description='Find nearest neighbors for cities')
    parser.add_argument('--input', type=str, default='assets/uscities.csv', help='Input CSV')
    parser.add_argument('--output', type=str, default='out/uscities_neighbors.csv', help='Output CSV')
    parser.add_argument('--distance', type=int, default=50, help='Distance threshold in km')
    parser.add_argument('--print', action='store_true', help='Print results')

    args = parser.parse_args()

    return process_cities(args.input, args.output, args.distance, args.print)


if __name__ == '__main__':
    main()
