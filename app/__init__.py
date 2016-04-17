from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bootstrap import Bootstrap

from config import config


db = SQLAlchemy()
bootstrap = Bootstrap()


def create_app(config_name):
    '''
    Return a Flask application instance given the configuration name.

    :param str config_name: The name of the configuration, ``'development'``,
                            ``'testing'``, ``'production'``, or ``'default'``
                            which is ``'development'``
    :return: A Flask application instance
    :rtype: ``Flask``
    '''
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    bootstrap.init_app(app)

    # Attach routes and custom error pages here
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
