from datetime import datetime, timezone
from models.todo import Todo, db

class TodoService:
    @staticmethod
    def get_all(user_id, sort_by=None, filter_by=None):
        stmt = db.select(Todo).where(
            Todo.user_id == user_id
        )

        if filter_by:
            stmt = stmt.where(
                Todo.title.ilike(f'{filter_by}%')
            )
        if sort_by == 'title':
            stmt = stmt.order_by(Todo.title)
        return db.session.execute(
            stmt
        ).scalars().all()

    @staticmethod
    def get_by_id(user_id, todo_id):
        stmt = db.select(Todo).where(
            Todo.todo_id == todo_id,
            Todo.user_id == user_id
        )

        return db.session.execute(
            stmt
        ).scalar_one_or_none()

    @staticmethod
    def add(user_id, title, description):
        new_todo = Todo(
            title=title,
            description=description,
            user_id=user_id
        )
        db.session.add(new_todo)
        db.session.commit()
        return new_todo

    @staticmethod
    def update(user_id, todo_id, title, description):
        todo = TodoService.get_by_id(user_id, todo_id)

        if todo:
            todo.title = title
            todo.description = description
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete(user_id, todo_id):
        todo = TodoService.get_by_id(user_id, todo_id)

        if todo:
            db.session.delete(todo)
            db.session.commit()
            return True
        return False

    @staticmethod
    def toggle_complete(user_id, todo_id):
        todo = TodoService.get_by_id(
            user_id,
            todo_id
        )

        if not todo:
            return False

        if todo.completed:
            todo.completed = False
            todo.completed_at = None
        else:
            todo.completed = True
            todo.completed_at = datetime.now(timezone.utc)

        db.session.commit()

        return True
