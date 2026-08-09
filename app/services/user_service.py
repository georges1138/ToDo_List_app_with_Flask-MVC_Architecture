from models.user import User, db


class UserService:

    @staticmethod
    def register(username, password):
        stmt = db.select(User).where(
            User.username == username
        )

        existing_user = db.session.execute(
            stmt
        ).scalar_one_or_none()

        if existing_user:
            return None

        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        return new_user

    @staticmethod
    def login(username, password):
        stmt = db.select(User).where(
            User.username == username
        )

        user = db.session.execute(
            stmt
        ).scalar_one_or_none()

        if user and user.check_password(password):
            return user

        return None
