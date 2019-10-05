from flask import Flask, abort, request, jsonify, json
from json import JSONEncoder, JSONDecoder
from Controllers import discussion_controller
from Entities.comment import *

app = Flask(__name__)


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


@app.route('/addComment/<json:comment>', methods=['POST'])
def add_comment(comment: Comment):
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


if __name__ == '__main__':
    app.run(debug=True)
