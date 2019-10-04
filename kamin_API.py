from flask import Flask, abort, request, jsonify, json
from json import JSONEncoder, JSONDecoder
from Controllers import discussion_controller
from Entities.comment import Comment
from Entities.discussion import Discussion

app = Flask(__name__)


@app.route('/getDiscussion/<int:discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    try:
        mockup = True
        discussion = discussion_controller.get_discussion(discussion_id)
        if mockup:
            discussion = Discussion()
            discussion.get_branches().append([])
            discussion.get_branches().append([])
            comment_0 = Comment("Ron", "I think John John Florence is the best surfer of all time!", None, 0)
            comment_1 = Comment("Guy", "But Kelly Slater won the tour 10 times in a row", comment_0, 0)
            comment_1_1 = Comment("Ron", "Yes but John John has way higher jumps", comment_1, 0)
            comment_1_2 = Comment("Gal", "You are right my friend, Kelly is better!", comment_1, 0)
            discussion.add_comment(comment_0)
            discussion.get_branches()[0].append(comment_0)
            discussion.add_comment(comment_1)
            discussion.get_branches()[0].append(comment_1)
            discussion.add_comment(comment_1_1)
            discussion.get_branches()[0].append(comment_1_1)

            discussion.get_branches()[1].append(comment_0)
            discussion.get_branches()[1].append(comment_1)
            discussion.add_comment(comment_1_2)
            discussion.get_branches()[1].append(comment_1_2)
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
