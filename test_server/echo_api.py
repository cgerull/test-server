"""
echo_api.py

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

URL: /echo
"""
# from datetime import datetime
# import socket
# import platform

# import json
from flask import (
    Blueprint, current_app, request, jsonify
)
# from flask.helpers import url_for
# from werkzeug.utils import redirect

from test_server.echo_data import EchoData


bp = Blueprint('echo_api', __name__, url_prefix='/')

@bp.route('/v1/echo', methods=['GET'])
def echo_api():
    """Build HTML response data and send page to requester."""
    # local_data = LocalData()
    request_data = EchoData(request)
    # response_data = build_response_data()
    # response_data = echo_data.get_local_data()

    request_fields = request_data.get_remote_data()
    request_headers = request_data.get_http_headers()

    request_info ={
        'fields': request_fields,
        'headers': request_headers,
        'environment': {
                        'version': current_app.config['VERSION'],
                        'environment': current_app.config['ENV']
                    }
    }

    # jsonify(remote_data.get_http_headers())

    return jsonify(request_info)
