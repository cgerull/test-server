"""
Init testserver application.
"""
import datetime
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from prometheus_client import multiprocess
from prometheus_client.core import CollectorRegistry
from prometheus_flask_exporter import PrometheusMetrics


# pylint: disable=C0415
def create_app(test_config=None):
    """
    Create and configure the Flask application.

    Arguments:
      test_config - Configuration mapping, default is none

    Returns:
      a Flask application object
    """
    print(
        f"INFO!Flask app {__name__} started by PID {os.getpid()}."
    )
    app = Flask(__name__, instance_relative_config=False)

    # Initialize Prometheus metrics
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry, path='/tmp')
    metrics = PrometheusMetrics(app, registry=registry)

    # Set / load app configuration
    app.config.from_mapping(
        VERSION='0.9.0',
        ENV='Intern',
        SECRET_KEY='dev',
        DB_TYPE=None,
        REDIS_SERVER=None,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('test_server.cfg', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    metrics.info(
        'testserver_info',
        'Testserver info',
        version=app.config['VERSION'],
        environment=app.config['ENV'])


    # Modify database name if SQLite is used.
    if 'sqlite' == app.config['DB_TYPE']:
        # Prevent duplicate initialization.
        if None is app.config.get('DATABASE'):
            if app.config['DB_PATH'] is None:
                app.config['DB_PATH'] = app.instance_path
            if app.config['DB_NAME'] is None:
                app.config['DB_NAME'] = app.name
            app.config['DATABASE'] = os.path.join(
                    app.config['DB_PATH'],
                    app.config['DB_NAME'] + '.sqlite')
            print(
                f"INFO! Setting database {app.config['DATABASE']} ."
                )

            # ensure the instance folder exists
            try:
                os.makedirs(app.config['DB_PATH'])
                print(f"INFO! Creating SQLite Path {app.config['DB_PATH']} .")
            except FileExistsError:
                print(
                    f"WARNING! SQLite Path {app.config['DB_PATH']} already exists, reusing."
                    )



    # # A simple page that gives the health status
    # @app.route('/health')
    # @metrics.do_not_track()
    # def health():
    #     return f"{__name__} is healthy."


    # If not None, initialize database
    if app.config['SQLALCHEMY_DATABASE_URI']:
        db = SQLAlchemy(app)
        migrate = Migrate(app, db)

    # if app.config['DB_TYPE']:
    #     from . import db_pg
    #     db_pg.init_app(app)

    # Health check and status page
    from . import health
    app.register_blueprint(health.bp)


    # Echo page returns the call with some additional information
    from . import echo
    app.register_blueprint(echo.bp)
    app.add_url_rule('/', endpoint='index')

    # Default authentication endpoint, uses Database to store account
    # information.
    from . import auth
    app.register_blueprint(auth.bp)

    # User management endpoint, uses Database to store account
    # information.
    # from . import user_mgmnt
    # app.register_blueprint(user_mgmnt.bp)

    # Print a status page
    from . import status
    app.register_blueprint(status.bp)
    # app.add_url_rule('/status/', endpoint='index')

    #
    # API urls
    #
    # Echo api returns the call with some additional information
    from . import request_api
    app.register_blueprint(request_api.bp)

    # SQL shit
    class RequestLogs(db.Model):
        __tablename__ = 'req_logs'
        id = db.Column(db.Integer, primary_key=True)
        response_code = db.Column(db.Integer, nullable=False)
        request_url = db.Column(db.String(80), nullable=True)
        request_from_ip = db.Column(db.String(20),nullable=True)
        created = db.Column(db.DateTime, default=datetime.datetime.utcnow)


        def __init__(self, response_code, request_url, request_from_ip):
            self.response_code = response_code
            self.request_url = request_url
            self.request_from_ip = request_from_ip


        def __repr__(self):
            return f'<Response {self.response_code}>'



    return app
