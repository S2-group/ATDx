from Controller import *
import multiprocessing as mp
from flask import Flask, request, session, redirect, url_for, abort, jsonify
from flask_github import GitHub

app = Flask(__name__)
app.config.from_object(__name__)

app.config['GITHUB_CLIENT_ID'] = 'XXX'
app.config['GITHUB_CLIENT_SECRET'] = 'YYY'

# setup github-flask
github = GitHub(app)

access_token = None

@app.route('/')
def api_root():
    return 'Welcome to my Webhook'


@app.route('/home')
def index():
    t = 'Everything is ready to start the analysis'
    return t


def post_comment(github_info):
    controller = Controller()
    name = github_info['pull_request']["head"]["repo"]["name"]
    controller.run_sua(name)

    controller.publish_report(name, github_info['pull_request']['number'], )

    body_of_comment = controller.get_body_comment(name)

    data_to_send_back = {'owner': github_info['repository']['owner']['login'], 'repo': github_info['pull_request']["head"]["repo"]["name"],
                         'pull_number': github_info['pull_request']['number'], 'body': body_of_comment}

    url_of_comments = github_info['pull_request']['comments_url']
    value = github.post(resource=url_of_comments, data=data_to_send_back)
    return value


@app.route('/Github', methods=['POST'])
def api_gh_message():
    if request.headers['Content-Type'] == 'application/json':
        github_info = request.json
        if 'pull_request' in github_info:
            if github_info['action'] == 'opened' or github_info['action'] == 'reopened':
                pool.apply_async(post_comment, args=(github_info,))
        return 'success', 200
    else:
        abort(400)


@github.access_token_getter
def token_getter():
    global access_token
    token_to_get = access_token
    if token_to_get is not None:
        return token_to_get


@app.route('/callback')
@github.authorized_handler
def authorized(oauth_token):
    global access_token
    next_url = request.args.get('next') or url_for('index')

    if oauth_token is None:
        print("Authorization failed.")
        return redirect(next_url)

    access_token = oauth_token
    return redirect(next_url)


@app.route('/login')
def login():
    if session.get('user_id', None) is None:
        return_value = github.authorize(scope='repo')
        return return_value
    else:
        return 'Already logged in'


@app.route('/user')
def user():
    return jsonify(github.get('/user'))


if __name__ == '__main__':
    # process
    pool = mp.Pool(1)
    app.run(debug=False, host="YOUR_IP_ADDRESS")
    pool.join()
