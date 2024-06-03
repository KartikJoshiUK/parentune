from flask import Flask, request, redirect, url_for, session
from services.db import db
from flask_migrate import Migrate
from services.marshmello import mm
import routes
import threading
from routes.blogRouter import notification_worker



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/parentune'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'kartik_secret'
db.init_app(app)
migrate = Migrate(app, db)
mm.init_app(app)
context = app.app_context()

def start_worker():
    threading.Thread(target=notification_worker, args=(app,), daemon=True).start()
start_worker()

app.register_blueprint(routes.auth, url_prefix='/auth')
app.register_blueprint(routes.user, url_prefix='/user')
app.register_blueprint(routes.notification, url_prefix='/notification')
app.register_blueprint(routes.child, url_prefix='/child')
app.register_blueprint(routes.parent, url_prefix='/parent')
app.register_blueprint(routes.blog, url_prefix='/blog')
app.register_blueprint(routes.feed, url_prefix='/feed')

if __name__ == '__main__':
    app.run(debug=True)
