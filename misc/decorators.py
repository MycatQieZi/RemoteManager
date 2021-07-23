from functools import wraps
from misc.consts import LOCKS
from misc.enumerators import ThreadLock
import random, time
import traceback
# static decorators

# make a certain class singleton, as name suggests
def singleton(cls):
    instances = {}
    def _wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _wrapper

def with_lock(lock, blocking=False, then_execute_callback=None):
    if isinstance(lock, str):
        thread_lock = LOCKS[ThreadLock(lock)]
    else:
        thread_lock = LOCKS[lock]
    def wrapper(fn):
        @wraps(fn)
        def execute_with_lock(self, *args, **kwargs):
            if thread_lock.acquire(blocking):
                try:
                    res = fn(self, *args, **kwargs)
                except Exception:
                    self.logger.error(traceback.format_exc())
                finally:
                    thread_lock.release()
                    if then_execute_callback:
                        then_execute_callback()
                return res
            else:
                if(self.logger):
                    self.logger.debug("线程占用, 下次一定")
        return execute_with_lock
    return wrapper

def with_countdown(fn):
    @wraps(fn)
    def timed_execution(*args, max_wait=5, randomly=False, timed=False, **kwargs):
        if(timed):
            countdown = random.randint(1, max_wait+1) if randomly else max_wait
            for i in range(countdown, 0, -1):
                time.sleep(1)
        return fn(*args, **kwargs)
    return timed_execution

def with_countdown2(max_wait=5, randomly=False, timed=False):
    def wrapper(fn):
        @wraps(fn)
        def timed_execution(self, *args, **kwargs):
            if(timed):
                countdown = random.randint(1, max_wait+1) if randomly else max_wait
                time.sleep(countdown)
            return fn(self, *args, **kwargs)
        return timed_execution
    return wrapper

def with_retry(retries=3, interval=5):
    def wrapper(fn):
        @wraps(fn)
        def fn_execution(self, *args, **kwargs):
            countdown = retries
            while True:
                try:
                    result = fn(self, *args, **kwargs)
                except Exception:
                    if(countdown>0):
                        countdown-=1
                        self.debug(f"执行失败, {interval}秒后重试第{retries-countdown}/{retries}次, 失败原因:\n%s", traceback.format_exc())
                        time.sleep(interval)
                    else:
                        raise
                else:
                    return result
        return fn_execution
    return wrapper

def with_retry2(fn):
    @wraps(fn)
    def fn_execution(self, *args, retries=3, interval=5, **kwargs):
        countdown = retries
        while True:
            try:
                result = fn(self, *args, **kwargs)
            except Exception:
                if(countdown>0):
                    countdown-=1
                    self.debug(f"执行失败, {interval}秒后重试第{retries-countdown}/{retries}次, 失败原因:\n%s", traceback.format_exc())
                    time.sleep(interval)
                else:
                    raise
            else:
                return result
    return fn_execution