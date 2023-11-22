from geopy import distance
import numpy as np


def relativeDistance(given: tuple, base: tuple) -> float:
    """
    Calculate the relative distance between two points.

    Args:
        given (tuple): The coordinates of the given point.
        base (tuple): The coordinates of the base point.

    Returns:
        float: The relative distance between the two points.
               If the given point is to the left or below the base point, the distance is negative.
               Otherwise, it is positive.
    """
    distance_ = distance.distance(given, base).m
    if given[0] < base[0] or given[1] < base[1]:
        return -1 * distance_
    return distance_

def makeXYPlaneInterp(func, samplingNum: int, array : np.ndarray, base: tuple) -> tuple:
    """
    Create a mapping for interpolation on the XY plane.

    Args:
        func: The function used for interpolation.
        samplingNum: The number of samples to be taken from the array.
        array: The input array.
        base: The base tuple used for interpolation.

    Returns:
        A tuple containing two numpy arrays: xp (x-coordinates) and yp (y-coordinates).
    """
    array = np.unique(array.ravel())
    xp = []
    yp = []
    for row in array.reshape((samplingNum, -1)):
        yp.append(relativeDistance(func(base, row[0]), base))
        xp.append(row[0])
    yp.append(relativeDistance(func(base, array[-1]), base))
    xp.append(array[-1])
    return [np.array(xp), np.array(yp)]

def mapCoordtoXPPlane(coord, xp: np.ndarray, fp: np.ndarray, size: int) -> tuple:
    """
    Maps geographic coordinates to XP coordinates.

    Args:
        coord (np.ndarray): Array of geographic coordinates.
        xp (np.ndarray): Array of XP coordinates.
        fp (np.ndarray): Array of FP coordinates.
        size (int): Size of the output array.

    Returns:
        tuple: Tuple containing the mapped XP coordinates.

    """
    return (np.interp(coord.ravel(), xp, fp)).reshape((size, size))

def merge(altitude_array, lat_array, lon_array, size):
    """
    Composite 3d vector

    Args:
        altitude_array (numpy.ndarray): Array of altitude values
        lat_array (numpy.ndarray): Array of latitude values
        lon_array (numpy.ndarray): Array of longitude values
        size (int): Size of the arrays

    Returns:
        numpy.ndarray: Reshaped array of 3D vectors
    """
    r = []
    for i in range(size):
        r.append(np.stack((lat_array[i], lon_array[i], altitude_array[i]), axis=1))
    return np.array(r).reshape((-1, 3))
