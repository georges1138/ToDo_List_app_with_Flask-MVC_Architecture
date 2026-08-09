from flask import Flask
from controllers.todo_controller import todo_controller
from controllers.theme_controller import theme_controller
from controllers.user_controller import user_controller
from middlewares.error_handler import setup_error_handler
from middlewares.authentication_middleware import require_login_middleware
from models import db
from config import Config


def create_app(test_config=None):
    app = Flask(__name__)

    # Load config
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    # Verify secret is set
    if not app.config.get("SECRET_KEY"):
        raise RuntimeError(
            "SECRET_KEY environment variable is required"
        )

    # Initialize the database
    db.init_app(app)

    # Setup error handler middleware
    setup_error_handler(app)

    # Setup authentication middleware
    require_login_middleware(app)

    # Register blueprints
    app.register_blueprint(todo_controller)
    app.register_blueprint(user_controller)
    app.register_blueprint(theme_controller)

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(
        host='0.0.0.0',
        port=3000
    )
