import collections
from flask import json, jsonify

from Entities.comment import Comment, CommentNode


class Discussion:
    # TODO: Consider to use uuid - id generator in advanced phases
    total_id = 0

    def __init__(self, *args, **kwargs):
        id = kwargs.get('id', None)
        if id is not None:
            self.id = id
        else:
            self.id = Discussion.total_id
            Discussion.total_id += 1
        self.title = kwargs.get('title', "")
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
        self.comments_list.append(comment)

    def get_actions(self):
        return self.actions

    def set_actions(self, input_actions):
        self.actions = input_actions

    def add_action(self, action):
        self.actions.append(action)

    def to_dict(self):
        return {
                'id': self.id,
                'categories': [c.__dict__ for c in self.categories],
                # 'comments_list': [comment.to_dict() for comment in self.comments_dict.values()],
                # 'comments_dict': {comment.id: comment.to_dict() for comment in
                #                   self.comments_dict.values()},
                'title': self.title,
                'actions': [a.__dict__ for a in self.actions]
                }


class DiscussionTree(Discussion):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_comment = kwargs.get('root_comment', None)
        tree = kwargs.get('tree', None)
        if tree != None:
            json_dict_to_discussion_tree(tree, self)

    def get_root_comment(self):
        return self.root_comment

    def set_root_comment(self, comment):
        self.root_comment = comment
        self.comments_list.append(comment)
        self.comments_dict[comment.get_id()] = comment
        if 'title' in comment.extra_data:
            self.title = comment.get_extra_data()['title']

    def add_comment(self, comment: CommentNode):
        super().add_comment(comment)
        parent_comment = self.comments_dict[comment.parent_id]
        parent_comment.get_child_comments().append(comment)

    def to_json_dict(self):
        discussion = self.to_dict()
        discussion_json_tree = tree_to_json(self.root_comment)
        return {'discussion': discussion, 'tree': discussion_json_tree}


def json_dict_to_discussion_tree(root_tree, discussion):
    discussion.set_root_comment(root_tree['id'])


def tree_to_json(comment_node):
    return {'node': comment_node.to_dict(),
            'children': [tree_to_json(child) for child in comment_node.get_child_comments()]}
