from flask import flash, render_template
from werkzeug.exceptions import HTTPException

from app import socketio
from app.errors import bp


@bp.app_errorhandler(HTTPException)
@socketio.on_error_default
def error_handler(e):
    """Handle general application errors."""
    flash(f'An error has occurred: {e}', 'danger')
    return render_template('errors/universal.html', title="Error")
