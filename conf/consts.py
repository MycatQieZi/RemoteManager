import logging
from enum import Enum

class Envs(Enum):
    DEV = 'dev'
    SIT = 'sit'
    UAT = 'uat'
    YMT = 'ymt'
    PROD = 'prod'

CONFIG = {
    Envs.DEV:{
        "host_addr": "http://localhost:8888",
        "api_prefix": "/v1/api/box",
        "logging": logging.DEBUG
    },
    Envs.SIT:{
        "host_addr":"",
        "api_prefix": "/v1/api/box",
        "logging": logging.DEBUG
    },
    Envs.UAT:{
        "host_addr":"",
        "api_prefix": "/v1/api/box",
        "logging": logging.DEBUG
    },
    Envs.YMT:{
        "host_addr":"",
        "api_prefix": "/v1/api/box",
        "logging": logging.DEBUG
    },
    Envs.PROD:{
        "host_addr":"",
        "api_prefix": "/v1/api/box",
        "logging": logging.INFO
    }

}

