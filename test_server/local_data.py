"""
server_info.py

Class for local system information.
Returns a dictonary.

    - get_server_info


    timestamp,
    platform',
    system,
    processor,
    architecture,
    local_ip
    hostname,


"""
from datetime import datetime
import socket
import platform
import os
from flask import (
    current_app
)

class LocalData():

    server_info = {}
    server_state = {}

    def __init__(self):
        self.local_data = self.set_local_data()
        self.server_info = self.set_server_info()
        self.server_state = self.set_server_state()


    def set_server_info(self):
        """
        Build a dictionary with timestamp, server ip,
        server name, secret and requester ip.
        """
        hostname = socket.gethostname()

        return {
            # 'Server time': datetime.now().isoformat(sep=' '),
            'Platform': platform.platform(),
            'System name': platform.system(),
            'Processor': platform.processor(),
            'Architecture': ' '.join(map(str,platform.architecture())),
            # 'Server IP': socket.gethostbyname(hostname),
            'Hostname': hostname,
        }


    def set_server_state(self):
        """
        Build a dictionary with timestamp, server ip
        and load average
        """
        hostname = socket.gethostname()

        return {
            'Server time': datetime.now().isoformat(sep=' '),
            'Server IP': socket.gethostbyname(hostname),
            'CPU load average': os.system("uptime | cut -f 4 -d ,"),
            'Server uptime': os.system("uptime | cut -f 4,5 -d ,"),
        }


    def get_server_info(self):
        """ 
        Return server_info dictonary.
        """
        return self.server_info


    def get_server_state(self):
        """ 
        Return server_state dictonary.
        """
        return self.server_state


    def get_uptime(self):
        """
        Get and trim server uptime.
        """
        uptime = os.system("uptime")
        # TODO Beautify data
        return uptime.s


    def get_secret_key(self):
        """
        Return secret key from:
            Docker secret file or
            Environment variable SECRET_KEY or
            a default value
        """
        secret = ''
        if current_app.config['SECRET_FILE'] is not None:
            try:
                with open(current_app.config['SECRET_FILE'], mode = 'r', encoding = 'utf_8') as file:
                    secret = file.read()
            except IOError:
                # no file, return configured secret
                secret = current_app.config['SECRET_KEY']
        else:
            secret = current_app.config['SECRET_KEY']
        return secret  


    def set_local_data(self):
        """
        Build a dictionary with timestamp, server ip,
        server name, secret and requester ip.
        """
        hostname = socket.gethostname()

        return {
            'now': datetime.now().isoformat(sep=' '),
            'platform': platform.platform(),
            'system': platform.system(),
            'processor': platform.processor(),
            'architecture': ' '.join(map(str,platform.architecture())),
            'local_ip': socket.gethostbyname(hostname),
            'container_name': hostname,
            'secret': self.get_secret_key(),
            # 'remote_ip': get_remote_ip(),
            # 'version': current_app.config['VERSION'],
            # 'environment': current_app.config['ENV']
        }