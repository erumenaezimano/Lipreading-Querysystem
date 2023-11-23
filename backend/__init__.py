import logging
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/Erumena/FlaskLipReading/lipreading.db'
app.config['SECRET_KEY']='9ee95231de5ebcd0f4f1b1ea'
db = SQLAlchemy(app)
ma = Marshmallow()
CORS(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"
migrate = Migrate(app, db)

cors = CORS(app, 
       resources={r"/*": {"origins": "http://localhost:3000"}},
            methods=["GET", "POST"],
            supports_credentials=True)

from lip.routes import search
app.route('/search', methods=['GET'])(search)


if __name__ == '__main__':
    app.run(debug=True)
