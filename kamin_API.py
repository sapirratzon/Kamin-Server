from flask import Flask, abort, request, jsonify, json
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from Controllers import discussion_controller
from Entities.comment import *

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/getDiscussion/<int:discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    try:
        if discussion_id > 45 and discussion_id != 777:
            raise IOError
        # 777 is mock up code
        if discussion_id == 777:
            discussion = discussion_controller.get_mock_discussion()
        else:
            discussion = discussion_controller.get_discussion_tree_tools(discussion_id)

        discussion_json_dict = discussion.to_json_dict()
        return jsonify(discussion=discussion_json_dict['discussion'], tree=discussion_json_dict['tree'])
    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return


@app.route('/addComment/<int:comment>', methods=['POST'])
def add_comment(comment: int):
    try:
        discussion = discussion_controller.get_discussion_tree_tools(comment.discussion_id)
        # create commentNode from comment
        comment_node = CommentNode()
        discussion.add_comment(comment_node)
        discussion_controller.analyze_discussion(discussion, comment_node)

    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return

    return comment_node.get_actions()


@socketio.on('chat message')
def chat_message(message):
    print(message)
    emit('chat message', {'data': message})

if __name__ == '__main__':
    # app.debug = True
    socketio.run(app)
