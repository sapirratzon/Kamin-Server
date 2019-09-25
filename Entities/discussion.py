class Discussion:
    # TODO: Consider to use uuid - id generator in advanced phases
    total_id = 0

    def __init__(self):
        self._id = Discussion.total_id
        Discussion.total_id += 1
        self._category = []
        self._comments = []
        self._actions = []

        # currently we won't use this
        self._analysis_data = None

    @property
    def id(self):
        return self.id

    @id.setter
    def id(self, input_id):
        self._id = input_id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, input_category):
        self._category = input_category

    @property
    def comments(self):
        return self._comments

    @comments.setter
    def comments(self, input_comments):
        self._comments = input_comments

    def add_comment(self, comment):
        self._comments.append(comment)

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, input_actions):
        self._actions = input_actions

    def add_action(self, action):
        self._actions.append(action)

    @property
    def analysis_data(self):
        return self._analysis_data

    @analysis_data.setter
    def analysis_data(self, data):
        self._analysis_data = data

    def serialize(self):
        return self.__dict__
