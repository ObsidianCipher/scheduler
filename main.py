"""
This is the main entry point for the Flask application. It initializes the database, sets up logging, and starts the Flask server.

"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify, request
from dbm import initialize_database 

initialize_database()  # Ensure the database is initialized before the app starts
if not os.path.exists('logs'):
    os.makedirs('logs')
    logging.basicConfig(
        handlers=[RotatingFileHandler('logs/app.log', maxBytes=100000, backupCount=10)],
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

if __name__ == '__main__':
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.urandom(24)  # Use a secure random key for session management
    app.run(debug=True, host='0.0.0.0', port=5000)