from collections import defaultdict
from itertools import combinations

import networkx as nx

import signal
import sys
import asyncio
import aiohttp

from gensim import corpora


dictionary = corpora.Dictionary.load('../data/spa.dict')
corpus = corpora.MmCorpus('../data/spa.mm')

SPA_graph = nx.Graph(name='SPA')

term_id_hash = defaultdict(list)
node_count = 0

for v_ind, vector in enumerate(corpus):
    # the second and third values should be the same in every case
    assert len(set(vector)) == len(vector)

    for term in vector:
        term_id_hash[term[0]].append(node_count)
        SPA_graph.add_node(node_count, vector_ind=v_ind, term_id=term[0], freq_per_doc=term[1])

        node_count += 1


class CreateNetwork:
    @staticmethod
    async def get_combinations_async(nodes):
        combs = list(combinations(nodes, 2))
        await asyncio.sleep(1)
        return combs

    @staticmethod
    async def add_edges_async(g, key):
        g.add_edge(*key)
        nx.set_edge_attributes(g, [{key: 1}], 'weight')
        await asyncio.sleep(1)
        return

    async def network_per_term_async(self, g, nodes, nodes_len):
        """Event Loops for Creating Network"""

        combin = await self.get_combinations_async(nodes)

        node_group = asyncio.gather(*[self.add_edges_async(g, key) for key in combin])

        return node_group

    async def network_per_node_count_async(self, g, nodes_list, nodes_len):
        """Event Loops for Creating Network"""
        network_group = asyncio.gather(*[self.network_per_term_async(g, nodes, nodes_len) for nodes in nodes_list])

        await asyncio.sleep(1)

        return network_group


node_groups_by_length = defaultdict(list)
for term, nodes in term_id_hash.items():
    nodes_len = len(nodes)
    if nodes_len > 1:
        node_groups_by_length[nodes_len].append(nodes)

io_loop = asyncio.get_event_loop()
client = aiohttp.ClientSession(loop=io_loop)


def signal_handler(signal, frame):
    io_loop.stop()
    client.close()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

count = 1
for node_len, node_list in node_groups_by_length.items():
    print(f'starting network for {node_len} -- Term freq: {len(node_list)} -- {round(count / len(node_groups_by_length), 2)}%')

    network_creator = CreateNetwork()

    _ = io_loop.run_until_complete(network_creator.network_per_node_count_async(SPA_graph, node_list, node_len))

    print(f'finished network for {node_len}\n')

    count += 1

io_loop.close()

nx.write_gpickle(SPA_graph, "test.gpickle")

print('Done')
