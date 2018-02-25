from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import requests


app = Flask(__name__)
Bootstrap(app)
app.config.update(
    DEBUG=True,
    TESTING=True,
    TEMPLATES_AUTO_RELOAD=True,
)


@app.route('/')
def hello_world():
    url = 'https://api.github.com/repos/kasztof/MountainsPortal/stats/code_frequency'
    r = requests.get(url)
    print(r.status_code)
    response_dict = r.json()
    weeks = response_dict
    user = {'username': 'Miguel'}
    return render_template('home.html', title='Home', user=user, weeks=weeks )


if __name__ == '__main__':
    app.run()
