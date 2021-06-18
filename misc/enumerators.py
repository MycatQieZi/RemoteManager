from enum import Enum

class Envs(Enum):
    LOCAL = 'local'
    DEV = 'dev'
    SIT = 'sit'
    UAT = 'uat'
    YMT = 'ymt'
    PROD = 'prod'

class FilePath(Enum):
    CONFIG = "ini"
    FS = 'fs'
    JAVA = 'java'
    JAR = 'jar'

class SettingsCategories(Enum):
    GENERAL = 'general'
    PATHS = 'paths'
    TIMER = 'timer'

class SettingsItems(Enum):
    # general
    ENV = 'env'
    LOGGING = 'logging'

    # paths
    CONFIG = 'config'
    PATCH = 'patch'
    PATCHMETA = 'patchmeta'
    FS = 'fs'
    JAVA = 'java'
    JAR = 'jar'

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

class PatchCyclePhase(Enum):
    READY = 0
    INCEPTION = 1
    DOWNLOAD = 2
    PENDING = 3
    INSTALLATION = 4
    ROLLBACK = 5

class PatchStatus(Enum):
    PENDING = 0
    DOWNLOADING = 1
    DOWNLOADED = 2
    INSTALLED = 3
    REVERTED = 4