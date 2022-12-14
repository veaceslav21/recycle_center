from flask import Flask
from flask_restful import Api
from flask_jwt import JWT


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recycle.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)

jwt = JWT(app, authentication, identity)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
