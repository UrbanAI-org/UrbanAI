from typing import Any


class AlwaysOnInterface:

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass

    def next(self):
        pass