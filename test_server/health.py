"""
Check app health endpoint.

"""

from flask import (
    Blueprint
)
from test_server.db import get_db

bp = Blueprint('health', __name__, url_prefix='/')

@bp.route('/health', methods=['GET'])
# @metrics.do_not_track()
def health():
    """Build HTML response data and send page to requester."""
    health_msg = "testserver is healthy."
    status = 200

    err = check_database() or check_redis()

    if err:
        health_msg = err
        status = 500

    return health_msg, status

def check_database():
    '''
    Test if the configured database is accessible and configured.
    '''
    status = ""
    my_db= get_db()
    if my_db is not None:
        try:
            my_cursor = my_db.cursor()
            my_cursor.execute(
                "SELECT * from req_log"
            )
        except my_db.OperationalError as err:
            status = f"ERROR! Can't connect to database. {err}"
    return status

def check_redis():
    '''
    Test if the configured redis is accessible.
    '''
    status = ""

    return status

# Add tests when future features will be developed.
