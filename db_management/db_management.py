import pymongo
from bson.objectid import ObjectId
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://gal_kamin:gal123456@cluster0-erofa.mongodb.net/test?retryWrites=true&w=majority")

kamin_db = client["kamindb"]

discussion_col = kamin_db["discussion"]
comment_col = kamin_db["comment"]
user_col = kamin_db["user"]
user_discussion_statistics_col = kamin_db["userDiscussionStatistics"]


class DBManagement:
    kamin_db = client["kamindb"]
    discussion_col = kamin_db["discussion"]
    comment_col = kamin_db["comment"]
    user_col = kamin_db["user"]
    user_discussion_statistics_col = kamin_db["userDiscussionStatistics"]

    def create_discussion(self, discussion):
        result = self.discussion_col.insert_one(discussion.to_dict())
        discussion.set_id(result.inserted_id.binary.hex())
        return result.inserted_id.binary.hex()

    def get_discussion(self, discussion_id):
        discussion = self.discussion_col.find_one({"_id": ObjectId(discussion_id)})
        comments = self.comment_col.find({"discussionId": discussion_id})
        comments_dict = {}
        for comment in comments:
            comments_dict[comment["_id"].binary.hex()] = comment
        return discussion, comments_dict

    def get_discussion_details(self, discussion_id):
        discussion = self.discussion_col.find_one({"_id": ObjectId(discussion_id)})
        return discussion

    def add_comment(self, comment):
        comment.set_timestamp(datetime.now().timestamp())
        result = self.comment_col.insert_one(comment.to_db_dict())
        comment_id = result.inserted_id.binary.hex()
        comment.set_id(comment_id)
        discussion = self.discussion_col.find_one({"_id": ObjectId(comment.get_discussion_id())})
        if discussion["root_comment_id"] is None:
            discussion_col.update_one({"_id": ObjectId(comment.get_discussion_id())},
                                      {"$set": {"root_comment_id": comment_id}})

        if comment.get_parent_id() is not None:
            parent_comment = self.comment_col.find_one({"_id": ObjectId(comment.get_parent_id())})
            child_ids = parent_comment["child_comments"]
            child_ids.append(comment.get_id())
            comment_col.update_one({"_id": ObjectId(comment.get_parent_id())}, {"$set": {"child_comments": child_ids}})

        # statistics
        self.update_statistics(comment)

        return result.inserted_id.binary.hex()

    def update_statistics(self, comment):
        # author statistics
        statistics = self.get_user_discussion_statistics(comment.get_author(), comment.get_discussion_id())
        commented_users = dict(statistics["commented_users"])
        username = self.get_user_by_id(comment.get_parent_id())["user_name"]
        if commented_users.__contains__(username):
            commented_users[username] += 1
        else:
            commented_users[username] = 1
        # num of words statistics
        text = comment["text"]
        num_of_words = len(text.split())
        total_words = statistics["total_words_num"]
        total_words += num_of_words
        self.user_discussion_statistics_col.update_one({"_id": ObjectId(statistics["_id"])},
                                                       {"$set": {"commented_users": commented_users,
                                                                 "total_words_num": total_words}})
        # parent statistics
        parent_statistics = self.get_user_discussion_statistics(comment.get_parent_id(), comment.get_discussion_id())
        responded_users = dict(parent_statistics["responded_users"])
        if responded_users.__contains__(comment.get_author()):
            responded_users[comment.get_author()] += 1
        else:
            responded_users[comment.get_author()] = 1
        self.user_discussion_statistics_col.update_one({"_id": ObjectId(parent_statistics["_id"])},
                                                       {"$set": {"responded_users": responded_users}})
        # discussion statistics
        discussion = self.get_discussion_details(comment.get_discussion_id())
        total_comments_num = discussion["total_comments_num"]
        self.update_discussion(comment.get_discussion_id(), "total_comments_num", total_comments_num + 1)

    def get_user_discussion_statistics(self, username, discussion_id):
        user_statistics = {}
        statistics = self.user_discussion_statistics_col.find_one({"user": username, "discussion_id": discussion_id})
        if statistics is not None:
            total_words = statistics["total_words_num"]
            commented_users = dict(statistics["commented_users"])
            num_of_commented_users = len(commented_users.keys())
            num_of_comments = sum(commented_users.values())
            responded_users = dict(statistics["responded_users"])
            num_of_responded_users = len(responded_users.keys())
            num_of_responses = sum(responded_users.values())
            user_statistics = {"total_words": total_words, "num_of_commented_users": num_of_commented_users,
                               "num_of_comments": num_of_comments, "num_of_responded_users": num_of_responded_users,
                               "num_of_responses": num_of_responses}
        return user_statistics

    def get_discussion_statistics(self, discussion_id):
        statistics_list = self.user_discussion_statistics_col.find_one({"discussion_id": discussion_id})
        max_commented_user = ""
        max_commented_num = 0
        max_responded_user = ""
        max_responded_num = 0
        discussion = self.get_discussion_details(discussion_id)
        num_of_participants = discussion["num_of_participants"]
        total_comments_num = discussion["total_comments_num"]
        for user_statistics in statistics_list:
            commented_users = dict(user_statistics["commented_users"])
            if len(commented_users.keys()) > max_commented_num:
                max_commented_user = user_statistics["user_id"]
            responded_users = dict(user_statistics["responded_users"])
            if len(responded_users.keys()) > max_responded_num:
                max_responded_user = user_statistics["user_id"]
        discussion_statistics = {"max_commented_user": max_commented_user, "max_responded_user": max_responded_user,
                                 "num_of_participants": num_of_participants, "total_comments_num": total_comments_num}
        return discussion_statistics

    def update_discussion(self, discussion_id, col_to_set, updated_value):
        result = self.discussion_col.update_one({"_id": ObjectId(discussion_id)}, {"$set": {col_to_set: updated_value}})
        return result.acknowledged

    def get_comment(self, comment_id):
        comment = self.comment_col.find_one({"_id": ObjectId(comment_id)})
        return comment

    def add_new_user(self, user):
        result = self.user_col.insert_one(user.to_dict())
        return result.inserted_id.binary.hex()

    def get_user(self, username):
        user = self.user_col.find_one({"user_name": username})
        return user

    def get_user_by_id(self, user_id):
        user = self.user_col.find_one({"_id": ObjectId(user_id)})
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
