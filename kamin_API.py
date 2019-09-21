from flask import Flask, abort, request, jsonify
from Controllers import discussion_controller

app = Flask(__name__)


@app.route('/getDiscussion', methods=['POST'])
def get_discussion():
    try:
        discussion_id = request.form.get('discussion_id', type=str)
        discussion = discussion_controller.get_discussion(discussion_id)

    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return

    return jsonify(discussion)


@app.route('/addComment', methods=['POST'])
def add_comment():
    try:
        comment = request.form.get('comment', type=str)
        discussion = discussion_controller.get_discussion(comment.discussion_id)
        discussion.add_comment(discussion)

    except IOError as e:
        app.logger.exception(e)
        abort(400)

    return "Success"


if __name__ == '__main__':
    app.run(debug=True)
