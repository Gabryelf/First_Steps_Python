import networkx as nx
import matplotlib.pyplot as plt
from all_friends import graph


def visualize_graph():
    G = nx.Graph()

    for person, friends in graph.items():
        for friend in friends:
            G.add_edge(person, friend)

    nx.draw(G, with_labels=True, node_color='lightblue',
            node_size=2000, font_size=10)
    plt.title("Ваша социальная сеть")
    plt.show()


visualize_graph()
