import sys
from src.database.database import database
from src.fetchers.TifRegionFetcher import TifRegionFetcher
from src.loaders.TifLoader import TifLoader
from datetime import datetime

def get_filenames(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            return lines
    except FileNotFoundError:
        print(f"File '{filename}' not found.")

if len(sys.argv) < 2:
    print("Usage: python generator.py <tifs_downloaded.txt>")
else:
    filename = sys.argv[1]
    filenames = get_filenames(filename)
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
