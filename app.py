from flask import Flask
from flask_restful import Api
from db import db
from users.views import LoginUser, SignUpUser, ResetPassword
from centers.views import CenterResource
import environ


env = environ.Env()
# reading .env file
environ.Env.read_env()

app = Flask(__name__)
app.secret_key = env("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recycle.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(SignUpUser, "/user/register")
api.add_resource(LoginUser, "/user/login")
api.add_resource(ResetPassword, "/user/reset_password")
api.add_resource(CenterResource, "")


if __name__ == "__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)
