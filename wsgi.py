""" Wsgi definition for Flask application."""
import sys
PROJECT_HOME = u'/home/web/test_server'
if PROJECT_HOME not in sys.path:
    sys.path = [PROJECT_HOME] + sys.path

from test_server import create_app
app = create_app()

if __name__ == "__main__":
    app.run()
    