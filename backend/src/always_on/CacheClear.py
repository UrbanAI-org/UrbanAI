from typing import Any
from datetime import timedelta, datetime
from src.always_on.AlwaysOnInterface import AlwaysOnInterface
import requests
class CaCheClear(AlwaysOnInterface):
    def __init__(self, key, period : timedelta) -> None:
        self.key = key
        self.period = period

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        requests.delete("localhost:9999/v1/clear/cache", json={"key":self.key})

    def next(self, curr: datetime):
        return curr + self.period
    
    def __repr__(self):
        return str(("always_on.CaCheClear.", self.period.__str__(), self.key))
    
    def __str__(self) -> str:
        return str(("CaChe Clear every", self.period.__str__()))
    
class RegionsClear(AlwaysOnInterface):
    def __init__(self, key, period : timedelta) -> None:
        self.key = key
        self.period = period

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        requests.delete("localhost:9999/v1/clear/regions", json={"key":self.key})

    def next(self, curr: datetime):
        return curr + self.period
    
    def __repr__(self):
        return str(("always_on.CaCheClear.", self.period.__str__(), self.key))
    
    def __str__(self) -> str:
        return str(("CaChe Clear every", self.period.__str__()))