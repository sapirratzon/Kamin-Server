class Comment():
    total_id = 0

    def __init__(self, user_name, content, commented_to, discussion_id, time=None):
        self._id = Comment.total_id
        Comment.total_id += 1
        self._user_name = ""
        self._content = ""
        self._commented_to = None
        self._discussion_id = ""
        self._actions = []
        self._tags = []

        if not commented_to is None and not commented_to == "":
            self._depth = commented_to.depth
        else:
            self._depth = 0
        self._time = time


    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, input_id):
        self._id = input_id

    @property
    def user_name(self):
        return self.user_name

    @user_name.setter
    def user_name(self, name):
        self._user_name = name

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, input_content):
        self._content = input_content

    @property
    def commented_to(self):
        return self._commented_to

    @commented_to.setter
    def commented_to(self, comment):
        self.commented_to = comment

    @property
    def discussion_id(self):
        return self._discussion_id

    @discussion_id.setter
    def discussion_id(self, input_id):
        self._discussion_id = input_id

    @property
    def depth(self):
        return self.depth

    @depth.setter
    def depth(self, input_depth):
        self._depth = input_depth

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, input_time):
        self._time = input_time

    def serialize(self):
        return self.__dict__

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, input_comment_actions):
        self._actions = input_comment_actions

    def add_action(self, action):
        self._actions.append(action)

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, input_comment_tags):
        self._tags = input_comment_tags

    def addtag(self, comment_tag):
        self._tags.append(comment_tag)