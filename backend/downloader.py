from src.downloader.tifDownloader import TifDownloader
from src.loaders.TifLoader import TifLoader
from src.fetchers.TifRegionFetcher import TifRegionFetcher
from src.database.database import database

USERNAME = "z5339228"
TOKEN = "nlw5ez9CSadUl39UWBQouLcY@6PkA7QtuM@YCkZPN4MCTWAwzrT6XzlHYKzmqwIj"


datasetName = "SRTM 1 Arc-Second Global"
downloader = TifDownloader(USERNAME, TOKEN, datasetName)
downloader.setRegion({'latitude' : -35, 'longitude' : 148}, { 'latitude' : -30 , 'longitude' : 150})
downloader.searchDataset()
downloader.searchRegion()
downloader.fetchResourceOptions()
links = downloader.requestResourceAccess()
filenames = downloader.fetchResource(links, 3)
downloader.close()
print("############################################################")
print("############################################################")
yes = input("Type Yes to generate Mesh. [Yes/No] : ")
if 'Y' not in yes.upper():
    print("You can generate any time you want. Script will exit in 3s")
    exit()
print("Generate MESH ...")
database.start()
for filename in filenames:
    if filename is not None:
        print("Open file:", filename)
        loader = TifLoader(f"data/{filename}", origin=[(-35 + -30) / 2, (148+150) / 2])
        fetcher = TifRegionFetcher.create_by_loader(loader)
        fetcher.make_pcd()
        fetcher.make_mesh()
database.close()
