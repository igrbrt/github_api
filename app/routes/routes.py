from flask import Blueprint
from ..controllers.userController import get
from ..controllers.homeController import home

routes = Blueprint('routes', __name__)

routes.route('/', methods=['GET'])(home)
routes.route('/', methods=['POST'])(get)