from Entities.analysis_data import AnalysisData
from Entities.comment import CommentNode

from db_management.db_management import DBManagement
from Entities.new_discussion import Discussion, DiscussionTree


class DiscussionController:

    db_management = DBManagement()

    def create_discussion(self, title, categories, root_comment_dict):
        disc = Discussion(title=title, categories=categories, root_comment_id=None)
        disc_id = self.db_management.create_discussion(disc)
        root_comment_dict["discussionId"] = disc_id
        root_comment_dict["parentId"] = None
        root_comment = self.add_comment(root_comment_dict)["comment"]
        discussion_tree = DiscussionTree(title=title, categories=categories, root_comment_id=root_comment.get_id(), root_comment=root_comment)
        discussion_tree.set_id(disc_id)

        return discussion_tree

    def get_discussions(self):
        discussions = self.db_management.get_discussions()
        return discussions

    def get_discussion(self, discussion_id):
        discussion, comments = self.db_management.get_discussion(discussion_id)
        root_comment_dict = comments[discussion["root_comment_id"]]
        root_comment = self.get_comment_recursive(root_comment_dict, comments)
        discussion_tree = DiscussionTree(title=discussion["title"], categories=discussion["categories"],
                                         root_comment_id=discussion["root_comment_id"], root_comment=root_comment)
        return discussion_tree

    def get_comment_recursive(self, comment_dict, comments):
        if "isAlerted" in comment_dict:
            if len(comment_dict["child_comments"]) is 0:
                comment = CommentNode(id=comment_dict["_id"].binary.hex(), author=comment_dict["author"],
                                      text=comment_dict["text"], parent_id=comment_dict["parentId"],
                                      discussion_id=comment_dict["discussionId"], extra_data=comment_dict["extra_data"],
                                      actions=comment_dict["actions"], labels=comment_dict["labels"],
                                      depth=comment_dict["depth"], timestamp=comment_dict["timestamp"],
                                      child_comments=[], is_alerted=comment_dict["isAlerted"])
                return comment

            child_list = []
            for comment_id in comment_dict["child_comments"]:
                child_comment_dict = comments[comment_id]
                child_list.append(self.get_comment_recursive(child_comment_dict, comments))

            comment = CommentNode(id=comment_dict["_id"].binary.hex(), author=comment_dict["author"], text=comment_dict["text"],
                                  parent_id=comment_dict["parentId"], discussion_id=comment_dict["discussionId"],
                                  extra_data=comment_dict["extra_data"], actions=comment_dict["actions"],
                                  labels=comment_dict["labels"], depth=comment_dict["depth"],
                                  timestamp=comment_dict["timestamp"], child_comments=child_list,
                                  is_alerted=comment_dict["isAlerted"])
            return comment
        else:
            if len(comment_dict["child_comments"]) is 0:
                comment = CommentNode(id=comment_dict["_id"].binary.hex(), author=comment_dict["author"],
                                      text=comment_dict["text"], parent_id=comment_dict["parentId"],
                                      discussion_id=comment_dict["discussionId"], extra_data=comment_dict["extra_data"],
                                      actions=comment_dict["actions"], labels=comment_dict["labels"],
                                      depth=comment_dict["depth"], timestamp=comment_dict["timestamp"],
                                      child_comments=[])
                return comment

            child_list = []
            for comment_id in comment_dict["child_comments"]:
                child_comment_dict = comments[comment_id]
                child_list.append(self.get_comment_recursive(child_comment_dict, comments))

            comment = CommentNode(id=comment_dict["_id"].binary.hex(), author=comment_dict["author"],
                                  text=comment_dict["text"],
                                  parent_id=comment_dict["parentId"], discussion_id=comment_dict["discussionId"],
                                  extra_data=comment_dict["extra_data"], actions=comment_dict["actions"],
                                  labels=comment_dict["labels"], depth=comment_dict["depth"],
                                  timestamp=comment_dict["timestamp"], child_comments=child_list)
            return comment

    def add_comment(self, comment_dict):
        comment = CommentNode(author=comment_dict["author"], text=comment_dict["text"],
                              parent_id=comment_dict["parentId"], discussion_id=comment_dict["discussionId"],
                              depth=comment_dict["depth"], child_comments=[], actions=[])
        # , labels=comment_dict["labels"])
        # Call KaminAI
        kamin_response = None
        # kamin_analyzed_data = AnalysisData(comment)
        # comment.set_actions(kamin_analyzed_data.get_comment_actions())
        # comment.set_labels(kamin_analyzed_data.get_comment_labels())
        comment.set_id(self.db_management.add_comment(comment))
        response = {"comment": comment,
                    "KaminAIresult": kamin_response}

        return response

