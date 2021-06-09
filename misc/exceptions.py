

class HttpRequestError(Exception):
    def __init__(self, request, message="Error occurred sending http request"):
        self.request = request
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}: status_code={self.request.status_code}, url={self.request.url}'


class ICBRequestError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'请求接口业务异常: {self.message}'
