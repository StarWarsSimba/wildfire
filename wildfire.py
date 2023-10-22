"""Geographic clustering of historical wildfire data
CS 210, University of Oregon
Your Name Here
Credits: TBD
"""
import doctest
import csv
import config

import graphics.utm_plot
import random

def make_map() -> graphics.utm_plot.Map:
    """Create and return a basemap display"""
    map = graphics.utm_plot.Map(config.BASEMAP_PATH,
                                config.BASEMAP_SIZE,
                                (config.BASEMAP_ORIGIN_EASTING, config.BASEMAP_ORIGIN_NORTHING),
                                (config.BASEMAP_EXTENT_EASTING, config.BASEMAP_EXTENT_NORTHING))
    return map

def get_fires_utm(path: str) -> list[tuple[int, int]]:
    """Read CSV file specified by path, returning a list
    of (easting, northing) coordinate pairs within the
    study area.

    >>> get_fires_utm("data/test_locations_utm.csv")
    [(442151, 4729315), (442151, 5071453), (914041, 4729315), (914041, 5071453)]
    """
    coord_pairs = []
    with open(path, newline="", encoding="utf-8") as source_file:
        reader = csv.DictReader(source_file)
        for row in reader:
            easting = int(row["Easting"])
            northing = int(row["Northing"])
            if in_bounds(easting, northing):
                coord_pairs.append((easting, northing))
    return coord_pairs

def in_bounds(easting: float, northing: float) -> bool:
    """Is the UTM value within bounds of the map?"""
    if (easting < config.BASEMAP_ORIGIN_EASTING
        or easting > config.BASEMAP_EXTENT_EASTING
        or northing < config.BASEMAP_ORIGIN_NORTHING
        or northing > config.BASEMAP_EXTENT_NORTHING):
        return False
    return True

def plot_points(fire_map: graphics.utm_plot.Map,
                points:  list[tuple[int, int]],
                size_px: int = 5,
                color: str = "green") -> list:
    """Plot all the points and return a list of handles that
    can be used for moving them.
    """
    symbols = []
    for point in points:
        easting, northing = point
        symbol = fire_map.plot_point(easting, northing,
                                     size_px=size_px, color=color)
        symbols.append(symbol)
    return symbols

def assign_random(points: list[tuple[int, int]], n: int) -> list[list[tuple[int, int]]]:
    """Returns a list of n lists of coordinate pairs.
    The i'th list is the points assigned randomly to the i'th cluster.
    """
    # Initially the assignments is a list of n empty lists
    assignments = []
    for i in range(n):
        assignments.append([])
    # Then we randomly assign points to lists
    for point in points:
        choice = random.randrange(n)
        assignments[choice].append(point)
    return assignments

def centroid(points: list[tuple[int, int]]) -> tuple[int, int]:
    """The centroid of a set of points is the mean of x and mean of y"""
    sum_x = 0
    sum_y = 0
    for x, y in points:
        sum_x += x
        sum_y += y
    mean_x = sum_x // len(points)
    mean_y = sum_y // len(points)
    return mean_x, mean_y

def cluster_centroids(clusters: list[list[tuple[int,int]]]) -> list[tuple[int,int]]:
    """Return a list containing the centroid corresponding to each assignment of
    points to a cluster.
    """
    centroids = []
    for cluster in clusters:
        centroids.append(centroid(cluster))
    return centroids

def main():
    doctest.testmod()
    fire_map = make_map()
    points = get_fires_utm(config.FIRE_DATA_PATH)
    fire_symbols = plot_points(fire_map, points, color="red")
    partition = assign_random(points, config.N_CLUSTERS)
    centroids = cluster_centroids(partition)
    centroid_symbols = plot_points(fire_map, centroids, size_px=10,
                                   color="blue")
    input("Press enter to quit")

if __name__ == "__main__":
    main()