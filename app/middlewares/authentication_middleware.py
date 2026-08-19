from flask import session, redirect, url_for, request

def require_login_middleware(app):
    @app.before_request
    def require_login():
        if request.path.startswith("/api/"):
            return

        if request.endpoint is None:
            return

        if request.endpoint not in ['user.auth_page', 'user.register', 'user.login', 'static']:
            if 'user_id' not in session:
                return redirect(url_for('user.auth_page'))
