from geopy import distance
import numpy as np


def relativeDistance(given : tuple, base: tuple) -> float:
    """
    return relative distance based on two points.
    """
    distance_ = distance.distance(given, base).m 
    if given[0] < base[0] or given[1] < base[1]:
        return -1 * distance_
    return distance_

def makeXYPlaneInterp(func, samplingNum: int, array : np.ndarray, base: tuple) -> tuple:
    """
    create mapping
    """
    array = np.unique(array.ravel())
    xp = []
    yp = []
    for row in array.reshape((samplingNum, -1)):
        yp.append(relativeDistance(func(base, row[0]), base))
        xp.append(row[0])
    yp.append(distance.distance(func(base, array[-1]), base).m)
    xp.append(array[-1])
    return [np.array(xp), np.array(yp)]

def mapCoordtoXPPlane(coord, xp: np.ndarray, fp: np.ndarray, size: int) -> tuple:
    """
    map geo coord to xp coord
    """
    return (np.interp(coord.ravel(), xp, fp)).reshape((size, size))

def merge(altitude_array, lat_array, lon_array, size):
        """
        Composite 3d vector
        """
        r = []
        for i in range(size):
                r.append(np.stack((lat_array[i], lon_array[i], altitude_array[i]), axis = 1))
        return np.array(r).reshape((-1, 3))