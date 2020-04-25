import json
from flask import Flask, abort, request, jsonify, g, url_for, render_template
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit, send, leave_room, ConnectionRefusedError
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
simulation_indexes = {}
simulation_order = {}
USERS = {}

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


@app.route('/api/getActiveDiscussionUsers/<string:discussion_id>', methods=['GET'])
def get_active_discussion_users(discussion_id):
    try:
        active_users = []
        moderator = discussion_controller.get_discussion_moderator(discussion_id)
        if len(USERS) > 0:
            active_users = list(dict(USERS[discussion_id]).keys())
            if active_users.__contains__(moderator):
                active_users.remove(moderator)
        return jsonify({'active_users': active_users}), 200
    except Exception as e:
        app.logger.exception(e)
        abort(500, e)


@app.route('/api/getActiveUsersConfigurations/<string:discussion_id>', methods=['GET'])
def get_active_users_configurations(discussion_id):
    try:
        config = {}
        moderator = discussion_controller.get_discussion_moderator(discussion_id)
        users_config = discussion_controller.get_all_users_discussion_configurations(discussion_id)
        if users_config.__contains__(moderator):
            users_config.pop(moderator)
        for user in users_config:
            if USERS[discussion_id].__contains__(user):
                config[user] = users_config[user]["configuration"]
        return jsonify({"config": config}), 200
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


@app.route('/api/getUserStatisticsInDiscussion', methods=['POST'])
def get_user_discussion_statistics():
    try:
        username = request.json.get('username')
        discussion_id = request.json.get('discussionId')
        if username is None or discussion_id is None:
            raise Exception("username or discussionId is Missing, can't get statistics!")
        if user_controller.get_user(username=username) is None:
            raise Exception("username is not exist, can't get statistics!")
        statistics = discussion_controller.get_user_discussion_statistics(username, discussion_id)
        if statistics is None:
            raise Exception("Statistics of username in discussionId is not exist!")
        return jsonify({"user_in_discussion_statistics": statistics}), 200
    except Exception as e:
        app.logger.exception(e)
        abort(500, e)


@app.route('/api/getDiscussionStatistics', methods=['POST'])
def get_discussion_statistics():
    try:
        discussion_id = request.json.get('discussionId')
        if discussion_id is None:
            raise Exception("discussionId is Missing, can't get statistics!")
        statistics = discussion_controller.get_discussion_statistics(discussion_id)
        if statistics is None:
            raise Exception("Statistics of username in discussionId is not exist!")
        return jsonify({"discussion_statistics": statistics}), 200
    except Exception as e:
        app.logger.exception(e)
        abort(500, e)


@app.route('/api/changeUserPermission', methods=['POST'])
@auth.login_required
def change_user_permission():
    try:
        user = g.user
        if user.get_permission() is not Permission.ROOT.value:
            raise Exception("Only ROOT user permitted to change permissions!")
        permission = json.loads(request.data)["permission"]
        username = json.loads(request.data)["username"]
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
        if discussion_tree is None:
            raise Exception("discussion_id is not exist!")
        discussion_json_dict = discussion_tree.to_json_dict()
        return jsonify({"discussion": discussion_json_dict['discussion'], "tree": discussion_json_dict['tree']})
    except IOError as e:
        app.logger.exception(e)
        abort(400)
        return


@app.route('/api/getDiscussions/<string:is_simulation>', methods=['GET'])
@auth.login_required
def get_discussions(is_simulation):
    try:
        is_simulation = (is_simulation == 'True')
        discussions_list = discussion_controller.get_discussions(is_simulation)
        return jsonify({"discussions": discussions_list})
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
        data = dict(request.json)
        if not data.keys().__contains__("title") or data["title"] is None:
            raise Exception("Title is missing, can't create discussion!")
        title = data["title"]
        if not data.keys().__contains__("categories"):
            raise Exception("Categories is missing, can't create discussion!")
        categories = data["categories"]
        if not data.keys().__contains__("root_comment_dict"):
            raise Exception("root_comment_dict Key is missing, can't create discussion!")
        root_comment = data["root_comment_dict"]
        if root_comment is None or len(root_comment) is 0 or root_comment["text"] == "" or root_comment["text"] is None:
            raise Exception("First comment is missing, can't create discussion!")
        if not data.keys().__contains__("configuration"):
            raise Exception("configuration Key is missing, can't create discussion!")
        configuration = data["configuration"]
        if configuration is None or len(configuration) is 0:
            raise Exception("configuration is missing, can't create discussion!")
        discussion_tree = discussion_controller.create_discussion(title, categories, root_comment, configuration)
        room = discussion_tree.get_id()
        ROOMS[room] = discussion_tree
        USERS[room] = {user.get_user_name(): ""}
        return jsonify(
            {'discussion_id': discussion_tree.get_id(), "root_comment_id": discussion_tree.get_root_comment_id()}), 201
    except Exception as e:
        app.logger.exception(e)
        abort(400, e)
        return


@socket_io.on('end_session')
def end_real_time_session(data):
    token = data['token']
    discussion_id = data['discussionId']
    user = verify_auth_token(token)
    if user.get_permission() is not Permission.MODERATOR.value:
        socket_io.emit("error", "User not permitted to end real-time session!")
    discussion_controller.end_real_time_session(discussion_id)
    USERS.pop(discussion_id)
    ROOMS.pop(discussion_id)
    socket_io.emit("end_session")


