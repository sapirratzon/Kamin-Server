from datetime import datetime
from TreeTools import TreeTools as tt
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
            if '[deleted]' not in edge or not remove_deleted:
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


# Id - name, Label - name, DiscussionsIds, DiscussionsURL
def get_nodes_csv():
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


def travese_collect_nodes_data(tree, nodes, i, title, url):
    node = tree['node']
    author = node['author']
    if not author in nodes:
        nodes[author] = (author, author, [], [], [])
        # nodes[author] = (author, author, str(i), title, url)
    if i not in nodes[author][2]:
        nodes[author][2].append(i)
    if title not in nodes[author][3]:
        nodes[author][3].append(title)
    if url not in nodes[author][4]:
        nodes[author][4].append(url)
    # else:
    #     if str(i) not in nodes[author][2]:
    #         nodes[author][2] += ', ' + i
    #     if title not in nodes[author][3]:
    #         nodes[author][3] += ', ' + title
    #     if url not in nodes[author][4]:
    #         nodes[author][4] += ', ' + url
    # node[node['author']][3] += ',' + node['extra_data']['title']
    # node[node['author']][3] += ',' + node['extra_data']['url']

    for child in tree['children']:
        travese_collect_nodes_data(child, nodes, i, title, url)


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
whole_network_to_csv('', True)
# get_nodes_csv()
