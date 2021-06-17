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
    ENV = 'env'
    LOGGING = 'logging'
    CONFIG = 'config'
    FS = 'fs'
    JAVA = 'java'
    JAR = 'jar'
    HB = 'heartbeat'
    VC = 'versionCheck'