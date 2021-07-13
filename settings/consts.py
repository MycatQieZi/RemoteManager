DEFAULT_FILE_TEMPLATE = \
"""\
[general]
host_addr=https://finear.ect888.com:6680
env=prod
logging=info
log_expiration=30
debug_mode=off

[paths]
config=\conf\configuration.ini
patch=\patch
patchmeta=\patch.meta
backup=\\backup

fs=C:\\Program Files\\FreeSWITCH
fs_conf=\\conf\\sip_profiles\\external\\
java=C:\\Program Files\\java
java_pid=\\pid.txt
jar=\\icb-box.jar
app_yml=\\application.yml
path_bat=\\DOS\\start.bat
data=\data

[timer]
heartbeat=30
versionCheck=3600
"""
