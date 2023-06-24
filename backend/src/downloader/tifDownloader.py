from src.downloader.requestSender import RequestService, ModuleOptions
import json
import re
import time
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED
import requests
import os 
import tqdm
class TifDownloader:
    requestSender = None
    lowerLeft = None 
    upperRight = None
    spatialFilter = None
    datasetName = None
    datasetAlias = None
    regionIds = None
    downloads = None

    def __init__(self, username, token, datasetName = None) -> None:
        options = ModuleOptions(username, token)
        self.requestSender = RequestService(options, None)
        self.requestSender.authenticate()
        self.datasetName = datasetName
    
    def setRegion(self, lowerLeft, upperRight):
        self.spatialFilter = {'filterType' : "mbr",
                                'lowerLeft' : lowerLeft,
                                'upperRight' : upperRight}
        pass 

    def searchDataset(self):
        print("Searching Dataset")
        payload = {'datasetName' : self.datasetName,
                            'spatialFilter' : self.spatialFilter}   
        datasets = self.requestSender.dispatchRequest("dataset-search", payload)

        if len(datasets) > 1:
            print("Found ", len(datasets), " datasets. Please confirm which is you are looking for\n")
            for dataset in datasets:
                print(f"Found Dataset {dataset['collectionName']}({dataset['datasetAlias']})")
            raise Exception("to many datasets found")
        
        elif len(datasets) == 0:
            raise Exception("datasets not found ")
        print("Found ", len(datasets), " datasets.\n")
        
        self.datasetAlias = datasets[0]['datasetAlias']
        return datasets[0]
    
    def searchRegion(self):
        payload = {
            "datasetName": self.datasetAlias,
            "sceneFilter": {
                'spatialFilter' : self.spatialFilter
            }
        }
        print("Searching Regions...\n\n")
        scenes = self.requestSender.dispatchRequest("scene-search", payload)
        if len(scenes['results']) == 0:
            raise Exception("Regions not found ")
        # TODO : 
        self.regionIds = [scene['entityId'] for scene in scenes['results']]


    def fetchResourceOptions(self):
        sceneIds = ",".join(self.regionIds)
        payload = {'datasetName' : self.datasetAlias, 'entityIds' : sceneIds}
        print("Fetching download options...\n\n")
        options = self.requestSender.dispatchRequest("download-options", payload)
        entities = {}
        for option in options:
            if option['entityId'] not in entities.keys():
                entities[option['entityId']] = []
            entities[option['entityId']].append({
                "id" : option['id'],
                "productName" : option['productName'],
                "filesize" : option['filesize'],
            })
        self.downloads = []
        total_size = 0
        for key, value in entities.items():
            has_tiff = False
            for option in value:
                if re.search(r"geotiff", option['productName'], re.IGNORECASE):
                    self.downloads.append({
                        "entityId": key,
                        "productId": option['id']
                    })
                    has_tiff = True
                    total_size += option['filesize']
                    break
            if not has_tiff:
                print(f"For Region({key}), GeoTIFF format is not avaiable. The default format will be download")
                self.downloads.append({
                        "entityId": key,
                        "productId": value[0]['id']
                    })
                total_size += value[0]['filesize']
        print(f"Estimated {len(self.downloads)} files will take {round(total_size / 1048576, 1) }MB")
                

    def requestResourceAccess(self):
        requestedDownloadsCount = len(self.downloads)
        # print(downloads)
        label = "URBANAI"
        payload = {
            'downloads' : self.downloads,
            'label': label
        }
        print("Fetching download links...\n\n")
        requestResults = self.requestSender.dispatchRequest("download-request", payload)
        # PreparingDownloads has a valid link that can be used but data may not be immediately available
        # Call the download-retrieve method to get download that is available for immediate download
        with open("urls.json", "w") as fl:
                json.dump(requestResults, fl)
        download_links = set()
        if requestResults['preparingDownloads'] != None and len(requestResults['preparingDownloads']) > 0:
            pass
            payload = {'label' : label}
            moreDownloadUrls = self.requestSender.dispatchRequest("download-retrieve", payload)
            with open("retrieve.json", "w") as fl:
                json.dump(moreDownloadUrls, fl)
            downloadIds = []  
                        
            for download in moreDownloadUrls['available']:
                if str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']:
                    downloadIds.append(download['downloadId'])
                    download_links.add(download['url'])
                    print("AVAIABLE DOWNLOAD: " + download['url'])
                
            for download in moreDownloadUrls['requested']:
                if str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']:
                    downloadIds.append(download['downloadId'])
                    download_links.add(download['url'])
                    print("AVAIABLE DOWNLOAD: " + download['url'])
            

            num_attemp = 0
            # Didn't get all of the reuested downloads, call the download-retrieve method again probably after 30 seconds
            while len(downloadIds) < (requestedDownloadsCount - len(requestResults['failed']) - len(requestResults['availableDownloads'])): 
                preparingDownloads = requestedDownloadsCount - len(downloadIds) - len(requestResults['failed'])
                print("\n", preparingDownloads, "downloads are not available. Waiting for 30 seconds.\n")
                time.sleep(30)
                num_attemp += 1
                print("Trying to retrieve data\n")
                if num_attemp > 10:
                    print("USGS Server is busy, you can try agagin later or stil waiting for processing.")
                moreDownloadUrls = self.requestSender.dispatchRequest("download-retrieve", payload)
                # print(moreDownloadUrls)
                for download in moreDownloadUrls['available']:                            
                    if download['downloadId'] not in downloadIds and (str(download['downloadId']) in requestResults['newRecords'] or str(download['downloadId']) in requestResults['duplicateProducts']):
                        downloadIds.append(download['downloadId'])
                        download_links.add(download['url'])
                        print("AVAIABLE DOWNLOAD: " + download['url']) 
                    # Get all available downloads
        for download in requestResults['availableDownloads']:
            download_links.add(download['url'])
            print("AVAIABLE DOWNLOAD: " + download['url'])   

        print("\nAll downloads are available to download.\n")
        return list(download_links)

    def fetchResource(self, links, concurrent_num = 5, skip_cache = True):
        def download(url):
            r = requests.get(url, stream=True)
            if r.ok:
                filename = r.headers['Content-Disposition'].split('filename=')[1].replace('"', "")
                print(f"Downloading {filename} ({round(int(r.headers['Content-Length']) / (1024 * 1024), 2)}MB)")
                if os.path.isfile("data/" + filename):
                    if skip_cache:
                        print(f"File: {filename} already cached, skip downloading.")
                        return filename
                    else:
                        os.remove("data/" + filename)
                with open("data/" + filename + ".downloading", 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024 * 8):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                            os.fsync(f.fileno())
                os.rename("data/" + filename + ".downloading", "data/" + filename)
                print(f"Downloading {filename} Completed")
                return filename
            else:  # HTTP status code 4XX/5XX
                print("Download failed: status code {}\n{}".format(r.status_code, r.text))
                return None

        print("Resource")
        executor = ThreadPoolExecutor(max_workers= concurrent_num)
        futures = [executor.submit(download, link) for link in links]
        wait(futures, return_when=ALL_COMPLETED, timeout= len(links) * 120 / concurrent_num * 1.2)
        filenames = [future.result() for future in futures]
        print("COMPLETE DOWNLOAD ALL")
        print(filenames)
        return filenames

    def close(self):
        self.requestSender.logout()