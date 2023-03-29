from tifProcess.tifLoader import Loader, Manager
import matplotlib.pyplot as plt
import open3d as o3d
import threading

def drawOneChunk():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    chunks = loader.cutWithXYPlaneCoord()
    chunk = chunks[0]
    chunk.toMesh(visualization = True)

def drawWhole():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    chunk = loader.toChunkWithXYPlaneCoord()
    chunk.toMesh(visualization = True)

def drawOneChunkByGeoCoord():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    chunks = loader.cutWithCoord()
    chunk = chunks[0]
    chunk.toMesh(visualization = True)

def drawMuliitpleChunksWithPCD():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    chunks = loader.cutWithXYPlaneCoord()
    chunk = chunks[0]
    chunk2 = chunks[1]
    pcd1 = chunk.toPointCloud()
    mesh1 = chunk.toMesh(pcd = pcd1,)
    pcd2 = chunk2.toPointCloud()
    mesh2 = chunk2.toMesh(pcd = pcd2)
    mesh1.compute_vertex_normals()
    mesh2.compute_vertex_normals()
    mesh1.paint_uniform_color([1, 0.706, 0])
    mesh2.paint_uniform_color([1, 0.706, 0])
    thread = threading.Thread(target=lambda meshs_ : o3d.visualization.draw_geometries(meshs_, mesh_show_back_face  = True), args=[[mesh1, mesh2, pcd1, pcd2]])
    thread.start()
    thread.join()



def saveMesh():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    chunks = loader.cutWithXYPlaneCoord()
    chunk = chunks[0]
    chunk.toMesh(visualization = True, save = True, filename = "save_file_example")

def saveMeshs():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    chunks = loader.cutWithXYPlaneCoord()
    meshs = []
    for chunk in chunks[0: 5]:
        mesh = chunk.toMesh(save=True)
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color([1, 0.706, 0])
        meshs.append(mesh)

    o3d.visualization.draw_geometries(meshs, mesh_show_back_face = True)

def loadMeshs():
    files = ('(10967.664430654855, -3572.355059097602)-((9384.184754926564, -2142.3807588684394)).ply',
    '(10967.664430654855, -5002.32886871952)-((9384.184754926564, -3572.355059097602)).ply',
    '(10967.664430654855, -6432.30199104978)-((9384.184754926564, -5002.32886871952)).ply',
    '(10967.664430654855, -7862.274230050952)-((9384.184754926564, -6432.30199104978)).ply',
    '(10967.664430654855, -9188.99841438455)-((9384.184754926564, -7862.274230050952)).ply')
    meshs = []
    for file in files:
        mesh = o3d.io.read_triangle_mesh(file)
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color([1, 0.706, 0])
        meshs.append(mesh)

    o3d.visualization.draw_geometries(meshs, mesh_show_back_face = True)

def checkChunks():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    loader.cutWithXYPlaneCoord()
    polygon = [
        (-33.05, 151.222),
        (-33.076, 151.744),
        (-33.42, 151.246),
    ]
    ids = Manager().searchChunk(polygon)
    print(len(ids))
    pass

def saveMan():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    loader.cutWithXYPlaneCoord()
    Manager().save()
    # before = Manager().tojson()
    print(Manager().tojson())
    Manager().clear()
    Manager().load()
    print(Manager().tojson())

def loadMan():
    Manager().load()
    print(Manager().tojson())

def loadWithCached():
    loader = Loader("data/s34_e151_1arc_v3.tif")
    chunks = loader.cutWithXYPlaneCoord()
    for chunk in chunks[0: 5]:
        mesh = chunk.toMesh(save=True)
    Manager().save()
    Manager().clear()
    Manager().load()
    meshs = []
    for chunk in chunks[0: 5]:
        mesh = chunk.toMesh(save=False)
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color([1, 0.706, 0])
        meshs.append(mesh)
    o3d.visualization.draw_geometries(meshs, mesh_show_back_face = True)

def searchByCached():
    # ASSUME saveMeshs() first
    Manager().load()
    polygon = [
            (-33.005, 151.0056),
            (-33.021, 151.078),
            (-33.037, 151.384),
        ]
    ids = Manager().searchChunk(polygon)
    meshs = []
    for id in ids:
        mesh = Manager().getChunkSaved(id, ".ply")
        if mesh is None:
            continue
        mesh.compute_vertex_normals()
        mesh.paint_uniform_color([1, 0.706, 0])
        meshs.append(mesh)
    o3d.visualization.draw_geometries(meshs, mesh_show_back_face = True)

def searchURLByCached():
    # ASSUME saveMeshs() first
    Manager().load()
    polygon = [
            (-33.005, 151.0056),
            (-33.021, 151.078),
            (-33.037, 151.384),
        ]
    ids = Manager().searchChunk(polygon)
    meshs = []
    for id in ids:
        mesh = Manager().getChunkSavedURL(id, ".ply")
        if mesh is None:
            continue
        meshs.append(mesh)
    print(meshs)

saveMeshs()