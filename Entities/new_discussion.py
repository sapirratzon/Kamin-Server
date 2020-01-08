
class Discussion:

    def __init__(self, *args, **kwargs):
        self.discussion_id = kwargs.get('id', 0)
        self.title = kwargs.get('title', "")
        self.categories = kwargs.get('categories', [])
        self.root_comment_id = kwargs.get('root_comment_id', 0)

    def get_id(self):
        return self.discussion_id

    def set_id(self, discussion_id):
        self.discussion_id = discussion_id

    def get_title(self):
        return self.title

    def set_title(self, title):
        self.title = title

    def get_categories(self):
        return self.categories

    def set_categories(self, input_categories):
        self.categories = input_categories

    def get_root_comment_id(self):
        return self.root_comment_id

    def set_root_comment_id(self, comment_id):
        self.root_comment_id = comment_id

    def to_dict(self):
        return {
                'categories': self.categories,
                'title': self.title,
                'root_comment_id': self.root_comment_id
                }


class DiscussionTree(Discussion):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root_comment = kwargs.get('root_comment', None)

    def get_root_comment(self):
        return self.root_comment

    def set_root_comment(self, comment):
        self.root_comment = comment

    def to_json_dict(self):
        discussion = self.to_dict()
        discussion_json_tree = tree_to_json(self.root_comment)
        return {'discussion': discussion, 'tree': discussion_json_tree}


def tree_to_json(comment_node):
    return {'node': comment_node.to_client_dict(),
            'children': [tree_to_json(child) for child in comment_node.get_child_comments()]}