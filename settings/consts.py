DEFAULT_FILE_TEMPLATE = \
"""\
[general]
env=prod
logging=info

[paths]
config=\conf\configuration.ini
patch=\patch
patchmeta=\patch.meta
backup=\\backup

fs=‪C:\Program Files\FreeSWITCH
fs_conf=\\conf\\sip_profiles\\external\\
java=
jar=
data=\data

[timer]
heartbeat=300
versionCheck=14400
"""
