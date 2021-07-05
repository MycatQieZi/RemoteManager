DEFAULT_FILE_TEMPLATE = \
"""\
[general]
env=prod
logging=info
log_expiration=30

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
heartbeat=300
versionCheck=14400
"""
