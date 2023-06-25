from src.optimizers.PcdCompress import Compresser
from src.fetchers.TifFetcher import TifFetcher
from src.database.database import database

database.start()
base, uids = TifFetcher.fetch_all()
Compresser(uids).execute()
database.close()
