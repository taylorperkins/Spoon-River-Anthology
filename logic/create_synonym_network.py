from collections import defaultdict
from copy import deepcopy

from gensim.corpora import Dictionary
import networkx as nx
from nltk.corpus import wordnet as wn


dictionary = Dictionary.load('../data/spa.dict')
pickled_graph = nx.read_gpickle("../logic/test.gpickle")


for ind, node in pickled_graph.nodes(data=True):
    pickled_graph.node[ind]['type'] = 'SPA'

syns_per_term = defaultdict(set)

syn_dict = Dictionary()
syn_to_node_map = dict()

# Keep updating this as we add in the synonyms
node_count = len(pickled_graph.nodes)

spa_nodes = deepcopy(pickled_graph.nodes(data=True))

for term_ind, node in spa_nodes:
    term = dictionary[node['term_id']]

    # syn nodes have already been created, the values are in in the list
    if term in syns_per_term:
        for syn in syns_per_term[term]:
            pickled_graph.add_edge(
                term_ind,
                syn_to_node_map[syn_dict.token2id[syn]],
                attr_dict={'weight': 0.5}
            )

    # synonyms have not been created for this term
    else:
        # get syns for term
        syns = wn.synsets(term)

        for syn_obj in syns:
            # extracts the text value from the syn object
            syn = syn_obj.name().split('.')[0]

            # We have not seen this syn yet
            if syn not in syn_dict.token2id:
                # add syn term to dictionary
                syn_dict.add_documents([[syn]])

                # add syn node to graph
                pickled_graph.add_node(
                    node_count,
                    type='SYN',
                    term_id=syn_dict.token2id[syn],
                    freq_per_doc=-1,
                    vector_ind=-1
                )
                syn_to_node_map[syn_dict.token2id[syn]] = node_count

                # Keep track of values
                node_count += 1

            if syn not in syns_per_term[term]:
                syns_per_term[term].add(syn)

                pickled_graph.add_edge(
                    term_ind,
                    syn_to_node_map[syn_dict.token2id[syn]],
                    attr_dict={'weight': 0.5}
                )

nx.write_gpickle(pickled_graph, "final_network.gpickle")
