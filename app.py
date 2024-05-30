from flask import Flask
from services.db import db
from flask_migrate import Migrate
from services.marshmello import mm
import routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/parentune'
db.init_app(app)
migrate = Migrate(app, db)
mm.init_app(app)

app.register_blueprint(routes.child, url_prefix='/child')
app.register_blueprint(routes.parent, url_prefix='/parent')
app.register_blueprint(routes.blog, url_prefix='/blog')
app.register_blueprint(routes.feed, url_prefix='/feed')

if __name__ == '__main__':
    app.run(debug=True)