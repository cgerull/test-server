import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'test_server.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('test_server.cfg', silent=False)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # Modify database name if SQLite is used.
    if ('sqlite' == app.config['DB_TYPE']):
        app.config['DATABASE'] = os.path.join(app.instance_path, app.config['DATABASE'] + '.sqlite')

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that gives the health status
    @app.route('/health')
    def health():
        return "{} is healthy.".format(__name__)

    from . import db
    db.init_app(app)

    from . import echo
    app.register_blueprint(echo.bp)
    app.add_url_rule('/', endpoint='index')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import status
    app.register_blueprint(status.bp)
    # app.add_url_rule('/', endpoint='index')

    return app