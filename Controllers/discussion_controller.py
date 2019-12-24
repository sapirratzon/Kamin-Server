import os

from Entities.analysis_data import AnalysisData
from Entities.comment import *
from Entities.discussion import Discussion, DiscussionTree
from TreeTools import TreeTools as tt


# TODO: implement reading discussion from file
def get_discussion_tree_tools(discussion_id=0,
                              discussion_path='resources\\discussions\\80919_labeled_trees.txt'):
    trees = tt.load_list_of_trees(discussion_path)
    root_tree = trees[discussion_id]
    discussion_tree = DiscussionTree(id=discussion_id)
    root_comment = CommentNode(author=root_tree['node']['author'], id=root_tree['node']['id'],
                               text=root_tree['node']['text'], parent_id=-1,
                               discussion_id=discussion_id, extra_data=root_tree['node']['extra_data'],
                               labels=root_tree['node']['labels'] if 'labels' in root_tree['node'] else None,
                               depth=0,
                               time_stamp=datetime.fromtimestamp(root_tree['node']['timestamp'])
                               )
    discussion_tree.set_root_comment(root_comment)
    [traverse_add_comments(child, discussion_tree, root_comment.get_id(), 1) for child in root_tree['children']]
    return discussion_tree


def traverse_add_comments(comment_tree, discussion_tree, parent_id, depth):
    comment_node = CommentNode(author=comment_tree['node']['author'], id=comment_tree['node']['id'],
                               text=comment_tree['node']['text'],
                               parent_id=parent_id, discussion_id=discussion_tree.get_id(),
                               extra_data=comment_tree['node']['extra_data'],
                               labels=comment_tree['node']['labels'] if 'labels' in comment_tree['node'] else None,
                               depth=depth, time_stamp=datetime.fromtimestamp(comment_tree['node']['timestamp'])
                               )
    discussion_tree.add_comment(comment_node)
    [traverse_add_comments(child, discussion_tree, comment_node.get_id(), depth + 1) for child in
     comment_tree['children']]
    print_traverse_in_order(discussion_tree.root_comment)


# TODO: understand how to analyze data
def analyze_discussion(discussion, comment):
    return AnalysisData(0, comment)


def add_comment(discussion, comment):
    discussion.add_comment(comment)
    analysis_data = analyze_discussion(discussion, comment)
    return analysis_data


def get_mock_discussion():
    discussion_path = 'resources\\discussions\\80919_labeled_trees.txt'
    # discussion_path = os.path.abs(__file__)
    discussion_id = 0
    trees = tt.load_list_of_trees(discussion_path)
    tree = trees[discussion_id]
    discussion_tree = DiscussionTree()
    root_comment = CommentNode(author=tree['node']['author'], id=tree['node']['id'],
                               text=tree['node']['text'], parent_id=-1,
                               discussion_id=discussion_id, extra_data=tree['node']['extra_data'],
                               labels=tree['node']['labels'] if 'labels' in tree['node'] else None,
                               depth=0,
                               time_stamp=datetime.fromtimestamp(tree['node']['timestamp'])
                               )
    discussion_tree.set_root_comment(root_comment)

    for sub_tree in tree['children']:
        node = sub_tree['node']
        comment_node = CommentNode(
            author=node['author'], text=node['text'], parent_id=root_comment.get_id(),
            discussion_id=discussion_id, extra_data=node['extra_data'],
            labels=node['labels'] if 'labels' in node else None,
            depth=1,
            time_stamp=datetime.fromtimestamp(node['timestamp'])
        )
        discussion_tree.add_comment(comment_node)

        for sub_sub_tree in sub_tree['children']:
            sub_node = sub_sub_tree['node']
            comment_node_child = CommentNode(
                author=sub_node['author'], text=sub_node['text'], parent_id=comment_node.get_id(),
                discussion_id=discussion_id, extra_data=sub_node['extra_data'],
                labels=sub_node['labels'] if sub_node.__contains__('labels') else None,
                depth=2,
                time_stamp=datetime.fromtimestamp(node['timestamp'])
            )
            discussion_tree.add_comment(comment_node_child)
            for sub_sub_sub_tree in sub_sub_tree['children']:
                sub_sub_node = sub_sub_sub_tree['node']
                sub_comment_node_child = CommentNode(
                    author=sub_sub_node['author'], text=sub_sub_node['text'], parent_id=comment_node_child.get_id(),
                    discussion_id=discussion_id, extra_data=sub_sub_node['extra_data'],
                    labels=sub_sub_node['labels'] if sub_sub_node.__contains__('labels') else None,
                    depth=3,
                    time_stamp=datetime.fromtimestamp(node['timestamp'])
                )
                discussion_tree.add_comment(sub_comment_node_child)
            comment_node_child.child_comments.sort(key=lambda c: c.get_time_stamp())
        comment_node.child_comments.sort(key=lambda c: c.get_time_stamp())
    print_traverse_in_order(discussion_tree.root_comment)
    root_comment.child_comments.sort(key=lambda c: c.get_time_stamp())

    return discussion_tree


def get_depth_space(comment):
    space = ""
    for i in range(1, comment.get_depth()):
        space += "      "
    return space


def print_traverse_in_order(comment_node):
    print(comment_node)
    [print_traverse_in_order(node) for node in comment_node.child_comments]

# get_mock_discussion()
# discussion = get_discussion_tree_tools()
# print_traverse_in_order(discussion.get_root_comment())
# print(discussion.to_json_dict())
#     print(child_comments[0].get_time_stamp())
#     print(round(child_comments[0].get_time_stamp().timestamp()))
