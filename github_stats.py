import datetime

import os
from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
import requests

import secret_settings
from forms import FindUserForm

GITHUB_API_URL = 'https://api.github.com'

app = Flask(__name__)
Bootstrap(app)
app.config.update(
    DEBUG=True,
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True,
    BOOTSTRAP_SERVE_LOCAL=True,
    SECRET_KEY=secret_settings.SECRET_KEY
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


@app.route('/', methods=['GET', 'POST'])
def home():
    form = FindUserForm()
    if form.validate_on_submit():
        username = form.username.data
        return redirect('/profile/' + username)
    return render_template('home.html', form=form)


@app.route('/profile/<username>')
def user_profile(username):
    repos = []
    response = requests.get(GITHUB_API_URL + '/users/' + username + '/repos')
    repositories = response.json()
    return render_template('user_profile.html', repos=repositories)


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
