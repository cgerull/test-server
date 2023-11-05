"""
Check app health endpoint.

"""

from flask import (
    Blueprint, current_app
)
from test_server.db import check_database
from test_server.persistent_counter import check_redis

bp = Blueprint('health', __name__, url_prefix='/')

@bp.route('/health', methods=['GET'])
# @metrics.do_not_track()
def health():
    """Build HTML response data and send page to requester."""
    health_msg = "testserver is healthy."
    status = 200

    db_err = check_database()
    redis_err = check_redis(current_app.config['REDIS_SERVER'])

    if not db_err['pass'] or not redis_err['pass']:
        health_msg = f"(DB: {db_err['msg']}; Redis: {redis_err['msg']})"
        status = 500

    return health_msg, status
