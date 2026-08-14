from sqlalchemy import func, cast, Date, Numeric
from models.todo import Todo, db


class ReportingService:
    @staticmethod
    def get_completion_rates():
        week_buck = cast(func.date_trunc('week', Todo.created_at), Date).label('week_buck')

        weekly_user_todos = db.select(
            Todo.user_id,
            week_buck,
            func.count().label('total_todos'),
            func.count().filter(Todo.completed.is_(True)).label('completed_todos')
        ).group_by(
            Todo.user_id,
            week_buck
        ).cte("weekly_user_todos")

        cumulative_stats = db.select(
            weekly_user_todos.c.user_id,
            weekly_user_todos.c.week_buck,
            weekly_user_todos.c.total_todos,
            weekly_user_todos.c.completed_todos,
            func.sum(weekly_user_todos.c.total_todos).over(
                partition_by=weekly_user_todos.c.user_id,
                order_by=weekly_user_todos.c.week_buck
            ).label('cumulative_total'),
            func.sum(weekly_user_todos.c.completed_todos).over(
                partition_by=weekly_user_todos.c.user_id,
                order_by=weekly_user_todos.c.week_buck
            ).label('cumulative_completed')
        ).cte("cumulative_stats")

        cumulative_completion_rate = func.round(
            (cast(cumulative_stats.c.cumulative_completed, Numeric) /
             func.nullif(cumulative_stats.c.cumulative_total, 0)) * 100,
            2
        ).label('cumulative_completion_rate')

        stmt = db.select(
            cumulative_stats.c.user_id,
            cumulative_stats.c.week_buck,
            cumulative_stats.c.total_todos,
            cumulative_stats.c.completed_todos,
            cumulative_stats.c.cumulative_total,
            cumulative_stats.c.cumulative_completed,
            cumulative_completion_rate
        ).order_by(
            cumulative_stats.c.user_id,
            cumulative_stats.c.week_buck
        )

        return db.session.execute(stmt).all()
