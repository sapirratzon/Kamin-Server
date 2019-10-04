import collections
from flask import json, jsonify

from Entities.comment import Comment


class Discussion:
    # TODO: Consider to use uuid - id generator in advanced phases
    total_id = 0

    def __init__(self, *args, **kwargs):
        self.id = Discussion.total_id
        Discussion.total_id += 1
        self.categories = kwargs.get('categories', [])
        self.comments_list = kwargs.get('comments_list', [])
        # dict of {comment_id: comment object}
        self.comments_dict = kwargs.get('comments_dict', {})
        self.actions = kwargs.get('actions', [])

    def get_id(self):
        return self.id

    def set_id(self, input_id):
        self.id = input_id

    def get_category(self):
        return self.categories

    def set_category(self, input_category):
        self.categories = input_category

    def get_comments_list(self):
        return self.comments_list

    def set_comments_list(self, comments):
        self.comments_list = comments

    def get_comments_dict(self):
        return self.comments_dict

    def set_comments_dict(self, input_comments):
        self.comments_dict = input_comments

    def get_comment(self, comment_id):
        return self.comments_dict[comment_id]

    def add_comment(self, comment):
        self.comments_dict[comment.id] = comment

    def get_actions(self):
        return self.actions

    def set_actions(self, input_actions):
        self.actions = input_actions

    def add_action(self, action):
        self.actions.append(action)

    def to_json(self):
        return jsonify(id=self.id,
                       categories=[c.__dict__ for c in self.categories],
                       comments_list=[comment.to_dict() for comment in self.comments_dict.values()],
                       comments_dict={comment.id: comment.to_dict() for comment in self.comments_dict.values()},
                       actions=[a.__dict__ for a in self.actions]
                       )

    def to_dict(self):
        return {
            "id": self.id,
            "categories": self.categories,
            "branches": [[comment.to_dict() for comment in branch] for branch in self.branches],
            "comments": self.comments_dict.values(),
            "actions": self.actions
        }


class DiscussionTree(Discussion):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_comment = kwargs.get('root_comment', None)

    def get_root_comment(self):
        return self.root_comment

    def set_root_comment(self, comment):
        self.root_comment = comment

    def add_comment(self, comment):
        super().add_comment(comment)
        parent_comment = self.comments_dict[comment.parent_id]
        parent_comment.add(comment)

    def to_json(self):
        discussion = super().to_json()
