from flask import Blueprint, render_template, request, redirect, url_for, session
from services.todo_service import TodoService


todo_service = TodoService()

todo_controller = Blueprint('todo', __name__)


@todo_controller.route('/', methods=['GET'])
def list_todos():
    user_id = session['user_id']

    sort_by = request.args.get('sort_by')
    filter_by = request.args.get('filter_by')

    todos = todo_service.get_all(
        user_id,
        sort_by=sort_by,
        filter_by=filter_by
    )

    if not todos:
        todos = []

    theme = session.get('theme', 'light')

    return render_template(
        'todo_list.html',
        todos=todos,
        theme=theme
    )


@todo_controller.route('/add', methods=['POST'])
def add():
    user_id = session['user_id']

    title = request.form.get('title')
    description = request.form.get('description')

    if title and description:
        todo_service.add(
            user_id,
            title,
            description
        )

    return redirect(url_for('todo.list_todos'))


@todo_controller.route('/edit/<int:todo_id>', methods=['GET'])
def edit_todo(todo_id):
    user_id = session['user_id']

    todo_item = todo_service.get_by_id(
        user_id,
        todo_id
    )

    if not todo_item:
        return redirect(url_for('todo.list_todos'))

    theme = session.get('theme', 'light')

    return render_template(
        'todo_edit.html',
        todo=todo_item,
        theme=theme
    )


@todo_controller.route('/update/<int:todo_id>', methods=['POST'])
def update(todo_id):
    user_id = session['user_id']

    title = request.form.get('title')
    description = request.form.get('description')

    if title and description:
        # Intentionally redirect whether the update succeeds or not.
        # A failure may mean this todo does not belong to the current user.
        todo_service.update(
            user_id,
            todo_id,
            title,
            description
        )

    return redirect(url_for('todo.list_todos'))


@todo_controller.route('/delete/<int:todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = session['user_id']

    # Intentionally redirect whether deletion succeeds or not.
    # Don't expose whether another user's todo exists.
    todo_service.delete(
        user_id,
        todo_id
    )

    return redirect(url_for('todo.list_todos'))


@todo_controller.route('/toggle/<int:todo_id>', methods=['POST'])
def toggle_complete(todo_id):
    user_id = session['user_id']

    todo_service.toggle_complete(
        user_id,
        todo_id
    )

    return redirect(url_for('todo.list_todos'))

