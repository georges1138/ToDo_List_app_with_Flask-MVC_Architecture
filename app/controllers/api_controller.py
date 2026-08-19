from flask import Blueprint, request, jsonify, g
from services.user_service import UserService
from services.token_service import TokenService
from services.todo_service import TodoService
from middlewares.api_authentication import require_api_token


api_controller = Blueprint(
    "api",
    __name__,
    url_prefix="/api/v1"
)


def _serialize_todo(todo):
    return {
        "todo_id": todo.todo_id,
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "created_at": todo.created_at.isoformat(),
        "completed_at": (
            todo.completed_at.isoformat()
            if todo.completed_at
            else None
        ),
    }


@api_controller.route("/tokens", methods=["POST"])
def create_token():
    # 1. request.get_json(...)
    # silent=True ensures it returns None instead of crashing if the request isn't valid JSON
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    # 2. extract username/password/name
    username = data.get("username")
    password = data.get("password")
    name = data.get("name")

    # 3. validate missing fields
    # Checks if any of the required fields evaluate to False (None or empty string "")
    if not username or not password or not name:
        return jsonify({"error": "Missing required fields: username, password, or name"}), 400

    # 4. UserService.login(...)
    # Pass the credentials to your service to verify them
    user = UserService.login(username, password)

    # 5. reject invalid credentials
    # If login fails, your service likely returns None or False
    if user is None:
        return jsonify({"error": "Invalid username or password"}), 401

    # 6. TokenService.issue_token(...)
    raw_token, api_token = TokenService.issue_token(user.id, name)

    # 7. return JSON + 201
    # 201 is the standard HTTP status code for "Created"
    return jsonify(
        {
            "token": raw_token,
            "token_id": api_token.token_id,
            "name": api_token.name,
        }
    ), 201


@api_controller.route("/todos", methods=["GET"])
@require_api_token
def get_todos():
    todo_data = []

    todos = TodoService.get_all(g.user_id)

    for todo in todos:
        todo_data.append(
            _serialize_todo(todo)
        )

    return jsonify(todo_data), 200


@api_controller.route("/todos/<int:todo_id>", methods=["GET"])
@require_api_token
def get_todo(todo_id):
    todo = TodoService.get_by_id(
        user_id=g.user_id,
        todo_id=todo_id
    )

    if todo is None:
        return jsonify({"error": "Todo not found"}), 404

    return jsonify(_serialize_todo(todo)), 200


@api_controller.route("/todos", methods=["POST"])
@require_api_token
def create_todo():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    title = data.get("title")
    description = data.get("description")

    # Checks if any of the required fields evaluate to False (None or empty string "")
    if not title or not description:
        return jsonify({"error": "Missing required fields: title or description"}), 400

    todo = TodoService.add(
        user_id=g.user_id,
        title=title,
        description=description
    )

    return jsonify(_serialize_todo(todo)), 201


@api_controller.route("/todos/<int:todo_id>", methods=["PUT"])
@require_api_token
def update_todo(todo_id):

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON payload"}), 400

    title = data.get("title")
    description = data.get("description")

    if not title or not description:
        return jsonify({"error": "Missing required fields: title or description"}), 400

    updated = TodoService.update(
        user_id=g.user_id,
        todo_id=todo_id,
        title=title,
        description=description
    )

    if updated is False:
        return jsonify({"error": "Todo not found"}), 404

    todo = TodoService.get_by_id(
        user_id=g.user_id,
        todo_id=todo_id
    )

    return jsonify(_serialize_todo(todo)), 200


@api_controller.route("/todos/<int:todo_id>", methods=["DELETE"])
@require_api_token
def delete_todo(todo_id):

    deleted = TodoService.delete(g.user_id, todo_id)

    if not deleted:
        return jsonify({"error": "Todo not found"}), 404

    return "", 204


@api_controller.route(
    "/todos/<int:todo_id>/completion",
    methods=["PATCH"]
)
@require_api_token
def toggle_todo_completion(todo_id):

    toggled = TodoService.toggle_complete(
        user_id=g.user_id,
        todo_id=todo_id
    )

    if not toggled:
        return jsonify({"error": "Todo not found"}), 404

    todo = TodoService.get_by_id(
        user_id=g.user_id,
        todo_id=todo_id
    )

    return jsonify(_serialize_todo(todo)), 200
