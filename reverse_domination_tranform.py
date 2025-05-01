
import networkx as nx
import matplotlib.pyplot as plt

def reconstruct_domination_graph(G_prime, centers):
    """Reconstruct domination graph by adding edges from each center to all nodes it dominates (weight ≤ 1)."""
    dom_adj = {v: [] for v in G_prime.nodes()}
    for v in G_prime.nodes():
        for s in centers:
            if v == s or G_prime[v][s]['weight'] <= 1:
                if v != s:
                    dom_adj[v].append(s)
                    dom_adj[s].append(v)
    return dom_adj

def build_graph_from_adjlist(adj_dict):
    G = nx.Graph()
    for u in adj_dict:
        G.add_node(u)  # ensure all nodes are included, even if isolated
        for v in adj_dict[u]:
            G.add_edge(u, v)
    return G

def visualize_dominating_graph(G, centers):
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    node_colors = ["red" if node in centers else "lightgreen" for node in G.nodes()]
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600)
    nx.draw_networkx_edges(G, pos, width=2)
    nx.draw_networkx_labels(G, pos, font_size=12)
    plt.title("Reconstructed Dominating Graph from MSMC Centers")
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    # Example G_prime with disconnected components and weights
    G_prime = nx.Graph()
    edges_with_weights = [
        (1, 2, 1), (1, 3, 1), (2, 3, 1),
        (4, 5, 1), (5, 6, 1), (4, 6, 1)
        # nodes 7 and 8 will be isolated and added manually
    ]
    G_prime.add_weighted_edges_from(edges_with_weights)
    G_prime.add_node(7)
    G_prime.add_node(8)

    centers = [1, 4, 7, 8]

    dom_adj = reconstruct_domination_graph(G_prime, centers)
    dom_G = build_graph_from_adjlist(dom_adj)

    print("Reconstructed Dominating Graph (Adjacency List):")
    for node, neighbors in dom_adj.items():
        print(f"{node}: {sorted(set(neighbors))}")

    visualize_dominating_graph(dom_G, centers)
