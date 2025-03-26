# Nearest cities

This is a simple tool for finding the nearest cities for each city in a dataset.
Source of the dataset: https://simplemaps.com/data/us-cities

## Installation

All the dependencies are listed in `requirements.txt`. You can install them with the following command:

```bash
pip install -r requirements.txt
```

Please also download the dataset from the link above and save it as `uscities.csv` in the `assets` directory of the project.

## Usage

### The API

The API is implemented in `neighbours.py`. You can use it as follows:

You may either use the function `find_nearest_cities` directly or use the class `NearestCityFinder`.

The function `find_nearest_cities` is useful to add neighbors to an existing DataFrame, while
the class `NearestCityFinder` is useful for queries.

### Command line interface

The CLI is implemented in `main.py`. It can be run with the following command:

```bash
python main.py --input <path_to_input_file> --output <path_to_output_file> --distance <distance in km>
```

#### Parameters

- `--input`: Path to the input file. The input file should be a CSV file with the following columns: `city`, `lat`, `lng`.
- `--output`: Path to the output file. The output file will be a CSV file with the following additional columns: `neighbors`.
- `--distance`: The maximum distance in kilometers to consider when finding the nearest cities. Default is 50 km
- `--print`: If this flag is set, the output will be printed to the console

## Implementation

The implementation is based on a Ball Tree data structure. 
The Ball Tree is a binary tree space partitioning structure.

Key points:
- The Ball Tree is built using the latitude and longitude of the cities
- The distance between two cities is calculated using the Haversine formula, because the cities are on the globe thus can't use euclidean distance
- The nearest neighbors are found using the Ball Tree query method
- The Ball Tree is built only once and can be used for multiple queries
- The query is not 100% accurate with distances close to the threshold, e.g.: with a threshold of 50 km, cities with a distance of 50.4 km might be considered neighbors, but others with 49.9 km are not.

Limitations:
- The Ball Tree is built in memory, so it might not be suitable for very large datasets
- The distance calculation is based on the Haversine formula, but not actual roads