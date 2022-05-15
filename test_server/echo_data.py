"""
api.py

Simple echo response to requester.
Returns simple system information.
    timestamp,
    platform',
    system,
    processor,
    architecture,
    local_ip
    container_name,
    secret,
    remote_ip

URL: /api/v1/echo
"""
# from datetime import datetime
# import socket
# import platform

# from flask import (
#     current_app, request
# )
# from flask.helpers import url_for

# from werkzeug.utils import redirect


class EchoData():

    remote_data = {}
    local_data = {}
    headers = {}

    def __init__(self, my_request):
        # self.local_data = self.set_local_data()
        self.remote_data = self.set_remote_data(my_request)


    # def set_local_data(self):
    #     """
    #     Build a dictionary with timestamp, server ip,
    #     server name, secret and requester ip.
    #     """
    #     hostname = socket.gethostname()

    #     return {
    #         'now': datetime.now().isoformat(sep=' '),
    #         'platform': platform.platform(),
    #         'system': platform.system(),
    #         'processor': platform.processor(),
    #         'architecture': ' '.join(map(str,platform.architecture())),
    #         'local_ip': socket.gethostbyname(hostname),
    #         'container_name': hostname,
    #         # 'secret': get_secret_key(),
    #         # 'remote_ip': get_remote_ip(),
    #         # 'version': current_app.config['VERSION'],
    #         # 'environment': current_app.config['ENV']
    #     }


    # def get_local_data(self):
    #     return self.local_data

    
    def get_remote_data(self):
        return self.remote_data


    def set_remote_data(self, my_request): 
        # self.remote_data = my_request.headers
        return {
            'remote_addr': self.get_remote_ip(my_request),
            'url': my_request.url,
            'url_charset': my_request.url_charset,
            'referrer': my_request.referrer,
            'user_agent': my_request.user_agent
        }
        

    def get_http_headers(self, my_request): 
        # self.headers = self.get_remote_data(my_request)
        result = {}
        for header in my_request.headers.envrion:
            if header.startswith('HTTP_'):
                result[header]=my_request.headers.envrion[header]

        return result
        

    def get_remote_ip(self, my_request):
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


    # def get_secret_key(self):
    #     """
    #     Return secret key from:
    #         Docker secret file or
    #         Environment variable SECRET_KEY or
    #         a default value
    #     """
    #     secret = ''
    #     if current_app.config['SECRET_FILE'] is not None:
    #         try:
    #             with open(current_app.config['SECRET_FILE'], mode = 'r', encoding = 'utf_8') as file:
    #                 secret = file.read()
    #         except IOError:
    #             # no file, return configured secret
    #             secret = current_app.config['SECRET_KEY']
    #     else:
    #         secret = current_app.config['SECRET_KEY']
    #     return secret   
