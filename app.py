# app.py
import os
import secrets
from flask import Flask
from routes.task_routes import task_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY') or secrets.token_hex(32)
app.register_blueprint(task_bp)

if __name__ == '__main__':
    app.run(debug=True)