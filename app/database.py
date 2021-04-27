"""
Database module for test server
"""
from app import app
from flask import (request, jsonify, render_template, redirect,
                   url_for, flash, make_response)
from datetime import datetime
import socket
import os
import yaml
import platform
# import PyMySQL
import mysql.connector

# Modules constants
localhost = socket.gethostname()

#
# HTML page
@app.route('/database', methods=['GET', 'POST'])
def db_view():
    """Build response data and send page to requester."""
    response_data = build_response_data()
    resp = make_response(
        render_template('db.html',
        title=app.config['APP_NAME'],
        footer=app.config['APP_FOOTER'],
        resp=response_data)
        )
    resp.headers['Server-IP'] = socket.gethostbyname(localhost)
    return resp

def build_response_data():
    """
    Build a dictionary with DB data.
    """
    return {
        'Not yet implemented.'
    }

def get_cursor():
    """
    Create DB connection and return a DB cursor. 
    Credentials and parameter are provided by the app.config
    obeject.
    """
    cursor = None
    try:
        with mysql.connector.connect(
            host = app.config['DB_SERVER'],
            user = app.config['DB_USER'],
            password = get_db_secret()
        ) as connection:
            cursor = connection.cursor 
    except Exception as e:
        print(e)
    return cursor
        
def get_db_secret():
    """
    Return secret key from:
        Docker secret file or
        Environment variable SECRET_KEY or
        a default value
    """
    secret = ''
    try:
        f = open(app.config['DB_SECRET_FILE'], 'r')
        secret = f.read()
    except:
        # no file, return configured secret
        secret = app.config['DB_SECRET_KEY']
    return secret


