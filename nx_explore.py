import networkx as nx
import matplotlib.pyplot as plt

import scrape_pfr

def album_graph_from_catalog(graph, catalog):
    if not graph:
        graph = nx.Graph()
    for album in catalog.albums:
        graph.add_node(album.title)

    return graph

if __name__ == "__main__":
    catalog = scrape_pfr.Catalog()
    catalog.add_pfr()
    graph = album_graph_from_catalog(graph=None, catalog=catalog)

    nx.draw(graph)
    plt.show()
