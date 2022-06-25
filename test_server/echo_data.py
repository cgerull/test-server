"""
echo_data.py

Simple class to organize the content
of an echo request.
"""

class EchoData():
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
        # self.local_data = self.set_local_data()
        self.remote_data = self.set_remote_data(my_request)

    def get_remote_data(self):
        """ Return the class data set."""
        return self.remote_data

    def set_remote_data(self, my_request):
        """ Set class data from http request."""
        # self.remote_data = my_request.headers
        return {
            'remote_addr': self.get_remote_ip(my_request),
            'url': my_request.url,
            'url_charset': my_request.url_charset,
            'referrer': my_request.referrer,
            'user_agent': my_request.user_agent.string,
        }

    @staticmethod
    def get_http_headers(my_request):
        """ Get HTTP headers from request."""
        # self.headers = self.get_remote_data(my_request)
        result = {}
        for header in my_request.headers.envrion:
            if header.startswith('HTTP_'):
                result[header]=my_request.headers.envrion[header]

        return result

    @staticmethod
    def get_remote_ip(my_request):
        """
        Get client ip address, trying to resolve any
        proxies that modify the my_request.
        """
        client_ip = ''
        if 'HTTP_X_REAL_IP' in my_request.environ :
            client_ip = my_request.environ['HTTP_X_REAL_IP']
        elif 'X_REAL_IP' in my_request.environ :
            client_ip = my_request.environ['X_REAL_IP']
        elif 'HTTP_X_FORWARDED_FOR' in my_request.environ :
            client_ip = my_request.environ['HTTP_X_FORWARDED_FOR']
        else:
            client_ip = my_request.remote_addr

        return client_ip
  