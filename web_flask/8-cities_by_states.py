#!/usr/bin/python3
"""Start web application with two routings
"""

from models import storage
from models.state import State
from flask import Flask, render_template


app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def states_list():
    """Render template with states
    """
    states = storage.all(State)

    # sort State object alphabetically by name
    # sorted_states = sorted(states.values(), key=lambda state: state.name)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def app_teardown(arg=None):
    """Clean-up session
    """
    storage.close()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
