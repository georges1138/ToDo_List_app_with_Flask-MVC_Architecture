from flask import render_template, session, request, jsonify
from werkzeug.exceptions import HTTPException


def setup_error_handler(app):

    @app.errorhandler(Exception)
    def handle_exception(e):

        if isinstance(e, HTTPException):
            code = e.code
            description = e.description
        else:
            code = 500
            description = "Something went wrong. Please try again later."

            app.logger.error(
                "Unhandled exception",
                exc_info=(type(e), e, e.__traceback__)
            )

        if request.path.startswith("/api/"):
            return jsonify({
                "error": description
            }), code

        # Existing HTML behavior stays below this point.
        theme = session.get("theme", "light")

        return render_template(
            "error_page.html",
            code=code,
            description=description,
            theme=theme
        ), code
