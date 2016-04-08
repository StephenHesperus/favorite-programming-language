from flask import Blueprint

main = Blueprint('main', __name__)
''':annotation: The main blueprint named ``main``.'''

from . import views
from . import errors
