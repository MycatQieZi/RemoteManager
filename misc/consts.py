from threading import Lock
from misc.enumerators import ThreadLock

LOCKS = {
    ThreadLock.HEARTBEAT: Lock(),
    ThreadLock.VERSION_CHECK: Lock(),
    ThreadLock.GET_TOKEN: Lock(),
    ThreadLock.INSTALL_UPDATE: Lock()
}

