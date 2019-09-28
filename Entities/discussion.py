import collections


class Discussion:
    # TODO: Consider to use uuid - id generator in advanced phases
    total_id = 0

    def __init__(self):
        self.id = Discussion.total_id
        Discussion.total_id += 1
        self.categories = []
        # pointer to comments in tree
        self.branches = []
        # dict of {comment_id: comment object}
        self.comments = collections.OrderedDict()
        self.actions = []
        # currently we won't use this
        self.analysis_data = None

    def get_id(self):
        return self.id

    def set_id(self, input_id):
        self.id = input_id

    def get_category(self):
        return self.categories

    def set_category(self, input_category):
        self.categories = input_category

    def get_comments(self):
        return self.comments

    def set_comments(self, input_comments):
        self.comments = input_comments

    def get_comment(self, comment_id):
        return self.comments[comment_id]

    def add_comment(self, comment):
        self.comments[comment.id] = comment

    def get_actions(self):
        return self.actions

    def set_actions(self, input_actions):
        self.actions = input_actions

    def add_action(self, action):
        self.actions.append(action)

    def get_branches(self):
        return self.branches

    def set_branch(self, branches):
        self.branches = branches

    def get_branch(self, branch_index):
        return self.branches[branch_index]

    def get_analysis_data(self):
        return self.analysis_data

    def set_analysis_data(self, data):
        self.analysis_data = data

    def serialize(self):
        return self.__dict__
