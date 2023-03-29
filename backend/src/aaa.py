from tifProcess.tifLoader import Loader, Manager
import matplotlib.pyplot as plt
import open3d as o3d
import threading

Manager().clear()
loader = Loader("data/s34_e151_1arc_v3.tif")

chunks = loader.cutWithXYPlaneCoord()
meshs = []
for chunk in chunks[0:5]:
    mesh = chunk.toMesh(save=True)
Manager().save()