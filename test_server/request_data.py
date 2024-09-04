"""
echo_data.py

Simple class to organize the content
of an echo request.
"""

class RequestData(): # TODO: refactor to RequestData
    """
        Retrieve from request
            'remote_addr'
            'url'
            'url_charset'
            'referrer'
            'user_agent'
    """
    remote_data = {}
    local_data = {}
    headers = {}

    def __init__(self, my_request):
        # self.remote_data = self.set_remote_data(my_request)
        self.request = my_request

    def get_remote_data(self):
        """ Return the class data set."""
        return {
            'RemoteAddr': self.get_remote_ip(),
            'URL': self.request.url,
            # 'Charset': self.request.charset,
            'Cookies': self.request.cookies,
            'Method': f"{self.request.environ['REQUEST_METHOD']} {self.request.environ['SERVER_PROTOCOL']}",
            'QueryString': self.request.environ['QUERY_STRING'],
            'Referrer': self.request.referrer,
            'UserAgent': self.request.user_agent.string,
        }

    # def set_remote_data(self, my_request):
    #     """ Set class data from http request."""
    #     return {
    #         'remote_addr': self.get_remote_ip(my_request),
    #         'url': my_request.url,
    #         'url_charset': my_request.charset,
    #         'accept_encodings': my_request.accept_encodings,
    #         'accept_languages': my_request.accept_languages,
    #         'accept_mimetypes': my_request.accept_mimetypes,
    #         'referrer': my_request.referrer,
    #         'user_agent': my_request.user_agent.string,
    #     }

    # @staticmethod
    def get_http_headers(self):
        """ Get HTTP headers from request."""
        result = {}
        for header in self.request.headers.environ:
            if header.startswith('HTTP_'):
                result[header]=self.request.headers.environ[header]

        return result

    # @staticmethod
    def get_remote_ip(self):
        """
        Get client ip address, trying to resolve any
        proxies that modify the request.
        """
        client_ip = ''
        if 'HTTP_X_REAL_IP' in self.request.environ :
            client_ip = self.request.environ['HTTP_X_REAL_IP']
        elif 'X_REAL_IP' in self.request.environ :
            client_ip = self.request.environ['X_REAL_IP']
        elif 'HTTP_X_FORWARDED_FOR' in self.request.environ :
            client_ip = self.request.environ['HTTP_X_FORWARDED_FOR']
        else:
            client_ip = self.request.remote_addr

        return client_ip
