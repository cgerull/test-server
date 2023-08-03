"""
status.py

Server system information.
    timestamp,
    uptime,
    platform',
    os-version,

URL: /status
"""

from flask import (
    Blueprint, current_app, render_template, flash, session, redirect, url_for
)
from test_server.local_data import LocalData

bp = Blueprint('status', __name__, url_prefix='/')


@bp.route('/status', methods=['GET'])
# @login_required
def status():
    """Build response data and send page to requester."""
    local_data = LocalData()

    if 'user_id' not in session.keys():
        flash("Not logged on, redirecting to login page.")
        return redirect(url_for("auth.login"))
    else:
        print(f"Statuspage permitted for user {session['user_id']}")

    return render_template('status/status.html',
                server_info=local_data.get_server_info(),
                server_state=local_data.get_server_state(),
                env={
                        'version': current_app.config['VERSION'],
                        'environment': current_app.config['ENV']
                    },
                )
