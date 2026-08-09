import pytest

from models import db
from models.user import User
from models.todo import Todo
from services.todo_service import TodoService


@pytest.fixture
def todo_scenario(app):
    user_a = User(
        username='alice',
        password_hash='fake-hash-a'
    )

    user_b = User(
        username='bob',
        password_hash='fake-hash-b'
    )

    db.session.add_all([user_a, user_b])
    db.session.commit()

    todo_a = Todo(
        title='Alice Todo',
        description="Alice's task",
        user_id=user_a.id
    )

    todo_b = Todo(
        title='Bob Todo',
        description="Bob's task",
        user_id=user_b.id
    )

    db.session.add_all([todo_a, todo_b])
    db.session.commit()

    return {
        'user_a': user_a,
        'user_b': user_b,
        'todo_a': todo_a,
        'todo_b': todo_b,
    }


def test_add_todo(app):
    user = User(
        username="alice",
        password_hash="fake-hash"
    )

    db.session.add(user)
    db.session.commit()

    todo = TodoService.add(
        user.id,
        "Buy milk",
        "Get whole milk"
    )

    assert todo.title == "Buy milk"
    assert todo.description == "Get whole milk"
    assert todo.user_id == user.id


def test_get_all_excludes_other_users(todo_scenario):
    user_a = todo_scenario["user_a"]
    todo_a = todo_scenario["todo_a"]
    todo_b = todo_scenario["todo_b"]

    todos = TodoService.get_all(user_a.id)

    todo_ids = [todo.todo_id for todo in todos]

    assert todo_a.todo_id in todo_ids
    assert todo_b.todo_id not in todo_ids


def test_get_by_id_returns_none_for_other_users_todo(todo_scenario):
    user_a = todo_scenario["user_a"]
    todo_b = todo_scenario["todo_b"]

    result = TodoService.get_by_id(
        user_a.id,
        todo_b.todo_id
    )

    assert result is None


def test_update_does_not_change_other_users_todo(todo_scenario):
    user_a = todo_scenario["user_a"]
    todo_b = todo_scenario["todo_b"]

    original_title = todo_b.title
    todo_b_id = todo_b.todo_id

    result = TodoService.update(
        user_a.id,
        todo_b_id,
        "Hacked title",
        "This should never be saved"
    )

    assert result is False

    db.session.expire_all()

    unchanged_todo = db.session.get(Todo, todo_b_id)

    assert unchanged_todo is not None
    assert unchanged_todo.title == original_title


def test_delete_does_not_remove_other_users_todo(todo_scenario):
    user_a = todo_scenario["user_a"]
    todo_b = todo_scenario["todo_b"]

    todo_b_id = todo_b.todo_id

    result = TodoService.delete(
        user_a.id,
        todo_b_id
    )

    assert result is False

    db.session.expire_all()

    existing_todo = db.session.get(Todo, todo_b_id)

    assert existing_todo is not None


def test_update_changes_owners_todo(todo_scenario):
    user_a = todo_scenario["user_a"]
    todo_a = todo_scenario["todo_a"]

    todo_a_id = todo_a.todo_id

    result = TodoService.update(
        user_a.id,
        todo_a_id,
        "Updated title",
        "Updated description"
    )

    assert result is True

    db.session.expire_all()

    updated_todo = db.session.get(Todo, todo_a_id)

    assert updated_todo is not None
    assert updated_todo.title == "Updated title"
    assert updated_todo.description == "Updated description"


def test_delete_removes_owners_todo(todo_scenario):
    user_a = todo_scenario["user_a"]
    todo_a = todo_scenario["todo_a"]

    todo_a_id = todo_a.todo_id

    result = TodoService.delete(
        user_a.id,
        todo_a_id
    )

    assert result is True

    db.session.expire_all()

    deleted_todo = db.session.get(Todo, todo_a_id)

    assert deleted_todo is None

