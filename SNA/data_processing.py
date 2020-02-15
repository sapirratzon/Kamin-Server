import csv
import json
from datetime import datetime
from TreeTools import TreeTools as tt
import pandas as pd

from Entities.comment import CommentNode


def seperated_networks_to_csv(file_path, path_to_save, ignore_deleted=True):
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
            if '[deleted]' not in edge or not ignore_deleted:
                final_edge_list.append(edge)
        df = pd.DataFrame(final_edge_list, columns=['Source', 'Target', 'Weight'])
        df.to_csv(path_to_save + "\\discussion_" + str(discussion_id) + "_weighted_edges.csv")


def whole_network_to_csv(file_path, ignore_deleted=True):
    matrix_list = []
    trees = tt.load_list_of_trees("80919_labeled_trees.txt")
    for i in range(0, 46):
        tree = trees[i]
        matrix_list.append(tt.answers_matrix(tree)['tree_map'])

    weighted_edge_list = tt.translate_matrix_list_to_weighted_edge_list(matrix_list, ignore_deleted)
    df = pd.DataFrame(weighted_edge_list, columns=['Source', 'Target', 'Weight'])
    df.to_csv("DataSet\\all_weighted_edges.csv")


"""
source - author of reply
target - target of reply
weight - count of same reply 
timestamp
text - content 
discussion idx = discussion idx in our title links file
title - title of discussion
ups
downs
"""


def get_edges_csv(ignore_deleted=True):
    trees = tt.load_list_of_trees("80919_labeled_trees.txt")
    edges = {}
    for i in range(0, len(trees)):
        tree = trees[i]
        travese_collect_edges_data(tree, edges, 'CMV-New-Discussion', i, tree['node']['extra_data']['title'],
                                   tree['node']['extra_data']['url'], True)
    gephi_edges = []
    for key in edges:
        edge = edges[key]
        gephi_edge = [edge['source'], edge['target'], edge['weight'], edge['timestamp'], ""]
        if len(edge['idxList']) > 1:
            for i in range(0, len(edge['idxList'])):
                gephi_edge[4] += str(edge["idxList"][i]) + ', '
        else:
            gephi_edge[4] = edge["idxList"][0]

        gephi_edges.append(gephi_edge)
    df = pd.DataFrame(gephi_edges,
                      columns=['Source', 'Target', 'Weight', 'Timestamp', 'DiscussionIdx'])
    df.to_csv("DataSet\\edges.csv")


def travese_collect_edges_data(tree, edges, parent_author, idx, title, url, ignore_deleted):
    node = tree['node']
    author = node['author']
    if not (ignore_deleted and ('[deleted]' in author or '[deleted]' in parent_author)):
        key = author + ' -> ' + parent_author
        if key not in edges:
            edges[key] = {}
            edges[key]["source"] = author
            edges[key]["target"] = parent_author
            edges[key]['weight'] = 0
            edges[key]["timestamp"] = node['timestamp']
            edges[key]["idxList"] = []
        edge = edges[key]
        edge['weight'] += 1
        if node['timestamp'] < edge['timestamp']:
            edge['timestamp'] = node['timestamp']
        if idx not in edge['idxList']:
            edge['idxList'].append(idx)
    for child in tree['children']:
        travese_collect_edges_data(child, edges, author, idx, title, url, ignore_deleted)


# Id - name, Label - name, DiscussionsIds, DiscussionsURL
def get_nodes_csv(ignore_deleted=True):
    trees = tt.load_list_of_trees("80919_labeled_trees.txt")
    nodes = {}
    for i in range(0, len(trees)):
        tree = trees[i]
        travese_collect_nodes_data(tree, nodes, i, tree['node']['extra_data']['title'],
                                   tree['node']['extra_data']['url'])
    nodes_disucssions_format = []
    nodes_gephi = {}
    for author in nodes:
        node = nodes[author]
        nodes_gephi[author] = [author, author, '', '', '']
        for i in range(0, len(node[2])):
            nodes_disucssions_format.append(
                (author, node[2][i], node[3][i], node[4][i]))
            nodes_gephi[author][2] += str(node[2][i]) + ', '
            nodes_gephi[author][3] += node[3][i] + ', '
            nodes_gephi[author][4] += node[4][i] + ', '
    df = pd.DataFrame(nodes_gephi.values(), columns=['Id', 'Label', 'DiscussionsIdx', 'DiscussionsTitles', 'Urls'])
    df.to_csv("DataSet\\all_nodes_data.csv")
    nodes_discussions_df = pd.DataFrame(nodes_disucssions_format,
                                        columns=['Id', 'DiscussionIdx', 'Discussion Title', 'Url'])
    nodes_discussions_df.to_csv("DataSet\\node_discussions.csv")
    return nodes


def travese_collect_nodes_data(tree, nodes, idx, title, url):
    node = tree['node']
    author = node['author']
    if not author in nodes:
        nodes[author] = (author, author, [], [], [])
    if idx not in nodes[author][2]:
        nodes[author][2].append(idx)
    if title not in nodes[author][3]:
        nodes[author][3].append(title)
    if url not in nodes[author][4]:
        nodes[author][4].append(url)
    for child in tree['children']:
        travese_collect_nodes_data(child, nodes, idx, title, url)


def print_title_link():
    trees = tt.load_list_of_trees("80919_labeled_trees.txt")
    with open('tiles-links.txt', 'w+') as file:
        for discussion_id in range(0, 46):
            tree = trees[discussion_id]
            title_link = str(discussion_id) + ". " + tree['node']['extra_data']['title'] + '\nlink: ' + \
                         tree['node']['extra_data']['url'] + '\n'
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
# trees = tt.load_list_of_trees("80919_labeled_trees.txt")

# print_title_link()
# get_edges_csv()
# get_nodes_csv()

trees = tt.load_list_of_trees("80919_labeled_trees.txt")
tree = trees[0]
print(tree['node'])