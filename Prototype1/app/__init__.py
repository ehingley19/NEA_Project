# Code taken from Grinberg, M (2023) 'The New and Improved Flask Mega-Tutorial (2024 Edition)', p. 11
# Creating an 'app' object as an instance of the class Flask
from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app import routes
