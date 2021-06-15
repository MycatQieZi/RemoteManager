import logging
from enum import Enum

class Envs(Enum):
    LOCAL = 'local'
    DEV = 'dev'
    SIT = 'sit'
    UAT = 'uat'
    YMT = 'ymt'
    PROD = 'prod'

CONFIG = {
    Envs.LOCAL:{
        "host_addr": "http://192.168.63.47:8888",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.DEV:{
        "host_addr": "http://11.8.39.197:18096",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.SIT:{
        "host_addr":"",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.UAT:{
        "host_addr":"",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.YMT:{
        "host_addr":"",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.PROD:{
        "host_addr":"",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.INFO
    }

}

