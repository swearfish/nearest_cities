from unittest import TestCase

from parameterized import parameterized

from nearest_city_finder import NearestCityFinder
import pandas as pd
import geopy.distance


class TestNearestCityFinder(TestCase):

    def setUp(self):
        self.cities = pd.read_csv('assets/uscities.csv')
        self.neighbors = NearestCityFinder(self.cities)
        self.distance_threshold_km = 50

    @parameterized.expand([0, 1, 2, 5501, 13702])
    def test_only_neighbors_within_distance(self, ref_index):

        """
        This test will verify that each found neighbor is within the distance threshold.
        """

        ref_row = self.cities.iloc[ref_index]
        neighbor_indices = self.neighbors.find_nearest_cities(self.distance_threshold_km, ref_row, ref_index)
        coords = ref_row[['lat', 'lng']]
        for neighbor_idx in neighbor_indices:
            neighbor_city = self.cities.iloc[neighbor_idx]
            neighbor_coords = neighbor_city[['lat', 'lng']]
            distance = geopy.distance.distance(coords, neighbor_coords).km
            # we shall leave a small margin of error, hence comparing with distance_threshold_km + 1
            self.assertLessEqual(distance, self.distance_threshold_km + 1)

    @parameterized.expand([0])
    def test_if_all_neighbors_found(self, ref_index):

        """
        This test will verify that all neighbors are found.
        """

        ref_row = self.cities.iloc[ref_index]
        neighbor_indices = [int(i) for i in
                            self.neighbors.find_nearest_cities(self.distance_threshold_km, ref_row, ref_index)]
        neighbor_indices.sort()
        coords = ref_row[['lat', 'lng']]
        for index, row in self.cities.iterrows():
            if index != ref_index:
                neighbor_city = self.cities.iloc[index]
                neighbor_coords = neighbor_city[['lat', 'lng']]
                distance = geopy.distance.distance(coords, neighbor_coords).km
                # if the distance is within the threshold, the neighbor should be found
                if (distance <= self.distance_threshold_km
                        # when not found
                        and index not in neighbor_indices
                        # we shall leave a small margin of error, hence comparing with distance + 1
                        and distance + 1 < self.distance_threshold_km):
                    self.fail(f'Neighbor not found: {neighbor_city["city"]} / {neighbor_city["state_id"]}')

    def test_if_no_neighbors(self):

        """
        This test will verify that a city is not its own neighbor.
        """

        for index, row in self.cities.iterrows():
            neighbor_indices = self.neighbors.find_nearest_cities(self.distance_threshold_km, row, index)
            self.assertNotIn(index, neighbor_indices)
