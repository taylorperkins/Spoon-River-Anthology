import networkx as nx


graph = nx.read_gpickle("./final_network.gpickle")


poem_4 = list()
poem_5 = list()


# This gives us all nodes associated with these two poems
for n, d in graph.nodes(data=True):

    if d['vector_ind'] == 4:
        poem_4.append(n)

    elif d['vector_ind'] == 5:
        poem_5.append(n)

type_attrs = nx.get_node_attributes(graph, 'type')

common_syns = set()
# Now we want the set of synonyms connecting the two poems.
for node_4 in poem_4:
    for node_5 in poem_5:
        neighbors = nx.common_neighbors(graph, node_4, node_5)

        for neighbor_ind in neighbors:
            if type_attrs[neighbor_ind] == 'SYN':
                common_syns.add(neighbor_ind)

subgraph = graph.subgraph(poem_5 + poem_4 + list(common_syns))
nx.write_gpickle(subgraph, "subgraph.gpickle")
