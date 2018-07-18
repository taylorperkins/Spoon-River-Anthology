from collections import defaultdict
import pickle

import pandas as pd
import networkx as nx


class CreateSimilarityMatrix:
    def __init__(self, subgraph_dir, similarity_matrix_path):
        self._subgraph_dir = subgraph_dir
        self._similarity_matrix_path = similarity_matrix_path

    def main(self, G):
        # for creating the similarity score
        print('Getting type attrs')
        type_attrs = nx.get_node_attributes(G, 'type')

        print('Creating base similarities matrix')
        similarities_matrix = pd.DataFrame(columns=list(range(246)))

        print('Getting nodes map')
        nodes_map = self._get_poem_nodes(G)

        similarities_map = dict()

        # This is a lot. But, I need it to create my matrix
        for i in range(246):
            print(f"initializing row for {i}")
            similarities_row = list()

            for j in range(246):
                print(f"{i}-{j} --> {round((j / 246) * 100, 2)}%")
                if i == j:
                    similarities_row.append(1)

                else:
                    poems_index = (min([i, j]), max([i, j]))
                    if poems_index in similarities_map:
                        similarities_row.append(similarities_map[poems_index])

                    else:
                        poem_1_nodes, poem_2_nodes = nodes_map[i], nodes_map[j]
                        if not poem_1_nodes or not poem_2_nodes:
                            raise Exception('Something fishy with your nodes. \n1: {poem_1_nodes}\n2: {poem_2_nodes}')

                        subgraph, similarity_score = self._create_subgraph_with_similarity_score(
                            G,
                            poem_1_nodes,
                            poem_2_nodes,
                            type_attrs
                        )

                        similarities_map[poems_index] = similarity_score
                        similarities_row.append(similarity_score)

                        self._write_subgraph_to_file(
                            v_ind_1=i,
                            v_ind_2=j,
                            subgraph=subgraph
                        )


            similarities_matrix.append(similarities_row)
            self._write_similarities_matrix_to_file(similarities_matrix)

        self._write_similarities_map_to_file(similarities_map)

    async def _create_similarities_score(self, G, i, j, types_attr, similarities_row, nodes_map, subgraph_map):
        if i == j:
            similarities_row.append(1)

        else:
            poems_index = (min([i, j]), max([i, j]))
            if poems_index in subgraph_map:
                similarities_row.append(subgraph_map[poems_index]['similarity_score'])

            else:
                poem_1_nodes, poem_2_nodes = nodes_map[i], nodes_map[j]
                if not poem_1_nodes or not poem_2_nodes:
                    raise Exception('Something fishy with your nodes. \n1: {poem_1_nodes}\n2: {poem_2_nodes}')

                subgraph, similarity_score = self._create_subgraph_with_similarity_score(
                    G,
                    poem_1_nodes,
                    poem_2_nodes,
                    types_attr
                )

                self._write_subgraph_to_file(
                    v_ind_1=i,
                    v_ind_2=j,
                    subgraph=subgraph
                )

    def _create_subgraph_with_similarity_score(self, G, v_1_nodes, v_2_nodes, type_attrs):
        # starts at 0, will ultimately normalize this after all have been calculated
        similarity_score = 0

        # for reference in the logic
        same_terms = set()
        common_syns = set()

        history = list()
        # Now we want the set of synonyms connecting the two poems.
        for node_1 in v_1_nodes:
            for node_2 in v_2_nodes:
                index = [min([node_1, node_2]), max(node_1, node_2)]

                # so we don't risk duplication in scoring.
                if index not in history:
                    history.append(index)

                    n1_term = G.nodes[node_1]['term_id']
                    n2_term = G.nodes[node_2]['term_id']

                    # Determine if connected
                    if n1_term == n2_term and n1_term not in same_terms:
                        same_terms.add(n1_term)
                        similarity_score += (G.nodes[node_1]['tf-idf'] + G.nodes[node_2]['tf-idf'])

                    else:
                        # synonym matching
                        neighbors = [neighbor_ind for neighbor_ind in nx.common_neighbors(G, node_1, node_2)
                                     if type_attrs[neighbor_ind] == 'SYN']

                        for neighbor_ind in neighbors:
                            common_syns.add(neighbor_ind)

                            similarity_score += (G.nodes[node_1]['tf-idf'] + G.nodes[node_2]['tf-idf']) / (len(neighbors) * 2)

        return G.subgraph(v_1_nodes + v_2_nodes + list(common_syns)), similarity_score

    @staticmethod
    def _get_poem_nodes(G):
        nodes_map = defaultdict(list)

        # This gives us all nodes associated all poems
        for n, d in G.nodes(data=True):
            if d['vector_ind'] >= 0:
                nodes_map[d['vector_ind']].append(n)

        return nodes_map

    def _write_subgraph_to_file(self, v_ind_1, v_ind_2, subgraph):
        nx.write_gpickle(subgraph, f"{self._subgraph_dir}/{v_ind_1}/{v_ind_2}.gpickle")

    def _write_similarities_map_to_file(self, similarities_map):
        pickle.dump(similarities_map, open('similarities_map.p', 'wb'))

    def _write_similarities_matrix_to_file(self, s_matrix):
        s_matrix.to_pickle(self._similarity_matrix_path)


if __name__ == '__main__':
    similarity_matrix = CreateSimilarityMatrix(
        subgraph_dir='../data/subgraphs',
        similarity_matrix_path='../data/similarities_matrix.pkl'
    )

    graph = nx.read_gpickle("../data/final_network.gpickle")

    similarity_matrix.main(graph)

    print('Done')
