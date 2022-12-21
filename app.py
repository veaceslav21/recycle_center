from flask import Flask
from db import db
import environ


env = environ.Env()
# reading .env file
environ.Env.read_env()


def create_app():
    app = Flask(__name__)
    app.secret_key = env("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///recycle.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    from db import db
    db.init_app(app)

    from users.views import user_bp
    from centers.views import center_bp
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(center_bp, url_prefix='/center')

    return app



if __name__ == "__main__":
    app = create_app()

    @app.before_first_request
    def create_tables():
        db.create_all()


    app.run(port=5000, debug=True)

