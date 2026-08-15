from flask import Blueprint, render_template, session
from services.reporting_service import ReportingService

reporting_service = ReportingService()

reporting_controller = Blueprint('reporting', __name__)


@reporting_controller.route('/stats', methods=['GET'])
def get_completion_stats():
    user_id = session['user_id']

    rows = reporting_service.get_completion_rates(user_id)

    theme = session.get('theme', 'light')

    return render_template(
        'stats.html',
        rows=rows,
        theme=theme
    )

