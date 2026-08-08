from models.todo import Todo, db

class TodoService:
    @staticmethod
    def get_all(user_id, sort_by=None, filter_by=None):
        query = Todo.query.filter_by(user_id=user_id)

        if filter_by:
            query = query.filter(Todo.title.ilike(f'{filter_by}%'))
        if sort_by == 'title':
            query = query.order_by(Todo.title)
        return query.all()

    @staticmethod
    def get_by_id(user_id, todo_id):
        return Todo.query.filter_by(
            todo_id=todo_id,
            user_id=user_id
        ).first()

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
