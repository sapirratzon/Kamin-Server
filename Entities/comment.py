from flask import json, jsonify


class Comment:
    total_id = 0

    def __init__(self, author, text, parent, discussion_id, time_stamp=None):
        self.id = Comment.total_id
        Comment.total_id += 1
        self.author = author
        self.text = text
        self.parent = None
        self.discussion_id = discussion_id
        # extra_data dict_keys(['file:line', 'subreddit', 'from_kind', 'from', 'title', 'num_comments', 'subreddit_id',
        # 'downs', 'saved', 'from_id', 'permalink', 'name', 'url', 'ups'])
        self.extra_data = {}
        self.actions = []
        self.labels = []
        if isinstance(parent, Comment):
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.time_stamp = time_stamp

    def get_id(self):
        return self.id

    def set_id(self, input_id):
        self.id = input_id

    def get_author(self):
        return self.author

    def set_author(self, name):
        self.author = name

    def get_text(self):
        return self.text

    def set_text(self, input_text):
        self.text = input_text

    def get_parent(self):
        return self.parent

    def set_parent(self, comment):
        self.parent = comment

    def get_discussion_id(self):
        return self.discussion_id

    def set_discussion_id(self, input_id):
        self.discussion_id = input_id

    def get_depth(self):
        return self.depth

    def set_depth(self, input_depth):
        self.depth = input_depth

    def get_time_stamp(self):
        return self.time_stamp

    def set_time_stamp(self, input_time_stamp):
        self.time_stamp = input_time_stamp

    def serialize(self):
        return self.__dict__

    def get_actions(self):
        return self.actions

    def set_actions(self, input_comment_actions):
        self.actions = input_comment_actions

    def add_action(self, action):
        self.actions.append(action)

    def get_labels(self):
        return self.labels

    def set_labels(self, input_comment_labels):
        self.labels = input_comment_labels

    def add_label(self, comment_tag):
        self.labels.append(comment_tag)

    def to_json(self):
        return jsonify(id=self.id,
                       author=self.author,
                       text=self.text,
                       parent_id=self.parent.id if self.parent is not None else "",
                       disscussion_id=self.discussion_id,
                       depth=self.depth,
                       # actions=[a.__dict__ for a in self.actions],
                       time_stamp=self.time_stamp)

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "parentId": self.parent.id if isinstance(self.parent, Comment) else "",
            "discussionId": self.discussion_id,
            "depth": self.depth,
            "time_stamp": self.time_stamp,
            "labels": self.labels,
            "actions": self.actions
        }
