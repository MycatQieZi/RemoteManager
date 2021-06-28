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
        "host_addr":"http://112.65.144.19:12001",
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

XMLS = [
	"callbox.xml",
	"numconvert.xml"
]

FS_CONF = {
	"callbox":{
		"username": {
			'name':'模拟分机号', 'value':''
		},
		"realm" : {
			'name':'盒子IP地址', 'value':''
		},
		"password" : {
			'name':'盒子线路密码', 'value':''
		}
	},
	"numconvert": {
		"username" : {
			'name':'线路名称', 'value':''
		},
		"realm" : {
			'name':'SIP远程地址', 'value':''
		},
		"password" : {
			'name':'模型线路密码', 'value':''
		}
	}
}

FS_CONF_MAPPING = {
    "callboxpassword": ('callbox', 'password'),
    "numconvertrealm": ('numconvert', 'realm'),
    "callboxrealm": ('callbox', 'realm'),
    "numconvertusername": ('numconvert', 'username'),
    "callboxusername": ('callbox', 'username'),
    "numconvertpassword": ('numconvert', 'password'),
}

