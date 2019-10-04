import TreeTools as tt
from Entities.discussion import *
from Entities.comment import *
import collections


def tree_to_discussion(discussion_path, discussion_id):
    trees = tt.load_list_of_trees(discussion_path)
    tree = trees[discussion_id]
    discussion = DiscussionTree()
    # print(tree['children'])
    for child_tree in tree['children']:
        print(child_tree)

    # print(tree['node']['author'])
    # root_node = tree['node']
    # root_comment = CommentNode(author=tree['node']['author'], text=tree['node']['text'], parent_id=-1,
    #                            discussion_id=discussion_id, extra_data=tree['node']['extra_data'],
    #                            labels=tree['node']['labels'] if tree['node'].__contains__('labels') else None,
    #                            depth=0,
    #                            time_stamp=tree['node']['timestamp']
    #                            )
    # discussion.set_root_comment(root_comment)
    # print(discussion)

def update_discussion_branches(discussion_path, discussion_id):

    discussion = Discussion()

    trees = tt.load_list_of_trees(discussion_path)
    tree = trees[discussion_id]
    branches = tt.get_branches(tree)
    # discussion.set_branches(branches)
    comments = collections.OrderedDict()
    for branch in branches:
        parent = None
        for node in branch:
            comment = comment.Comment(node['author'], node['text'], parent, discussion_id, node['timestamp'])
            parent = comment
            comments[comment.get_id()] = comment

            # discussion.set_comments(comment)
    return comments


path = 'C:\\Users\\ronel\\PycharmProjects\\TreeTools\\80919_labeled_trees.txt'
tree_to_discussion(discussion_path=path, discussion_id=0)

# comments = update_discussion_branches(path, 0)
# print(comments)

# branch = branches[0]
# branch1 = branches[1]
# branch2 = branches[2]
# branch3 = branches[3]
# print('First branch has the length of', len(branch))
# print('An element in branch is the node we saw above - it is a dictionary and has the following keys:', branch[0].keys())
# print('\nLets print the discussion1:\n')
# for node in branch:
#     print(node['author'], ':', node['text'][:50], '...')
#
# print('\nLets print the discussion2:\n')
# for node1 in branch1:
#     print(node1['author'], ':', node1['text'][:50], '...')
#
# print('\nLets print the discussion3:\n')
# for node2 in branch2:
#     print(node2['author'], ':', node2['text'][:50], '...')
#
# print('\nLets print the discussion4:\n')
# for node3 in branch3:
#     print(node3['author'], ':', node3['text'][:50], '...')

#
# print('\nNow let\'s take a closer look at the last node in this branch - it has an extra key "labels":')
# print(branch[2].keys())
# print('The labels are:', branch[2]['labels'])

# How many labeled nodes do we have in this tree?
# labeled_nodes = [node for node in nodes if 'labels' in node and len(node['labels']['consolidated']) > 0]
# print('Labeled nodes:', len(labeled_nodes), 'Out of total nodes:', len(nodes))
#
# Surprise! All labels except the root are labeled.
# counted_labels = Counter([label for node in labeled_nodes for label in node['labels']['consolidated']])
# print('Our label frequencies for this tree are:')
# print(counted_labels)

# Now let's dive a bit into the text - sometimes it contains 'mentions', 'quotes' or is deleted/removed.
# print('Deleted nodes:', len([node['text'] for node in nodes if node['text'] == '[deleted]' or
#                             node['text'] == '[removed]']))
# # The nodes usually are deleted for two reasons: a user changes his mind and deletes his post,
# # or an admin removes it for violating rules
# texts_with_quotes = [node['text'] for node in nodes if '<quote>' in node['text']]
# print('Texts that contain quotes:', len(texts_with_quotes))
# print('\n',texts_with_quotes[0], '\n')
# texts_with_mentions = [node['text'] for node in nodes if '/u/' in node['text']]
# print('Texts that contain mentions:', len(texts_with_mentions))
# # Oops.. no mentions here. May be in another tree?
# nodes_with_mentions = [node for node in tt.get_nodes(trees[1]) if '/u/' in node['text']]
# print('Texts that contain mentions (another tree):', len(nodes_with_mentions))
# # Bingo! Found a mention.
# print('\n', nodes_with_mentions[0]['author'], ':', nodes_with_mentions[0]['text'], '\n')
#
#
# # A bit deeper. ExtraData:
# extra_data = tree['node']['extra_data']
# print('Extra data can have many keys:', extra_data.keys())
# # A post can have 'downVotes' and 'upVotes':
# print('UpVotes:', extra_data['ups'], 'DownVotes:', extra_data['downs'])
# # And we can easily find the original discussion on reddit using the 'url':
# print('url:', extra_data['url'])
# print('If we sort by \'OLD\' a discussion on the reddit website,'
#       'we\'d get it exactly in the same order as we have it in our branches:')
# print('https://www.reddit.com/r/changemyview/comments/4rl42j/cmv_abortion_should_remain_legal/?sort=old')
# print('Pay attention that the ID of a tree appears also in the url:', tree['node']['id'])
