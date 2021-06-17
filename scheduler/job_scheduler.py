from scheduler.repeating_timer import RepeatingTimer
from utils.my_logger import logger

@logger
class JobScheduler:

    def __init__(self):
        r_timer = self.set_update_looper(self.do_sth)
        r_timer.start()

    def set_update_looper(self, operation_fn):
        return RepeatingTimer(10.0, operation_fn)
        

    def do_sth(self):
        self.debug("timer auto logging test")
