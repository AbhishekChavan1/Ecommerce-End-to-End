"""Shop Blueprint initialization."""
from flask import Blueprint

shop_bp = Blueprint('shop', __name__, template_folder='../templates/shop')

from . import routes, forms