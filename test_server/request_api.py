"""
request_api.py

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
from flask import (
    Blueprint, current_app, request, jsonify
)
from test_server.request_data import RequestData

bp = Blueprint('request_api', __name__, url_prefix='/')


@bp.route('/v1/echo', methods=['GET'])
def request_api():
    """Build HTML response data and send page to requester."""
    request_data = RequestData(request)
    request_fields = request_data.get_request_data()
    request_headers = request_data.get_http_headers()

    request_info ={
        'fields': request_fields,
        'headers': request_headers,
        'environment': {
                        'version': current_app.config['VERSION'],
                        'environment': current_app.config['ENV']
                    }
    }

    return jsonify(request_info)
