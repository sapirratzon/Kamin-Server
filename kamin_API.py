from flask import Flask
from flask import request

app = Flask(__name__)


@app.route('/getDiscussion', methods=['POST'])
def get_discussion():
    try:
        discussion_id = request.form.get('discussion_id', type=str)

    except IOError as e:
        app.logger.exception(e)
        return "No such file or directory"
    return "Success"


@app.route('/addComment', methods=['POST'])
def add_comment():
    try:
        comment = request.form.get('comment', type=str)

    except IOError as e:
        app.logger.exception(e)
        return "No such file or directory"
    return "Success"


if __name__ == '__main__':
    app.run(debug=True)