import json

from flask import Flask, abort, request, jsonify, g, url_for, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit, send
from flask_httpauth import HTTPBasicAuth
from Controllers.discussion_controller import DiscussionController
from Controllers.user_controller import UserController
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from Entities.user import Permission



# initialization
app = Flask(__name__)
CORS(app)
socket_io = SocketIO(app, cors_allowed_origins='*')
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'
ROOMS = {}  # dict to track active rooms
UsersRoom = {}

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
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        if username is None or password is None:
            raise Exception("username or password is Missing, can't create new user!")
        if user_controller.get_user(username=username) is not None:
            raise Exception("username is already exist, can't create new user!")
        user_id = user_controller.add_new_user(username=username, password=password, first_name=first_name,
                                               last_name=last_name)
        return jsonify({'user_id': user_id}), 200
    except Exception as e:
        app.logger.exception(e)
        abort(500, e)

# TODO: this is not safe in production
@app.route('/api/getUser', methods=['GET'])
def get_user():
    try:
        username = request.args.get('username')
        user = user_controller.get_user(username=username)
        if not user:
            raise Exception("username is not exist!")
        return jsonify(
            {'username': user.get_user_name(), 'password': user.get_password(), 'first_name': user.get_first_name(),
             'last_name': user.get_last_name(), 'permission': user.get_permission()}), 200
    except Exception as e:
        app.logger.exception(e)
        abort(500, e)


@app.route('/api/getUsers', methods=['GET'])
def get_users():
    try:
        users, moderators = user_controller.get_users()
        return jsonify(
            {'users': users, 'moderators': moderators}), 200
    except Exception as e:
        app.logger.exception(e)
        abort(500, e)


@app.route('/api/changeUserPermission', methods=['GET'])
@auth.login_required
def change_user_permission():
    try:
        user = g.user
        if user.get_permission() is not Permission.ROOT.value:
            raise Exception("Only ROOT user permitted to change permissions!")
        permission = request.args.get('permission')
        username = request.args.get('username')
        user = user_controller.get_user(username=username)
        if not user:
            raise Exception("username is not exist!")
        result = user_controller.change_user_permission(user, permission)
        return jsonify(result), 200
    except Exception as e:
        app.logger.exception(e)
        abort(500, e)


@app.route('/api/login')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(app.config['SECRET_KEY'], 60000)
    user = g.user
    permission = user.get_permission()
    return jsonify({'token': token.decode('ascii'), 'permission': permission, 'duration': 60000})


@app.route('/api/resource')
@auth.login_required
def get_resource():
    print("gal")
    return jsonify({'data': 'Hello, %s!' % g.user.get_user_name()})


@app.route('/api/getDiscussion/<string:discussion_id>', methods=['GET'])
@auth.login_required
def get_discussion(discussion_id):
    try:
        discussion_tree = discussion_controller.get_discussion(discussion_id)
        #     room = discussion_tree.get_id()
        #     ROOMS[room] = discussion_tree
        discussion_json_dict = discussion_tree.to_json_dict()
        return jsonify({"discussion": discussion_json_dict['discussion'], "tree": discussion_json_dict['tree']})
    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return


@app.route('/api/createDiscussion', methods=['POST'])
@auth.login_required
def create_discussion():
    try:
        user = g.user
        if user.get_permission() is not Permission.MODERATOR.value:
            raise Exception("User not permitted to create discussion!")
        title = request.json["title"]
        if title is None:
            raise Exception("Title is missing, can't create discussion!")
        categories = request.json["categories"]
        root_comment = json.loads(request.json["root_comment_dict"])
        if root_comment is None or len(root_comment) is 0 or root_comment["text"] == "" or root_comment["text"] is None:
            raise Exception("Message is missing, can't create discussion!")
        discussion_tree = discussion_controller.create_discussion(title, categories, root_comment)
        room = discussion_tree.get_id()
        ROOMS[room] = discussion_tree
        # join_room(room)
        # socket_io.emit('createDiscussion', {'room': room, 'root_id': discussion_tree.get_root_comment_id()})
        return jsonify({'discussion_id': discussion_tree.get_id(), "root_comment_id": discussion_tree.get_root_comment_id()}), 201
    except Exception as e:
        app.logger.exception(e)
        abort(500, e)
        return


@socket_io.on('join')
def on_join(data):
    token = data['token']
    room = data['discussion_id']
    user = verify_auth_token(token)
    # TODO: for production only
    username = user.get_user_name()
    if room not in ROOMS:
        ROOMS[room] = discussion_controller.get_discussion(room)
        UsersRoom[room] = {}
    # write to log that username join to room
    join_room(room)
    UsersRoom[room][username] = request.sid
    discussion_json_dict = ROOMS[room].to_json_dict()
    socket_io.emit("join room", data=discussion_json_dict, room=UsersRoom[room][username])
    # socket_io.emit("user joined", data=username + " joined the discussion", room=room)
    socket_io.emit("join room", data=discussion_json_dict, room=request.sid)
    socket_io.emit("user joined", data=username + " joined the discussion", room=room)

@socket_io.on("add comment")
def add_comment(request_comment):
    json_string = request_comment
    comment_dict = json.loads(json_string)
    room = comment_dict['discussionId']
    response = discussion_controller.add_comment(comment_dict)
    ROOMS[room].add_comment(response["comment"])
    response["comment"] = response["comment"].to_client_dict()
    socket_io.send(response, room=room)

    kamin_analyze = response["KaminAIAnalyze"]
    # for user in kamin_analyze["users"]:
    #     socket_io.send(response["comment"], room=room)

#        socket_io.send({"labels": kamin_analyze["labels"], "actions": kamin_analyze["actions"]}, room=UsersRoom[room][user])
    socket_io.send(response["comment"], room=room)


@socket_io.on('connect')
def client_connect():
    print("client connected")


@socket_io.on('disconnect')
def client_disconnect():
    print("client disconnected")


if __name__ == '__main__':
    #app.debug = True
    socket_io.run(app, debug=False)
    print("bla")
