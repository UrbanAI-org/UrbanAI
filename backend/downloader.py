from src.downloader.tifDownloader import TifDownloader
from src.loaders.TifLoader import TifLoader
from src.fetchers.TifRegionFetcher import TifRegionFetcher
from src.database.database import database
from datetime import datetime


USERNAME = "z5339228"
TOKEN = "nlw5ez9CSadUl39UWBQouLcY@6PkA7QtuM@YCkZPN4MCTWAwzrT6XzlHYKzmqwIj"


datasetName = "SRTM 1 Arc-Second Global"
downloader = TifDownloader(USERNAME, TOKEN, datasetName)
# downloader.setRegion({'latitude' : -35, 'longitude' : 148}, { 'latitude' : -30 , 'longitude' : 150})
downloader.setRegion({'latitude' : -34, 'longitude' : 149}, { 'latitude' : -32 , 'longitude' : 152})
downloader.searchDataset()
downloader.searchRegion()
downloader.fetchResourceOptions()
links = downloader.requestResourceAccess()
filenames = downloader.fetchResource(links, 3)
downloader.close()
print("############################################################")
print("############################################################")
mesh_space = len(filenames) * 75
pcd_space = len(filenames) * 312
print(f"Estimated need for space: \n{mesh_space}MB for meshes \n{pcd_space}MB for point clouds \nTotal:{mesh_space + pcd_space}")
print("Ensure empty the dataset")
yes = input("Type Yes to generate Mesh. [Yes/No] : ")
if 'Y' not in yes.upper():
    print("You can generate any time you want. list will save to tifs_downloaded.txt")
    print("To continue")
    print("python generator.py tifs_downloaded.txt")
    with open("tifs_downloaded.txt", "w") as fl:
        fl.write('\n'.join(filenames))
        exit()

print("Generate MESH ...")
database.start()
curr = 0
max = len(filenames)

for filename in filenames:
    if filename is not None:
        before = datetime.now()
        print("Open file:", filename)
        loader = TifLoader(f"data/{filename}", origin=[-33.5, 150])
        fetcher = TifRegionFetcher.create_by_loader(loader)
        fetcher.make_pcd()
        fetcher.make_mesh()
        after = datetime.now()
        curr += 1
        print("Estimate time left", (after - before) * (max - curr))
database.close()
