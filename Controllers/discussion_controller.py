import os

from Entities.analysis_data import AnalysisData
from Entities.comment import *
from Entities.discussion import Discussion, DiscussionTree
from TreeTools import TreeTools as tt


# TODO: implement reading discussion from file
def get_discussion_tree_tools(discussion_id=0,
                              discussion_path='C:\\Users\\ronel\\PycharmProjects\\Kamin-Server\\80919_labeled_trees.txt'):
    trees = tt.load_list_of_trees(discussion_path)
    root_tree = trees[discussion_id]
    discussion_tree = DiscussionTree()
    root_comment = CommentNode(author=root_tree['node']['author'], text=root_tree['node']['text'], parent_id=-1,
                               discussion_id=discussion_id, extra_data=root_tree['node']['extra_data'],
                               labels=root_tree['node']['labels'] if root_tree['node'].__contains__('labels') else None,
                               depth=0,
                               time_stamp=datetime.fromtimestamp(root_tree['node']['timestamp'])
                               )
    discussion_tree.set_root_comment(root_comment)
    [add_comments_in_order(child, discussion_tree, root_comment.get_id(), 1) for child in root_tree['children']]
    return discussion_tree


def add_comments_in_order(comment_tree, discussion_tree, parent_id, depth):
    comment_node = CommentNode(author=comment_tree['node']['author'], text=comment_tree['node']['text'],
                               parent_id=parent_id, discussion_id=discussion_tree.get_id(),
                               extra_data=comment_tree['node']['extra_data'],
                               labels=comment_tree['node']['labels'] if comment_tree['node'].__contains__(
                                   'labels') else None,
                               depth=depth, time_stamp=datetime.fromtimestamp(comment_tree['node']['timestamp'])
                               )
    discussion_tree.add_comment(comment_node)
    [add_comments_in_order(child, discussion_tree, comment_node.get_id(), depth + 1) for child in
     comment_tree['children']]


# TODO: understand how to analyze data
def analyze_discussion(discussion, comment):
    return AnalysisData(0, comment)


def add_comment(discussion, comment):
    discussion.add_comment(comment)
    analysis_data = analyze_discussion(discussion, comment)
    return analysis_data


def get_mock_discussion():
    discussion_path = 'C:\\Users\\ronel\\PycharmProjects\\Kamin-Server\\80919_labeled_trees.txt'
    # discussion_path = os.path.abs(__file__)
    discussion_id = 0
    trees = tt.load_list_of_trees(discussion_path)
    tree = trees[discussion_id]
    discussion_tree = DiscussionTree()
    root_comment = CommentNode(author=tree['node']['author'], text=tree['node']['text'], parent_id=-1,
                               discussion_id=discussion_id, extra_data=tree['node']['extra_data'],
                               labels=tree['node']['labels'] if tree['node'].__contains__('labels') else None,
                               depth=0,
                               time_stamp=datetime.fromtimestamp(tree['node']['timestamp'])
                               )
    discussion_tree.set_root_comment(root_comment)

    for sub_tree in tree['children']:
        node = sub_tree['node']
        comment_node = CommentNode(
            author=node['author'], text=node['text'], parent_id=root_comment.get_id(),
            discussion_id=discussion_id, extra_data=node['extra_data'],
            labels=node['labels'] if node.__contains__('labels') else None,
            depth=1,
            time_stamp=datetime.fromtimestamp(node['timestamp'])
        )
        discussion_tree.add_comment(comment_node)

        for sub_sub_tree in sub_tree['children']:
            node = sub_sub_tree['node']
            comment_node_child = CommentNode(
                author=node['author'], text=node['text'], parent_id=comment_node.get_id(),
                discussion_id=discussion_id, extra_data=node['extra_data'],
                labels=node['labels'] if node.__contains__('labels') else None,
                depth=2,
                time_stamp=datetime.fromtimestamp(node['timestamp'])
            )
            discussion_tree.add_comment(comment_node_child)
        comment_node.child_comments.sort(key=lambda c: c.get_time_stamp())
    root_comment.child_comments.sort(key=lambda c: c.get_time_stamp())
    """
    [print(get_depth_space(comment) + str(comment.id) + ". " + comment.author + ":" + str(
        comment.get_time_stamp()) + ", depth = " + str(comment.get_depth()) + ", parent id = " + str(comment.parent_id))
     for comment in discussionTree.comments_list]
    print("\n~~~~~~~~~After Sort By Time Stamp~~~~~~~~~\n")
    [print(get_depth_space(comment) + str(comment.id) + ". " + comment.author + ":" + str(
        comment.get_time_stamp()) + ", depth = " + str(comment.get_depth()) + ", parent id = " + str(comment.parent_id))
     for comment in discussion_tree.comments_list]
        """
    print("\n~~~~~~~~~~~~Traverse In Order~~~~~~~~~~~~~\n")
    traverse_in_order(discussion_tree.root_comment)

    return discussion_tree


def get_depth_space(comment):
    space = ""
    for i in range(1, comment.get_depth()):
        space += "      "
    return space


def traverse_in_order(comment_node):
    print(comment_node)
    [traverse_in_order(node) for node in comment_node.child_comments]


# discussion = get_discussion()
# traverse_in_order(discussion.get_root_comment())
# print(discussion.to_json_dict())
#     print(child_comments[0].get_time_stamp())
#     print(round(child_comments[0].get_time_stamp().timestamp()))
