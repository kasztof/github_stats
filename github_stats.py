import datetime

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
Bootstrap(app)
app.config.update(
    DEBUG=True,
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True,
    BOOTSTRAP_SERVE_LOCAL=True
)


def get_list_of_nth_elements(data, n):
    result_list = []
    for d in data:
        result_list.append(d[n])
    return result_list


def get_weeks(data):
    additions_list = []
    for d in data:
        additions_list.append(datetime.datetime.utcfromtimestamp(d[0]).strftime('%Y-%m-%d'))
    print(additions_list)
    return additions_list


@app.route('/')
def hello_world():
    user = {'username': 'Miguel'}
    return render_template('home.html', title='Home', user=user)


@app.route("/chart")
def chart():
    url = 'https://api.github.com/repos/kasztof/MountainsPortal/stats/code_frequency'
    r = requests.get(url)
    response_data = r.json()
    additons_data = get_list_of_nth_elements(response_data, 1)
    deletions_data = get_list_of_nth_elements(response_data, 2)
    weeks_data = get_weeks(response_data)

    return render_template('chart.html', additions=additons_data, deletions=deletions_data, weeks=weeks_data)


if __name__ == '__main__':
    app.run()
