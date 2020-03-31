

class AnalysisData:

    def __init__(self, *args, **kwargs):
        self.discussion_id = kwargs.get('discussion_id', "")
        self.triggered_comment_id = kwargs.get('triggered_comment_id', "")
        self.relevant_users = kwargs.get('relevant_users', [])
        self.comment_labels = kwargs.get('comment_labels', {})
        self.actions = kwargs.get('actions', {})

    def get_discussion_id(self):
        return self.discussion_id

    def set_discussion_id(self, discussion_id):
        self.discussion_id = discussion_id

    def get_triggered_comment(self):
        return self.triggered_comment_id

    def set_triggered_comment(self, comment_id):
        self.triggered_comment_id = comment_id

    def get_relevant_users(self):
        return self.relevant_users

    def set_relevant_users(self, relevant_users):
        self.relevant_users = relevant_users

    def get_comment_labels(self):
        return self.comment_labels

    def set_comment_labels(self, comment_labels):
        self.comment_labels = comment_labels

    def get_actions(self):
        return self.actions

    def set_actions(self, actions):
        self.actions = actions



