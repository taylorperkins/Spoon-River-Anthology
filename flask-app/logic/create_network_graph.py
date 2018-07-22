import pickle
import os
import glob

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import networkx as nx
import nxviz as nv
from gensim.corpora import Dictionary


def create_network_graph(p1, p2):
    files = glob.glob('static/images/*_network_graph.png')
    for f in files:
        os.remove(f)

    p_graph = nx.read_gpickle(f'../notebooks/pivot/combined_graphs/{p1}/{p2}.gpickle')

    chapter_names = pickle.load(open('../notebooks/pivot/chapter_names.p', 'rb'))
    spa_dictionary = Dictionary.load('../notebooks/pivot/spa.dict')
    syn_dictionary = Dictionary.load('../notebooks/pivot/syn.dict')

    for node, data in p_graph.nodes(data=True):
        # it's a synonym node
        if data['type'] == 'SYN':
            data['document'] = 'Synonym'
            data['term'] = syn_dictionary[data['term_id']]

        else:
            data['document'] = chapter_names[str(data['doc_id'])]
            data['term'] = spa_dictionary[data['term_id']]

    p_graph = nx.relabel_nodes(
        p_graph,
        {node: f"{node}: {data['term']}" for node, data in p_graph.nodes(data=True)}
    )

    ap = nv.CircosPlot(
        p_graph,
        node_color='doc_id',
        node_grouping='document',
        group_label_position='middle',
        group_label_color=True,
        node_labels=True,
        node_label_layout="numbers",
        figsize=(8, 7)
    )

    ap.draw_group_labels()

    ap.draw()

    plt.savefig(f'./static/images/{p1}_{p2}_network_graph.png')
