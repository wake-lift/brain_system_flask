from flask import render_template
from werkzeug import exceptions

from . import app


@app.errorhandler(exceptions.NotFound)
def page_not_found(error):
    return render_template('common_pages/404.html'), 404


@app.errorhandler(exceptions.Forbidden)
def forbidden(error):
    return render_template('common_pages/403.html'), 403


@app.errorhandler(exceptions.BadRequest)
def bad_request(error):
    return render_template('common_pages/400.html'), 400


@app.errorhandler(exceptions.InternalServerError)
def internal_server_error(error):
    return render_template('common_pages/500.html'), 500
