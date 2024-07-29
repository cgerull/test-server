"""
Check app health endpoint.

"""

from flask import (
    Blueprint, current_app
)
from test_server.db import check_database
from test_server.persistent_counter import check_redis
from test_server.persistent_counter import get_redis_connection

bp = Blueprint('health', __name__, url_prefix='/')

@bp.route('/health', methods=['GET'])
# @metrics.do_not_track()
def health():
    """Build HTML response data and send page to requester."""
    health_msg = "testserver is healthy."
    status = 200

    db_check = check_database()
    redis_check = None


    if current_app.config['REDIS_SERVER'] is not None:
        redis_connection = get_redis_connection(
            current_app.config['REDIS_SERVER'],
            current_app.config['REDIS_PORT'],
            current_app.config['REDIS_PASSWORD'],
            )
        redis_check = check_redis(redis_connection)


    if redis_check:
        if not redis_check['pass']:
            health_msg = f"(Redis: {redis_check['msg']})"
            status = 500

    if db_check:
        if not db_check['pass']:
            health_msg = f"(DB: {db_check['msg']})"
            status = 500

    return health_msg, status
