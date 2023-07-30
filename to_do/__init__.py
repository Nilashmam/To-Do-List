import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_caching import Cache

SECRET_KEY = "some secret"

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

cache = Cache(config={"CACHE_TYPE":"RedisCache","CACHE_REDIS_HOST":"0.0.0.0","CACHE_REDIS_PORT":6379})
cache.init_app(app)
   

from to_do.api.views import todo
app.register_blueprint(todo)


with app.app_context():
 db.create_all()


login_manager = LoginManager()
login_manager.init_app(app)

from to_do.api.models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
    
