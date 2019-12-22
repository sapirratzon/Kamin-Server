import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://gal_kamin:gal123456@cluster0-erofa.mongodb.net/test?retryWrites=true&w=majority")

kamin_db = client["kamindb"]

discussion_col = kamin_db["discussion"]
comment_col = kamin_db["comment"]
user_col = kamin_db["user"]


class DBManagement:
    kamin_db = client["kamindb"]
    discussion_col = kamin_db["discussion"]
    comment_col = kamin_db["comment"]
    user_col = kamin_db["user"]

    def create_discussion(self, discussion):
        result = self.discussion_col.insert_one(discussion.to_dict())
        discussion.set_id(result.inserted_id.binary)
        return result.inserted_id.binary

    def get_discussion(self, discussion_id):
        discussion = self.discussion_col.find({"_id": ObjectId(discussion_id)})
        comments = self.comment_col.find({"discussion_id": discussion_id})
        return discussion, comments

    def add_comment(self, comment):
        result = self.comment_col.insert_one(comment.to_dict())
        comment_id = result.inserted_id.binary
        comment.set_id(comment_id)
        discussion = self.discussion_col.find_one({'_id': ObjectId(comment.get_discussion_id())})
        # discussion = self.discussion_col.find({"_id": comment.get_discussion_id()})
        if discussion["root_comment_id"] is None:
            discussion_col.update_one({"_id": ObjectId(comment.get_discussion_id())}, {"$set": {"root_comment_id": comment_id}})

        if comment.get_parent_id() is not None:
            parent_comment = self.comment_col.find_one({"_id": ObjectId(comment.get_parent_id())})
            child_ids = parent_comment["child_comments"]
            child_ids.append(comment.get_id())
            comment_col.update_one({"_id": ObjectId(comment.get_parent_id())}, {"$set": {"child_comments": child_ids}})

        return result.inserted_id.binary

