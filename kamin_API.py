from flask import Flask, abort, request, jsonify, json
from json import JSONEncoder, JSONDecoder
from Controllers import discussion_controller


app = Flask(__name__)


@app.route('/getDiscussion/<int:discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    try:
        mockup = True
        discussion = discussion_controller.get_discussion(discussion_id)
        if mockup:
            discussion = discussion_controller.get_mock_discussion()

        return discussion.to_json()
    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return


@app.route('/addComment/<Comment:comment>', methods=['POST'])
def add_comment(comment):
    try:
        discussion = discussion_controller.get_discussion(comment.discussion_id)
        comment_node = discussion.add_comment(comment)
        discussion_controller.analyze_discussion(discussion, comment_node)

    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return

    return comment_node.get_actions()


if __name__ == '__main__':
    app.run(debug=True)
