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


def get_json_data(user, repository, git_api_suffix):
    response = requests.get(GITHUB_API_URL + '/repos/' + user + '/' + repository + '/stats/' + git_api_suffix)
    return response.json()


def unix_to_utc(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')


def get_commits_sum_from_day(commit_activity_data, day_num):
    return sum([week['days'][day_num] for week in commit_activity_data])


@app.route('/', methods=['GET', 'POST'])
def home():
    form = FindUserForm()
    if form.validate_on_submit():
        username = form.username.data
        return redirect('/profile/' + username)
    return render_template('home.html', form=form)


@app.route('/profile/<username>')
def user_profile(username):
    response = requests.get(GITHUB_API_URL + '/users/' + username + '/repos')
    repositories = response.json()
    return render_template('user_profile.html', repos=repositories)


@app.route('/stats/<user>/<repository>')
def repository_stats(user, repository):
    code_frequency_data = get_json_data(user, repository, 'code_frequency')
    weeks_labels = [unix_to_utc(item[0]) for item in code_frequency_data]
    additions = [item[1] for item in code_frequency_data]
    deletions = [item[2] for item in code_frequency_data]

    commit_activity_data = get_json_data(user, repository, 'commit_activity')
    commits_sum_by_days = [get_commits_sum_from_day(commit_activity_data, i) for i in range(7)]

    participation_data = get_json_data(user, repository, 'participation')['all']

    return render_template('chart.html', user=user, repository=repository,
                           additions=additions, deletions=deletions, weeks=weeks_labels,
                           days_data=commits_sum_by_days, week_activity_data=participation_data)


if __name__ == '__main__':
    app.run()
