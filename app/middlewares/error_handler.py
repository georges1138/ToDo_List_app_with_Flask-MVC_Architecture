from flask import render_template
from werkzeug.exceptions import HTTPException

def setup_error_handler(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Determine the error code
        code = e.code if isinstance(e, HTTPException) else 500
        # Render the custom error page with the error code and description
        return render_template("error_page.html", code=code, description=str(e)), code
