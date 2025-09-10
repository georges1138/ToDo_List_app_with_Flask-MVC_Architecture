from models.todo import Todo, db

class TodoService:
    @staticmethod
    def get_all(sort_by=None, filter_by=None):
        query = Todo.query
        if filter_by:
            query = query.filter(Todo.title.ilike(f'{filter_by}%'))
        if sort_by == 'title':
            query = query.order_by(Todo.title)
        return query.all()

    @staticmethod
    def get_by_id(todo_id):
        return Todo.query.get(todo_id)

    @staticmethod
    def add(title, description):
        new_todo = Todo(title, description)
        db.session.add(new_todo)
        db.session.commit()
        return new_todo

    @staticmethod
    def update(todo_id, title, description):
        todo = TodoService.get_by_id(todo_id)
        if todo:
            todo.title = title
            todo.description = description
            db.session.commit()
            return True
        return False

    @staticmethod
    def delete(todo_id):
        todo = TodoService.get_by_id(todo_id)
        if todo:
            db.session.delete(todo)
            db.session.commit()
            return True
        return False
