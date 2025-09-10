from models.user import User, db

class UserService:
    @staticmethod
    def register(username, password):
        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return None  # User already exists

        # Create a new user
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return new_user

    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None
