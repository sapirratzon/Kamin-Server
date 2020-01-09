from flask import Flask, abort, request, jsonify, g, url_for
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from Controllers import discussion_controller
from flask_httpauth import HTTPBasicAuth
from Controllers.discussion_controller import DiscussionController
from Controllers.user_controller import UserController
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


# initialization
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

# extensions
auth = HTTPBasicAuth()
user_controller = UserController()
discussion_controller = DiscussionController()


def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    user = user_controller.get_user(data['id'])
    return user


@auth.verify_password
def verify_password(username_or_token, password):
    user = verify_auth_token(username_or_token)
    if not user:
        user = user_controller.get_user(username=username_or_token)
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True


@app.route('/api/newUser', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    if username is None or password is None:
        abort(400) # missing arguments
    if user_controller.get_user(username=username) is not None:
        abort(400) # existing user
    user_id = user_controller.add_new_user(username=username, password=password, first_name=first_name, last_name=last_name)
    return jsonify({'user_id': user_id}), 201


@app.route('/api/getUser', methods=['GET'])
def get_user():
    username = request.args.get('username')
    user = user_controller.get_user(username=username)
    if not user:
        abort(400)
    return jsonify({'username': user.get_user_name(), 'password': user.get_password(), 'first_name': user.get_first_name(), 'last_name': user.get_last_name()}), 201


@app.route('/api/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(app.config['SECRET_KEY'], 600)
    return jsonify({'token': token.decode('ascii'), 'duration': 600})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    print("gal")
    return jsonify({'data': 'Hello, %s!' % g.user.get_user_name()})


@app.route('/api/createDiscussion', methods=['POST'])
# @auth.login_required
def create_discussion():
    try:
        title = request.json.get('title')
        categories = request.json.get('categories')
        discussion_id = discussion_controller.create_discussion(title, categories)
        return jsonify({'discussion': discussion_id}), 201
    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return


@app.route('/api/addComment', methods=['POST'])
# @auth.login_required
def add_comment():
    comment_dict = {}
    try:
        comment_dict["author"] = request.json.get('author')
        comment_dict["text"] = request.json.get('text')
        comment_dict["parentId"] = request.json.get('parentId')
        comment_dict["discussionId"] = request.json.get('discussionId')
        comment_dict["extra_data"] = request.json.get('extra_data')
        comment_dict["time_stamp"] = request.json.get('time_stamp')
        comment_dict["depth"] = request.json.get('depth')
        response = discussion_controller.add_comment(comment_dict)
    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return

    return jsonify(response), 201


@app.route('/api/getDiscussion/<string:discussion_id>', methods=['GET'])
def get_discussion(discussion_id):
    try:
        discussion_tree = discussion_controller.get_discussion(discussion_id)
        discussion_json_dict = discussion_tree.to_json_dict()
        return jsonify({"discussion": discussion_json_dict['discussion'], "tree": discussion_json_dict['tree']})
    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return


@socketio.on('chat message')
def chat_message(message):
    print(message)
    emit('chat message', {'data': message})


if __name__ == '__main__':
    app.debug = True
    socketio.run(app)
