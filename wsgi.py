""" Wsgi definition for Flask application."""
import sys
project_home = u'/home/web/test_server'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

from test_server import create_app
app = create_app()

if __name__ == "__main__":
    app.run()