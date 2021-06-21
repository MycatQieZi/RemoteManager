# static decorators

# make a certain class singleton, as name suggests
def singleton(cls, *args, **kwargs):
    instances = {}
    def _wrapper(**kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return _wrapper
