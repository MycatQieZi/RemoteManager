from threading import Timer

class RepeatingTimer(Timer): 
    # def __init__(self, interval, function, lock, *args, **kwargs):
    #     super(RepeatingTimer, self).__init__(interval, function, *args, **kwargs)
    #     self.lock = lock

    def run(self):
        while not self.finished.is_set():
            # is_acquired = self.lock.acquire(blocking=False)
            # if not is_acquired:
            #     print("locked, next")
            #     continue 
            self.function(*self.args, **self.kwargs)
            # self.lock.release()
            self.finished.wait(self.interval)