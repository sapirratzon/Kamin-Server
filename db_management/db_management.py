import pymongo
from bson.objectid import ObjectId
from datetime import datetime

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
        discussion.set_id(result.inserted_id.binary.hex())
        return result.inserted_id.binary.hex()

    def get_discussions(self):
        discussions = self.discussion_col.find()
        discussions_list = {}
        for discussion in discussions:
            discussions_list[discussion["_id"].binary.hex()] = discussion["title"]
        return discussions_list

    def get_discussion(self, discussion_id):
        discussion = self.discussion_col.find_one({"_id": ObjectId(discussion_id)})
        comments = self.comment_col.find({"discussionId": discussion_id})
        comments_dict = {}
        for comment in comments:
            comments_dict[comment["_id"].binary.hex()] = comment
        return discussion, comments_dict

    def add_comment(self, comment):
        comment.set_timestamp(datetime.now().timestamp())
        result = self.comment_col.insert_one(comment.to_db_dict())
        comment_id = result.inserted_id.binary.hex()
        comment.set_id(comment_id)
        discussion = self.discussion_col.find_one({'_id': ObjectId(comment.get_discussion_id())})
        if discussion["root_comment_id"] is None:
            discussion_col.update_one({"_id": ObjectId(comment.get_discussion_id())}, {"$set": {"root_comment_id": comment_id}})

        if comment.get_parent_id() is not None:
            parent_comment = self.comment_col.find_one({"_id": ObjectId(comment.get_parent_id())})
            child_ids = parent_comment["child_comments"]
            child_ids.append(comment.get_id())
            comment_col.update_one({"_id": ObjectId(comment.get_parent_id())}, {"$set": {"child_comments": child_ids}})

        return result.inserted_id.binary.hex()

    def get_comment(self, comment_id):
        comment = self.comment_col.find_one({"_id": ObjectId(comment_id)})
        return comment

    def add_new_user(self, user):
        result = self.user_col.insert_one(user.to_dict())
        return result.inserted_id.binary.hex()

    def get_user(self, username):
        user = self.user_col.find_one({"user_name": username})
        return user

    def get_users(self):
        users = []
        moderators = []
        for user in self.user_col.find():
            if user["permission"] == 1:
                users.append(user["user_name"])
            if user["permission"] == 2:
                moderators.append(user["user_name"])
        return users, moderators

    def change_user_permission(self, user, permission):
        result = self.user_col.update_one({"_id": ObjectId(user.get_user_id())}, {"$set": {"permission": permission}})
        return result.acknowledged


