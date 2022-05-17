# -*- coding: utf-8 -*-
"""
Created on Mon May 16 22:54:21 2022

@author: sameed.atta
"""

from os import environ, path
from decouple import config

try:
    basedir = path.abspath(path.dirname(__file__))
except:
    pass

TEMP_ENV = config('ENV')


class Config:
    """Base config."""
    pass
    
    DATABASE_NAME = "travel_db"



class DevConfig(Config):
    ENV = 'development'
    DEBUG = True
    TESTING = True
    MARIADB_HOST = config('MARIADB_HOST')
    MARIADB_PORT = config('MARIADB_PORT')
    MARIADB_USER = config('MARIADB_USER')
    MARIADB_PASSWORD = config("MARIADB_PASSWORD")
    
    

    
class TestConfig(Config):
    ENV = 'testing'
    DEBUG = False
    TESTING = False
    MARIADB_HOST = config('MARIADB_DOCKER_HOST', cast=str)
    MARIADB_PORT = config('MARIADB_DOCKER_PORT', cast=int)
    MARIADB_USER = config('MARIADB_USER', cast=str)
    MARIADB_PASSWORD = config("MARIADB_PASSWORD", cast=str)
    
    
    
    

class ProdConfig(Config):
    ENV = 'production'
    DEBUG = False
    TESTING = False


def get_env():
    if TEMP_ENV == 'development':
        app_config = DevConfig()
        return app_config
    if TEMP_ENV == 'testing':
        app_config = TestConfig()
        return app_config
    if TEMP_ENV == 'production':
        app_config = ProdConfig()
        return app_config
    