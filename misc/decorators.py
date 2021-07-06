from functools import wraps
import random, time
# static decorators

# make a certain class singleton, as name suggests
def singleton(cls, *args, **kwargs):
    instances = {}
    def _wrapper(**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _wrapper

def with_lock(thread_lock, blocking=False, logger=None):
    def wrapped_with_lock(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if thread_lock.acquire(blocking):
                res = fn(*args, **kwargs)
                thread_lock.release()
                return res
            else:
                if(logger):
                    logger.debug("线程占用, 下次一定")
        return wrapper
    return wrapped_with_lock

def with_countdown(fn):
    def timed_execution(*args, max_wait=5, randomly=False, timed=False, **kwargs):
        if(timed):
            countdown = random.randint(1, max_wait+1) if randomly else max_wait
            for i in range(countdown, 0, -1):
                time.sleep(1)
        return fn(*args, **kwargs)
    return timed_execution
