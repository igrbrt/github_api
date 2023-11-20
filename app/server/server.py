from flask import Flask
from ..routes.routes import routes
from ..extensions import database
from apscheduler.schedulers.background import BackgroundScheduler
from ..services.userService import update_users

class Server():
  def __init__(self,config_object):
    self.app = Flask(__name__)
    self.app.config.from_pyfile(config_object)
    self.app.register_blueprint(routes)
    database.init_app(self.app)

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(update_users,'interval',hours=24)
    scheduler.start()

server = Server("settings.py")