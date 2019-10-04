from datetime import datetime

from flask import json, jsonify


class Comment:
    total_id = 0

    def __init__(self, *args, **kwargs):
        self.id = Comment.total_id
        Comment.total_id += 1
        self.author = kwargs.get('author', '')
        self.text = kwargs.get('text', '')
        self.parent_id = kwargs.get('parent_id', '')
        self.discussion_id = kwargs.get('discussion_id', '')
        self.extra_data = kwargs.get('extra_data', {})
        self.actions = kwargs.get('actions', [])
        self.labels = kwargs.get('labels', [])
        self.depth = kwargs.get('depth', 0)
        self.time_stamp = kwargs.get('time_stamp', datetime.now())

    """
    extra_data dict_keys(['file:line', 'subreddit', 'from_kind', 'from', 'title', 'num_comments', 'subreddit_id',
    'downs', 'saved', 'from_id', 'permalink', 'name', 'url', 'ups'])
    """

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

    def get_parent_id(self):
        return self.parent_id

    def set_parent_id(self, parnet_id):
        self.parent_id = parnet_id

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
                       parent_id=self.parent_id,
                       disscussion_id=self.discussion_id,
                       depth=self.depth,
                       # actions=[a.__dict__ for a in self.actions],
                       time_stamp=self.time_stamp)

    def to_dict(self):
        return {
            "id": self.id,
            "author": self.author,
            "text": self.text,
            "parentId": self.parent_id,
            "discussionId": self.discussion_id,
            "depth": self.depth,
            "time_stamp": self.time_stamp,
            "labels": self.labels,
            "actions": self.actions,
            "extra_data": self.extra_data
        }

    def get_depth_space(self):
        space = ""
        for i in range(1, self.get_depth()):
            space += "      "
        return space


class CommentNode(Comment):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.child_comments = kwargs.get('child_comments', [])

    def get_child_comments(self):
        return self.child_comments

    def set_child_comments(self, children):
        self.child_comments = children

    def __str__(self):
        return self.get_depth_space() + str(self.id) + ". " + self.author + ": " + str(
            self.get_time_stamp()) + ", depth = " + str(self.get_depth()) + ", parent id = " + str(
            self.parent_id)
