from enum import Enum

class ResourceAttr(Enum):
    UNIQUE_ID = "uid"
    DB_ID = "id"
    EXPIRE = "expired"
    LAST_UPDATE = "last_update"
    PATH = "pth"

class ResourceType(Enum):
    MESH = "meshes"
    PCD = "pcds"