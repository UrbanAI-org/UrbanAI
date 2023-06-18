from src.always_on.AlwaysOnInterface import AlwaysOnInterface
from threading import Thread
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
pool = ThreadPoolExecutor()
class Launcher:
    loop = True
    queue = []
    def __init__(self) -> None:
        pass

    def add(self, always_on : AlwaysOnInterface):
        next = always_on.next()
        item = AlwaysOnItem(always_on, next)
        self.queue.append(item)

    def launch(self):

        def start():
            while self.loop:
                if len(self.queue) > 0:
                    if datetime.now() > self.queue[0]:
                        self.queue[0].update()
                        sorted(self.queue)

        thread = Thread(target=start)
        self.queue = sorted(self.queue)
        thread.start()
        pass

    def close(self):
        self.loop = False


class AlwaysOnItem:
    def __init__(self, always_on : AlwaysOnInterface, runTime) -> None:
        self.always_on = always_on
        self.runTime = runTime

    def update(self):
        def run():
            self.runTime = self.always_on.next()
            self.always_on.__call__()
        pool.submit(run)


    def __lt__(self, obj):
        return ((self.runTime) < (obj.runTime))
  
    def __gt__(self, obj):
        return ((self.runTime) > (obj.runTime))
  
    def __le__(self, obj):
        return ((self.runTime) <= (obj.runTime))
  
    def __ge__(self, obj):
        return ((self.runTime) >= (obj.runTime))
  
    def __eq__(self, obj):
        return (self.runTime == obj.runTime)
  
    def __repr__(self):
        return str((self.always_on.__repr__(), self.runTime))