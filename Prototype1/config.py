# Code based on Grinberg, M (2023) 'The New and Improved Flask Mega-Tutorial (2024 Edition)', p. 28
import os

# Creating a class Config, in which configuration settings are defined as class variables
class Config:
    # Defining SECRET_KEY, an important variable whose value is used by Flask and some Flask extensions as
    # a cryptographic key used to prevent CSRF attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
