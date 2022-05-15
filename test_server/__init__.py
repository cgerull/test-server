import os

from flask import Flask
from prometheus_client import multiprocess
from prometheus_client.core import CollectorRegistry
from prometheus_flask_exporter import PrometheusMetrics

def create_app(test_config=None):
    """ 
    Create and configure the Flask application.

    Arguments:
      test_config - Configuration mapping, default is none

    Returns:
      a Flask application object
    """

    app = Flask(__name__, instance_relative_config=False)
    
    # Initialize Prometheus metrics
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry, path='/tmp')
    metrics = PrometheusMetrics(app, registry=registry) 

    # Set / load app configuration
    app.config.from_mapping(
        VERSION='0.1.0',
        ENV='Intern',
        SECRET_KEY='dev',
        DB_TYPE=None,
        DB_PATH=None,
        DB_NAME=None,
        DATABASE=os.path.join(app.instance_path, 'test_server.sqlite'),
        REDIS_SERVER=None,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('test_server.cfg', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # metrics.info('testserver_info', 'Testserver info', version=app.config['VERSION'], environment=app.config['ENV'])


    # Modify database name if SQLite is used.
    if ('sqlite' == app.config['DB_TYPE']):
        if app.config['DB_PATH'] is None : app.config['DB_PATH'] = app.instance_path
        app.config['DATABASE'] = os.path.join(app.config['DB_PATH'], app.config['DB_NAME'] + '.sqlite')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # A simple page that gives the health status
    @app.route('/health')
    @metrics.do_not_track()
    def health():
        return "{} is healthy.".format(__name__)


    # If not None, initialize database
    if app.config['DB_TYPE']:
        from . import db
        db.init_app(app)

    # Echo page returns the call with some additional information
    from . import echo
    app.register_blueprint(echo.bp)
    app.add_url_rule('/', endpoint='index')

    # Default authentication endpoint, uses Database to store account
    # information.
    from . import auth
    app.register_blueprint(auth.bp)

    # Print a status page
    from . import status
    app.register_blueprint(status.bp)
    # app.add_url_rule('/status/', endpoint='index')

    return app
