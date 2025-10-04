# Code taken from Grinberg, M (2023) 'The New and Improved Flask Mega-Tutorial (2024 Edition)', p. 11
# Creating an 'app' object as an instance of the class Flask
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models
