class HttpRequestError(Exception):
    def __init__(self, request, message="Error occurred sending http request"):
        self.request = request
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: status_code={self.request.status_code}, url={self.request.url}'

class NotFoundError(Exception):
    pass

class ICBRequestError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'请求接口业务异常: {self.message}'

class FileDownloadError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'文件下载异常异常: {self.message}'

class NoFileError(Exception):
    pass

class UpdateIsNoGo(Exception):
    def __init__(self, message, stack_trace=""):
        self.message = message
        self.stack_trace = stack_trace
        super().__init__(self.message)

    def __str__(self):
        return f'更新被阻止, 原因: {self.message}, 报错信息: {self.stack_trace}'

    def cause(self):
        return f'更新被阻止, 原因: {self.message}'

    def trace(self):
        return f'报错信息: {self.stack_trace}'
