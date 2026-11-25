"""
This is the main entry point for the Flask application. It initializes the database, sets up logging, and starts the Flask server.

"""
import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask

from db_manager import initialize_database

os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    handlers=[RotatingFileHandler('logs/app.log', maxBytes=100000, backupCount=10)],
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

initialize_database()  # Ensure the database is initialized before the app starts

app = Flask(__name__)
# Set SECRET_KEY in the environment so sessions survive restarts.
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or os.urandom(24)

if __name__ == '__main__':
    # Debug mode exposes an interactive debugger, so it is opt-in and local-only.
    debug = os.environ.get('FLASK_DEBUG') == '1'
    app.run(debug=debug, host='127.0.0.1' if debug else '0.0.0.0', port=5000)
