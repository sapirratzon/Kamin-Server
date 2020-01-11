from _datetime import datetime

import TreeTools.TreeTools as tt
import pandas as pd

from Entities.comment import CommentNode


def seperated_networks_to_csv(file_path, path_to_save, remove_deleted=True):
    trees = tt.load_list_of_trees("80919_labeled_trees.txt")
    # tt.extract_networks_from_trees(trees, ['DA', 'QU', 'MN'], 'networks.csv' )
    first_tree = trees[0]
    root_comment = CommentNode(author=first_tree['node']['author'], text=first_tree['node']['text'], parent_id=None,
                               discussion_id=first_tree, extra_data=first_tree['node']['extra_data'],
                               labels=first_tree['node']['labels'] if 'labels' in first_tree['node'] else None,
                               depth=0, time_stamp=datetime.fromtimestamp(first_tree['node']['timestamp']),
                               child_comments=[])

    for discussion_id in range(0, 46):
        tree = trees[discussion_id]
        root_comment = CommentNode(author=tree['node']['author'], text=tree['node']['text'], parent_id=None,
                                   discussion_id=tree, extra_data=tree['node']['extra_data'],
                                   labels=tree['node']['labels'] if 'labels' in tree['node'] else None,
                                   depth=0, time_stamp=datetime.fromtimestamp(tree['node']['timestamp']),
                                   child_comments=[])
        matrix = tt.answers_matrix(tree)
        weighted_edge_list = tt.translate_matrix_to_edgelist(matrix['tree_map'], True)
        final_edge_list = []
        for edge in weighted_edge_list:
            if not '[deleted]' in edge or not remove_deleted:
                final_edge_list.append(edge)
        df = pd.DataFrame(final_edge_list, columns=['Source', 'Target', 'Weight'])
        df.to_csv(path_to_save + "\\discussion_" + str(discussion_id) + "_weighted_edges.csv")


def whole_network_to_csv(file_path, remove_deleted=True):
    matrix_list = []
    trees = tt.load_list_of_trees("80919_labeled_trees.txt")
    for i in range(0, 46):
        tree = trees[i]
        matrix_list.append(tt.answers_matrix(tree)['tree_map'])

    weighted_edge_list = tt.translate_matrix_list_to_weighted_edge_list(matrix_list, remove_deleted)
    df = pd.DataFrame(weighted_edge_list, columns=['Source', 'Target', 'Weight'])
    df.to_csv("DataSet\\all_weighted_edges.csv")


def print_title_link():
    trees = tt.load_list_of_trees("80919_labeled_trees.txt")
    with open('tiles-links.txt','w+') as file:
        for discussion_id in range(0, 46):
            tree = trees[discussion_id]
            title_link = str(discussion_id)+". "+ tree['node']['extra_data']['title'] +'\nlink: ' +tree['node']['extra_data']['url'] + '\n'
            file.write(title_link)
            print(title_link)




# seperated_networks_to_csv('',"DataSet\\seperated_weighted")
# whole_network_to_csv('', False)

trees = tt.load_list_of_trees("80919_labeled_trees.txt")
# tt.extract_networks_from_trees(trees, ['DA', 'QU', 'MN'], 'networks.csv' )
first_tree = trees[0]
root_comment = CommentNode(author=first_tree['node']['author'], text=first_tree['node']['text'], parent_id=None,
                           discussion_id=first_tree, extra_data=first_tree['node']['extra_data'],
                           labels=first_tree['node']['labels'] if 'labels' in first_tree['node'] else None,
                           depth=0, time_stamp=datetime.fromtimestamp(first_tree['node']['timestamp']),
                           child_comments=[])

# features =list(first_tree['node'].keys())
# features.extend(root_comment.extra_data.keys())
# print(root_comment.extra_data['num_comments'])
# print(features)
trees = tt.load_list_of_trees("80919_labeled_trees.txt")

print_title_link()