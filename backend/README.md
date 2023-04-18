# file structure

- backend
    - server.py
    - urbanAI.db
    - src
        - database
            - database.py
                - class `Database`
            - singletonMeta.py
                - class `SingletonMeta`
        - fetchers
            - regionDataFetcher.py
                - class `RegionDataFetcher`
            - resourceFetcher.py
                - class `ResourceFetcher` (ABC)
                - class `MeshResourceFetcher`
                - class `PcdResourceFetcher`
            - FetchersConsts.py
                - Enum `ResourceAttr` : UNIQUE_ID, DB_ID, EXPIRE, LAST_UPDATE, PATH
                - Enum `ResourceType` : MESH, PCD
            - TifRegionFetcher.py
                - class `TifRegionFetcher`
        - loaders
            - tifLoader.py
                - class `TifLoader`
            - utils.py

# Route
## POST /v1/api/region/mesh
## GET /v1/download