@socket_io.on('join')
def on_join(data):
    token = data['token']
    room = data['discussion_id']
    user = verify_auth_token(token)
    if not user:
        socket_io.emit("unauthorized", room=request.sid)
        return
    username = user.get_user_name()
    if room not in ROOMS:
        discussion = discussion_controller.get_discussion(room)
        if discussion is None:
            socket_io.emit("error", data="join Error - discussionId not exist!", room=request.sid)
            return
        ROOMS[room] = discussion
        USERS[room] = {}
    join_room(room)
    USERS[room][username] = request.sid
    discussion_controller.add_user_discussion_statistics(username, room)
    discussion_json_dict = ROOMS[room].to_json_dict()
    discussion_controller.add_user_discussion_statistics(username, room)
    data = {"discussionDict": discussion_json_dict}
    if ROOMS[room].is_simulation:
        if room not in simulation_indexes:
            simulation_order[room] = "regular"
            simulation_indexes[room] = 1
        data["currentIndex"] = simulation_indexes[room]
        data["simulationOrder"] = simulation_order[room]
    configuration = discussion_controller.get_user_discussion_configuration(username, room)
    if configuration is None:
        discussion_controller.add_user_discussion_configuration(username, room,
                                                                ROOMS[room].get_configuration()["default_config"])
    else:
        discussion_json_dict["discussion"]["configuration"]["default_config"] = configuration
    socket_io.emit("join room", data=discussion_json_dict, room=request.sid)
    socket_io.emit("user joined", data=username + " joined the discussion", room=room)


@socket_io.on('leave')
def on_leave(data):
    data = json.loads(data)
    room = data['discussionId']
    username = data['username']
    leave_room(room)
    USERS[room].pop(username)
    socket_io.emit("user leave", data=username + " leaved the discussion", room=room)


@socket_io.on("add comment")
def add_comment(request_comment):
    json_string = request_comment
    comment_dict = json.loads(json_string)
    room = comment_dict['discussionId']
    response = discussion_controller.add_comment(comment_dict)
    ROOMS[room].add_comment(response["comment"])
    response["comment"] = response["comment"].to_client_dict()
    socket_io.send(response, room=room)


@socket_io.on("add alert")
def add_alert(request_alert):
    alert_dict = json.loads(request_alert)
    room = alert_dict["discussionId"]
    response = discussion_controller.add_alert(alert_dict)
    extra_data = alert_dict["extra_data"]
    if extra_data["Recipients_type"] == "parent":
        parent_user_name = discussion_controller.get_author_of_comment(alert_dict["parentId"])
        socket_io.emit("new alert", data=response["comment"].to_client_dict(), room=USERS[room][parent_user_name])
    elif extra_data["Recipients_type"] == "all":
        socket_io.emit("user joined", data=response["comment"].to_client_dict(), room=room)
    else:  # TODO: Check for list of users
        recipients_users = extra_data["users_list"]
        for user in recipients_users:
            socket_io.emit("new alert", data=response["comment"].to_client_dict(), room=USERS[room][user])


@socket_io.on("change configuration")
def change_configuration(request_configuration):
    configuration_dict = json.loads(request_configuration)
    room = configuration_dict["discussionId"]
    if not ROOMS[room].is_simulation:
        discussion_controller.change_configuration(configuration_dict)
    extra_data = configuration_dict["extra_data"]
    recipients_type = extra_data["recipients_type"]
    users_dict = dict(extra_data["users_list"])
    users_list = users_dict.keys()
    if recipients_type == "all":
        for user in get_active_discussion_users():
            discussion_controller.update_user_discussion_configuration(user, room, users_dict["all"])
        socket_io.emit("new configuration", data=users_dict["all"], room=room)
    else:
        for user in users_list:  # TODO: Check for list of users
            discussion_controller.update_user_discussion_configuration(user, room, users_dict[user])
            socket_io.emit("new configuration", data=users_dict[user], room=USERS[room][user])


@socket_io.on('connect')
def client_connect():
    print("client connected")


@socket_io.on('disconnect')
def client_disconnect():
    print("client disconnected")


@socket_io.on("next")
def handle_next(request_data):
    room = request_data['discussionId']
    if not ROOMS[room].is_simulation:
        socket_io.emit("error", data="next failed - Discussion is not a simulation", room=request.sid)
        return
    if simulation_indexes[room] <= ROOMS[room].total_comments_num:
        simulation_indexes[room] += 1
    socket_io.emit("next", room=room)


@socket_io.on("back")
def handle_back(request_data):
    room = request_data['discussionId']
    if not ROOMS[room].is_simulation:
        socket_io.emit("error", data="back failed - Discussion is not a simulation", room=request.sid)
        return
    if simulation_indexes[room] > 1:
        simulation_indexes[room] -= 1
    socket_io.emit("back", room=room)


@socket_io.on("all")
def handle_all(request_data):
    room = request_data['discussionId']
    if not ROOMS[room].is_simulation:
        socket_io.emit("error", data="all failed - Discussion is not a simulation", room=request.sid)
        return
    simulation_indexes[room] = ROOMS[room].total_comments_num
    socket_io.emit("all", room=room)


@socket_io.on("reset")
def handle_reset(request_data):
    room = request_data['discussionId']
    if not ROOMS[room].is_simulation:
        socket_io.emit("error", data="reset failed - Discussion is not a simulation", room=request.sid)
        return
    simulation_indexes[room] = 1
    socket_io.emit("reset", room=room)


@socket_io.on("change_simulation_order")
def change_order(request_data):
    room = request_data['discussionId']
    if not ROOMS[room].is_simulation:
        socket_io.emit("error", data="change sim order failed - Discussion is not a simulation")
        return
    if simulation_order[room] == "regular":
        simulation_order[room] = "chronological"
    else:
        simulation_order[room] = "regular"
    socket_io.emit("change_simulation_order", room=room)


if __name__ == '__main__':
    # app.debug = True
    socket_io.run(app, debug=False)
    print("bla")

