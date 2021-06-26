import logging
from misc.enumerators import Envs

CONFIG = {
    Envs.LOCAL.value:{
        "host_addr": "http://192.168.63.47:8888",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.DEV.value:{
        "host_addr": "http://11.8.39.197:18096",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.SIT.value:{
        "host_addr":"",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.UAT.value:{
        "host_addr":"http://www.tongtongcf.com:12001",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.YMT.value:{
        "host_addr":"",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.DEBUG
    },
    Envs.PROD.value:{
        "host_addr":"",
        "api_prefix": "/v1/api/center818/box",
        "logging": logging.INFO
    }

}

REMOTE_CONF_MAPPING = {
    "callboxPassword": ('FreeSWITCH', 'callboxPassword'),
    "numconvertRealm": ('FreeSWITCH', 'numconvertRealm'),
    "callboxRealm": ('FreeSWITCH', 'callboxRealm'),
    "numconvertUsername": ('FreeSWITCH', 'numconvertUsername'),
    "outnum": ('city', 'out'),
    "citynum": ('city', 'num'),
    "callboxUsername": ('FreeSWITCH', 'callboxUsername'),
    "numconvertPassword": ('FreeSWITCH', 'numconvertPassword'),
    "hostAdr": ('host', 'adr'),
    "dbfileName": ('dbfile', 'name')
}

