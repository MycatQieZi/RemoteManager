from enum import Enum
from functools import total_ordering

class Envs(Enum):
    LOCAL = 'local'
    DEV = 'dev'
    SIT = 'sit'
    UAT = 'uat'
    YMT = 'ymt'
    PROD = 'prod'

class FilePath(Enum):
    CONFIG = "config"
    FS = 'fs'
    FS_CONF = 'fs_conf'
    JAVA = 'java'
    JAR = 'jar'
    JAVA_PID = 'java_pid'
    PATH_BAT = 'path_bat'
    APP_YML = "app_yml"

class SettingsCategories(Enum):
    GENERAL = 'general'
    PATHS = 'paths'
    TIMER = 'timer'

class SettingsItems(Enum):
    # general
    HOST_ADDR='host_addr'
    ENV = 'env'
    LOGGING = 'logging'
    LOG_EXP = 'log_expiration'

    # paths
    CONFIG = 'config'
    PATCH = 'patch'
    PATCHMETA = 'patchmeta'
    FS = 'fs'
    FS_CONF = 'fs_conf'
    JAVA = 'java'
    JAVA_PID = 'java_pid'
    JAR = 'jar'
    PATH_BAT = 'path_bat'
    APP_YML = 'app_yml'

    # timer
    HB = 'heartbeat'
    VC = 'versionCheck'

class UpgradeMark(Enum):
    OPTIONAL = 1
    MANDATORY = 2

class VersionInfo(Enum):
    VCODE = 'versionCode'
    VNUM = 'versionNum'
    MD5 = 'fileMd5'
    REMARK = 'remark'
    STAT = 'status'
    CONFMAP = 'argumentConfigMap'

class FS_Status(Enum):
    OTHER = -1
    FAIL_WAIT = 0
    REGED = 1
    NO_REG = 2

@total_ordering
class PatchCyclePhase(Enum):
    READY = 0
    INCEPTION = 1
    DOWNLOAD = 2
    PENDING = 3
    PREPPED = 4
    COMPLETE = 5
    ROLLEDBACK = 6
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

class PatchStatus(Enum):
    PENDING = 0
    DOWNLOADING = 1
    DOWNLOADED = 2
    INSTALLED = 3
    REVERTED = 4