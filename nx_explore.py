import pdb
import itertools

import networkx as nx
import matplotlib.pyplot as plt

import scrape_pfr

def album_graph_from_catalog(graph, catalog):
    if not graph:
        graph = nx.Graph()
    for album in catalog.albums:
        graph.add_node(album.title)
    return graph

def dict_to_sorted_list(dict_, fun, reverse=False):
    return sorted(((key, val) for key, val in dict_.iteritems()), key = fun, reverse=reverse)

if __name__ == "__main__":
    reload(scrape_pfr)
    catalog = scrape_pfr.Catalog()
    catalog.add_pfr()
    catalog.delete_albums_by_artist('UnderCover Presents')
    graph = album_graph_from_catalog(graph=None, catalog=catalog)

    for name, albums in catalog.musician_credits.iteritems():
        edges = itertools.product(albums, repeat=2)
        for edge in edges:
            graph.add_edge(*edge)

    print("\nBetweenness centrality")
    btw = nx.betweenness_centrality(graph)
    print dict_to_sorted_list(btw, lambda x: x[1], reverse=True)

    print("\nEdge betweenness centrality")
    edge_btw = nx.edge_betweenness_centrality(graph)
    print dict_to_sorted_list(edge_btw, lambda x: x[1], reverse=True)

    # nx.draw(graph)
    # plt.show()
    # plt.close()
