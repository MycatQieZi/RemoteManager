from misc.enumerators import VersionInfo, PatchStatus

class PatchObject(object):
    def __init__(self, version_data):
        self.version_code = version_data[VersionInfo.VCODE.value]
        self.version_num = version_data[VersionInfo.VNUM.value]
        self.file_MD5 = version_data[VersionInfo.MD5.value]
        self.remark = version_data[VersionInfo.REMARK.value]
        self.status = PatchStatus.PENDING

    def set_status(self, new_status):
        self.status = new_status
    
    