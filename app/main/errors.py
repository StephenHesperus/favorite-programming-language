from flask import render_template

from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    '''Application 404 error handler.'''
    return render_template('404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    '''Application 500 error handler.'''
    return render_template('500.html'), 500
