from Controller import *
import multiprocessing as mp
from flask import *
from flask_github import GitHub

app = Flask(__name__)


@app.route('/')
def api_root():
    return 'Welcome to my Webhook'


@app.route('/Github', methods=['POST'])
def api_gh_message():
    if request.headers['Content-Type'] == 'application/json':
        some_info = request.json
        print(some_info['pull_request']['head']['repo']['name'])
        pool.apply_async(controller.run)

        return 'success', 200
    else:
        abort(400)


if __name__ == '__main__':
    # process
    pool = mp.Pool(1)
    controller = Controller()

    app.run(debug=True)
    pool.join()