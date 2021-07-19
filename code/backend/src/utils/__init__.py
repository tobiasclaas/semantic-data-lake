from functools import wraps

from flask_jwt_extended import verify_jwt_in_request
from werkzeug.utils import redirect


def login_required(function):
    @wraps(function)
    def decorated(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return function(*args, **kwargs)
        except Exception as e:
            print ("No user logged in")
            return redirect('/')

    return decorated