from flask import Blueprint, redirect, url_for, session

theme_controller = Blueprint('theme', __name__)


@theme_controller.route('/set_theme/<string:theme>', methods=['GET'])
def set_theme(theme):
    session['theme'] = theme
    return redirect(url_for('todo.list_todos'))