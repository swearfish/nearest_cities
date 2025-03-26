from collections.abc import Callable, Hashable

import numpy as np
from pandas import DataFrame, Series
from sklearn.neighbors import BallTree

EARTH_RADIUS_KM = 6371.0


class NearestCityFinder:
    """
    A class to find nearest neighbors for cities.
    """

    def __init__(self, cities: DataFrame, leaf_size: int = 25):

        """
        Initialize the Neighbors class.
        :param cities: DataFrame with the cities
        :param leaf_size: The number of points at which the algorithm switches to brute-force search
        """

        if 'lat' not in cities.columns or 'lng' not in cities.columns or 'city' not in cities.columns:
            raise ValueError('Columns "lat", "lng", "city" must be present in the DataFrame')

        self.cities = cities
        self.cities_geo = cities[['lat', 'lng']].values
        self.cities_rad = np.radians(self.cities_geo)
        # PyCharm does not recognize the BallTree constructor signature
        # noinspection PyArgumentList
        self.tree = BallTree(self.cities_rad, leaf_size=leaf_size, metric='haversine')

    def find_nearest_cities(self, distance_threshold_km: float,
                            city_row: Series = None,
                            city_index: int | Hashable = None):

        """
        Find nearest neighbors for a given city.
        :param distance_threshold_km: The distance threshold in kilometers for the neighbors
        :param city_row: The row of the city in the DataFrame
        :param city_index: The index of the city in the DataFrame. Slower if not provided.
        :return: The indices of the neighbor cities
        """

        if city_row is None and city_index is None:
            raise ValueError('Either row or index must be provided')

        if city_row is None:
            city_row = self.cities.iloc[city_index]
        elif city_index is None:
            city_index = self.cities.index[self.cities['city'] == city_row['city']][0]

        # Convert distance threshold to radians
        distance_threshold = distance_threshold_km / EARTH_RADIUS_KM

        # Convert city coordinates to radians for the BallTree
        lat, lng = city_row['lat'], city_row['lng']
        geo_coord = (lat, lng)
        rad_coord = np.radians(geo_coord)

        # Find all cities around the city coordinates within the distance threshold
        idx = self.tree.query_radius([rad_coord], distance_threshold)

        # Remove the city itself from the neighbors
        filtered_idx = [i for i in idx[0] if i != city_index]

        return filtered_idx


def find_nearest_cities(cities: DataFrame, distance_threshold_km: float,
                        print_results: bool = False,
                        report_progress: Callable[[int, int, bool], None] = lambda i, t, f: None):

    """
    Find nearest neighbors for all cities in the DataFrame.
    Result is stored in a new column 'neighbors'.
    :param cities: The DataFrame with the cities
    :param distance_threshold_km:  The distance threshold in kilometers for the neighbors
    :param print_results: For debugging purposes, print the neighbors for each city
    :param report_progress: A function to report the progress
    :return: None
    """

    nearest_city_finder = NearestCityFinder(cities)
    result = []
    has_state_id = 'state_id' in cities.columns

    progress = 0
    total = len(cities)
    report_progress(0, total, True)

    for index, row in cities.iterrows():

        idx = nearest_city_finder.find_nearest_cities(distance_threshold_km, row, index)
        result.append(idx)

        if print_results:
            if has_state_id:
                neighbor_cities = cities.iloc[idx][['city', 'state_id']].values.tolist()
                print(f'Neighbors for {row["city"]} / {row["state_id"]}: {neighbor_cities}\n')
            else:
                neighbor_cities = cities.iloc[idx][['city']].values.tolist()
                print(f'Neighbors for {row["city"]}: {neighbor_cities}\n')

        progress += 1
        report_progress(progress, total, False)

    report_progress(total, total, True)
    cities['nearest_cities'] = result
