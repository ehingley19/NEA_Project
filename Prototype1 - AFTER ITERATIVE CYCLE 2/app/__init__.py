# Code taken from Grinberg, M (2023) 'The New and Improved Flask Mega-Tutorial (2024 Edition)', p. 11
# Creating an 'app' object as an instance of the class Flask
from flask import Flask
app = Flask(__name__)
from app import routes
