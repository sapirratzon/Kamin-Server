from datetime import datetime
import bisect
from Entities.analysis_data import AnalysisData
from Entities.comment import *
from Entities.discussion import Discussion, DiscussionTree
import TreeTools as tt


# TODO: implement reading discussion from file
def get_discussion(id=0, ):
    return Discussion()


# TODO: understand how to analyze data
def analyze_discussion(discussion, comment):
    return AnalysisData(0, comment)


def add_comment(discussion, comment):
    discussion.add_comment(comment)
    analysis_data = analyze_discussion(discussion, comment)
    return analysis_data


def get_mock_discussion():
    discussion_path = 'C:\\Users\\ronel\\PycharmProjects\\TreeTools\\80919_labeled_trees.txt'
    discussion_id = 0
    trees = tt.load_list_of_trees(discussion_path)
    tree = trees[discussion_id]
    discussion = DiscussionTree()
    root_comment = CommentNode(author=tree['node']['author'], text=tree['node']['text'], parent_id=-1,
                               discussion_id=discussion_id, extra_data=tree['node']['extra_data'],
                               labels=tree['node']['labels'] if tree['node'].__contains__('labels') else None,
                               depth=0,
                               time_stamp=datetime.fromtimestamp(tree['node']['timestamp'])
                               )
    discussion.set_root_comment(root_comment)
    # print(root_comment.get_text())
    child_comments = []

    for sub_tree in tree['children']:
        node = sub_tree['node']
        comment_node = CommentNode(
            author=node['author'], text=node['text'], parent_id=root_comment.get_id(),
            discussion_id=discussion_id, extra_data=node['extra_data'],
            labels=node['labels'] if node.__contains__('labels') else None,
            depth=1,
            time_stamp=datetime.fromtimestamp(node['timestamp'])
        )
        discussion.comments_dict[comment_node.id] = comment_node
        discussion.comments_list.append(comment_node)
        for sub_sub_tree in sub_tree['children']:
            node = sub_sub_tree['node']
            comment_node = CommentNode(
                author=node['author'], text=node['text'], parent_id=comment_node.get_id(),
                discussion_id=discussion_id, extra_data=node['extra_data'],
                labels=node['labels'] if node.__contains__('labels') else None,
                depth=2,
                time_stamp=datetime.fromtimestamp(node['timestamp'])
            )
            comment_node.child_comments.append(comment_node)
            discussion.comments_dict[comment_node.id] = comment_node
            discussion.comments_list.append(comment_node)
        comment_node.child_comments.sort(key=lambda c: c.get_time_stamp())
        root_comment.child_comments.append(comment_node)

    [print(get_depth_space(comment) + str(comment.id) + ". " + comment.author + ":" + str(
        comment.get_time_stamp()) + ", depth = " + str(comment.get_depth()) + ", parent id = " + str(comment.parent_id))
     for comment in discussion.comments_list]
    child_comments.sort(key=lambda c: c.get_time_stamp())
    sorted(child_comments, key=lambda c: c.timestamp, reverse=True)
    print("\n~~~~~~~~~After Sort By Time Stamp~~~~~~~~~\n")
    [print(get_depth_space(comment) + str(comment.id) + ". " + comment.author + ":" + str(
        comment.get_time_stamp()) + ", depth = " + str(comment.get_depth()) + ", parent id = " + str(comment.parent_id))
     for comment in discussion.comments_list]
    # print_in_order(discussion.root_comment)

    return discussion


def get_depth_space(comment):
    space = ""
    for i in range(1, comment.get_depth()):
        space += "      "
    return space


def printInorder(comment_node):
    if comment_node:
        for child_comment in comment_node.get_child_comments():
            printInorder(comment_node)

        print(get_depth_space(comment_node) + str(comment_node.id) + ". " + comment_node.author + ":" + str(
            comment_node.get_time_stamp()) + ", depth = " + str(comment_node.get_depth()) + ", parent id = " + str(
            comment_node.parent_id))


def print_in_order(comment_node):
    [printInorder(node) for node in comment_node.child_comments]
    print(get_depth_space(comment_node) + str(comment_node.id) + ". " + comment_node.author + ":" + str(
        comment_node.get_time_stamp()) + ", depth = " + str(comment_node.get_depth()) + ", parent id = " + str(
        comment_node.parent_id))


# Iterative function for inorder tree traversal
def inOrder(comment_node):
    # Set current to root of binary tree
    current = comment_node
    stack = []  # initialize stack
    done = 0

    while True:

        # Reach the left most Node of the current Node
        if len(current.get_child_comments()):

            # Place pointer to a tree node on the stack
            # before traversing the node's left subtree
            stack.append(current)

            current = current.left

            # BackTrack from the empty subtree and visit the Node
        # at the top of the stack; however, if the stack is
        # empty you are done
        elif (stack):
            current = stack.pop()
            print(get_depth_space(comment_node) + str(comment_node.id) + ". " + comment_node.author + ":" + str(
                comment_node.get_time_stamp()) + ", depth = " + str(comment_node.get_depth()) + ", parent id = " + str(
                comment_node.parent_id))  # Python 3 printing

            # We have visited the node and its left
            # subtree. Now, it's right subtree's turn
            current = current.right

        else:
            break

    print()


get_mock_discussion()

#     print(child_comments[0].get_time_stamp())
#     print(round(child_comments[0].get_time_stamp().timestamp()))
