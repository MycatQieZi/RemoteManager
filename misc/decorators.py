from functools import wraps
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
