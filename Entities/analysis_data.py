from enum import Enum


class AnalysisData:

    def __init__(self, discussion_id, triggering_comment):
        self._discussion_id = discussion_id
        self._triggered_by = triggering_comment
        # general actions for discussion
        self._general_actions = []

        # list of actions for each comment <commentId,[actions]>
        self._comment_actions = {}

        # we probably won't need this but just in case
        self._comment_tags = {}

    @property
    def discussion_id(self):
        return self._discussion_id

    @discussion_id.setter
    def discussion_id(self, input_id):
        self._discussion_id = input_id

    @property
    def triggered_by(self):
        return self._triggered_by

    @triggered_by.setter
    def triggered_by(self, comment):
        self.triggered_by = comment

    @property
    def general_actions(self):
        return self._general_actions

    @general_actions.setter
    def general_actions(self, actions):
        self._general_actions = actions

    def add_general_action(self, action):
        self._general_actions.append(action)

    @property
    def comment_actions(self):
        return self._comment_actions

    @comment_actions.setter
    def comment_actions(self, comments_actions):
        self._comment_actions = comments_actions

    def add_comment_actions(self, comment, actions):
        if not self.comment_actions.get(comment):
            self.comment_actions[comment] = []
        self.comment_actions[comment].append(actions)

    def serialize(self):
        return self.__dict__

class CommentAction(Enum):
    BoldComment = 1
    ReportModerator = 2
    Meaningful = 3


class Action(Enum):
    WarnDiscussionEscalating = 1
    PositiveReinforcementForAll = 2
