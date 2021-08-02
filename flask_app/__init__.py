from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'random_string'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://gqnwmdyz:Syo5nPIcWuyuswX_BWPj9F5mhxma--4G@john.db.elephantsql.com/gqnwmdyz'
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL') #posgresql
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite+pysqlite:///SD_Cosmetics.db' #sqlite

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    db.init_app(app)
    migrate.init_app(app, db)

    from flask_app.models import customer, sales
    from flask_app.routes import main_routes, admin_routes
    app.register_blueprint(main_routes.bp)
    app.register_blueprint(admin_routes.admin_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

